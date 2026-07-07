"""PawPal+ core system.

Class skeletons generated from diagrams/uml.mmd.
No logic yet -- just names, attributes, and empty method stubs.
"""


class Task:
    """A single pet-care item (walk, feeding, meds, grooming, etc.)."""

    def __init__(
        self,
        name,
        duration,
        priority,
        category=None,
        fixed_time=None,
        recurrence=None,
        status="scheduled",
    ):
        self.name = name
        self.duration = duration          # minutes
        self.priority = priority          # e.g. "high" / "medium" / "low"
        self.category = category
        self.fixed_time = fixed_time      # locked start time, or None if flexible
        self.recurrence = recurrence      # e.g. "daily" / "weekly" / None
        self.status = status              # "scheduled" / "done" / "skipped"

    def mark_done(self):
        """Mark this task as completed."""
        pass

    def is_valid(self):
        """Return True if the task's fields are valid (duration > 0, etc.)."""
        pass


class Pet:
    """Combined owner + pet info, and the pet's list of care tasks."""

    def __init__(
        self,
        owner_name,
        available_minutes,
        name,
        species=None,
        age=None,
        special_needs=None,
        preferences=None,
    ):
        # Owner info
        self.owner_name = owner_name
        self.available_minutes = available_minutes
        self.preferences = preferences if preferences is not None else {}
        # Pet info
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs
        # A Pet holds Task objects
        self.tasks = []

    def add_task(self, task):
        """Add a Task to this pet's task list."""
        pass

    def edit_task(self, task_id):
        """Edit an existing task."""
        pass

    def remove_task(self, task_id):
        """Remove a task from this pet's task list."""
        pass


class Plan:
    """The generated daily plan: what was scheduled, what was dropped, and why."""

    def __init__(
        self,
        scheduled_tasks=None,
        dropped_tasks=None,
        total_time_used=0,
        reasoning="",
    ):
        self.scheduled_tasks = scheduled_tasks if scheduled_tasks is not None else []
        self.dropped_tasks = dropped_tasks if dropped_tasks is not None else []
        self.total_time_used = total_time_used
        self.reasoning = reasoning

    def explain(self):
        """Return a human-readable explanation of why the plan looks this way."""
        pass

    def summary(self):
        """Return a short summary (tasks scheduled, skipped, time used)."""
        pass


class Scheduler:
    """Reads a Pet's constraints and its tasks, then produces a Plan."""

    def __init__(self, pet):
        # A Scheduler works from a Pet object
        self.pet = pet
        self.tasks = pet.tasks
        self.available_minutes = pet.available_minutes
        self.preferences = pet.preferences

    def sort_by_priority(self):
        """Return tasks ordered by priority (ties broken by duration/fixed time)."""
        pass

    def fit_to_budget(self):
        """Select tasks that fit within available_minutes."""
        pass

    def resolve_conflicts(self):
        """Handle overlapping time slots between fixed-time tasks."""
        pass

    def generate_plan(self):
        """Build and return a Plan from the pet's tasks and constraints."""
        pass
