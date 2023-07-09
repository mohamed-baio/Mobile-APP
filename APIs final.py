import frappe
import requests
from frappe import _
from frappe.utils import getdate, date_diff
from frappe import _
from datetime import datetime, timedelta

success = 200
not_found = 400


# @frappe.whitelist(allow_guest=True)
# def get_user_profile(email, password):
#     try:
#         representative = frappe.get_doc("Mobile Users", {"email": email})
#         if not representative or not frappe.utils.password.check_password(
#             representative.password, password
#         ):
#             frappe.throw(_("Invalid email or password"), frappe.AuthenticationError)
#         profile_data = frappe.get_doc("Mobile Users", representative)
#         user_data = {
#             "full_name": profile_data.full_name,
#             "email": profile_data.email,
#             "mobile_number": profile_data.mobile_number,
#             "image": profile_data.image,
#         }
#         return user_data
#     except Exception as e:
#         frappe.log_error(title="failed", message=e)
#         return {"failed ": False, "message": str(e)}


# ###################
# @frappe.whitelist()
# def get_mobile_user_data(customer_name, email, password):
#     try:
#         # Check if customer_name exists in Mobile Customer Master Data doctype
#         customer = frappe.get_doc(
#             "Mobile Customer Master Data", {"customer_name": customer_name}
#         )
#         if not customer:
#             return {"success": False, "message": "Invalid customer_name"}

#         # Make an HTTP request to the server with Mobile Users data
#         url = f"http://94.250.201.76/api/resource/Mobile Customer Master Data/Onco/get_mobile_user_data"
#         payload = {"email": email, "password": password}
#         response = requests.post(url, json=payload)

#         if response.status_code == 200:
#             data = response.json()
#             if data.get("success"):
#                 return {
#                     "success": True,
#                     "message": "Validation successful",
#                     "token": data.get("token"),
#                     "mobile_number": data.get("mobile_number"),
#                 }
#             else:
#                 return {"success": False, "message": "Invalid username or password"}

#         return {"success": False, "message": "An error occurred"}


#     except Exception as e:
#         frappe.log_error("Error in get_mobile_user_data", title="API Endpoint")
#         return {"success": False, "message": "An error occurred"}


@frappe.whitelist(allow_guest=True)
def get_userdata(email, password):
    try:
        hub_endpoint = (
            "http://94.250.201.76/api/resource/Mobile Customer Master Data/Onco"
        )
        header = {"Authorization": "token a36b58072b4844c:2d936d76c477a78"}

        response = requests.get(hub_endpoint, headers=header)
        response.raise_for_status()

        data = response.json()

        customer_name = data.get("data", {}).get("customer_name")
        is_active = data.get("data", {}).get("is_active")
        user_data = None
        users = data.get("data", {}).get("users", [])
        for user in users:
            if user["email"] == email and user["password"] == password:
                user_data = {
                    "name": user["name"],
                    "full_name": user["full_name"],
                    "email": user["email"],
                    "password": user["password"],
                    "token": user["token"],
                    "mobile_number": user["mobile_number"],
                    "address": user["address"],
                }
                break

        if user_data:
            return frappe.as_json(
                {
                    "customer_name": customer_name,
                    "is_active": is_active,
                    "user_data": user_data,
                }
            )
        else:
            raise ValueError("Invalid email or password")

    except requests.exceptions.RequestException as e:
        raise ValueError("Failed ") from e


# @frappe.whitelist(allow_guest=True)
# def get_userdata(email, password):

#     hub_endpoint = "http://94.250.201.76/api/resource/Mobile Customer Master Data/Onco"
#     header = {"Authorization": "token a36b58072b4844c:2d936d76c477a78"}

#     response = requests.get(hub_endpoint, headers=header)
#     if response.status_code == 200:
#         data = response.json()

#         # customer_name = data["data"]["customer_name"]
#         # is_active = data["data"]["is_active"]
#         # users = data["data"]["users"][0]
#         customer_name = data.get("data", {}).get("customer_name")
#         is_active = data.get("data", {}).get("is_active")
#         user_data = None
#         users = data.get("data", {}).get("users", [])
#         for user in users:
#             if user["email"] == email and user["password"] == password:
#                 user_data = {
#                     "name": user["name"],
#                     "full_name": user["full_name"],
#                     "email": user["email"],
#                     "password": user["password"],
#                     "token": user["token"],
#                     "mobile_number": user["mobile_number"],
#                     "address": user["address"],
#                 }
#                 break

