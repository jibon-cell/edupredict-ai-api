import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os
import pickle

# ========================
# Dataset
# ========================

data = pd.read_csv("student_data.csv")

X = data[["Attendance", "CT", "Study_Hours", "Mid_Marks", "Previous_GPA"]]

y = data["GPA"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)
prediction = model.predict(X_test)

score = r2_score(y_test, prediction)

print("Model Accuracy:", round(score * 100, 2), "%")

# ========================
# Save Model
# ========================

with open(
    "student_model.pkl",
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )

print(
    "Model saved successfully"
)


# ========================
# About
# ========================


def about_project():

    about = tk.Toplevel()

    about.title("About Project")

    about.geometry("500x300")

    about.configure(bg="#222222")

    tk.Label(
        about,
        text="""
Student Performance &
Result Prediction System

Uses Machine Learning
for GPA prediction.

Developed by:
S.B. Jibon
""",
        bg="#222222",
        fg="white",
        font=("Arial", 12),
    ).pack(pady=30)


# ========================
# History
# ========================


def show_history():

    history = tk.Toplevel()

    history.title("History")

    history.geometry("700x400")

    text = tk.Text(history)

    text.pack(fill="both", expand=True)

    try:

        with open("history.csv", "r") as file:

            text.insert(tk.END, file.read())

    except:

        text.insert(tk.END, "No History")
        
# ========================
# Clear Fields
# ========================

def clear_fields():

    all_entries = [

        name_entry,
        id_entry,
        attendance_entry,
        ct1_entry,
        ct2_entry,
        study_entry,
        mid_obtained_entry,
        mid_full_entry,
        previous_entry
    ]

    for field in all_entries:

        field.delete(
            0,
            tk.END
        )


# ========================
# Predict
# ========================


def predict():

    try:

        name = name_entry.get()
        sid = id_entry.get()

        attendance = int(attendance_entry.get())

        ct1 = int(ct1_entry.get())

        ct2 = int(ct2_entry.get())

        study = int(study_entry.get())

        previous = float(previous_entry.get())

        # ====================
        # Validation
        # ====================

        if attendance < 0 or attendance > 100:
            raise ValueError

        if ct1 < 0 or ct1 > 5:
            raise ValueError

        if ct2 < 0 or ct2 > 5:
            raise ValueError

        if study < 0:
            raise ValueError

        if previous < 0 or previous > 4:
            raise ValueError

        if mid_obtained_entry.get() == "" or mid_full_entry.get() == "":

            mid_percent = 0

        else:

            mid_percent = round(
                (int(mid_obtained_entry.get()) / int(mid_full_entry.get())) * 100, 2
            )

    except:

        messagebox.showerror(
            "Input Error",
            """Check input values:

Attendance = 0-100
CT = 0-5
Previous GPA = 0-4
Study Hours >= 0
""",
        )

        return
    # CT %

    ct = round(((ct1 + ct2) / 10) * 100, 2)

    # Predict GPA

    new = pd.DataFrame(
        {
            "Attendance": [attendance],
            "CT": [ct],
            "Study_Hours": [study],
            "Mid_Marks": [mid_percent],
            "Previous_GPA": [previous],
        }
    )

    gpa = round(model.predict(new)[0], 2)

    gpa = max(min(gpa, 4), 0)

    # Grade

    if gpa >= 3.75:
        grade = "A+"

    elif gpa >= 3.50:
        grade = "A"

    elif gpa >= 3.00:
        grade = "B+"

    elif gpa >= 2.50:
        grade = "B"

    elif gpa >= 2.00:
        grade = "C"

    else:
        grade = "F"

    # Risk

    if gpa >= 3.5:

        risk = "Low"
        color = "green"

    elif gpa >= 2.5:

        risk = "Medium"
        color = "orange"

    else:

        risk = "High"
        color = "red"

    # Recommendation

    recommendation = []

    if attendance < 60:
        recommendation.append("Increase class attendance")

    if study < 3:
        recommendation.append("Increase study hours")

    if ct < 50:
        recommendation.append("Improve class test performance")

    if previous < 2.5:
        recommendation.append("Improve previous GPA")

    if len(recommendation) == 0:
        recommendation.append("Keep up good work")

    recommendation = "\n".join(recommendation)

    # Save History

    if not os.path.exists("history.csv"):

        with open("history.csv", "w") as f:

            f.write("Name,ID,GPA,Risk\n")

    with open("history.csv", "a") as f:

        f.write(f"{name},{sid},{gpa},{risk}\n")

    # Result Window

    result = tk.Toplevel()

    result.title("Result")

    result.geometry("800x600")

    result.configure(bg="#222222")

    tk.Label(
        result,
        text=f"""

Name: {name}

ID: {sid}

Predicted GPA: {gpa}

Grade: {grade}

Risk: {risk}

CT: {ct}%

Mid: {mid_percent}%

""",
        bg="#222222",
        fg=color,
        font=("Arial", 13, "bold"),
    ).pack()

    tk.Label(
        result,
        text=f"""
Recommendation

{recommendation}
""",
        bg="#333333",
        fg="white",
        font=("Arial", 11, "bold"),
        width=35,
        height=5,
    ).pack(pady=10)

    # GPA Progress Bar

    canvas = tk.Canvas(result, width=300, height=30, bg="#222222", highlightthickness=0)

    canvas.pack(pady=10)

    # Background Bar

    canvas.create_rectangle(20, 10, 280, 30, fill="gray")

    # GPA Fill

    gpa_width = (gpa / 4) * 260

    canvas.create_rectangle(20, 10, 20 + gpa_width, 30, fill=color)

    canvas.create_text(
        150,
        20,
        text=f"GPA Progress: {gpa}/4.0",
        fill="white",
        font=("Arial", 10, "bold"),
    )

    fig = plt.Figure(figsize=(6, 3))

    ax = fig.add_subplot(111)

    labels = ["Attendance", "CT", "Study", "Mid", "GPA"]

    values = [attendance / 20, ct / 20, study, mid_percent / 20, gpa]
    ax.bar(labels, values)

    ax.set_title("Student Performance Analysis")

    ax.set_ylabel("Score")

    graph = FigureCanvasTkAgg(fig, result)

    graph.draw()

    graph.get_tk_widget().pack()


