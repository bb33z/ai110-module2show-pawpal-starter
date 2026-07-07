# PawPal+ Project Reflection

## 1. System Design

The 3 core actions that a user should be able to do is enter general information, generate a plan, and view the displayed plan.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My UML design consists of 4 classes called pet, task, scheduler, and owner. The Owner class holds user information consisting of what the user inputs. The Pet class holds user information which consists of the owner information, pet information, species, age, and any special needs. The Task class shows us what task needs to be carried out (walk, feedings, etc.) and shows the time duration and priority the task may have. The schedulrer class is the logic engine. It takes the information from Pet and Task to create a plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Originally I was given 5 classes before realizing it was a reduncancy to have.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The constraints that my scheduler considers is time of day, completion status, and frequency. I decided that time matters the most because time is important when it comes to scheduling and frequency. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is in conflict detection, which only flags tasks that share the same start time. The only tradeoff is that it isn't able to catch 30 minute overlaps for example because there isn't anything showing duration.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Claude to debug and figure out why some git commits weren't compiling. Asking it to explain what was wrong was really useful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When using the AI, it tried to make me create 5 classes instead of 4 for some reason. While looking closer I realized it was making the visual output it's own class. The way I verified that it was wrong was by reviewing the steps and realizing that the owner and pet classes weren't supposed to be combined and that plan shouldn't have existed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested the behaviors of my scheduler by using pytest. I tested for task completion, task addition, sorting correctness, reccurence logic, and conflict detection. The tests were important because these are the main things the app said it would do.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm confident that the scheduler works the best to it's ability. All of my test did pass and cover the general basis of what's needed. If I had more time I'd test for an owner or pet with no tasks or tasks with no set time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm satisfied with the recurring task feature because it automates a process that would have been a manual import for every single day you need to do it.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another itteration I would add duration to the tasks so that conflict detection could better detect overlapping tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One thing I learned was how seperating logic and data makes the system easier to test. I also learned to double check my AI inputs.
