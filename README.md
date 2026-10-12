# Student Performance Analytics System

## Project Overview

The **Student Performance Analytics System** is a Python-based data analysis project that analyzes student academic performance and attendance. It calculates marks, averages, grades, pass/fail results, and subject-wise statistics, and presents the results using Matplotlib visualizations.

## Objective

The main objective of this project is to use Python and its data analysis libraries to process student records, evaluate academic performance, analyze attendance, and present meaningful insights through charts and statistical summaries.

## Technologies Used

- **Python** – Core programming language
- **Pandas** – Data manipulation and analysis
- **NumPy** – Numerical calculations
- **Matplotlib** – Data visualization
- **CSV** – Dataset storage
- **Visual Studio Code** – Development environment

## Dataset Description

The project uses `students.csv`, which contains records of 20 students.

The dataset includes the following columns:

| Column | Description |
|---|---|
| Student_ID | Unique student identification number |
| Name | Student's name |
| Department | Student's department |
| Python | Marks in Python |
| Mathematics | Marks in Mathematics |
| AI | Marks in Artificial Intelligence |
| Attendance | Attendance percentage |

## Key Features

- Loads student records from a CSV file.
- Calculates total and average marks.
- Assigns grades based on average marks.
- Determines academic pass/fail status.
- Calculates overall class performance statistics.
- Identifies the highest- and lowest-performing students.
- Performs subject-wise performance analysis.
- Identifies the top three students.
- Analyzes attendance against the 75% threshold.
- Displays results in the terminal.
- Generates charts using Matplotlib.

## Grading Criteria

Grades are assigned based on average marks:

| Average Marks | Grade |
|---|---|
| 90 and above | A+ |
| 80 to below 90 | A |
| 70 to below 80 | B |
| 60 to below 70 | C |
| 50 to below 60 | D |
| Below 50 | F |

A student passes if they score at least 40 marks in every subject.

Attendance of 75% or above meets the attendance threshold. Students with attendance below 75% are flagged separately.

## Visualizations

The project generates four charts using Matplotlib:

1. Subject-wise average marks
2. Pass/fail distribution
3. Top three student performers
4. Student attendance comparison

## Project Structure

```text
internship/
├── prg.py
├── students.csv
├── README.md
├── documentation.md
├── output_chart.png
└── screenshots/
    ├── out1.png
    ├── out2.png
    └── out3.png