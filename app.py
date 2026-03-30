import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Persist owner object in session state across reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
elif st.session_state.owner.name != owner_name:
    st.session_state.owner.edit_name(owner_name)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "pets" not in st.session_state:
    st.session_state.pets = []

st.markdown("### Pets")
if st.button("Add pet"):
    new_pet = Pet(name=pet_name, pet_type=species, breed="Unknown")
    st.session_state.owner.add_pet(new_pet)
    st.session_state.pets.append({"name": new_pet.name, "type": new_pet.pet_type, "breed": new_pet.breed})
    st.success(f"Added pet {new_pet.name}")

if st.session_state.pets:
    st.write("Current pets:")
    st.table(st.session_state.pets)
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. These will be added to your Owner scheduler.")
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    # Create Task in Owner scheduler
    task_time = datetime.now() + timedelta(minutes=int(duration))
    created = st.session_state.owner.create_task(
        pet_id=st.session_state.owner.pets[0].pet_id if st.session_state.owner.pets else "",
        description=task_title,
        time_scheduled=task_time,
        priority={"low": 3, "medium": 2, "high": 1}[priority],
    )
    if created:
        st.session_state.tasks.append(
            {"title": task_title, "duration_minutes": int(duration), "priority": priority, "for": st.session_state.owner.pets[0].name if st.session_state.owner.pets else "Unknown"}
        )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not st.session_state.owner.pets:
        st.error("Add at least one pet before generating a schedule.")
    else:
        schedule = st.session_state.owner.scheduler.generate_daily_task_list(datetime.now())
        if not schedule:
            st.info("No tasks scheduled for today.")
        else:
            st.success("Today's Schedule")
            for task in schedule:
                pet = st.session_state.owner.get_pet_by_id(task.pet_id)
                pet_name = pet.name if pet else "Unknown Pet"
                st.write(
                    f"{task.time_scheduled.strftime('%H:%M')} - {pet_name} - {task.description} (priority {task.priority})"
                )
