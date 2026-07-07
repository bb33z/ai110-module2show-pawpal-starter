from datetime import datetime, time as dtime

import streamlit as st

# Bring in the classes we built in pawpal_system.py
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Keep the owner's name in sync with the persisted object.
owner.name = st.text_input("Owner name", value=owner.name)

# ---------------------------------------------------------------------------
# Add a Pet  ->  Owner.add_pet()
# ---------------------------------------------------------------------------
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet") and pet_name:
        owner.add_pet(Pet(pet_name, species=species))   # method that handles the data
        st.success(f"Added {pet_name}!")

if not owner.pets:
    st.info("No pets yet. Add one above to get started.")
    st.stop()

st.divider()

# ---------------------------------------------------------------------------
# Add a Task  ->  Pet.add_task()
# ---------------------------------------------------------------------------
st.subheader("Add a Task")
pets_by_name = {pet.name: pet for pet in owner.pets}
with st.form("add_task_form", clear_on_submit=True):
    which_pet = st.selectbox("For which pet?", list(pets_by_name.keys()))
    description = st.text_input("Task", value="Morning walk")
    task_time = st.time_input("Time")
    frequency = st.selectbox("Frequency", ["daily", "weekly"])
    if st.form_submit_button("Add task") and description:
        pets_by_name[which_pet].add_task(
            Task(description, time=task_time.strftime("%H:%M"), frequency=frequency)
        )
        st.success(f"Added '{description}' for {which_pet}!")

st.divider()

# ---------------------------------------------------------------------------
# Edit a Task  ->  Task.update()
# ---------------------------------------------------------------------------
st.subheader("Edit a Task")
all_pairs = owner.get_all_tasks_with_pet()
if not all_pairs:
    st.info("No tasks to edit yet. Add one above.")
else:
    # Map a readable label back to the (pet, task) we want to edit.
    edit_labels = {
        f"{task.time or '—'} · {task.description} ({pet.name})": (pet, task)
        for pet, task in all_pairs
    }
    edit_choice = st.selectbox("Which task do you want to edit?", list(edit_labels.keys()))
    edit_pet, edit_task = edit_labels[edit_choice]

    with st.form("edit_task_form"):
        # Pre-fill the form with the task's current values.
        new_desc = st.text_input("Task", value=edit_task.description)
        current_time = (
            datetime.strptime(edit_task.time, "%H:%M").time()
            if edit_task.time
            else dtime(8, 0)
        )
        new_time = st.time_input("Time", value=current_time)
        freq_options = ["daily", "weekly"]
        freq_index = freq_options.index(edit_task.frequency) if edit_task.frequency in freq_options else 0
        new_freq = st.selectbox("Frequency", freq_options, index=freq_index)
        if st.form_submit_button("Save changes"):
            edit_task.update(
                description=new_desc,
                time=new_time.strftime("%H:%M"),
                frequency=new_freq,
            )
            st.success(f"Updated '{new_desc}' for {edit_pet.name}!")

st.divider()

# ---------------------------------------------------------------------------
# Mark a Task complete  ->  Scheduler.complete_task() (may spawn a recurrence)
# ---------------------------------------------------------------------------
scheduler = Scheduler(owner)

st.subheader("Mark a Task Done")
pending_pairs = sorted(
    scheduler.filter_tasks(completed=False),
    key=lambda pair: pair[1].time or "99:99",
)
if not pending_pairs:
    st.info("No pending tasks to complete. 🎉")
else:
    # Map a readable label back to the (pet, task) so we know what to complete.
    labels = {
        f"{task.time or '—'} · {task.description} ({pet.name})": (pet, task)
        for pet, task in pending_pairs
    }
    with st.form("complete_task_form", clear_on_submit=True):
        choice = st.selectbox("Which task did you finish?", list(labels.keys()))
        if st.form_submit_button("Mark complete"):
            done_pet, done_task = labels[choice]
            upcoming = scheduler.complete_task(done_task)
            st.success(f"Marked '{done_task.description}' complete for {done_pet.name}!")
            if upcoming is not None:
                st.info(
                    f"🔁 Next {upcoming.frequency} occurrence scheduled for {upcoming.due_date}."
                )

st.divider()

# ---------------------------------------------------------------------------
# Today's Schedule  ->  Scheduler over the Owner's pets
# ---------------------------------------------------------------------------
st.subheader("Today's Schedule")

# Conflict warnings come first and prominently: a pet owner needs to see a
# double-booking before scanning the plan. st.warning (not st.error) signals
# "review this" without implying the app broke, and each message names the
# exact time and clashing tasks so it's actionable.
for warning in scheduler.detect_conflicts():
    st.warning(f"⚠️ {warning}")

# Filter controls (wired to Scheduler.filter_tasks()).
col_pet, col_done = st.columns(2)
with col_pet:
    pet_choice = st.selectbox("Show pet", ["All pets"] + list(pets_by_name.keys()))
with col_done:
    show_completed = st.checkbox("Include completed tasks", value=False)

# Filter, then sort by time (untimed tasks last).
pairs = scheduler.filter_tasks(
    completed=None if show_completed else False,
    pet_name=None if pet_choice == "All pets" else pet_choice,
)
pairs = sorted(pairs, key=lambda pair: pair[1].time or "99:99")

if not pairs:
    st.info("No tasks match this view. Add some above or adjust the filters.")
else:
    # Render as a clean table for a professional look.
    rows = [
        {
            "Time": task.time or "—",
            "Task": task.description,
            "Pet": pet.name,
            "Frequency": task.frequency,
            "Status": "✅ done" if task.completed else "⏳ pending",
        }
        for pet, task in pairs
    ]
    st.table(rows)

st.caption(
    f"{len(scheduler.pending_tasks())} pending · "
    f"{len(scheduler.completed_tasks())} completed across all pets"
)
