"""Testing ground for PawPal+.

Builds a small owner/pets/tasks setup and exercises the Scheduler's sorting
and filtering methods so we can verify the logic in the terminal: python main.py
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def show(pairs):
    """Print a list of (pet, task) pairs, one per line."""
    for pet, task in pairs:
        box = "x" if task.completed else " "
        print(f"  {task.time}  [{box}] {task.description}  ({pet.name})")


def main():
    owner = Owner("Betsy")
    biscuit = Pet("Biscuit", species="Golden Retriever")
    mochi = Pet("Mochi", species="Cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # Add tasks deliberately OUT OF ORDER to prove sorting works.
    biscuit.add_task(Task("Dinner", time="18:00", frequency="daily"))
    mochi.add_task(Task("Play session", time="12:00", frequency="weekly"))
    biscuit.add_task(Task("Morning walk", time="08:00", frequency="daily"))
    mochi.add_task(Task("Litter change", time="07:30", frequency="daily"))
    # Deliberate clash: Mochi's breakfast is at 08:00, same as Biscuit's walk.
    mochi.add_task(Task("Breakfast", time="08:00", frequency="daily"))

    # Mark one task done so completion filtering has something to show.
    biscuit.tasks[0].mark_complete()  # Dinner

    scheduler = Scheduler(owner)

    # --- Conflict detection: flag tasks scheduled at the same time ---
    print("Conflict check")
    print("=" * 40)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  ⚠️  {warning}")
    else:
        print("  No conflicts.")
    print()

    # --- Sorting: tasks come back ordered by time even though added jumbled ---
    print("Sorted by time")
    print("=" * 40)
    pet_of = {id(task): pet for pet, task in owner.get_all_tasks_with_pet()}
    for task in scheduler.sort_by_time():
        box = "x" if task.completed else " "
        print(f"  {task.time}  [{box}] {task.description}  ({pet_of[id(task)].name})")

    # --- Filtering: by completion status ---
    print("\nPending only")
    print("=" * 40)
    show(scheduler.filter_tasks(completed=False))

    print("\nCompleted only")
    print("=" * 40)
    show(scheduler.filter_tasks(completed=True))

    # --- Filtering: by pet name ---
    print("\nMochi's tasks only")
    print("=" * 40)
    show(scheduler.filter_tasks(pet_name="Mochi"))

    # --- Recurrence: completing a recurring task spawns the next occurrence ---
    print("\nCompleting Mochi's daily 'Litter change'...")
    print("=" * 40)
    litter = mochi.tasks[-1]  # Litter change (daily), added last
    upcoming = scheduler.complete_task(litter)
    print(f"  next occurrence created: {upcoming!r}")

    print("\nMochi's tasks after completion (note the new due-dated copy)")
    print("=" * 40)
    show(scheduler.filter_tasks(pet_name="Mochi"))


if __name__ == "__main__":
    main()
