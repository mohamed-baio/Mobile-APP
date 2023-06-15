# Mobile-APP
## Endpoint:{base_url}/api/method/mobile_app.apis.get_all_tasks
### Method :GET
### URL Parameters:
__ Status --> 'Planned'-'In Progress'-'Completed'-'All'
__ representative  --> representative assigned to the tasks

### Sample Request
curl --location --request GET '{base_url}/api/method/mobile_app.apis.get_all_tasks?status=Completed&representative=ahmed@test.com' \

### Sample Response
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
        },
