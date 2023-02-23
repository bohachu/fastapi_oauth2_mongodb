# must consider following parameters in framework:
# "max_concurrent_tasks": 10,
# "timeout": 3600,
# "retry_attempts": 3,
# "retry_delay": 10,

api_run_input = {
    "github_username": "your_github_username",
    "repo": "your_repo_name",
    "github_token": "your_github_token",
    "work_dir": "/your/path",
    "run": "python your_file_name.py",
    "export": {
        "API_KEY": "my_private_key",
        "DB_PASSWORD": "my_password"
    },
    "tasks_args": [
        ["/google_drive/input1.zip", "/google_drive/output1.zip"],
        ["/google_drive/input2.zip", "/google_drive/output2.zip"]
    ]

}

api_run_output = {
    "success": true,
    "message": "Tasks submitted successfully.",
    "task_ids": [
        "6f950c6d-f465-47b1-8f46-3c28e7f719d9",
        "7a2d0879-7bfc-4d4b-9fc4-6f8a684cde5f"
    ]
}
