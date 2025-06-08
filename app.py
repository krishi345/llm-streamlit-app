import streamlit as st
import pandas as pd
from datetime import date, datetime
import json
import os

st.set_page_config(layout="centered", page_title="Task Manager App")

st.title("📝 My Awesome Task Manager")

# User selection/input
user_id = st.text_input("Enter your User ID (e.g., your name)", key="user_id_input")

# Only proceed if a user_id is entered
if user_id:
    TASKS_FILE = f"{user_id}_tasks.json"

    # Functions to save and load tasks
    def save_tasks():
        file_path = os.path.join(".", TASKS_FILE)
        with open(file_path, "w") as f:
            # Convert date objects to string before saving
            serializable_tasks = []
            for task in st.session_state.tasks:
                task_copy = task.copy()
                if isinstance(task_copy["deadline"], date):
                    task_copy["deadline"] = task_copy["deadline"].isoformat()
                serializable_tasks.append(task_copy)
            json.dump(serializable_tasks, f, indent=4)

    def load_tasks():
        if "tasks" not in st.session_state:
            file_path = os.path.join(".", TASKS_FILE)
            try:
                with open(file_path, "r") as f:
                    loaded_tasks = json.load(f)
                    # Convert date strings back to date objects
                    for task in loaded_tasks:
                        if isinstance(task["deadline"], str):
                            task["deadline"] = datetime.fromisoformat(task["deadline"]).date()
                    st.session_state.tasks = loaded_tasks
            except FileNotFoundError:
                st.session_state.tasks = []
            except json.JSONDecodeError:
                st.error("Error reading tasks file. Starting with an empty list.")
                st.session_state.tasks = []

    # Load tasks when the app starts
    load_tasks()

    def add_task(name, description, deadline):
        st.session_state.tasks.append({"name": name, "description": description, "deadline": deadline, "done": False})
        save_tasks() # Save after adding a task

    def mark_done(task_index):
        st.session_state.tasks[task_index]["done"] = not st.session_state.tasks[task_index]["done"]
        save_tasks() # Save after marking a task as done

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
else:
    st.warning("Please enter a User ID to manage your tasks.")
