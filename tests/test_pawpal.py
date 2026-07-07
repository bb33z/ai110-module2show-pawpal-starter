"""Basic tests for PawPal+ core behaviors."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    """Calling mark_complete() should change the task's status to completed."""
    task = Task("Morning walk", time="08:00")

    assert task.completed is False        # starts incomplete
    task.mark_complete()
    assert task.completed is True         # now complete


def test_task_addition_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count."""
    pet = Pet("Biscuit", species="Golden Retriever")

    assert len(pet.tasks) == 0            # no tasks yet
    pet.add_task(Task("Feeding", time="09:00"))
    assert len(pet.tasks) == 1            # one task after adding


def test_completing_recurring_task_creates_next_occurrence():
    """Completing a daily task should spawn a fresh copy due one day later."""
    owner = Owner("Betsy")
    pet = Pet("Biscuit")
    owner.add_pet(pet)
    task = Task("Morning walk", time="08:00", frequency="daily", due_date=date.today())
    pet.add_task(task)

    scheduler = Scheduler(owner)
    upcoming = scheduler.complete_task(task)

    assert task.completed is True                      # original marked done
    assert len(pet.tasks) == 2                         # a new occurrence was added
    assert upcoming.completed is False                 # the copy is not done
    assert upcoming.due_date == date.today() + timedelta(days=1)


def test_detect_conflicts_flags_same_time_tasks():
    """Two tasks at the same time should produce one warning; none otherwise."""
    owner = Owner("Betsy")
    biscuit = Pet("Biscuit")
    mochi = Pet("Mochi")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    biscuit.add_task(Task("Walk", time="08:00"))
    mochi.add_task(Task("Breakfast", time="08:00"))   # same slot -> conflict
    mochi.add_task(Task("Nap", time="14:00"))         # unique slot -> fine

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_completing_one_off_task_does_not_recur():
    """A task with a non-recurring frequency should not spawn a copy."""
    owner = Owner("Betsy")
    pet = Pet("Biscuit")
    owner.add_pet(pet)
    task = Task("Vet visit", time="10:00", frequency="once")
    pet.add_task(task)

    scheduler = Scheduler(owner)
    upcoming = scheduler.complete_task(task)

    assert upcoming is None                            # nothing created
    assert len(pet.tasks) == 1                         # list unchanged
