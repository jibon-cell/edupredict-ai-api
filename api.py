from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("student_model.pkl")


@app.route("/")
def home():
    return jsonify({
        "message": "Student AI API Running"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received"
            }), 400

        attendance = float(data["attendance"])
        ct1 = float(data["ct1"])
        ct2 = float(data["ct2"])
        study = float(data["study_hours"])
        mid_obtained = float(data["mid_obtained"])
        mid_full = float(data["mid_full"])
        previous = float(data["previous_gpa"])

        # ====================
        # Validation
        # ====================

        if attendance < 0 or attendance > 100:
            return jsonify({
                "error":"Attendance must be 0-100"
            }),400

        if ct1 < 0 or ct1 > 5:
            return jsonify({
                "error":"CT1 must be 0-5"
            }),400

        if ct2 < 0 or ct2 > 5:
            return jsonify({
                "error":"CT2 must be 0-5"
            }),400

        if study < 0:
            return jsonify({
                "error":"Study hours cannot be negative"
            }),400

        if previous < 0 or previous > 4:
            return jsonify({
                "error":"Previous GPA must be 0-4"
            }),400

        if mid_full < 0:
            return jsonify({
                "error":"Mid full marks invalid"
            }),400

        if mid_obtained > mid_full:
            return jsonify({
                "error":"Obtained marks exceed full marks"
            }),400


        # ====================
        # Calculate percentages
        # ====================

        ct=((ct1+ct2)/10)*100

        if mid_full==0:
            mid_percent=0
        else:
            mid_percent=(mid_obtained/mid_full)*100


        # ====================
        # AI prediction
        # ====================

        new=np.array([[

            attendance,
            ct,
            study,
            mid_percent,
            previous

        ]])

        gpa=round(
            float(
                model.predict(new)[0]
            ),
            2
        )

        gpa=max(
            min(gpa,4),
            0
        )


        # ====================
        # Grade
        # ====================

        if gpa>=3.75:
            grade="A+"

        elif gpa>=3.50:
            grade="A"

        elif gpa>=3.00:
            grade="B+"

        elif gpa>=2.50:
            grade="B"

        elif gpa>=2.00:
            grade="C"

        else:
            grade="F"


        # ====================
        # Risk
        # ====================

        if gpa>=3.5:
            risk="Low"

        elif gpa>=2.5:
            risk="Medium"

        else:
            risk="High"


        # ====================
        # Recommendation
        # ====================

        tips=[]

        if attendance<60:
            tips.append(
                "Increase attendance"
            )

        if study<3:
            tips.append(
                "Increase study hours"
            )

        if ct<50:
            tips.append(
                "Improve CT performance"
            )

        if previous<2.5:
            tips.append(
                "Improve previous GPA"
            )

        if len(tips)==0:
            tips.append(
                "Keep up good work"
            )


        return jsonify({

            "prediction":gpa,
            "grade":grade,
            "risk":risk,
            "recommendation":"\n".join(tips)

        })


    except Exception as e:

        return jsonify({

            "error":str(e)

        }),500


import os

if __name__=="__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )