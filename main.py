"""Testing ground for PawPal+.

Builds a small owner/pets/tasks setup and prints today's schedule so we can
verify the core logic works from the terminal:  python main.py
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner("Betsy")
    biscuit = Pet("Biscuit", species="Golden Retriever")
    mochi = Pet("Mochi", species="Cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    biscuit.add_task(Task("Morning walk", time="08:00", frequency="daily"))
    biscuit.add_task(Task("Dinner", time="18:00", frequency="daily"))
    mochi.add_task(Task("Litter change", time="07:30", frequency="daily"))
    mochi.add_task(Task("Play session", time="12:00", frequency="weekly"))

    scheduler = Scheduler(owner)

    print(f"Today's Schedule for {owner.name}")
    print("=" * 40)
    for pet, task in sorted(
        owner.get_all_tasks_with_pet(),
        key=lambda pair: pair[1].time or "99:99",
    ):
        box = "x" if task.completed else " "
        print(f"  {task.time}  [{box}] {task.description}  ({pet.name})")
    print("=" * 40)
    print(f"{len(scheduler.pending_tasks())} tasks pending")


if __name__ == "__main__":
    main()
