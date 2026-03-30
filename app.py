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

# Task creation form
col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)

with col2:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    
    # Pet selection - only show if pets exist
    if st.session_state.owner.pets:
        if len(st.session_state.owner.pets) == 1:
            selected_pet_name = st.session_state.owner.pets[0].name
            st.write(f"**Pet:** {selected_pet_name}")
        else:
            pet_options = [pet.name for pet in st.session_state.owner.pets]
            selected_pet_name = st.selectbox("Assign to pet", pet_options)
    else:
        selected_pet_name = None
        st.warning("Add a pet first before creating tasks.")
    
    # Frequency selection
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly", "monthly"], 
                           help="How often should this task repeat?")

if st.button("Add task"):
    if not st.session_state.owner.pets:
        st.error("Please add at least one pet before creating tasks.")
    else:
        # Find the selected pet
        selected_pet = next((p for p in st.session_state.owner.pets if p.name == selected_pet_name), None)
        if selected_pet:
            # Create Task in Owner scheduler
            task_time = datetime.now() + timedelta(minutes=int(duration))
            created = st.session_state.owner.create_task(
                pet_id=selected_pet.pet_id,
                description=task_title,
                time_scheduled=task_time,
                priority={"low": 3, "medium": 2, "high": 1}[priority],
                frequency=frequency
            )
            if created:
                st.session_state.tasks.append(
                    {"title": task_title, "duration_minutes": int(duration), "priority": priority, 
                     "for": selected_pet.name, "frequency": frequency}
                )
                st.success(f"Added {frequency} task '{task_title}' for {selected_pet.name}")
        else:
            st.error("Could not find the selected pet.")

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
        scheduler = st.session_state.owner.scheduler
        today = datetime.now()

        # conflict detection first
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.warning("Potential scheduling conflicts detected below. Adjust times or priorities to avoid overlap.")
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("No scheduling conflicts detected.")

        # generate today's schedule and sort by time
        today_tasks = scheduler.generate_daily_task_list(today)
        sorted_tasks = scheduler.sort_by_time(today_tasks)

        if not sorted_tasks:
            st.info("No tasks scheduled for today.")
        else:
            st.success("Today's Schedule")
            table_rows = []
            for task in sorted_tasks:
                pet = st.session_state.owner.get_pet_by_id(task.pet_id)
                pet_name = pet.name if pet else "Unknown Pet"
                status = "Done" if task.completion else "Pending"
                table_rows.append({
                    "Time": task.time_scheduled.strftime("%H:%M"),
                    "Pet": pet_name,
                    "Task": task.description,
                    "Priority": task.priority,
                    "Status": status,
                    "Frequency": task.frequency,
                })

            st.table(table_rows)

            # Also provide filtered views
            pending_tasks = scheduler.filter_tasks(sorted_tasks, completion_status=False)
            if pending_tasks:
                st.info("Pending tasks for urgent attention:")
                st.table([{
                    "Time": t.time_scheduled.strftime("%H:%M"),
                    "Pet": st.session_state.owner.get_pet_by_id(t.pet_id).name if st.session_state.owner.get_pet_by_id(t.pet_id) else "Unknown",
                    "Task": t.description,
                    "Priority": t.priority,
                    "Frequency": t.frequency,
                } for t in pending_tasks])

            if st.session_state.owner.pets:
                selected_pet = st.selectbox("Filter by pet", [p.name for p in st.session_state.owner.pets])
                pet_tasks = scheduler.filter_tasks(sorted_tasks, pet_name=selected_pet, owner=st.session_state.owner)
                st.info(f"Tasks for {selected_pet}:")
                st.table([{
                    "Time": t.time_scheduled.strftime("%H:%M"),
                    "Task": t.description,
                    "Priority": t.priority,
                    "Status": "Done" if t.completion else "Pending",
                    "Frequency": t.frequency,
                } for t in pet_tasks])

