# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

- **Multi-pet task tracking** — one `Owner` manages multiple `Pet`s, each with its own list of care tasks.
- **Sorting by time** — tasks are ordered chronologically by their `"HH:MM"` start time (`Scheduler.sort_by_time()`, `daily_plan()`).
- **Filtering** — narrow tasks by completion status and/or pet (`Scheduler.filter_tasks()`), plus convenience filters like `pending_tasks()`.
- **Conflict warnings** — detects when two tasks (for the same or different pets) share a time slot and returns a warning instead of crashing (`Scheduler.detect_conflicts()`).
- **Daily/weekly recurrence** — completing a recurring task automatically schedules its next occurrence with the due date advanced via `datetime.timedelta` (`Scheduler.complete_task()` + `Task.next_occurrence()`).
- **Interactive Streamlit UI** — add pets and tasks, mark tasks done, filter, and view today's schedule as a table with conflict warnings.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

A snippet of `python main.py` output (see the full walkthrough at the end):

```
Conflict check
========================================
  ⚠️  Conflict at 08:00: Morning walk (Biscuit), Breakfast (Mochi)

Sorted by time
========================================
  07:30  [ ] Litter change  (Mochi)
  08:00  [ ] Morning walk  (Biscuit)
  08:00  [ ] Breakfast  (Mochi)
  12:00  [ ] Play session  (Mochi)
  18:00  [x] Dinner  (Biscuit)
```

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest
```

**What the tests cover** (`tests/test_pawpal.py`):

- **Task completion** — `mark_complete()` flips a task's status to done.
- **Task addition** — adding a task to a `Pet` increases its task count.
- **Sorting correctness** — `Scheduler.sort_by_time()` returns tasks in chronological order even when added out of order.
- **Recurrence logic** — completing a `"daily"` task creates a new task due the following day, and a one-off task does *not* recur.
- **Conflict detection** — `Scheduler.detect_conflicts()` flags two tasks scheduled at the same time.

Successful test run:

```
============================= test session starts ==============================
platform linux -- Python 3.12.1, pytest-9.1.1, pluggy-1.6.0
rootdir: /workspaces/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 6 items

tests/test_pawpal.py ......                                              [100%]

============================== 6 passed in 0.01s ===============================
```

**Confidence Level: ★★★★☆ (4/5)**

All six tests pass and cover every core behavior (sorting, filtering, recurrence, and
conflict detection) along both happy paths and key edge cases. I held back one star
because a few edge cases are not yet tested — an owner or pet with no tasks, tasks with
no time (`time=None`), and non-zero-padded times like `"9:00"` (which would sort
incorrectly). The logic that *is* tested is reliable; the remaining risk is in untested
inputs.

## 📐 Smarter Scheduling

The `Scheduler` class (in `pawpal_system.py`) reads every task across all of an
owner's pets and organizes them. Each feature below names the method that implements it.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.daily_plan()` | Orders tasks chronologically by their `"HH:MM"` time using `sorted(key=...)`; untimed tasks sort last. `daily_plan()` returns only pending tasks, time-ordered. |
| Filtering | `Scheduler.filter_tasks()`, `pending_tasks()`, `completed_tasks()`, `tasks_by_frequency()` | `filter_tasks(completed=?, pet_name=?)` filters by completion status and/or pet; the others are convenience filters for common cases. |
| Conflict handling | `Scheduler.detect_conflicts()` | Lightweight detection: groups tasks by time and returns warning strings for any slot with more than one task (across the same or different pets). Warns instead of raising. Checks exact start times only, not overlapping durations. |
| Recurring tasks | `Scheduler.complete_task()`, `Task.next_occurrence()` | Completing a `"daily"` or `"weekly"` task auto-creates its next occurrence with `due_date` advanced via `datetime.timedelta` (+1 day / +1 week). One-off tasks don't recur. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Set the **owner name** (e.g. "Betsy").
2. **Add a pet** — "Biscuit", a dog.
3. **Add tasks**: Biscuit's "Morning walk" at 08:00 (daily).
4. Use the **Show pet** or click **Include completed tasks** to see finished ones.
5. **Mark a Task Done**, complete Biscuit's "Morning walk"

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
