import os
import pandas as pd
import streamlit as st

CSV_FILE = "todo_routine.csv"

COLUMNS = ["id", "task", "description", "day", "is_completed"]


def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)
        return df
    else:
        df = pd.read_csv(CSV_FILE)
        if not df.empty:
            df["is_completed"] = df["is_completed"].astype(bool)
        return df


def save_data(df: pd.DataFrame):
    df.to_csv(CSV_FILE, index=False)



st.set_page_config(page_title="Weekly Routine To-Do", page_icon="📅")

if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = load_data()

st.title("Weekly Routine To-Do List")
st.caption("Phase 1: Data Engine Setup")

st.subheader("Data Saat Ini (Cek Session State & CSV):")
st.dataframe(st.session_state.tasks_df, use_container_width=True)

st.success("✅ Fondasi data berhasil dimuat/dibuat!")