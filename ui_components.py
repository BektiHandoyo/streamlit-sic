import time
import pandas as pd
import streamlit as st
from database import add_task, update_task_status
from helpers import DAYS_LIST, get_today_name, calculate_progress


def render_sidebar_form():
    st.sidebar.header("➕ Tambah Tugas Rutin")

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
            st.sidebar.error("❌ Nama tugas tidak boleh kosong!")
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
            st.sidebar.success("✅ Tugas berhasil ditambahkan!")
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("🗑️ Reset Task")
    if st.sidebar.button("🔄 Reset Status Mingguan", use_container_width=True):
        st.session_state.tasks_df = reset_weekly_tasks(
            st.session_state.tasks_df
        )
        st.sidebar.success("✅ Seluruh tugas dikembalikan ke status 'Pending'!")
        st.rerun()

def render_dashboard_metrics():
    today_name = get_today_name()
    df_all = st.session_state.tasks_df
    df_today = df_all[df_all["day"] == today_name]

    tot_today, comp_today, pct_today = calculate_progress(df_today)
    tot_week, comp_week, pct_week = calculate_progress(df_all)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📊 Progress Hari Ini ({today_name})")
        if tot_today > 0:
            st.metric(
                label="Tugas Selesai",
                value=f"{comp_today} / {tot_today}",
                delta=f"{int(pct_today * 100)}%",
            )
            st.progress(pct_today)
        else:
            st.caption("Belum ada tugas untuk hari ini.")

    with col2:
        st.subheader("🗓️ Progress Minggu Ini")
        if tot_week > 0:
            st.metric(
                label="Total Tugas Seminggu Selesai",
                value=f"{comp_week} / {tot_week}",
                delta=f"{int(pct_week * 100)}%",
            )
            st.progress(pct_week)
        else:
            st.caption("Belum ada tugas rutin mingguan.")


def render_today_tasks():
    today_name = get_today_name()
    st.write(f"## 🌟 Tugas Hari Ini ({today_name})")

    df_today = st.session_state.tasks_df[
        st.session_state.tasks_df["day"] == today_name
    ]

    if df_today.empty:
        st.info(
            f"Belum ada tugas rutin yang dijadwalkan untuk hari {today_name}."
        )
        return

    edited_df = st.data_editor(
        df_today,
        key="table_today",
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "id": None,
            "task": st.column_config.TextColumn("Nama Tugas"),
            "description": st.column_config.TextColumn("Deskripsi"),
            "day": None,
            "is_completed": st.column_config.CheckboxColumn("Selesai"),
        },
    )

    _sync_table_changes(df_today, edited_df)

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

                _sync_table_changes(df_day, edited_df)

                for index, row in edited_df.iterrows():
                    original_row = df_day[df_day["id"] == row["id"]].iloc[0]
                    if row["is_completed"] != original_row["is_completed"]:
                        st.session_state.tasks_df = update_task_status(
                            st.session_state.tasks_df,
                            row["id"],
                            row["is_completed"],
                        )
                        st.rerun()

def _sync_table_changes(original_df: pd.DataFrame, edited_df: pd.DataFrame):
    original_ids = set(original_df["id"])
    edited_ids = set(edited_df["id"])
    deleted_ids = original_ids - edited_ids

    if deleted_ids:
        for del_id in deleted_ids:
            st.session_state.tasks_df = delete_task(
                st.session_state.tasks_df, del_id
            )
        st.rerun()

    for _, row in edited_df.iterrows():
        orig_row = original_df[original_df["id"] == row["id"]]
        if not orig_row.empty:
            if row["is_completed"] != orig_row.iloc[0]["is_completed"]:
                st.session_state.tasks_df = update_task_status(
                    st.session_state.tasks_df, row["id"], row["is_completed"]
                )
                st.rerun()