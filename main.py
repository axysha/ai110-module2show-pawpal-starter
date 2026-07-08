from datetime import date

from pawpal_system import Owner, Pet, Task, Priority, Scheduler

owner = Owner(name="Joseph")

buddy = Pet(name="Buddy", age=3, breed="Labrador", owner=owner)
whiskers = Pet(name="Whiskers", age=5, breed="Tabby", owner=owner)
owner.pets.extend([buddy, whiskers])

# Tasks added out of priority/duration order on purpose, to exercise sorting.
buddy.add_task(Task("Grooming", duration_minutes=60, priority=Priority.LOW, frequency="weekly"))
buddy.add_task(Task("Evening walk", duration_minutes=20, priority=Priority.MEDIUM))
buddy.add_task(Task("Morning walk", duration_minutes=30, priority=Priority.HIGH))
whiskers.add_task(Task("Litter box cleaning", duration_minutes=15, priority=Priority.HIGH))
whiskers.add_task(Task("Nail trim", duration_minutes=20, priority=Priority.LOW))
whiskers.add_task(Task("Feeding", duration_minutes=10, priority=Priority.MEDIUM, frequency="weekly"))

# Mark a few tasks complete so filter_tasks(completed=...) has something to show.
# If a task recurs (daily/weekly), mark_complete() hands back the next occurrence,
# which we append to the owning pet's task list.
for pet, task in [(buddy, buddy.tasks[0]), (whiskers, whiskers.tasks[2])]:
    next_occurrence = task.mark_complete()
    if next_occurrence is not None:
        pet.add_task(next_occurrence)

schedules_by_pet_name = {}

for pet in owner.pets:
    # Only schedule tasks that are still pending and actually due today —
    # a next-week recurrence created by mark_complete() shouldn't appear in today's plan.
    todays_tasks = [task for task in pet.tasks if not task.completed and task.due_date <= date.today()]
    scheduler = Scheduler(todays_tasks, available_minutes=45)
    scheduler.generate_plan()
    schedules_by_pet_name[pet.name] = scheduler._scheduled

    print(f"Daily plan for {pet.name} ({pet.breed}):")
    print(scheduler.explain_plan())

    # Shuffle the scheduled plan, then use sort_by_start_time() to restore chronological order.
    scheduler._scheduled = list(reversed(scheduler._scheduled))
    print("Reversed, then re-sorted by start_time:")
    for st in scheduler.sort_by_start_time():
        print(f"  {st.start_time} - {st.task.name}")
    print("-----")

print("Checking for schedule conflicts between Buddy and Whiskers:")
buddy_scheduler = Scheduler([], available_minutes=45)
buddy_scheduler._scheduled = schedules_by_pet_name["Buddy"]
conflicts = buddy_scheduler.detect_conflicts(
    schedules_by_pet_name["Whiskers"], self_label="Buddy", other_label="Whiskers"
)
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")

print("Completed tasks across all pets:")
for task in owner.filter_tasks(completed=True):
    print(f"  {task.name}")

print("Incomplete tasks for Buddy only:")
for task in owner.filter_tasks(completed=False, pet_name="Buddy"):
    print(f"  {task.name}")