#         if user_data:
#             return frappe.as_json(
#                 {
#                     "customer_name": customer_name,
#                     "is_active": is_active,
#                     "user_data": user_data,
#                 }
#             )
#         else:
#             raise ValueError("Invalid email or password")
#     else:
#         raise ValueError("Failed")


######################################################
@frappe.whitelist(allow_guest=True)
def get_counts():
    unplanned = frappe.get_value(
        "Opportunity", filters={"status_plan": "Unplanned"}, fieldname="count(*)"
    )
    cancelled = frappe.get_value(
        "Opportunity", filters={"status_plan": "Cancelled"}, fieldname="count(*)"
    )
    response = {
        "unplanned_opportunity_count": unplanned,
        "cancelled_opportunity_count": cancelled,
    }
    return response


###################################################
@frappe.whitelist(allow_guest=True)
def get_status_percentages(transaction_date, lead_owner):
    closed_count = frappe.get_value(
        "Opportunity",
        filters={
            "transaction_date": transaction_date,
            "lead_owner": lead_owner,
            "status": "Closed",
        },
        fieldname="count(*)",
    )
    in_progress_count = frappe.get_value(
        "Opportunity",
        filters={
            "transaction_date": transaction_date,
            "lead_owner": lead_owner,
            "status": "Open",
        },
        fieldname="count(*)",
    )
    open_count = frappe.get_value(
        "Opportunity",
        filters={
            "transaction_date": transaction_date,
            "lead_owner": lead_owner,
            "status": "Open",
        },
        fieldname="count(*)",
    )

    total_count = closed_count + in_progress_count + open_count

    completed_percentage = (closed_count / total_count) * 100
    in_progress_percentage = (in_progress_count / total_count) * 100
    incomplete_percentage = (open_count / total_count) * 100

    response = {
        "completed_percentage": completed_percentage,
        "in_progress_percentage": in_progress_percentage,
        "incomplete_percentage": incomplete_percentage,
    }

    return response


############## TASK ###################################
### get info of all tasks of one representative
# @frappe.whitelist(allow_guest=True)
# def get_all_tasks(status, representative):
#     tasks = frappe.db.sql(
#         f""" SELECT name,subject,representative,type,priority,expected_time,exp_start_date,exp_end_date,status,description FROM `tabTask` WHERE status='{status}' and representative = '{representative}';""",
#         as_dict=True,
#     )

#     try:
#         frappe.db.commit()
#         return tasks
#     except Exception as B:
#         frappe.log_error("Failed to Return all Tasks: {0}".format(B))
#         frappe.db.rollback()
#         return "Failed to Return all Tasks"


@frappe.whitelist(allow_guest=True)
def get_all_todo(status, owner):
    tasks = frappe.db.sql(
        f""" SELECT name,date,owner,reference_type,priority,status FROM `tabToDo` WHERE status='{status}' and owner = '{owner}';""",
        as_dict=True,
    )

    try:
        frappe.db.commit()
        return tasks
    except Exception as B:
        frappe.log_error("Failed to Return all Tasks: {0}".format(B))
        frappe.db.rollback()
        return "Failed to Return all Tasks"


### add new task
@frappe.whitelist(allow_guest=True)
def add_new_todo(
    owner,
    date,
    status,
    priority,
    reference_type,
    description,
    # attach_files
):
    """
    priorty : Low,Medium,High
    date format : yyyy/mm/dd
    """
    new_task = frappe.get_doc(
        {
            "doctype": "ToDo",
            "owner": owner,
            "date": date,
            "status": status,
            "priority": priority,
            "reference_type": reference_type,
            "description": description,
        }
    )
    new_task.db_insert()
    try:
        frappe.db.commit()
        return "Task Created "
    except Exception as B:
        frappe.log_error("Failed to Create New Task: {0}".format(B))
        frappe.db.rollback()
        return "Failed to Create New Task"


#### update status of task
@frappe.whitelist(allow_guest=True)
def update_task_status(name, status):
    frappe.db.sql(f"""UPDATE `tabToDo` SET status='{status}' WHERE name='{name}';""")
    try:
        frappe.db.commit()
        return "Task Updated"
    except Exception as F:
        frappe.log_error("failed to update the status :{0}".format(F))
        frappe.db.rollback()
        return "failed to update the status"


#### Delete task
@frappe.whitelist(allow_guest=True)
def delete_task(name):
    frappe.db.sql(f"""DELETE FROM `tabToDo` WHERE name='{name}'""")
    try:
        frappe.db.commit()
        return "Task Deleted"
    except Exception as F:
        frappe.log_error("failed to delete the task".format(F))
        return "failed to delete the task"


