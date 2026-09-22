import os
import pandas as pd

CSV_FILE = "todo_routine.csv"
COLUMNS = ["id", "task", "description", "day", "is_completed"]


def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)
        return df

    df = pd.read_csv(CSV_FILE)
    if not df.empty:
        df["is_completed"] = df["is_completed"].astype(bool)
        df["description"] = df["description"].fillna("")
    return df


def save_data(df: pd.DataFrame):
    df.to_csv(CSV_FILE, index=False)


def add_task(df: pd.DataFrame, new_task: dict) -> pd.DataFrame:
    new_df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
    save_data(new_df)
    return new_df


def update_task_status(
    df: pd.DataFrame, task_id: int, status: bool
) -> pd.DataFrame:
    df.loc[df["id"] == task_id, "is_completed"] = status
    save_data(df)
    return df