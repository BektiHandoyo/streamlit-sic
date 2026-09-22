import time
import os
import pandas as pd
import streamlit as st

CSV_FILE = "todo_routine.csv"
COLUMNS = ["id", "task", "description", "day", "is_completed"]
DAYS_LIST = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu",
    "Minggu",
]


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


st.set_page_config(
    page_title="Weekly Routine To-Do", layout="wide"
)

if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = load_data()


st.sidebar.header("+ Tambah Tugas Rutin")

with st.sidebar.form(key="add_task_form", clear_on_submit=True):
    task_input = st.text_input(
        "Nama Tugas*", placeholder="Ex. Olahraga Pagi"
    )
    desc_input = st.text_area(
        "Deskripsi", placeholder="Ex. Jogging 30 menit / Gym"
    )
    day_input = st.selectbox("Hari Pelaksanaan*", options=DAYS_LIST)

    submit_button = st.form_submit_button(label="Simpan Tugas")

if submit_button:
    if task_input.strip() == "":
        st.sidebar.error("Nama tugas tidak boleh kosong!")
    else:
        new_id = int(time.time() * 1000)

        new_row = {
            "id": new_id,
            "task": task_input,
            "description": desc_input,
            "day": day_input,
            "is_completed": False,
        }

        new_df = pd.DataFrame([new_row])
        st.session_state.tasks_df = pd.concat(
            [st.session_state.tasks_df, new_df], ignore_index=True
        )

        save_data(st.session_state.tasks_df)

        st.sidebar.success("Tugas berhasil ditambahkan!")
        st.rerun()


st.title("📅 Weekly Routine To-Do List")

st.write("### Data Terimpan Saat Ini:")
st.dataframe(st.session_state.tasks_df, use_container_width=True)