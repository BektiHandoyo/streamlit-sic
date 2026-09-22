import datetime
import pandas as pd

DAYS_LIST = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

DAY_MAP = {
    0: "Senin",
    1: "Selasa",
    2: "Rabu",
    3: "Kamis",
    4: "Jumat",
    5: "Sabtu",
    6: "Minggu",
}


def get_today_name() -> str:
    today_num = datetime.datetime.now().weekday()
    return DAY_MAP[today_num]


def calculate_progress(df: pd.DataFrame) -> tuple[int, int, float]:
    if df.empty:
        return 0, 0, 0.0

    total = len(df)
    completed = int(df["is_completed"].sum())
    percentage = completed / total
    return total, completed, percentage