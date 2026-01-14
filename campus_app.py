import streamlit as st
from datetime import datetime, time, timedelta
import json

# Page configuration
st.set_page_config(page_title="Daily Scheduler", page_icon="📅", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .task-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    .high-priority { border-left-color: #ff4444; background-color: #fff5f5; }
    .medium-priority { border-left-color: #ffaa00; background-color: #fffbf0; }
    .low-priority { border-left-color: #00cc66; background-color: #f0fff4; }
    .completed { opacity: 0.6; text-decoration: line-through; }
    .time-slot { font-weight: bold; color: #1f77b4; }
    .category-badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "Day View"
if 'filter_category' not in st.session_state:
    st.session_state.filter_category = "All"
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.now().date()

# Categories for tasks
CATEGORIES = ["Work", "Personal", "Health", "Learning", "Social", "Other"]
CATEGORY_COLORS = {
    "Work": "#3b82f6",
    "Personal": "#8b5cf6",
    "Health": "#10b981",
    "Learning": "#f59e0b",
    "Social": "#ec4899",
    "Other": "#6b7280"
}

# Header
col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
with col_header1:
    st.title("📅 Daily Scheduler")
with col_header2:
    selected_date = st.date_input("Date", value=st.session_state.selected_date, key="date_picker")
    if selected_date != st.session_state.selected_date:
        st.session_state.selected_date = selected_date
        st.rerun()
with col_header3:
    view_mode = st.selectbox("View", ["Day View", "List View", "Timeline"], key="view_selector")
    st.session_state.view_mode = view_mode

st.markdown("---")

# Sidebar for adding tasks and filters
with st.sidebar:
    st.header("➕ Quick Add Task")
    
    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("Task Name*", placeholder="e.g., Team meeting")
        
        col_time1, col_time2 = st.columns(2)
        with col_time1:
            task_time = st.time_input("Start Time", value=time(9, 0))
        with col_time2:
            task_duration = st.selectbox("Duration", 
                [15, 30, 45, 60, 90, 120, 180, 240], 
                index=3,
                format_func=lambda x: f"{x} min" if x < 60 else f"{x//60}h {x%60}m" if x%60 else f"{x//60}h"
            )
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            task_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
        with col_p2:
            task_category = st.selectbox("Category", CATEGORIES)
        
        task_description = st.text_area("Description", placeholder="Add details...")
        
        col_tags, col_reminder = st.columns(2)
        with col_tags:
            task_tags = st.text_input("Tags", placeholder="meeting, urgent")
        with col_reminder:
            task_reminder = st.checkbox("Set Reminder", value=False)
        
        task_location = st.text_input("Location", placeholder="Conference Room A")
        
        submit_button = st.form_submit_button("Add Task", type="primary", use_container_width=True)
        
        if submit_button:
            if task_name:
                new_task = {
                    "id": len(st.session_state.tasks),
                    "name": task_name,
                    "date": st.session_state.selected_date.strftime("%Y-%m-%d"),
                    "time": task_time.strftime("%H:%M"),
                    "duration": task_duration,
                    "priority": task_priority,
                    "category": task_category,
                    "description": task_description,
                    "tags": [tag.strip() for tag in task_tags.split(",") if tag.strip()],
                    "reminder": task_reminder,
                    "location": task_location,
                    "completed": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.tasks.append(new_task)
                st.success("✅ Task added!")
                st.rerun()
            else:
                st.error("⚠️ Please enter a task name")
    
    st.markdown("---")
    
    # Filters
    st.subheader("🔍 Filters")
    filter_category = st.selectbox("Category", ["All"] + CATEGORIES, key="filter_cat")
    filter_priority = st.multiselect("Priority", ["High", "Medium", "Low"])
    show_completed = st.checkbox("Show Completed", value=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    if st.button("📋 Export Tasks", use_container_width=True):
        if st.session_state.tasks:
            st.download_button(
                "Download JSON",
                data=json.dumps(st.session_state.tasks, indent=2),
                file_name=f"tasks_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    if st.button("🗑️ Clear Completed", use_container_width=True):
        st.session_state.tasks = [t for t in st.session_state.tasks if not t['completed']]
        st.rerun()
    
    if st.button("🔄 Clear All Tasks", use_container_width=True):
        st.session_state.tasks = []
        st.rerun()

# Filter tasks for selected date
date_str = st.session_state.selected_date.strftime("%Y-%m-%d")
filtered_tasks = [t for t in st.session_state.tasks if t.get('date', date_str) == date_str]

# Apply filters
if filter_category != "All":
    filtered_tasks = [t for t in filtered_tasks if t['category'] == filter_category]
if filter_priority:
    filtered_tasks = [t for t in filtered_tasks if t['priority'] in filter_priority]
if not show_completed:
    filtered_tasks = [t for t in filtered_tasks if not t['completed']]

# Main content area
if st.session_state.view_mode == "Timeline":
    st.header("📊 Timeline View")
    
    # Create hourly timeline
    if filtered_tasks:
        sorted_tasks = sorted(filtered_tasks, key=lambda x: x['time'])
        
        for hour in range(24):
            hour_str = f"{hour:02d}:00"
            hour_tasks = [t for t in sorted_tasks if t['time'].startswith(f"{hour:02d}:")]
            
            if hour_tasks:
                st.markdown(f"### {hour_str}")
                for task in hour_tasks:
                    priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                    status = "✅" if task['completed'] else "⭕"
                    
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"**{status} {task['time']} - {task['name']}** {priority_emoji[task['priority']]}")
                            st.caption(f"🏷️ {task['category']} | ⏱️ {task['duration']} min")
                        with col2:
                            if st.button("✓", key=f"complete_tl_{task['id']}"):
                                task['completed'] = not task['completed']
                                st.rerun()
                        with col3:
                            if st.button("🗑️", key=f"delete_tl_{task['id']}"):
                                st.session_state.tasks.remove(task)
                                st.rerun()
                st.markdown("---")
    else:
        st.info("No tasks scheduled for this time")

elif st.session_state.view_mode == "List View":
    st.header("📝 List View")
    
    if filtered_tasks:
        sorted_tasks = sorted(filtered_tasks, key=lambda x: (not x['completed'], x['priority'] == 'High', x['time']))
        
        for task in sorted_tasks:
            priority_colors = {"High": "high-priority", "Medium": "medium-priority", "Low": "low-priority"}
            
            with st.expander(f"{'✅' if task['completed'] else '⭕'} {task['time']} - {task['name']} ({task['category']})", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Priority:** {task['priority']} | **Duration:** {task['duration']} min")
                    if task['description']:
                        st.markdown(f"**Description:** {task['description']}")
                    if task['location']:
                        st.markdown(f"📍 **Location:** {task['location']}")
                    if task['tags']:
                        st.markdown(f"🏷️ **Tags:** {', '.join(task['tags'])}")
                    if task['reminder']:
                        st.markdown("🔔 **Reminder set**")
                
                with col2:
                    if st.button("Toggle Complete", key=f"toggle_{task['id']}", use_container_width=True):
                        task['completed'] = not task['completed']
                        st.rerun()
                    
                    if st.button("Delete", key=f"del_{task['id']}", type="secondary", use_container_width=True):
                        st.session_state.tasks.remove(task)
                        st.rerun()
    else:
        st.info("📭 No tasks match your filters")

else:  # Day View
    col_main, col_summary = st.columns([2, 1])
    
    with col_main:
        st.header("📆 Day View")
        
        if filtered_tasks:
            sorted_tasks = sorted(filtered_tasks, key=lambda x: x['time'])
            
            for task in sorted_tasks:
                priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                category_color = CATEGORY_COLORS[task['category']]
                
                # Task card
                with st.container():
                    col_check, col_content, col_actions = st.columns([1, 8, 2])
                    
                    with col_check:
                        completed = st.checkbox("", value=task['completed'], key=f"check_{task['id']}", label_visibility="collapsed")
                        if completed != task['completed']:
                            task['completed'] = completed
                            st.rerun()
                    
                    with col_content:
                        st.markdown(f"### {task['time']} - {task['name']} {priority_emoji[task['priority']]}")
                        st.markdown(f"<span class='category-badge' style='background-color: {category_color}20; color: {category_color};'>{task['category']}</span> ⏱️ {task['duration']} min", unsafe_allow_html=True)
                        
                        if task['description']:
                            st.caption(task['description'])
                        
                        if task['location']:
                            st.caption(f"📍 {task['location']}")
                    
                    with col_actions:
                        if st.button("🗑️", key=f"del_day_{task['id']}"):
                            st.session_state.tasks.remove(task)
                            st.rerun()
                
                st.markdown("---")
        else:
            st.info("📭 No tasks scheduled for this day")
    
    with col_summary:
        st.header("📊 Summary")
        
        if filtered_tasks:
            total_tasks = len(filtered_tasks)
            completed_tasks = sum(1 for t in filtered_tasks if t['completed'])
            total_time = sum(t['duration'] for t in filtered_tasks)
            
            # Metrics
            st.metric("Total Tasks", total_tasks)
            st.metric("Completed", f"{completed_tasks}/{total_tasks}")
            st.metric("Total Time", f"{total_time//60}h {total_time%60}m")
            
            # Progress
            if total_tasks > 0:
                progress = completed_tasks / total_tasks
                st.progress(progress)
                st.caption(f"{int(progress * 100)}% Complete")
            
            st.markdown("---")
            
            # Category breakdown
            st.subheader("By Category")
            categories = {}
            for task in filtered_tasks:
                categories[task['category']] = categories.get(task['category'], 0) + 1
            
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                st.markdown(f"**{cat}:** {count}")
            
            st.markdown("---")
            
            # Priority breakdown
            st.subheader("By Priority")
            priorities = {"High": 0, "Medium": 0, "Low": 0}
            for task in filtered_tasks:
                priorities[task['priority']] += 1
            
            for priority, count in priorities.items():
                emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                st.markdown(f"{emoji[priority]} **{priority}:** {count}")
            
            # Upcoming task
            st.markdown("---")
            st.subheader("⏰ Next Up")
            incomplete = [t for t in sorted(filtered_tasks, key=lambda x: x['time']) if not t['completed']]
            if incomplete:
                next_task = incomplete[0]
                st.info(f"**{next_task['time']}** - {next_task['name']}")
            else:
                st.success("All tasks completed! 🎉")
        else:
            st.info("Add tasks to see summary")

# Footer
st.markdown("---")
st.caption("💡 Tip: Use categories and priorities to organize your day effectively!")
