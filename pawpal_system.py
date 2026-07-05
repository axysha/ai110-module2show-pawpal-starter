from dataclasses import dataclass, field
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


@dataclass
class Pet:
    name: str
    age: int
    breed: str
    owner: "Owner" = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)


class Scheduler:
    def __init__(self, tasks: list[Task], available_minutes: int):
        self.tasks = tasks
        self.available_minutes = available_minutes

    def generate_plan(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        pass

    def sort_by_priority(self) -> list[Task]:
        pass

    def filter_by_time_budget(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass
