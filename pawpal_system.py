from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum


class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: Priority
    completed: bool = False
    task_type: str = ""
    frequency: str = "none"
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> "Task | None":
        """Mark this task as completed and generate its next recurrence, if any.

        Sets completed=True on this task. If frequency is "daily" or "weekly",
        returns a new, incomplete Task with the same name/duration/priority/task_type/
        frequency and a due_date advanced by one day or one week respectively. If
        frequency is "none", returns None since there is nothing to recur.

        Returns:
            A new Task representing the next occurrence, or None if this task doesn't recur.
        """
        self.completed = True
        if self.frequency == "daily":
            next_due = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = self.due_date + timedelta(weeks=1)
        else:
            return None
        return Task(
            name=self.name,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            task_type=self.task_type,
            frequency=self.frequency,
            due_date=next_due,
        )


@dataclass
class Pet:
    # Assumption: caller is responsible for keeping owner.pets and pet.owner in sync.
    # TODO: add __post_init__ to auto-append self to owner.pets when constructed with an owner.
    name: str
    age: int
    breed: str
    owner: "Owner" = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class ScheduledTask:
    task: Task
    start_time: str


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def get_all_tasks(self) -> list[Task]:
        """Flatten and return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> list[Task]:
        """Return tasks across this owner's pets, optionally narrowed by completion status and/or pet name.

        Args:
            completed: If given, only include tasks whose completed flag matches this value.
                Leave as None to include tasks regardless of completion status.
            pet_name: If given, only include tasks belonging to the pet with this name.
                Leave as None to include tasks from every pet.

        Returns:
            The matching tasks, in the order their owning pets/tasks appear.
        """
        result = []
        for pet in self.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                result.append(task)
        return result


class Scheduler:
    _PRIORITY_ORDER = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}

    def __init__(self, tasks: list[Task], available_minutes: int, day_start_time: str = "08:00"):
        self.tasks = tasks
        self.available_minutes = available_minutes
        self.day_start_time = day_start_time
        self._plan: list[Task] = []
        self._skipped: list[Task] = []
        self._scheduled: list[ScheduledTask] = []

    def generate_plan(self) -> list[ScheduledTask]:
        """Sort, filter, and time-stamp tasks to produce the day's scheduled plan."""
        self.tasks = self.sort_by_priority()
        self._plan = self.filter_by_time_budget()
        self._scheduled = self._assign_start_times(self._plan)
        return self._scheduled

    def _assign_start_times(self, tasks: list[Task]) -> list[ScheduledTask]:
        """Compute a sequential clock start time for each task from day_start_time."""
        current_time = datetime.strptime(self.day_start_time, "%H:%M")
        scheduled = []
        for task in tasks:
            scheduled.append(ScheduledTask(task=task, start_time=current_time.strftime("%H:%M")))
            current_time += timedelta(minutes=task.duration_minutes)
        return scheduled

    def sort_by_priority(self) -> list[Task]:
        """Order tasks by priority (high to low), breaking ties by shorter duration."""
        return sorted(
            self.tasks,
            key=lambda task: (self._PRIORITY_ORDER[task.priority], task.duration_minutes),
        )

    def sort_by_start_time(self) -> list[ScheduledTask]:
        """Order the current scheduled plan chronologically by start_time.

        Sorts using the raw "HH:MM" strings as the key rather than parsing them into
        datetime objects. This is safe because the values are always zero-padded
        24-hour times, so string comparison already matches chronological order
        (e.g. "08:00" < "09:30" < "13:00").

        Returns:
            A new list of ScheduledTask, earliest start_time first. Does not mutate self._scheduled.
        """
        return sorted(self._scheduled, key=lambda st: st.start_time)

    def detect_conflicts(
        self, other_scheduled: list[ScheduledTask], self_label: str = "", other_label: str = ""
    ) -> list[str]:
        """Find overlapping time ranges between this plan and another scheduled plan.

        Two ScheduledTasks conflict when their [start_time, start_time + duration_minutes)
        ranges overlap. Every pair of tasks (one from this plan, one from other_scheduled)
        is compared, so more than one conflict can be reported for the same task. This
        never raises on a conflict; it only collects warnings for the caller to handle.

        Args:
            other_scheduled: The scheduled plan to compare against (e.g. another pet's plan).
            self_label: Human-readable name for this plan's owner, used in warning text.
            other_label: Human-readable name for other_scheduled's owner, used in warning text.

        Returns:
            A list of warning strings, one per overlapping pair, or an empty list if none overlap.
        """

        def time_range(scheduled_task: ScheduledTask) -> tuple[datetime, datetime]:
            start = datetime.strptime(scheduled_task.start_time, "%H:%M")
            end = start + timedelta(minutes=scheduled_task.task.duration_minutes)
            return start, end

        warnings = []
        for mine in self._scheduled:
            mine_start, mine_end = time_range(mine)
            for theirs in other_scheduled:
                their_start, their_end = time_range(theirs)
                if mine_start < their_end and their_start < mine_end:
                    warnings.append(
                        f"Conflict: '{mine.task.name}' ({self_label}) overlaps with "
                        f"'{theirs.task.name}' ({other_label}) at {mine.start_time}"
                    )
        return warnings

    def filter_by_time_budget(self) -> list[Task]:
        """Split tasks into an included plan and a skipped list based on available_minutes."""
        included = []
        skipped = []
        remaining = self.available_minutes
        for task in self.tasks:
            if task.duration_minutes <= remaining:
                included.append(task)
                remaining -= task.duration_minutes
            else:
                skipped.append(task)
        self._skipped = skipped
        return included

    def explain_plan(self) -> str:
        """Render the scheduled plan and any skipped tasks as human-readable lines."""
        lines = [
            f"{st.start_time} — {st.task.name} ({st.task.duration_minutes} min) "
            f"[priority: {st.task.priority.name.lower()}]"
            for st in self._scheduled
        ]
        lines += [
            f"skipped {task.name} — insufficient time remaining"
            for task in self._skipped
        ]
        return "\n".join(lines)
