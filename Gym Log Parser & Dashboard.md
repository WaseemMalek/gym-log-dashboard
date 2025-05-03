Waseem's Gym Log Parser & Dashboard

A personal data project that turns my own unstructured gym notes into a structured dataset and visual dashboard for tracking my progress, training volume, and consistency over time.

🚀 Features

🧠 Smart Parser (Python)

Reads messy, free-form gym logs from a .txt file

Extracts exercise names, weights, reps, and sets

Handles edge cases like:

Skipped full exercises (- skipped)

Skipped last N sets (- skipped last 3 sets)

Notes like "form can improve" or "tired"

Normalizes exercise names (e.g. deadlift, deadlifts, dead lift → Deadlifts)

Outputs clean .csv data

📊 Streamlit Dashboard

Select an exercise and view either:

Max weight progression over time

Volume progression over time (weight × reps × sets)

View gym visit frequency grouped by:

Year

Month

Week

Day

Gaps in training clearly highlighted

🧰 Tech Stack / Skills Used

Python 3.10+

Regular Expressions (regex) — to parse unstructured text

pandas — for data wrangling and aggregation

matplotlib — for plotting trends

Streamlit — to build an interactive dashboard

Datetime & Period handling — to group and visualize gym visit frequency

📁 Project Structure

gym-log-dashboard/
├── data/
│   └── gym_log_raw.txt           # Raw input (optional in repo)
├── src/
│   └── parser.py                 # Main parsing script
├── gym_dashboard.py             # Streamlit dashboard
├── requirements.txt             # Dependencies
├── README.md                    # You're here!
└── .gitignore

🛠️ How to Run

1. Set up environment

pip install -r requirements.txt

2. Parse your raw log

python src/parser.py

Outputs structured_gym_log.csv in the data/ folder.

3. Launch the dashboard

streamlit run gym_dashboard.py

📷 Screenshots

Add screenshots here:

Line chart of bench press progress

Bar chart showing visit frequency

📌 Future ideas

Personal best (PB) detection

Interactive note viewing

Trendline/averages overlay

Exercise grouping (e.g. push/pull/legs)

Made with Python 🐍, Streamlit 📊, and sweat 💪.