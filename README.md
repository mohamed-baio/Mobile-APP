# Mobile-APP
## Endpoint:{base_url}/api/method/mobile_app.apis.get_all_tasks
### Method :GET
### URL Parameters:
__ Status --> 'Planned'-'In Progress'-'Completed'-'All'
__ representative  --> representative assigned to the tasks

### Sample Request
curl --location --request GET '{base_url}/api/method/mobile_app.apis.get_all_tasks?status=Completed&representative=ahmed@test.com' \

''' Sample Response
{
    "message": [
        {
            "name": "TASK-2023-00005",
            "subject": "Meeting with doctors ",
            "representative": "ahmed@test.com",
            "type": "visited",
            "priority": "High",
            "start_date": "9:00:00",
            "completed_on": null,
            "exp_start_date": "2023-06-08",
            "status": "Completed",
            "days": "Monday",
            "description": "we will meet the doctor"
        }
}

____________________________________________________________________________________________________________________________
## Endpoint :{base_url}/api/method/mobile_app.apis.add_new_task
### Method :POST

### Example
#### Request Body
 ** curl --location --request POST '{base_url}/api/method/mobile_app.apis.add_new_task?subject=visit new doctor3&representative=test@test.com&status=Completed&priority=Important&days=Monday&exp_start_date=2023-10-12&start_time=10:30&description=this is important&type=official' \
#### Response
 ** "Task Created"
 
 ____________________________________________________________________________________________________________________________
 ## Endpoint :{base_url}/api/method/mobile_app.apis.update_task_status
 ### Method :PUT
 
 ### Example
 #### Request Body
  ** curl --location --request PUT '{base_url}/api/method/mobile_app.apis.update_task_status?name=TASK-2023-00011&status=In Progress' \
#### Response
** "Task Status Created"

____________________________________________________________________________________________________________________________
## Endpoint :{base_url}/api/method/mobile_app.apis.delete_task
### Method :DELETE

### Example
#### Request Body
**curl --location --request DELETE '{base_url}/api/method/mobile_app.apis.delete_task?subject=Visit new doctor1' \
#### Response
** "Task Deleted"
______________________________________________________________________________________________________________________________
