# Scheduling

<https://gist.github.com/nihal111/23faa51c3f88a281b676dcbac77ce015?permalink_comment_id=2396063#gistcomment-2396063>

- Install pywin32 from here(<https://github.com/mhammond/pywin32>) or pip install pywin32.

- Use Windows Task Scheduler to schedule the python script to run on every startup.

- Follow instructions from here

  - Create a Task

  - In General, check "Run with highest privileges"

  - Set Trigger as "On workstation unlock"

  - Set Action as "Start a Program" with Program/Script="C:\source\synchronize_time\synchronize_time.bat"
