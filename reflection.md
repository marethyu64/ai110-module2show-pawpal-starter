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

My scheduler considers the constraints for time, priority, pet association, frequency, and completion status. For time, each task has a specific scheduled datetime, where the scheduler groups them by date and time sequentially. For priority, each task has a priority level based on their number, with 1 being the highest priority. For pet association, tasks are linked to specific pets based on their pet_id attribute, so that the user can tell which pet the task is for. Frequency allows tasks to repeat once, daily, weekly, or monthly, which allows the user to have recurring tasks that don't need to constantly be set. Lastly, I considered the constraint of completion status, in which the scheduler tracks which tasks are complete or still pending, allowing the owner to tell what they have and haven't done. I decided which constraints mattered most by carefully reading over the README.md, imagining what constraints I as a pet owner would immediately expect first, and asking Copilot if I missed any constraints.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff the scheduler makes is only checking for exact time matches instead of overlapping time durations. Currently, the conflict detection algorithm groups tasks by their exact scheduled datetime and flags any time slot with multiple tasks as a conflict. This approach doesn't consider how long each task takes or whether tasks might overlap partially. This tradeoff is reasonable for this scenario because the current system doesn't track task durations, so we can't determine overlaps. Furthermore, only checking for exact time conflicts are easy for users to understand and resolve, and checking exact matches would require more processing time. Since this is still a work in progress app, checking for overlapping times can still be implemented in the future, but it's important to lay down the vital features first.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

During this project I used VS Code Copilot to generate UML class diagrams with Mermaid.js, asked to create a plan of how it would implement the scheduling algorithm, and to help debug issues I couldn't figure out. The prompts that were most helpful was asking for inline code suggestions as well as using Copilot smart actions for generating docstring and test templates.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One example of a time I didn't just accept what the AI suggested was during the conflict detection part. Copilot gave me a version using a list comprehension with defaultdict, but I decided to keep my original version with explicit loops and intermediate variables instead. I made this choice because my version is easier to read and understand, which matters more in a teaching project like this one. I verified the decision by running the test suite and manually reading the code path, then deciding that clarity and maintainability matter more than compactness for this codebase.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I implemented 6 tests to cover the core functionality of my scheduler. These include tests for marking tasks complete, adding tasks, and sorting them in chronological order. I also tested that recurring tasks (both daily and weekly) automatically create the next occurrence when completed, and that the conflict detection system correctly catches when two tasks are scheduled at the same time. These tests were important because they helped me uncover any bugs that I didn't notice to prevent errors in the future the user might come across.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident that my scheduler works correctly, but won't be surprised to hear about a few minor bugs here and there. I made sure Copilot looked through all of my code to verify it worked cleanly, asked it to create test cases, tested most edge cases, and went through the streamlit site myself looking for bugs. If I had more time, I would add tests for duplicate tasks (the user adds the same task twice), invalid data (negative priorities, no pet IDs, etc.), and inconsistent days-in-a-month handling (Feb only has 28 days, other months have 30/31).  

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most proud of learning how to modify the frontend and adding the ability to assign tasks to certain pets and add recurring tasks, since it was asked of in the assignment.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would like to redesign the Streamlit UI and add more functionality to it, since the current template is a bit empty. Although it's not asked of in the assignment, I would have liked to spend more time making my own UI so that I could fully realize the vision I had for PawPal+.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned about working with AI on this project is that it isn't fully reliable. It's not the driver in the car, it's the passenger on the side that can direct you. It's important that I, the driver, understand where we're going and where the directions are taking us. Furthermore, I realized that tests are an extremely reliable way to know if I can trust AI-generated code, as it gives me way more confidence that my code works rather than my AI saying it does.