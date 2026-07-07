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
# Today's Schedule  ->  Scheduler over the Owner's pets
# ---------------------------------------------------------------------------
st.subheader("Today's Schedule")
scheduler = Scheduler(owner)
plan = scheduler.daily_plan()          # pending tasks, ordered by time

if not plan:
    st.info("No pending tasks yet. Add some above.")
else:
    # Map each task back to its pet so we can show which pet it belongs to.
    pet_of = {id(task): pet for pet, task in owner.get_all_tasks_with_pet()}
    for task in plan:
        pet = pet_of[id(task)]
        st.write(f"**{task.time}** — {task.description}  ·  _{pet.name}_ ({task.frequency})")
    st.caption(
        f"{len(scheduler.pending_tasks())} pending · "
        f"{len(scheduler.completed_tasks())} completed"
    )
