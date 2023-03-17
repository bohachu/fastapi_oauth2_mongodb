'''

{
    "token": "ASDFSDFDSF",
    "github_username": "bohachu",
    "repo": "add_two_number",
    "github_token": "ASDKFJsadfkjADFKJSDAFKJ",
    "work_dir": "/",
    "run": "python add_two_number.py",
    "export": {
   	   "s3_output_end_point": "http://127.0.0.1",
    },
    "tasks_args": [
   	   ["https://drive.google.com/?document_id=ASDFADSF1"],
   	   ["https://drive.google.com/?document_id=ASDFADSF2"],
    ]
}

Output
{
  "action": "run_github",
  "username": "bohachu",
  "time": "2022-03-01T10:00:00Z",
  "success": true,
  "message": "Tasks submitted successfully.",
  "task_ids": [
	"6f950c6d-f465-47b1-8f46-3c28e7f719d9",
	"7a2d0879-7bfc-4d4b-9fc4-6f8a684cde5f"
  ]
}


https://falra.net/api/status
Input
{
  "token": "ASDFSDFDSF",
  "task_ids": [
	"6f950c6d-f465-47b1-8f46-3c28e7f719d9",
	"7a2d0879-7bfc-4d4b-9fc4-6f8a684cde5f"
  ]
}

Output
{
  "action": "run_github",
  "username": "bohachu",
  "time": "2022-03-01T10:00:00Z",
  "success": true,
  "message": "Tasks found success.",
  "tasks_status":[
{
    "task_id": "6f950c6d-f465-47b1-8f46-3c28e7f719d9",
    "status": "completed",
    "start_time": "2022-03-01T10:00:00",
    "end_time": "2022-03-01T10:10:00",
    "execution_time": 600,
    "stdout": "Hello, world!",
    "stderr": ""
  },
{
    "task_id": "7a2d0879-7bfc-4d4b-9fc4-6f8a684cde5f",
    "status": "completed",
    "start_time": "2022-03-01T10:00:00",
    "end_time": "2022-03-01T10:10:00",
    "execution_time": 600,
    "stdout": "Hello, world!",
    "stderr": ""
  }]
}

'''