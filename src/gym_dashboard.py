import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the structured gym log CSV
df = pd.read_csv("data/structured_public.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Calculate Volume column if not already present
df["Volume"] = df["Weight (kg)"] * df["Reps"] * df["Sets"]

# Sidebar: Select exercise and metric
st.sidebar.title("Exercise Viewer")
exercise_list = sorted(df["Exercise"].dropna().unique())
selected_exercise = st.sidebar.selectbox("Select an exercise:", exercise_list)

metric = st.sidebar.radio("Metric to view:", ["Max Weight", "Total Volume"])

# Filter data by selected exercise
exercise_df = df[df["Exercise"] == selected_exercise]

# Group and plot
if metric == "Max Weight":
    grouped = exercise_df.groupby("Date")["Weight (kg)"].max().reset_index()
else:
    grouped = exercise_df.groupby("Date")["Volume"].sum().reset_index()

# Plotting the selected exercise metric
st.title(f"{selected_exercise} — {metric} Over Time")

fig, ax = plt.subplots(figsize=(10, 5))
if metric == "Max Weight":
    ax.plot(grouped["Date"], grouped["Weight (kg)"], marker='o')
    ax.set_ylabel("Max Weight (kg)")
else:
    ax.plot(grouped["Date"], grouped["Volume"], marker='o')
    ax.set_ylabel("Total Volume (kg × reps × sets)")

ax.set_xlabel("Date")
ax.set_title(f"{selected_exercise} — {metric} Progression")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# ---- Frequency of Gym Visits ----
st.header("Gym Visit Frequency")

# Drop duplicates to count unique visit days
daily_visits = df[["Date"]].drop_duplicates()
daily_visits["Year"] = daily_visits["Date"].dt.year

daily_visits["Month"] = daily_visits["Date"].dt.to_period("M")
daily_visits["Week"] = daily_visits["Date"].dt.to_period("W")
daily_visits["Day"] = daily_visits["Date"].dt.date

grouping = st.selectbox("Group gym visits by:", ["Year", "Month", "Week", "Day"])

# Count visits per selected group
grouped_counts = daily_visits.groupby(grouping).size().reset_index(name="Visit Count")

# Fill in missing time periods
if grouping in ["Month", "Week"]:
    date_range = pd.date_range(df["Date"].min(), df["Date"].max(), freq="W" if grouping == "Week" else "MS")
    full_index = pd.Series(pd.PeriodIndex(date_range, freq="W" if grouping == "Week" else "M"), name=grouping)
    grouped_counts = full_index.to_frame().merge(grouped_counts, on=grouping, how="left").fillna(0)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(grouped_counts[grouping].astype(str), grouped_counts["Visit Count"])
ax2.set_title(f"Gym Visits Grouped by {grouping}")
ax2.set_xlabel(grouping)
ax2.set_ylabel("Visit Count")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)
