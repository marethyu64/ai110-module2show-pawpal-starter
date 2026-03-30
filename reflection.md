# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Three core actions a user should be able to perform is creating a schedule, add tasks, and add pets.

In my initial UML design, I'll have classes for Owner, Pet, Task, and Scheduler. The Owner class will have attributes such as name, owner preferences, and a list of pets from the Pet class. The methods the Owner class will have is adding pets, editing name, and editing preferences. The Pet class will have attributes such as pet type, breed, name, and logs (last walked, last groomed, etc.). Its methods consist of updating the logs, updating pet info, and deleting the pet. The Task class will have attributes time scheduled, task priority, and completion. Its methods consist of editing task info, marking task completion, and deleting itself. The Scheduler class will have the attributes of time available and a list of tasks from the Task class. Its methods will be adding tasks, adding a schedule, and generating a daily list of tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
