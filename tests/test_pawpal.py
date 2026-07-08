from datetime import date

from pawpal_system import Pet, Priority, ScheduledTask, Scheduler, Task


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


# --- Sorting correctness ---------------------------------------------------


def test_sort_by_start_time_orders_chronologically():
    """Happy path: an out-of-order schedule comes back sorted earliest-first."""
    scheduler = Scheduler(tasks=[], available_minutes=0)
    scheduler._scheduled = [
        ScheduledTask(task=Task("Dinner", 30, Priority.MEDIUM), start_time="13:00"),
        ScheduledTask(task=Task("Walk", 30, Priority.HIGH), start_time="08:00"),
        ScheduledTask(task=Task("Meds", 10, Priority.HIGH), start_time="10:30"),
    ]

    ordered = scheduler.sort_by_start_time()

    assert [st.start_time for st in ordered] == ["08:00", "10:30", "13:00"]


def test_sort_by_start_time_empty_schedule_returns_empty_list():
    """Edge case: a pet with no tasks yields an empty (not error-ing) schedule."""
    scheduler = Scheduler(tasks=[], available_minutes=0)

    assert scheduler.sort_by_start_time() == []


def test_sort_by_start_time_tie_keeps_both_tasks_in_original_order():
    """Edge case: two tasks at the exact same time must both survive the sort."""
    scheduler = Scheduler(tasks=[], available_minutes=0)
    first = ScheduledTask(task=Task("Walk", 30, Priority.HIGH), start_time="09:00")
    second = ScheduledTask(task=Task("Feeding", 10, Priority.MEDIUM), start_time="09:00")
    scheduler._scheduled = [first, second]

    ordered = scheduler.sort_by_start_time()

    assert ordered == [first, second]


# --- Recurrence logic --------------------------------------------------------


def test_mark_complete_daily_task_creates_next_day_task():
    """Happy path: completing a daily task produces tomorrow's occurrence."""
    task = Task(
        "Morning walk",
        duration_minutes=30,
        priority=Priority.HIGH,
        frequency="daily",
        due_date=date(2026, 7, 8),
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 7, 9)
    assert next_task.name == task.name
    assert next_task.duration_minutes == task.duration_minutes
    assert next_task.priority == task.priority
    assert next_task.frequency == "daily"


def test_mark_complete_non_recurring_task_returns_none():
    """Edge case: a one-off task must not spawn a phantom recurrence."""
    task = Task("One-time vet visit", duration_minutes=45, priority=Priority.MEDIUM)

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is None


# --- Conflict detection -------------------------------------------------------


def test_detect_conflicts_flags_overlapping_times():
    """Happy path: overlapping time ranges across two plans are flagged."""
    scheduler = Scheduler(tasks=[], available_minutes=0)
    scheduler._scheduled = [ScheduledTask(task=Task("Walk", 30, Priority.HIGH), start_time="09:00")]
    other_scheduled = [ScheduledTask(task=Task("Vet visit", 30, Priority.MEDIUM), start_time="09:15")]

    warnings = scheduler.detect_conflicts(other_scheduled, self_label="Buddy", other_label="Max")

    assert len(warnings) == 1
    assert "Buddy" in warnings[0] and "Max" in warnings[0]


def test_detect_conflicts_flags_duplicate_start_times():
    """Edge case: two tasks booked at the exact same time must be flagged."""
    scheduler = Scheduler(tasks=[], available_minutes=0)
    scheduler._scheduled = [ScheduledTask(task=Task("Walk", 30, Priority.HIGH), start_time="09:00")]
    other_scheduled = [ScheduledTask(task=Task("Grooming", 20, Priority.LOW), start_time="09:00")]

    warnings = scheduler.detect_conflicts(other_scheduled, self_label="Buddy", other_label="Max")

    assert len(warnings) == 1


def test_detect_conflicts_back_to_back_tasks_do_not_conflict():
    """Edge case: one task ending exactly when the next starts is not an overlap."""
    scheduler = Scheduler(tasks=[], available_minutes=0)
    scheduler._scheduled = [ScheduledTask(task=Task("Walk", 30, Priority.HIGH), start_time="09:00")]
    other_scheduled = [ScheduledTask(task=Task("Vet visit", 30, Priority.MEDIUM), start_time="09:30")]

    assert scheduler.detect_conflicts(other_scheduled, self_label="Buddy", other_label="Max") == []


def test_detect_conflicts_with_no_tasks_returns_empty_list():
    """Edge case: an empty schedule (pet with no tasks) reports no conflicts."""
    scheduler = Scheduler(tasks=[], available_minutes=0)
    scheduler._scheduled = []

    assert scheduler.detect_conflicts([], self_label="Buddy", other_label="Max") == []
