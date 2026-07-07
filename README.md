# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

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

Terminal output from running `python main.py`:

```
Today's Schedule for Betsy
========================================
  07:30  [ ] Litter change  (Mochi)
  08:00  [ ] Morning walk  (Biscuit)
  12:00  [ ] Play session  (Mochi)
  18:00  [ ] Dinner  (Biscuit)
========================================
4 tasks pending
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
