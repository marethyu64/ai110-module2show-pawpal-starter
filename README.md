# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Features

- Owner/pet model: `Owner`, `Pet`, `Task`, and `Scheduler` classes in `pawpal_system.py`
- Task creation: `Owner.create_task()` attaches tasks to pets in the scheduler
- Time-based sorting: `Scheduler.sort_by_time(tasks)` returns tasks in chronological order
- Task filtering: `Scheduler.filter_tasks(tasks, completion_status, pet_name, owner)` for targeted views
- Recurring tasks: `Scheduler.mark_task_complete(task)` auto-generates next daily/weekly task
- Conflict detection: `Scheduler.detect_conflicts()` flags exact datetime collisions
- Multi-step schedule retrieval: `Scheduler.generate_daily_task_list(date)` returns prioritized daily plan
- Owner persistence in UI: `st.session_state.owner` in `app.py` keeps data while the Streamlit session runs

## Smarter Scheduling

The PawPal+ scheduler now includes advanced features for efficient pet care planning:

### Task Organization
- **Time-based sorting**: Sort tasks chronologically with `sort_by_time()`
- **Smart filtering**: Filter tasks by completion status or specific pets with `filter_tasks()`
- **Priority ordering**: Tasks are sorted by priority (1 = highest) within time slots

### Recurring Tasks
- **Automatic scheduling**: Daily and weekly tasks automatically create next occurrences when completed
- **Seamless workflow**: Mark a daily medication task complete, and tomorrow's dose is scheduled automatically
- **Flexible frequencies**: Support for daily, weekly, monthly, and one-time tasks

### Conflict Detection
- **Lightweight validation**: Detects exact time conflicts between tasks
- **Clear warnings**: Provides user-friendly messages when scheduling conflicts occur
- **Non-blocking**: Returns warnings instead of crashing the application

### Example Usage
```python
# Sort tasks by time
time_sorted = scheduler.sort_by_time(tasks)

# Filter for pending tasks only
pending = scheduler.filter_tasks(tasks, completion_status=False)

# Check for scheduling conflicts
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
```

## 📸 Demo

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Testing PawPal+

Run tests with:

```bash
python -m pytest
```

This test suite covers:

- Task creation and task count behavior
- Sorting correctness by datetime order (`sort_by_time`)
- Task filtering by completion and pet name
- Recurring task behavior for daily and weekly frequencies (`mark_task_complete`)
- Conflict detection for exact duplicate task times (`detect_conflicts`)

Confidence Level: ★★★★★ (5/5) based on consistent green test results.

