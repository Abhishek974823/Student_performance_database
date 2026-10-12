
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

INPUT_FILE = "students_input.csv"
SUBJECTS = ["Python", "Mathematics", "AI"]
PASS_MARK = 40
ATTENDANCE_THRESHOLD = 75


def assign_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    return "F"


def load_dataset(filename):
    df = pd.read_csv(filename)

    required = [
        "Student_ID", "Name", "Department",
        *SUBJECTS, "Attendance"
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df.empty:
        raise ValueError("The dataset is empty.")

    for col in SUBJECTS + ["Attendance"]:
        df[col] = pd.to_numeric(df[col], errors="raise")

    if df[required].isnull().any().any():
        raise ValueError("The dataset contains missing values.")

    for subject in SUBJECTS:
        if not df[subject].between(0, 100).all():
            raise ValueError(f"{subject} marks must be between 0 and 100.")

    if not df["Attendance"].between(0, 100).all():
        raise ValueError("Attendance must be between 0 and 100.")

    return df


def calculate_results(df):
    df = df.copy()

    marks = df[SUBJECTS].to_numpy(dtype=float)
    df["Total"] = np.sum(marks, axis=1)
    df["Average"] = np.round(np.mean(marks, axis=1), 2)
    df["Grade"] = df["Average"].apply(assign_grade)

    # Pass only if every subject mark is at least 40
    passed = df[SUBJECTS].ge(PASS_MARK).all(axis=1)
    df["Result"] = np.where(passed, "Pass", "Fail")

    df["Attendance_Status"] = np.where(
        df["Attendance"] >= ATTENDANCE_THRESHOLD,
        "Meets 75% Requirement",
        "Below 75%"
    )

    return df


def display_analysis(df):
    subject_avg = df[SUBJECTS].mean()

    passed_count = int((df["Result"] == "Pass").sum())
    failed_count = int((df["Result"] == "Fail").sum())

    highest = df["Average"].max()
    lowest = df["Average"].min()

    highest_students = df.loc[
        df["Average"] == highest, "Name"
    ].tolist()

    lowest_students = df.loc[
        df["Average"] == lowest, "Name"
    ].tolist()

    print("\n" + "=" * 55)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 55)

    print("\nSTUDENT RESULTS")
    print("-" * 55)
    print(
        df[
            ["Student_ID", "Name", "Department", "Total",
             "Average", "Grade", "Result"]
        ].to_string(index=False)
    )

    print("\nCLASS SUMMARY")
    print("-" * 55)
    print("Total students:", len(df))
    print("Students passed:", passed_count)
    print("Students failed:", failed_count)
    print("Overall class average:", round(df["Average"].mean(), 2))
    print("Highest student average:", highest)
    print("Highest-performing student(s):", ", ".join(highest_students))
    print("Lowest student average:", lowest)
    print("Lowest-performing student(s):", ", ".join(lowest_students))

    print("\nSUBJECT-WISE ANALYSIS")
    print("-" * 55)
    for subject in SUBJECTS:
        print(
            f"{subject}: average={subject_avg[subject]:.2f}, "
            f"highest={df[subject].max()}, "
            f"lowest={df[subject].min()}"
        )

    print("Best-performing subject:", subject_avg.idxmax())
    print("Lowest-performing subject:", subject_avg.idxmin())

    print("\nTOP 3 PERFORMERS")
    print("-" * 55)
    print(
        df.nlargest(3, "Average")[
            ["Name", "Average", "Grade"]
        ].to_string(index=False)
    )

    print("\nATTENDANCE ANALYSIS")
    print("-" * 55)
    print("Average attendance:", round(df["Attendance"].mean(), 2), "%")
    print(
        "Students meeting 75% requirement:",
        int((df["Attendance"] >= ATTENDANCE_THRESHOLD).sum())
    )
    print(
        "Students below 75%:",
        int((df["Attendance"] < ATTENDANCE_THRESHOLD).sum())
    )

    below = df.loc[
        df["Attendance"] < ATTENDANCE_THRESHOLD,
        ["Name", "Attendance"]
    ]

    if below.empty:
        print("No students are below 75% attendance.")
    else:
        print("\nStudents below 75% attendance:")
        print(below.to_string(index=False))

    return subject_avg, passed_count, failed_count


def create_dashboard(df, subject_avg, passed_count, failed_count):
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(
        "Student Performance Analytics Dashboard",
        fontsize=18,
        fontweight="bold"
    )

    ax = axes[0, 0]
    bars = ax.bar(
        subject_avg.index,
        subject_avg.values,
        color=["royalblue", "darkorange", "seagreen"]
    )
    ax.set_title("Average Marks by Subject")
    ax.set_ylabel("Average Marks (out of 100)")
    ax.set_ylim(0, 110)
    ax.bar_label(bars, fmt="%.2f")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    ax = axes[0, 1]
    labels = []
    values = []
    colors = []

    if passed_count:
        labels.append(f"Pass ({passed_count})")
        values.append(passed_count)
        colors.append("mediumseagreen")

    if failed_count:
        labels.append(f"Fail ({failed_count})")
        values.append(failed_count)
        colors.append("lightcoral")

    ax.set_title("Pass/Fail Distribution")
    ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90
    )

    ax = axes[1, 0]
    top_three = df.nlargest(3, "Average").sort_values(
        "Average", ascending=True
    )
    bars = ax.barh(
        top_three["Name"],
        top_three["Average"],
        color="mediumpurple"
    )
    ax.set_title("Top 3 Performing Students")
    ax.set_xlabel("Average Marks")
    ax.set_xlim(0, 110)
    ax.bar_label(bars, fmt="%.2f")
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    ax = axes[1, 1]
    attendance_counts = [
        int((df["Attendance"] >= ATTENDANCE_THRESHOLD).sum()),
        int((df["Attendance"] < ATTENDANCE_THRESHOLD).sum())
    ]
    bars = ax.bar(
        ["Attendance >= 75%", "Attendance < 75%"],
        attendance_counts,
        color=["cornflowerblue", "darkorange"]
    )
    ax.set_title("Attendance Comparison")
    ax.set_ylabel("Number of Students")
    ax.bar_label(bars)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def main():
    try:
        data = load_dataset(INPUT_FILE)
        data = calculate_results(data)

        subject_avg, passed_count, failed_count = display_analysis(data)

        print("\nOpening Matplotlib dashboard...")
        create_dashboard(data, subject_avg, passed_count, failed_count)

    except FileNotFoundError:
        print("Error: students.csv was not found.")
        print("Keep students.csv in the same folder as prg.py.")

    except (ValueError, TypeError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
