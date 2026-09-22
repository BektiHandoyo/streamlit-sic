import streamlit as st
from database import load_data
from ui_components import (
    render_dashboard_metrics,
    render_sidebar_form,
    render_today_tasks,
    render_weekly_schedule,
)

st.set_page_config(
    page_title="Weekly Routine To-Do", page_icon="📅", layout="wide"
)

if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = load_data()

st.title("📅 Weekly Routine To-Do List")

render_sidebar_form()

render_dashboard_metrics()
st.divider()

render_today_tasks()
st.divider()
render_weekly_schedule()