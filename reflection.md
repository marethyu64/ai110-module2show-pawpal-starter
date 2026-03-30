# PawPal+ Project Reflection

## 1. System Design

Three core actions a user should be able to perform is creating a schedule, add tasks, and add pets.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

In my initial UML design, I'll have classes for Owner, Pet, Task, and Scheduler. The Owner class will have attributes such as name, owner preferences, and a list of pets from the Pet class. The methods the Owner class will have is adding pets, editing name, and editing preferences. The Pet class will have attributes such as pet type, breed, name, and logs (last walked, last groomed, etc.). Its methods consist of updating the logs, updating pet info, and deleting the pet. The Task class will have attributes time scheduled, task priority, and completion. Its methods consist of editing task info, marking task completion, and deleting itself. The Scheduler class will have the attributes of time available and a list of tasks from the Task class. Its methods will be adding tasks, adding a schedule, and generating a daily list of tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

My design did change during implementation. The most important changes were adding a connection between Pet and Task as well as adding a connection between Owner and Scheduler. When I first brainstormed, I didn't take into account how some tasks were for specific pets only, which is why the AI suggested I add a pet_id attribute for each task. That way, the owner will know what pet the task is referring to. In addition, the Scheduler class now has the Owner class as one of its attributes so that it can access the owner preferences and pets.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff the scheduler makes is only checking for exact time matches instead of overlapping time durations. Currently, the conflict detection algorithm groups tasks by their exact scheduled datetime and flags any time slot with multiple tasks as a conflict. This approach doesn't consider how long each task takes or whether tasks might overlap partially.

This tradeoff is reasonable for this scenario because:
1. **Simplicity**: The current system doesn't track task durations, so we can't determine overlaps
2. **Clarity**: Exact time conflicts are unambiguous and easy for users to understand and resolve
3. **Performance**: Checking exact matches is computationally simple (O(n) time complexity)
4. **Progressive enhancement**: The system can be extended later to include duration-based overlap detection when task durations are added

For a pet care scheduling app, this approach prioritizes preventing obviously problematic schedules (multiple tasks at the exact same time) over more complex overlap scenarios that might be acceptable depending on task types and pet needs.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I shared the `detect_conflicts()` method with Copilot and asked how it could be simplified for better readability or performance, the AI suggested a more "Pythonic" version using `collections.defaultdict` and a list comprehension:

```python
from collections import defaultdict

def detect_conflicts(self) -> List[str]:
    time_groups = defaultdict(list)
    
    for task in self.tasks:
        time_groups[task.time_scheduled].append(task)
    
    warnings = [
        f"⚠️  Scheduling conflict at {time_key.strftime('%m/%d %H:%M')}: "
        f"{', '.join(f\"'{t.description}'\" for t in tasks_at_time)} are scheduled simultaneously"
        for time_key, tasks_at_time in time_groups.items()
        if len(tasks_at_time) > 1
    ]
    
    return warnings
```

While this version is more concise and uses Python idioms effectively, I decided to keep the original implementation. The original version is more readable for developers learning Python, with explicit loops and clear variable names that make the algorithm's logic easier to follow. For an educational project like PawPal+, prioritizing code readability over conciseness is more appropriate. I verified this decision by considering the target audience (students) and the project's goals (learning system design and Python programming).

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
