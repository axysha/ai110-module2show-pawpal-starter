from pawpal_system import Pet, Priority, Task


def test_mark_complete():
    task = Task("Morning walk", duration_minutes=30, priority=Priority.HIGH)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", age=3, breed="Labrador")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feeding", duration_minutes=10, priority=Priority.MEDIUM))

    assert len(pet.tasks) == 1
