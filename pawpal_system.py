from dataclasses import dataclass, field
from datetime import datetime, timedelta
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

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


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