########################### VACATION ############################################################
@frappe.whitelist(allow_guest=True)
def get_vacations(employee_name):
    vacation = frappe.db.sql(
        f"""SELECT employee,employee_name,leave_type,from_date,to_date,total_leave_days,status,description, leave_approver FROM `tabLeave Application` WHERE employee_name='{employee_name}';""",
        as_dict=True,
    )
    try:
        frappe.db.commit()
        return vacation
    except Exception as F:
        frappe.log_error("failed to get vacations".format(F))
        return "failed to get all vacations"


################################### Clients ####################################################
# Two Endpoints :- 2-Get each client information ########################################


# 1-Get all clients(Doctors)
@frappe.whitelist(allow_guest=True)
def get_all_clients():
    clients = frappe.get_all("Lead", fields=["lead_name", "medical_specialty"])
    try:
        frappe.db.commit()
        return clients
    except Exception as H:
        frappe.log_error("Failed to get all clients: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get all clients"


## put location of client --Note
# 2-Get each client information
@frappe.whitelist(allow_guest=True)
def get_client_details(lead_name):
    client = frappe.db.sql(
        f"""SELECT lead_name,medical_specialty,mobile_no,email_id,location FROM `tabLead` WHERE lead_name='{lead_name}';""",
        as_dict=True,
    )
    try:
        frappe.db.commit()
        return client
    except Exception as H:
        frappe.log_error("Failed to get this client: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get client info"


######################### POC #########################################################
@frappe.whitelist(allow_guest=True)
def get_poc(address):
    poc = frappe.db.sql(
        f"""SELECT address,client_name,poc,frequency,medical_specialty FROM `tabPOC` WHERE address='{address}';""",
        as_dict=True,
    )
    try:
        frappe.db.commit()
        return poc
    except Exception as H:
        frappe.log_error("Failed to get POC: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get POC"


############################## Activity #################################################
## Get Activities


@frappe.whitelist(allow_guest=True)
def get_activities(expense_type, employee):
    activity = frappe.db.sql(
        f"""SELECT employee,expense_type,employee_name,status,advance_amount,posting_date,client, purpose FROM `tabEmployee Advance` WHERE expense_type='{expense_type}' and employee='{employee}';""",
        as_dict=True,
    )
    try:
        frappe.db.commit()
        return activity
    except Exception as H:
        frappe.log_error("Failed to get all activities: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get all activities"


## POST Activity or Expense #########################################
@frappe.whitelist(allow_guest=True)
def new_activity(
    employee,
    expense_type,
    advance_amount,
    lead,
    purpose,
    exchange_rate,
    advance_account,
):
    """
    status : Approved,Rejected,Draft
    date format : YYYY-MM-DD
    """

    try:
        if not frappe.db.exists("Lead", lead):
            return "Lead not found"
        if not frappe.db.exists("Employee", employee):
            return "Employee not found"

        new_activity = frappe.get_doc(
            {
                "doctype": "Employee Advance",
                "employee": employee,
                "expense_type": expense_type,
                "advance_amount": advance_amount,
                "lead": lead,
                "purpose": purpose,
                "exchange_rate": 1.0,
                "advance_account": advance_account,
            }
        )
        new_activity.insert()
        frappe.db.commit()
        return "activity created"
    except Exception as e:
        frappe.log_error("failed to create new activity :{0}".format(e))
        frappe.db.rollback()
        return "failed to create new activity"


############### Expenses ##################################################
# Get all expenses
@frappe.whitelist(allow_guest=True)
def get_expenses(employee, expense_type):
    expense = frappe.db.sql(
        f"""SELECT employee,expense_type,employee_name,status,advance_amount,posting_date,client, purpose FROM `tabEmployee Advance` WHERE expense_type='{expense_type}' and employee='{employee}';""",
        as_dict=True,
    )
    try:
        frappe.db.commit()
        return expense
    except Exception as H:
        frappe.log_error("Failed to get all expenses: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get expenses"


################### Settlement ###############################################


############### Test Add settlement ####################
##1-
@frappe.whitelist(allow_guest=True)
def add_expense_claim(employee, expense_approver, posting_date):
    try:
        doc = frappe.new_doc("Expense Claim")
        doc.employee = employee
        doc.expense_approver = expense_approver
        doc.posting_date = posting_date
        doc_child = {
            "expenses": [
                {
                    "expense_type": "Activity",
                    "amount": 50.0,
                    "sanctioned_amount": 50.0,
                    "payable_account": "Creditors - A",
                }
            ]
        }
        doc.set("expenses", [])
        for expense in doc_child:
            doc.append("expenses", expense)
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        doc_name = str(doc.name)
        return {"success": True, "document_name": doc_name}
    except Exception as e:
        frappe.log_error(title="post new expense claim", message=e)
        return {"failed ": False, "message": str(e)}


##2-######### Second Try ###################################
@frappe.whitelist(allow_guest=True)
def add_expense_claims(employee, expense_approver, posting_date):
    try:
        doc_child = {
            "expenses": [
                {
                    "expense_type": "Activity",
                    "amount": 50.0,
                    "sanctioned_amount": 50.0,
                }
            ]
        }
        doc = frappe.new_doc("Expense Claim")
        doc.employee = employee
        doc.expense_approver = expense_approver
        doc.posting_date = posting_date
        doc.expenses = doc_child
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        doc_name = doc.name
        return {"success": True, "document_name": doc_name}
    except Exception as e:
        frappe.log_error(title="post new expense claim", message=e)
        return {"failed ": False, "message": str(e)}


#################### update settlement status ###########################
@frappe.whitelist(allow_guest=True)
def update_settlement_status(expense_claim_name, approval_status, is_paid, status):
    expense_claim = frappe.get_doc("Expense Claim", expense_claim_name)
    expense_claim.approval_status = approval_status
    expense_claim.is_paid = is_paid
    expense_claim.status = status
    try:
        expense_claim.save()
        return {"success": True, "message": f"{expense_claim_name} status updated"}
    except Exception as H:
        frappe.log_error("Cannot Postpone : {0}".format(H))
        frappe.db.rollback()
        return {"failed ": False, "message": str(H)}


################### TEST Update status of settlement###################################
@frappe.whitelist(allow_guest=True)
def update_expense_status(docname):
    try:
        doc = frappe.get_doc("Expense Claim", docname)
        doc.status = "Paid"
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "message": "Expense claim status updated to paid"}
    except Exception as k:
        frappe.log_error(title="Update Expense Claim Status", message=k)
        return {"success": False, "message": str(k)}


################ Get settlements per employee #############################
@frappe.whitelist(allow_guest=True)
def get_settlements(employee, status=None):
    settlements = frappe.get_all(
        "Expense Claim",
        filters={"employee": employee, "status": status},
        fields=["employee", "expense_type", "status", "total_claimed_amount"],
    )
    try:
        frappe.db.commit()
        return {"success": True, "data": settlements}
    except Exception as H:
        frappe.log_error("Failed to get settlements: {0}".format(H))
        frappe.db.rollback()
        return "Failed to settlements"


########### Get more details Settlements #####################################
@frappe.whitelist(allow_guest=True)
def get_settlement_detail(employee, name, status=None):
    settlement = frappe.db.sql(
        f"""SELECT employee,employee_name,expense_type , approval_status,is_paid,
                                          total_claimed_amount,total_advance_amount,posting_date 
                                          from `tabExpense Claim` WHERE employee='{employee}' and name='{name}';""",
        as_dict=True,
    )
    try:
        frappe.db.commit()
        return settlement
    except Exception as H:
        frappe.log_error("Failed to get details: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get details"


####################### CLM On Visit ################################################
@frappe.whitelist(allow_guest=True)
def get_representative(lead_owner):
    leads = frappe.get_all(
        "Lead",
        filters={"lead_owner": lead_owner},
        fields=["lead_name", "medical_specialty"],
    )
    try:
        frappe.db.commit()
        return {"success": True, "data": leads}
    except Exception as H:
        frappe.log_error("Failed to get Representative Leads: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get Representative Leads"


##################### Product #################################################
@frappe.whitelist(allow_guest=True)
def get_product_bundle_items(product_bundle_name):
    items = frappe.get_all(
        "Product Bundle Item",
        filters={"parent": product_bundle_name},
        fields=["item_code", "image"],
    )
    results = []

    for item in items:
        item_code = item.item_code
        image = item.image

        result = {"item_code": item_code, "image": image}
        results.append(result)

    return {"success": True, "data": results}


#####################################################################################
@frappe.whitelist(allow_guest=True)
def get_opportunity_content(opportunity_name):
    opportunity = frappe.get_doc(
        "Opportunity",
        opportunity_name,
        fields=["party_name", "customer_name", "status"],
    )

    if opportunity.include_clm:
        product_bundle = frappe.get_doc("Product Bundle", opportunity.product_bundle)
        bundle_content = product_bundle.get("items")
        content_data = []
        for item in bundle_content:
            content_data.append({"item_code": item.item_code, "image": item.image})
        return {"data": content_data}

    else:
        return {"data": []}


#######################  Get All Product Bundles ########################
@frappe.whitelist(allow_guest=True)
def get_opportunity_contents():
    opportunity_info = frappe.db.sql(
        """SELECT si.name,si.party_name,mi.item_code,mi.image FROM `tabOpportunity` AS si JOIN `tabProduct Bundle Item` AS mi ON mi.parent = si.name ;""",
        as_dict=True,
    )
    try:
        frappe.db.commit()
        return opportunity_info
    except Exception as H:
        frappe.log_error("Failed to get details: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get details"


########## get all opportunity ############################################
@frappe.whitelist(allow_guest=True)
def get_opportunities_by_lead_owner(lead_owner):
    start_date = datetime.now() - timedelta(days=7)

    opportunities = frappe.get_all(
        "Opportunity",
        filters={"creation": [">=", start_date], "lead_owner": lead_owner},
        fields=["name", "status_plan"],
    )

    return opportunities


################### add feedback ##########################################
@frappe.whitelist(allow_guest=True)
def update_to_discuss(opportunity_name, to_discuss):
    try:
        opportunity = frappe.get_doc("Opportunity", opportunity_name)

        if not opportunity:
            return {"success": False, "message": "Opportunity not found"}

        opportunity.to_discuss = to_discuss
        opportunity.save()

        return {"success": True, "message": "to_discuss field updated successfully"}
    except Exception as e:
        frappe.log_error("Failed to update to_discuss field", title="Update to_discuss")
        return {"success": False, "message": str(e)}


#
# ################### Visit #################################
# Postpone visit Update Method ###
@frappe.whitelist(allow_guest=True)
def update_visit(opportunity_name, contact_date, to_discuss):
    opportunity = frappe.get_doc("Opportunity", opportunity_name)
    opportunity.transaction_date = contact_date
    opportunity.to_discuss = to_discuss
    try:
        opportunity.save()
        return {"success": True, "message": f"Opportunity {opportunity_name} postponed"}
    except Exception as H:
        frappe.log_error("Cannot Postpone : {0}".format(H))
        frappe.db.rollback()
        return "Cannot Postpone"


###################### unplanned visit ###############################


@frappe.whitelist(allow_guest=True)
def add_unplanned_visit(
    opportunity_from, title, party_name, status, contact_date, to_discuss, status_plan
):
    """
    date format : yyyy-mm-dd

    """
    unplanned_visit = frappe.get_doc(
        {
            "doctype": "Opportunity",
            "opportunity_from": opportunity_from,
            "title": title,
            "party_name": party_name,
            "contact_date": contact_date,
            "status": status,
            "status_plan": status_plan,
            "to_discuss": to_discuss,
        }
    )
    unplanned_visit.db_insert()
    try:
        frappe.db.commit()
        return " Created "
    except Exception as H:
        frappe.log_error("Failed to Create : {0}".format(H))
        frappe.db.rollback()
        return "Failed to Create"


######################### GET Unplanned visits ################################################
@frappe.whitelist(allow_guest=True)
def get_unplanned_visits(status_plan):
    unplanned_visits = frappe.get_all(
        "Opportunity",
        filters={"status_plan": status_plan},
        fields=["customer_name", "medical_specialty"],
    )
    try:
        frappe.db.commit()
        return {"success": True, "data": unplanned_visits}
    except Exception as H:
        frappe.log_error("Failed to get Unplanned visits: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get Unplanned visits"


################### GET Uncovered visits #################################################
# @frappe.whitelist(allow_guest=True)
# def get_uncovered_doctors():


############################ Sales ###################################


@frappe.whitelist(allow_guest=True)
def get_sales_info_with_medicine():
    sales_info = frappe.db.sql(
        """SELECT si.account_type,si.distributors_type,si.distribution_places,si.from_date,si.to_date,si.total_unit,si.total_value,si.target_value,mi.item,mi.quantity,mi.rate FROM `tabSales Info` AS si JOIN `tabMedicine Item` AS mi ON mi.parent = si.name ;""",
        as_dict=True,
    )
    try:
        frappe.db.commit()
        return sales_info
    except Exception as H:
        frappe.log_error("Failed to get details: {0}".format(H))
        frappe.db.rollback()
        return "Failed to get details"
