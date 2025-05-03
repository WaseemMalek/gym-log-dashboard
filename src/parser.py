import re
import pandas as pd
from datetime import datetime

def normalize_exercise_name(name):
    name = name.strip().lower()
    mapping = {
        "squat": "Squats",
        "squats": "Squats",
        "deadlift": "Deadlifts",
        "deadlifts": "Deadlifts",
        "dead lift": "Deadlifts",
        "bench": "Bench Press",
        "benchpress": "Bench Press",
        "bench press": "Bench Press",
        # Add more mappings as needed
    }
    return mapping.get(name, name.title())

def parse_gym_log(file_path):
    """Parses a gym log text file into a structured pandas DataFrame."""
    with open(file_path, "r", encoding="utf-8") as file:
        raw_text = file.read()

    # Split text into blocks based on dates
    blocks = re.split(r"(\d{1,2}/\d{1,2}/\d{2})", raw_text)
    blocks = [b.strip() for b in blocks if b.strip()]

    print("\n=== Blocks after splitting ===")
    for idx, b in enumerate(blocks):
        print(f"[{idx}] {b}")
    print("===============================\n")

    data = []

    # Process every date + exercises pair
    for i in range(1, len(blocks), 2):
        date_str = blocks[i]

        if i + 1 >= len(blocks):
            print(f"Skipping date {date_str} — no exercises listed.")
            continue

        exercises_text = blocks[i + 1]

        if not exercises_text.strip():
            print(f"Skipping date {date_str} — exercises block is empty.")
            continue

        try:
            date = datetime.strptime(date_str, "%d/%m/%y").date()
        except ValueError:
            print(f"Skipping invalid date: {date_str}")
            continue

        # Process each exercise line
        for line in exercises_text.split('\n'):
            line = line.strip()
            if not line:
                continue

            if ':' not in line:
                print(f"Skipping free text/note: '{line}'")
                continue

            # Extract the note (after dash) if present
            note_match = re.search(r"-\s*(.*)$", line)
            note = note_match.group(1).strip() if note_match else None

            # Skip whole line if note contains 'skipped'
            if note and "skipped" in note.lower():
                if not re.search(r"skipped last (\d+)?\s*sets?", note.lower()):
                    print(f"Skipping entire exercise due to note containing 'skipped': '{line}'")
                    continue

            # Remove note portion before parsing
            line = line.split('-')[0].strip()

            if ':' not in line:
                print(f"Skipping malformed line (no colon after removing note): '{line}'")
                continue

            exercise, details = line.split(':', 1)
            exercise = normalize_exercise_name(exercise.strip())
            details = details.strip()

            # Match full kg x reps x sets
            sets_match = re.findall(r'(\d+)\s*kg\s*[xX]\s*(\d+)(?:\s*[xX]\s*(\d+))?', details)

            if sets_match:
                # Expand grouped sets into individual sets
                all_sets = []
                for s in sets_match:
                    weight = int(s[0])
                    reps = int(s[1])
                    sets_count = int(s[2]) if s[2] else 1
                    all_sets.extend([(weight, reps)] * sets_count)

                # Detect skipped last N sets (or just 1 if not specified)
                skip_n = 0
                if note:
                    match = re.search(r"skipped last (\d+)?\s*sets?", note.lower())
                    if match:
                        skip_n = int(match.group(1)) if match.group(1) else 1

                sets_to_use = all_sets[:-skip_n] if skip_n else all_sets

                for weight, reps in sets_to_use:
                    data.append({
                        "Date": date,
                        "Exercise": exercise,
                        "Weight (kg)": weight,
                        "Reps": reps,
                        "Sets": 1,
                        "Note": note
                    })

                if skip_n:
                    print(f"Skipped last {skip_n} set(s) for '{exercise}' on {date_str}")

            else:
                # Try just a weight
                weight_match = re.search(r'(\d+)\s*kg', details)
                if weight_match:
                    weight = int(weight_match.group(1))
                    data.append({
                        "Date": date,
                        "Exercise": exercise,
                        "Weight (kg)": weight,
                        "Reps": None,
                        "Sets": None,
                        "Note": note
                    })
                else:
                    print(f"Skipping exercise '{exercise}' — no weight found.")

    return pd.DataFrame(data)

if __name__ == "__main__":
    # File paths
    input_file = "data/gym_log_raw.txt"
    output_full = "data/structured_gym_log.csv"
    output_public = "public_data/structured_public.csv"

    df = parse_gym_log(input_file)
    print(f"\nParsed {len(df)} rows.")
    print(df.head())

    if not df.empty:
        # Save full version with notes
        df.to_csv(output_full, index=False)
        print(f"Saved full structured data to '{output_full}'")

        # Save public version without notes
        df.drop(columns=["Note"]).to_csv(output_public, index=False)
        print(f"Saved public version to '{output_public}' (no notes)")
    else:
        print("No data to save.")

