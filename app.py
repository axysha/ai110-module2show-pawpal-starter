import streamlit as st
from pawpal_system import Owner, Pet, Task, Priority, Scheduler, ScheduledTask

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

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
st.session_state.owner.name = owner_name
owner = st.session_state.owner

st.markdown("### Pets")
st.caption("Add one or more pets for this owner.")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    pet_age = st.number_input("Age", min_value=0, max_value=30, value=1)
with col3:
    pet_breed = st.text_input("Breed", value="Tabby")

if st.button("Add pet"):
    owner.pets.append(Pet(name=pet_name, age=int(pet_age), breed=pet_breed, owner=owner))

if owner.pets:
    st.write("Current pets:")
    st.table(
        [{"name": p.name, "age": p.age, "breed": p.breed, "tasks": len(p.tasks)} for p in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Pick a pet, then add a few tasks. These feed directly into that pet's task list.")

if owner.pets:
    pets_by_name = {p.name: p for p in owner.pets}
    selected_pet_name = st.selectbox("Pet", list(pets_by_name.keys()))
    selected_pet = pets_by_name[selected_pet_name]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        selected_pet.add_task(
            Task(name=task_title, duration_minutes=int(duration), priority=Priority[priority.upper()])
        )

    if selected_pet.tasks:
        st.write(f"Current tasks for {selected_pet.name}:")
        st.table(
            [
                {"name": t.name, "duration_minutes": t.duration_minutes, "priority": t.priority.name}
                for t in selected_pet.tasks
            ]
        )
    else:
        st.info(f"No tasks yet for {selected_pet.name}. Add one above.")
else:
    st.info("Add a pet before adding tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a prioritized daily plan for the selected pet's tasks.")

available_minutes = st.number_input("Available minutes today", min_value=1, max_value=1440, value=120)

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add a pet and some tasks first.")
    else:
        scheduler = Scheduler(selected_pet.tasks, available_minutes=int(available_minutes))
        scheduler.generate_plan()
        st.write(f"Daily plan for {selected_pet.name} ({selected_pet.breed}):")
        st.text(scheduler.explain_plan())