# ========================
# Main Window
# ========================

root = tk.Tk()

root.title("Student Predictor")

root.geometry("900x650")

root.configure(bg="#222222")


main = tk.Frame(root, bg="#222222")

main.pack()


logo = Image.open("logo.png")

logo = logo.resize((80, 80))

photo = ImageTk.PhotoImage(logo)

tk.Label(main, image=photo, bg="#222222").grid(row=0, column=0, columnspan=4)


tk.Label(
    main,
    text="Student Performance Prediction System",
    bg="#222222",
    fg="cyan",
    font=("Arial", 18, "bold"),
).grid(row=1, column=0, columnspan=4, pady=15)


labels = [
    "Student Name",
    "Student ID",
    "Attendance %",
    "CT1",
    "CT2",
    "Study Hours",
    "Mid Obtained",
    "Mid Full Marks",
    "Previous GPA",
]

entries = []

for i, text in enumerate(labels):

    tk.Label(main, text=text, bg="#222222", fg="white").grid(
        row=i // 2 + 2, column=(i % 2) * 2, padx=10, pady=10
    )

    e = tk.Entry(main, width=25, font=("Arial", 11))

    e.grid(row=i // 2 + 2, column=(i % 2) * 2 + 1)

    entries.append(e)


(
    name_entry,
    id_entry,
    attendance_entry,
    ct1_entry,
    ct2_entry,
    study_entry,
    mid_obtained_entry,
    mid_full_entry,
    previous_entry,
) = entries


# ====================
# Button Frame
# ====================

button_frame = tk.Frame(
    main,
    bg="#222222"
)

button_frame.grid(
    row=8,
    column=0,
    columnspan=4,
    pady=20
)


tk.Button(
    button_frame,
    text="Predict",
    bg="green",
    fg="white",
    width=15,
    command=predict
).pack(
    side="left",
    padx=15
)


tk.Button(
    button_frame,
    text="History",
    bg="purple",
    fg="white",
    width=15,
    command=show_history
).pack(
    side="left",
    padx=15
)


tk.Button(
    button_frame,
    text="About",
    bg="blue",
    fg="white",
    width=15,
    command=about_project
).pack(
    side="left",
    padx=15
)


tk.Button(
    button_frame,
    text="Clear",
    bg="red",
    fg="white",
    width=15,
    command=clear_fields
).pack(
    side="left",
    padx=15
)


root.mainloop()
