from pawpal_system import Owner, Pet, Task, Priority, Scheduler

owner = Owner(name="Joseph")

buddy = Pet(name="Buddy", age=3, breed="Labrador", owner=owner)
whiskers = Pet(name="Whiskers", age=5, breed="Tabby", owner=owner)
owner.pets.extend([buddy, whiskers])

buddy.add_task(Task("Morning walk", duration_minutes=30, priority=Priority.HIGH))
buddy.add_task(Task("Grooming", duration_minutes=60, priority=Priority.LOW))
whiskers.add_task(Task("Feeding", duration_minutes=10, priority=Priority.MEDIUM))
whiskers.add_task(Task("Litter box cleaning", duration_minutes=15, priority=Priority.HIGH))

for pet in owner.pets:
    scheduler = Scheduler(pet.tasks, available_minutes=45)
    scheduler.generate_plan()

    print(f"Daily plan for {pet.name} ({pet.breed}):")
    print(scheduler.explain_plan())
    print("-----")
