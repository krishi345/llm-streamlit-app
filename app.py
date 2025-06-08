import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(layout="centered", page_title="Task Manager App")

st.title("📝 My Awesome Task Manager")

# Initialize session state for tasks if it doesn't exist
if "tasks" not in st.session_state:
    st.session_state.tasks = []

def add_task(name, description, deadline):
    st.session_state.tasks.append({"name": name, "description": description, "deadline": deadline, "done": False})

def mark_done(task_index):
    st.session_state.tasks[task_index]["done"] = not st.session_state.tasks[task_index]["done"]

# --- Add New Task Section ---
st.subheader("Add New Task")

with st.form(key="add_task_form", clear_on_submit=True):
    new_task_name = st.text_input("Task Name", placeholder="e.g., Finish project report")
    new_task_description = st.text_area("Description", placeholder="e.g., Need to include all data analysis and conclusions.")
    new_task_deadline = st.date_input("Deadline", value=date.today())

    add_task_button = st.form_submit_button("Add Task")

    if add_task_button:
        if new_task_name:
            add_task(new_task_name, new_task_description, new_task_deadline)
            st.success(f"Task '{new_task_name}' added!")
        else:
            st.warning("Task Name cannot be empty!")

st.markdown("--- ")

# --- Display Tasks Section ---
st.subheader("My Tasks")

if st.session_state.tasks:
    # Display tasks in reverse order (newest first)
    for i, task in enumerate(reversed(st.session_state.tasks)):
        # Get original index for marking as done
        original_index = len(st.session_state.tasks) - 1 - i

        task_status = "✅" if task["done"] else "⏳"
        st.markdown(f"### {task_status} {task['name']}")
        st.write(f"**Description:** {task['description']}")
        st.write(f"**Deadline:** {task['deadline'].strftime('%Y-%m-%d')}")

        st.checkbox("Mark as Done", value=task["done"], key=f"task_done_{original_index}", on_change=mark_done, args=(original_index,))
        st.markdown("--- ")
else:
    st.info("No tasks added yet. Add a new task above!")
