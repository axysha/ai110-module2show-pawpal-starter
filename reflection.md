# PawPal+ Project Reflection

## 1. System Design
Users should be able to add pet information (name, age, breed, etc) and owner information (name, occupancy,city/location)
Users should be able to create and save a task like "Take Roxy on a walk ~ 30 minutes"
Users should be able to see the overview(list based on priorities) of tasks on the home page. 

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
The initial design consists of four core classes — Owner, Pet, Task, and Scheduler — along with a Priority enum to constrain task urgency to LOW, MEDIUM, or HIGH. Owner holds a name and a list of associated Pet objects, while Pet stores identifying details (name, age, breed) along with a back-reference to its Owner and a list of Task objects it owns. Task is a lightweight data class capturing what needs to be done — name, duration, priority, completion status, and task type — with no behavior of its own. Scheduler is the only class with real logic: it takes a pool of tasks and a time budget, then sorts, filters, and assembles them into a daily plan while generating a plain-language explanation of its choices. The Owner–Pet and Pet–Task relationships are modeled as composition, since pets and tasks don't have independent existence outside their owner or pet, while Scheduler–Task is a simple association, since the scheduler operates on tasks without owning them. This structure keeps data (Owner, Pet, Task) and behavior (Scheduler) cleanly separated, following a single-responsibility principle per class.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, I slightly changed my design by avoiding ambiguity in the generate_plan() method by matching its setup to the other methods, like sort_by_priority() and filter_by_time_budget(). I'm also making an assumption in my design that a caller is responsible for keeping owner.pets and pet.owner in sync.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The scheduler really only weighs two constraints, priority and available time. Every task carries a priority level and a duration, and the scheduler leans on priority as the main ordering signal, using duration only as a second reference when two tasks share the same priority. Available time acts as a hard cutoff rather than something the scheduler negotiates around, so once the minutes run out, whatever is left simply gets skipped and reported as such rather than squeezed in. Priority was treated as the constraint that mattered most because the whole point of the app is helping an owner get through the most important thing first when time is limited, so something like a high priority feeding shouldn't lose its spot to a low priority grooming task just because grooming happened to be entered first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One trade off is that the scheduler always sorts strictly by priority first and duration second, with no way to pin a task to a specific time of day. That means something like feeding at a fixed hour has no way to stay in-place there, since a higher priority task can always shift everything after it later. This keeps the scheduling logic simple and easy to reason about, but it sacrifices the kind of real world scheduling where certain tasks genuinely need to happen at a particular time rather than just in some order.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used AI tools in all parts of developing this project. In the beginning, I used it for system design and brainstorming the object set-up for this app. Then I used it to help me build the UML diagrams. After I utilized different chats for developing, ui funcionality, testing, and other tasks. My most effective prompting techinque was to give a clear action and attach relevant context files for the best useful output. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
One clear example was I asked Claude to make tests/test_pawpal.py import from pawpal_system.py, Claude decided to write an empty conftest.py at the project root as a safety net for the import path but I rejected that tool call and asked "what exactly is this for?" instead of accepting it.  I evaluated the suggestion by asking follow-up questions to make sure that the action was neccesary/releavnt to the task or not. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested the three core algorithms behind the scheduling system: chronological sorting of a day's plan, daily-task recurrence, and duplicate/overlapping time-slot detection. These matter because each one silently produces wrong output rather than crashing. I specifically verified the happy path for each (in-order results, next-day task creation, flagged overlaps) alongside edge cases like empty schedules, same start times, and duplicate bookings. 


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I am overall confident that my scheduler works correctly and some edge cases I would like to test next time the weekly recurrence (due_date + 7 days, not 1), multi-day/multi-pet conflict detection across more than two schedules at once, and behavior when available_minutes is zero or negative in filter_by_time_budget

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The part of the project I felt most satisfied with was collaborating with Claude Code and getting to design this app through Python OOP principles

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would try to scope the design of each class better and really figure the connections between the classes and what variables/methods each class needed for a specific features or functionalities. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
It's important to be clear and iterative when designing systems or working with AI. Providing AI with the proper context and updates helps the design transform from conception to real working code with functionality. It's also crucial to go over AI suggestions and use best human judgement before implementing a full design plan. 
