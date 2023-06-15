# Mobile-APP
## Endpoint:{base_url}/api/method/mobile_app.apis.get_all_tasks
### Method :GET

### URL Parameters:
__Status --> 'Planned'-'In Progress'-'Completed'-'All'
__representative  --> representative assigned to the tasks

### Example
#### Sample Request
```
curl --location --request GET '{base_url}/api/method/mobile_app.apis.get_all_tasks?status=Completed&representative=ahmed@test.com' \
```
#### Sample Response
```
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
```
____________________________________________________________________________________________________________________________
## Endpoint :{base_url}/api/method/mobile_app.apis.add_new_task
### Method :POST

### Example
#### Request Body
```
curl --location --request POST '{base_url}/api/method/mobile_app.apis.add_new_task?subject=visit new doctor3&representative=test@test.com&status=Completed&priority=Important&days=Monday&exp_start_date=2023-10-12&start_time=10:30&description=this is important&type=official' \
```
#### Response
 ```
 "Task Created"
 ```
 ____________________________________________________________________________________________________________________________
 ## Endpoint :{base_url}/api/method/mobile_app.apis.update_task_status
 ### Method :PUT
 
 ### Example
 #### Request Body
 ```
 curl --location --request PUT '{base_url}/api/method/mobile_app.apis.update_task_status?name=TASK-2023-00011&status=In Progress' \
 ```
#### Response
```
"Task Status Updated"
```

____________________________________________________________________________________________________________________________
## Endpoint :{base_url}/api/method/mobile_app.apis.delete_task
### Method :DELETE

### Example
#### Request Body
```
curl --location --request DELETE '{base_url}/api/method/mobile_app.apis.delete_task?subject=Visit new doctor1' \
```
#### Response
```
"Task Deleted"
```
______________________________________________________________________________________________________________________________
## Endpoint :{base_url}/api/method/mobile_app.apis.get_vacations
### Method :GET
### URL Parameters:
__employee_name

### Example
#### Sample Request
```
curl --location --request GET '{base_url}/api/method/mobile_app.apis.get_vacations?employee_name=Elmaghraby' \
```
#### Sample Response
```
{
    "message": [
        {
            "employee": "HR-EMP-00004",
            "employee_name": "elmaghraby",
            "leave_type": "Sick Leave",
            "from_date": "2023-07-12",
            "to_date": "2023-07-13",
            "total_leave_days": 0.0,
            "status": "Pending",
            "description": "sick leave",
            "leave_approver": null
        },
        {
            "employee": "HR-EMP-00004",
            "employee_name": "elmaghraby",
            "leave_type": "Sick Leave",
            "from_date": "2023-06-15",
            "to_date": "2023-06-16",
            "total_leave_days": 2.0,
            "status": "Pending",
            "description": null,
            "leave_approver": null
        },
        {
            "employee": "HR-EMP-00004",
            "employee_name": "elmaghraby",
            "leave_type": "Sick Leave",
            "from_date": "2023-07-20",
            "to_date": "2023-07-21",
            "total_leave_days": 0.0,
            "status": "Pending",
            "description": "sick leave",
            "leave_approver": null
        },
        {
            "employee": "HR-EMP-00004",
            "employee_name": "elmaghraby",
            "leave_type": "Sick Leave",
            "from_date": "2023-07-20",
            "to_date": "2023-07-21",
            "total_leave_days": 0.0,
            "status": "Pending",
            "description": "sick leave",
            "leave_approver": null
        }
    ]
}
```
