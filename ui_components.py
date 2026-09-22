import time
import pandas as pd
import streamlit as st
from database import add_task, update_task_status
from helpers import DAYS_LIST, get_today_name


def render_sidebar_form():
    st.sidebar.header("+ Tambah Tugas Rutin")

    with st.sidebar.form(key="add_task_form", clear_on_submit=True):
        task_input = st.text_input(
            "Nama Tugas*", placeholder="Misal: Olahraga Pagi"
        )
        desc_input = st.text_area(
            "Deskripsi", placeholder="Misal: Jogging 30 menit"
        )
        day_input = st.selectbox("Hari Pelaksanaan*", options=DAYS_LIST)
        submit_button = st.form_submit_button(label="Simpan Tugas")

    if submit_button:
        if task_input.strip() == "":
            st.sidebar.error("Nama tugas tidak boleh kosong!")
        else:
            new_task = {
                "id": int(time.time() * 1000),
                "task": task_input,
                "description": desc_input,
                "day": day_input,
                "is_completed": False,
            }
            st.session_state.tasks_df = add_task(
                st.session_state.tasks_df, new_task
            )
            st.sidebar.success("Tugas berhasil ditambahkan!")
            st.rerun()


def render_today_tasks():
    today_name = get_today_name()
    st.write(f"## Tugas Hari Ini ({today_name})")

    df_today = st.session_state.tasks_df[
        st.session_state.tasks_df["day"] == today_name
    ]

    if df_today.empty:
        st.info(
            f"Belum ada tugas rutin yang dijadwalkan untuk hari {today_name}."
        )
        return

    for _, row in df_today.iterrows():
        label_text = f"**{row['task']}**" + (
            f" — *{row['description']}*" if row["description"] else ""
        )
        checked = st.checkbox(
            label=label_text,
            value=row["is_completed"],
            key=f"today_{row['id']}",
        )

        if checked != row["is_completed"]:
            st.session_state.tasks_df = update_task_status(
                st.session_state.tasks_df, row["id"], checked
            )
            st.rerun()


def render_weekly_schedule():
    today_name = get_today_name()
    st.write("## 🗓️ Jadwal Rutin Seminggu")

    for day in DAYS_LIST:
        df_day = st.session_state.tasks_df[
            st.session_state.tasks_df["day"] == day
        ]
        task_count = len(df_day)

        header_label = (
            f"📌 {day} (Hari Ini)" if day == today_name else f"📅 {day}"
        )
        header_label += f" — {task_count} Tugas"

        with st.expander(header_label, expanded=(day == today_name)):
            if df_day.empty:
                st.caption("Tidak ada tugas rutin untuk hari ini.")
            else:
                edited_df = st.data_editor(
                    df_day,
                    key=f"table_week_{day}",
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "task": st.column_config.TextColumn(
                            "Nama Tugas", disabled=True
                        ),
                        "description": st.column_config.TextColumn(
                            "Deskripsi", disabled=True
                        ),
                        "is_completed": st.column_config.CheckboxColumn(
                            "Selesai", help="Centang jika tugas sudah selesai"
                        ),
                    },
                )

                for index, row in edited_df.iterrows():
                    original_row = df_day[df_day["id"] == row["id"]].iloc[0]
                    if row["is_completed"] != original_row["is_completed"]:
                        st.session_state.tasks_df = update_task_status(
                            st.session_state.tasks_df,
                            row["id"],
                            row["is_completed"],
                        )
                        st.rerun()