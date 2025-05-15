from parking_issuer import run_parking_job
from datetime import datetime, timedelta
import pytz
import time
import os
import json

WEEKDAY_TO_INDEX = {
    "monday": 0, "tuesday": 1, "wednesday": 2,
    "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
}
DANISH_TIMEZONE = pytz.timezone("Europe/Copenhagen")
PERMIT_DURATION_HOURS = 10
LAST_RUN_FILE = os.path.join("data", ".last_run.json")


def load_schedule(file_path="schedule.txt"):
    days = []
    times = []
    phone_no = None
    license_plate = None

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip().lower()
                if line.startswith("days:"):
                    days = [x.strip() for x in line[5:].split(",") if x.strip()]
                elif line.startswith("times:"):
                    times = [x.strip() for x in line[6:].split(",") if x.strip()]
                elif line.startswith("phone_no:"):
                    phone_no = line[9:].strip()
                elif line.startswith("license_plate:"):
                    license_plate = line[14:].strip()

    except Exception as e:
        raise RuntimeError(f"Failed to read schedule file: {e}")

    if not days:
        raise ValueError("No 'days:' found in schedule file.")
    if not times:
        raise ValueError("No 'times:' found in schedule file.")

    sorted_days = sorted(days, key=lambda d: WEEKDAY_TO_INDEX[d])
    sorted_times = sorted(times, key=lambda t: datetime.strptime(t, "%H:%M").time())

    return sorted_days, sorted_times, phone_no, license_plate


TARGET_DAYS, TARGET_TIMES, PHONE_NO, LICENSE_PLATE = load_schedule()


def load_last_run():
    if not os.path.exists(LAST_RUN_FILE):
        return None
    try:
        with open(LAST_RUN_FILE, "r") as f:
            data = json.load(f)
            return datetime.fromisoformat(data["timestamp"])
    except Exception as e:
        print(f"Could not load last run: {e}")
        return None


def save_last_run(dt: datetime):
    try:
        with open(LAST_RUN_FILE, "w") as f:
            json.dump({"timestamp": dt.isoformat()}, f)
            print("Saving state as timestamp")
    except Exception as e:
        print(f"Could not save last run: {e}")


def should_run_now(now: datetime) -> bool:
    return (
        now.strftime('%A').lower() in TARGET_DAYS and
        now.strftime('%H:%M') in TARGET_TIMES
    )


def get_next_run_time(now: datetime, allowed_days: list, allowed_times: list) -> datetime:
    target_times = sorted([
        datetime.strptime(t, "%H:%M").time()
        for t in allowed_times
    ])

    for day_offset in range(0, 8):  # up to 7 days ahead
        candidate_day = now + timedelta(days=day_offset)
        weekday_name = candidate_day.strftime('%A').lower()
        if weekday_name not in allowed_days:
            continue

        for t in target_times:
            candidate_dt = datetime.combine(candidate_day.date(), t, tzinfo=now.tzinfo)
            if candidate_dt > now:
                return candidate_dt

    raise RuntimeError("No valid run time found in the next 7 days. Check your schedule.")


def check_schedule_spacing(min_hours_between=PERMIT_DURATION_HOURS) -> bool:

    if len(TARGET_DAYS) != len(set(TARGET_DAYS)):
        print("Duplicate day detected in schedule.")
        return False

    parsed_times = [datetime.strptime(t, "%H:%M").time() for t in TARGET_TIMES]
    all_run_times = []

    for day in TARGET_DAYS:
        day_index = WEEKDAY_TO_INDEX[day]
        for t in parsed_times:
            dt = datetime(2000, 1, 3 + day_index, t.hour, t.minute)
            all_run_times.append(dt)

    all_run_times.sort()
    extended = all_run_times + [dt + timedelta(days=7) for dt in all_run_times]

    for i in range(len(extended) - 1):
        delta = extended[i + 1] - extended[i]
        if delta < timedelta(hours=min_hours_between):
            print(f"Too close: {extended[i].strftime('%A %H:%M')} and {extended[i+1].strftime('%A %H:%M')} ({delta})")
            return False

    print("All scheduled times are spaced correctly.")
    return True


def job(now: datetime):
    print(f"Running job at {now} (DK)")

    run_parking_job(PHONE_NO, LICENSE_PLATE, DANISH_TIMEZONE)


if __name__ == "__main__":
    print(f"Scheduler started. Watching {TARGET_DAYS} at {TARGET_TIMES} (DK)...")

    if not check_schedule_spacing():
        raise SystemExit("Schedule validation failed. Exiting.")

    last_run = load_last_run()
    print(f"Last run: {last_run}")

    while True:
        now = datetime.now(DANISH_TIMEZONE)
        next_run = get_next_run_time(now, TARGET_DAYS, TARGET_TIMES)

        wait_seconds = (next_run - now).total_seconds()
        print(f"Next run scheduled at {next_run} (in {int(wait_seconds)} seconds)")
        time.sleep(wait_seconds)

        now = datetime.now(DANISH_TIMEZONE)
        job(now)
        last_run = now
        save_last_run(now)