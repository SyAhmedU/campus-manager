import streamlit as st
from datetime import datetime, time
import json

# Page configuration
st.set_page_config(page_title="Daily Scheduler", page_icon="📅", layout="wide")

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Title
st.title("📅 Daily Scheduler")
st.markdown("---")

# Sidebar for adding tasks
with st.sidebar:
    st.header("Add New Task")
    
    task_name = st.text_input("Task Name")
    task_time = st.time_input("Time", value=time(9, 0))
    task_duration = st.number_input("Duration (minutes)", min_value=15, max_value=480, value=60, step=15)
    task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    task_notes = st.text_area("Notes (optional)")
    
    if st.button("Add Task", type="primary"):
        if task_name:
            new_task = {
                "id": len(st.session_state.tasks),
                "name": task_name,
                "time": task_time.strftime("%H:%M"),
                "duration": task_duration,
                "priority": task_priority,
                "notes": task_notes,
                "completed": False
            }
            st.session_state.tasks.append(new_task)
            st.success("Task added!")
            st.rerun()
        else:
            st.error("Please enter a task name")
    
    st.markdown("---")
    if st.button("Clear All Tasks", type="secondary"):
        st.session_state.tasks = []
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Today's Schedule")
    
    if st.session_state.tasks:
        # Sort tasks by time
        sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x['time'])
        
        for task in sorted_tasks:
            # Priority color coding
            priority_colors = {
                "High": "🔴",
                "Medium": "🟡",
                "Low": "🟢"
            }
            
            # Create expandable task card
            with st.expander(f"{priority_colors[task['priority']]} {task['time']} - {task['name']}", expanded=False):
                col_a, col_b = st.columns([3, 1])
                
                with col_a:
                    st.write(f"**Duration:** {task['duration']} minutes")
                    st.write(f"**Priority:** {task['priority']}")
                    if task['notes']:
                        st.write(f"**Notes:** {task['notes']}")
                
                with col_b:
                    completed = st.checkbox("Complete", value=task['completed'], key=f"check_{task['id']}")
                    if completed != task['completed']:
                        task['completed'] = completed
                        st.rerun()
                    
                    if st.button("Delete", key=f"del_{task['id']}"):
                        st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task['id']]
                        st.rerun()
    else:
        st.info("No tasks scheduled yet. Add a task using the sidebar!")

with col2:
    st.header("Summary")
    
    if st.session_state.tasks:
        total_tasks = len(st.session_state.tasks)
        completed_tasks = sum(1 for t in st.session_state.tasks if t['completed'])
        total_time = sum(t['duration'] for t in st.session_state.tasks)
        
        st.metric("Total Tasks", total_tasks)
        st.metric("Completed", completed_tasks)
        st.metric("Total Time", f"{total_time} min")
        
        # Progress bar
        if total_tasks > 0:
            progress = completed_tasks / total_tasks
            st.progress(progress)
            st.write(f"{int(progress * 100)}% Complete")
        
        # Priority breakdown
        st.markdown("### Priority Breakdown")
        priorities = {"High": 0, "Medium": 0, "Low": 0}
        for task in st.session_state.tasks:
            priorities[task['priority']] += 1
        
        for priority, count in priorities.items():
            if count > 0:
                st.write(f"{priority}: {count}")
    else:
        st.info("Add tasks to see summary statistics")

# Footer
st.markdown("---")
st.caption("Daily Scheduler App - Manage your day efficiently!")
