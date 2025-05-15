from datetime import datetime, timedelta
import pytz
import time
import os
import json

def load_schedule(file_path="schedule.txt"):
    days = set()
    times = set()

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip().lower()
                if line.startswith("days:"):
                    days = set(x.strip() for x in line[5:].split(",") if x.strip())
                elif line.startswith("times:"):
                    times = set(x.strip() for x in line[6:].split(",") if x.strip())
    except Exception as e:
        raise RuntimeError(f"Failed to read schedule file: {e}")

    if not days:
        raise ValueError("No 'days:' found in schedule file.")
    if not times:
        raise ValueError("No 'times:' found in schedule file.")

    return days, times


TARGET_DAYS, TARGET_TIMES = load_schedule()
DANISH_TIMEZONE = pytz.timezone("Europe/Copenhagen")
PERMIT_DURATION_HOURS = 10
LAST_RUN_FILE = ".last_run.json"

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

def job(now: datetime):
    print(f"Running job at {now} (DK)")
    # Task logic here...

def sleep_until_next_minute(now: datetime):
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    sleep_time = (next_minute - now).total_seconds()
    print(f"Sleeping for {sleep_time}")
    time.sleep(sleep_time)


if __name__ == "__main__":
    print(f"Scheduler started. Watching {TARGET_DAYS} at {TARGET_TIMES} (DK)...")
    last_run = load_last_run()
    print(f"Last run: {last_run}")

    while True:
        now = datetime.now(DANISH_TIMEZONE)

        if should_run_now(now):
            if not last_run or now >= last_run + timedelta(hours=PERMIT_DURATION_HOURS):
                job(now)
                last_run = now
                save_last_run(now)
                if PERMIT_DURATION_HOURS != 0:
                    print(f"Sleeping for {PERMIT_DURATION_HOURS} hours")
                    time.sleep(PERMIT_DURATION_HOURS * 3600)
                else:
                    sleep_until_next_minute(now)

        else:
            sleep_until_next_minute(now)
