import pandas as pd
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Dataset load
data = pd.read_csv("student_data.csv")

# Features
X = data[["Attendance", "CT", "Study_Hours"]]

# Target
y = data["GPA"]

# Train-Test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# User Input
attendance = int(input("Enter Attendance (%): "))
ct = int(input("Enter CT Marks (out of 10): "))
study_hours = int(input("Enter Study Hours: "))

# New student data
new_student = pd.DataFrame({
    "Attendance": [attendance],
    "CT": [ct],
    "Study_Hours": [study_hours]
})

# Predict GPA
predicted_gpa = model.predict(new_student)

gpa = predicted_gpa[0]

print("\nPredicted GPA:")
print(round(gpa,2))

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

print("\nPredicted Grade:")
print(grade)

# Risk Level
if gpa >= 3.50:
    risk = "Low"
elif gpa >= 2.50:
    risk = "Medium"
else:
    risk = "High"

print("\nRisk Level:")
print(risk)

# Recommendations
print("\nRecommendations:")

if gpa < 2.5:
    print("- Increase study time by 2 hours/day")
    print("- Improve attendance")
    print("- Focus more on CT preparation")

elif gpa < 3.5:
    print("- Increase study time by 1 hour/day")
    print("- Practice regularly")
    print("- Improve class participation")

else:
    print("- Keep up the good work")
    print("- Maintain your study routine")

# Model Score
score = r2_score(y_test, model.predict(X_test))

print("\nModel Score:")
print(round(score,2))