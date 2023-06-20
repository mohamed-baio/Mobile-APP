import frappe
import requests
from frappe import _
from frappe.utils import getdate, date_diff

success = 200
not_found = 400


############## TASK ###################################
### get info of all tasks of one representative
@frappe.whitelist(allow_guest=True)
def get_all_tasks(status, representative):
    tasks = frappe.db.sql(
        f""" SELECT name,subject,representative,type,priority,start_date,exp_start_date,status,days,description FROM `tabTask` WHERE status='{status}' and representative = '{representative}';""",
        as_dict=True,
    )

    return tasks


### add new task
@frappe.whitelist(allow_guest=True)
def add_new_task(
    subject,
    representative,
    status,
    type,
    priority,
    days,
    exp_start_date,
    start_time,
    description,
    # attach_files
):
    """
    priorty : Low,Medium,High,Important
    status : Planned,In progress,Completed
    date format : dd/mm/yyyy
    time format : Hrs-Mins

    """
    new_task = frappe.get_doc(
        {
            "doctype": "Task",
            "subject": subject,
            "representative": representative,
            "status": status,
            "type": type,
            "priority": priority,
            "days": days,  ##Example:sunday
            "exp_start_date": exp_start_date,  ## YYYY-MM-DD
            "start_time": start_time,  ## Hrs-Mins
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
    frappe.db.sql(f"""UPDATE `tabTask` SET status='{status}' WHERE name='{name}';""")
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
    frappe.db.sql(f"""DELETE FROM `tabTask` WHERE name='{name}'""")
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
    return vacation


# @frappe.whitelist(allow_guest=True)
# def get_vacations1():
#     vacation = frappe.db.sql(
#         f"""SELECT employee,employee_name,leave_type,from_date,to_date,status,description, leave_approver FROM `tabLeave Application` ;""",
#         as_dict=True,
#     )
#     return vacation

# @frappe.whitelist(allow_guest=True)
# def get_vacation(status, employee):
#     headers = {"content-type": "application/json"}
#     response = requests.get(headers=headers)
#     if response.status_code == success:
#         data = response.json()
#         return data

#     else:
#         print(f"request failed {response.status_code}")


@frappe.whitelist(allow_guest=True)
def add_new_vacation(
    employee,
    employee_name,
    leave_type,
    from_date,
    to_date,
    # total_leave_days,
    status,
    description,
):
    """
    status : Approved,Rejected,Pending
    date format : YYYY-MM-DD

    """

    def get_total_leave_days(leave_application_name):
        leave_application = frappe.get_doc("Leave Application", leave_application)
        if leave_application:
            from_date = getdate(leave_application.from_date)
            to_date = getdate(leave_application.to_date)
            total_leave_days = date_diff(to_date, from_date) + 1
            return {"total_leave_days": total_leave_days}
        else:
            frappe.throw(_("Leave Application not found."))

    new_vacation = frappe.get_doc(
        {
            "doctype": "Leave Application",
            "employee": employee,
            "employee_name": employee_name,
            "leave_type": leave_type,
            "from_date": from_date,
            "to_date": to_date,
            # "total_leave_days": total_leave_days,
            "status": status,
            "description": description,
        }
    )

    new_vacation.db_insert()
    try:
        frappe.db.commit()
        return "Vacation Created "
    except Exception as H:
        frappe.log_error("Failed to Create New Vacation: {0}".format(H))
        frappe.db.rollback()
        return "Failed to Create New Vacation"


# add new vacation another way ####################
@frappe.whitelist(allow_guest=True)
def create_leave_application(employee, from_date, to_date, leave_type):
    leave_allocation = frappe.get_all(
        "Leave Allocation",
        filters={"employee": employee},
        fields=["from_date", "to_date"],
    )

    if leave_allocation:
        allocation_from_date = leave_allocation[0].from_date
        allocation_to_date = leave_allocation[0].to_date

        if from_date < allocation_from_date or to_date > allocation_to_date:
            frappe.throw(_("Application period is outside leave allocation period."))
    # Create a new Leave Application document
    leave_application = frappe.new_doc("Leave Application")
    leave_application.employee = employee
    leave_application.from_date = from_date
    leave_application.to_date = to_date
    leave_application.leave_type = leave_type

    try:
        leave_application.insert()
        frappe.db.commit()
        return {
            "message": _("Leave Application created successfully."),
            "leave_application_name": leave_application.name,
        }
    except Exception as D:
        frappe.db.rollback()
        frappe.throw(_("Failed to create leave Application : {0}").format(str(D)))
################################### Clients ####################################################
# Two Endpoints :- 2-Get each client information ########################################


# 1-Get all clients(Doctors)
@frappe.whitelist(allow_guest=True)
def get_all_clients():
    clients = frappe.get_all("Lead", fields=["lead_name", "medical_specialty"])
    return clients


## put location of client --Note
# 2-Get each client information
@frappe.whitelist(allow_guest=True)
def get_client_details(lead_name):
    client = frappe.db.sql(
        f"""SELECT lead_name,medical_specialty,mobile_no,email_id,location FROM `tabLead` WHERE lead_name='{lead_name}';""",
        as_dict=True,
    )
    return client


######################### POC #########################################################
@frappe.whitelist(allow_guest=True)
def get_poc(address):
    poc = frappe.db.sql(
        f"""SELECT address,client_name,poc,frequency,specialty FROM `tabPOC` WHERE address='{address}';""",
        as_dict=True,
    )
    return poc


############################## Activity #################################################
## Get Activities


@frappe.whitelist(allow_guest=True)
def get_activities(expense_type):
    activity = frappe.db.sql(
        f"""SELECT employee,expense_type,employee_name,approval_status,amount,client, comment,attach_files FROM `tabExpense Claim` WHERE expense_type='{expense_type}';""",
        as_dict=True,
    )
    return activity


## POST Activity or Expense #########################################
@frappe.whitelist(allow_guest=True)
def add_new_activity(
    employee,
    employee_name,
    expense_type,
    approval_status,
    amount,
    client,
    comment,
    # attach_files,
):
    """
    status : Approved,Rejected,Draft
    date format : YYYY-MM-DD

    """
    new_activity = frappe.get_doc(
        {
            "doctype": "Expense Claim",
            "employee": employee,
            "employee_name": employee_name,
            "expense_type": expense_type,
            "approval_status": approval_status,
            "amount": amount,
            "client": client,
            "comment": comment,
        }
    )
    new_activity.db_insert()
    try:
        frappe.db.commit()
        return "Activity Created "
    except Exception as H:
        frappe.log_error("Failed to Create New Activity: {0}".format(H))
        frappe.db.rollback()
        return "Failed to Create New Activity"


############### Expenses ##################################################
# Get all expenses
@frappe.whitelist(allow_guest=True)
def get_expenses(expense_type, approval_status):
    expense = frappe.db.sql(
        f"""SELECT employee,expense_type,employee_name,approval_status,amount,client, comment,attach_files FROM `tabExpense Claim` WHERE expense_type='{expense_type}' and approval_status='{approval_status}';""",
        as_dict=True,
    )
    return expense


####################### CLM ################################################
@frappe.whitelist(allow_guest=True)
def get_product_bundle_items(product_bundle_name):
    items = frappe.get_all(
        "Product Bundle Item",
        filters={"parent": product_bundle_name},
        fields=["item_code", "qty"],
    )
    results = []

    for item in items:
        item_code = item.item_code
        qty = item.qty

        result = {"item_code": item_code, "qty": qty}
        results.append(result)

    return {"success": True, "data": results}


# @frappe.whitelist(allow_guest=True)
# def get_product_bundle_items_with_active():
#     product_bundles = frappe.get_all(
#         "Product Bundle",
#         filters={"include_clm": 1},
#         fields=["include_clm"],
#     )
#     results = []

#     for bundle in product_bundles:
#         bundle_name = bundle.name

#         items =     items = frappe.get_all(
#         "Product Bundle Item",
#         filters={"parent": bundle_name},
#         fields=["item_code", "qty"])
#         item_list = []

#         for item in items:
#             item_code = item.item_code,
#             qty = item.qty


#             item_info = {
#                 "item_code":item_code,
#                 "qty":qty
#             }
#             item_list.append(item_info)
#         result = {
#             "bundle_name":bundle_name,
#             "items":item_list
#         }
#         results.append(result)
#         return {
#             "success":True,
#             "data":results
#         }
#
# ################### Visit #################################
# Postpone visit Update Method ###
@frappe.whitelist(allow_guest=True)
def postpone_visit(party_name, date, to_discuss):
    """
    date format : YYYY-MM-DD

    """
    frappe.db.sql(
        f"""UPDATE `tabOpportunity` SET date='{date}' and to_discuss='{to_discuss}' WHERE party_name='{party_name}' ;"""
    )
    try:
        frappe.db.commit()
        return "Visit Postponed"
    except Exception as S:
        frappe.log_error("failed to postponed the visit :{0}".format(S))
        frappe.db.rollback()
        return "failed to postponed the visit"
