"""PawPal+ core system.

Core implementation of the four classes:
  Task      -- a single care activity
  Pet       -- a pet and its list of tasks
  Owner     -- manages multiple pets, provides access to all their tasks
  Scheduler -- retrieves, organizes, and manages tasks across all pets
"""


class Task:
    """A single care activity (e.g. 'Morning walk')."""

    def __init__(self, description, time=None, frequency="daily", completed=False):
        """Create a care activity with a description, optional time, and frequency."""
        self.description = description   # what the task is
        self.time = time                # when it should happen, e.g. "08:00" (or None)
        self.frequency = frequency      # "daily", "weekly", etc.
        self.completed = completed       # has it been done?

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Reset the task to not-yet-done."""
        self.completed = False

    def __repr__(self):
        """Return a readable one-line view of the task."""
        box = "x" if self.completed else " "
        when = f" @ {self.time}" if self.time else ""
        return f"[{box}] {self.description}{when} ({self.frequency})"


class Pet:
    """A pet and the care tasks that belong to it."""

    def __init__(self, name, species=None, age=None, special_needs=None):
        """Create a pet with basic details and an empty task list."""
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs
        self.tasks = []                 # a list of Task objects

    def add_task(self, task):
        """Attach a Task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task):
        """Remove a Task from this pet (no-op if it isn't there)."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self):
        """Return this pet's list of tasks."""
        return self.tasks

    def __repr__(self):
        """Return a readable one-line view of the pet and its task count."""
        species = f", {self.species}" if self.species else ""
        return f"{self.name}{species} ({len(self.tasks)} tasks)"


class Owner:
    """The owner: manages multiple pets and provides access to all their tasks."""

    def __init__(self, name, preferences=None):
        """Create an owner with a name, preferences, and an empty pet list."""
        self.name = name
        self.preferences = preferences if preferences is not None else {}
        self.pets = []                  # a list of Pet objects

    def add_pet(self, pet):
        """Add a Pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return every task across all of this owner's pets (flattened)."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_all_tasks_with_pet(self):
        """Return (pet, task) pairs so callers know which pet each task belongs to."""
        return [(pet, task) for pet in self.pets for task in pet.get_tasks()]

    def __repr__(self):
        """Return a readable one-line view of the owner and pet count."""
        return f"{self.name} (owns {len(self.pets)} pets)"


class Scheduler:
    """The 'brain': retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner):
        """Create a scheduler that reads tasks from the given owner."""
        self.owner = owner              # the Scheduler works from an Owner

    def get_all_tasks(self):
        """Retrieve every task by delegating to the Owner (single access point)."""
        return self.owner.get_all_tasks()

    def pending_tasks(self):
        """Return tasks that haven't been completed yet."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def completed_tasks(self):
        """Return tasks that are already done."""
        return [task for task in self.get_all_tasks() if task.completed]

    def tasks_by_frequency(self, frequency):
        """Return tasks matching a given frequency (e.g. 'daily')."""
        return [task for task in self.get_all_tasks() if task.frequency == frequency]

    def sort_by_time(self):
        """Return all tasks ordered by their scheduled time (untimed tasks last)."""
        return sorted(self.get_all_tasks(), key=lambda task: task.time or "99:99")

    def daily_plan(self):
        """Return today's still-pending tasks, ordered by time."""
        pending = self.pending_tasks()
        return sorted(pending, key=lambda task: task.time or "99:99")
