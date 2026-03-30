# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

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

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
