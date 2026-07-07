"""Basic tests for PawPal+ core behaviors."""

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
