import pandas as pd
import random

data=[]

for i in range(3000):

    attendance=random.randint(0,100)

    ct1=random.randint(0,5)
    ct2=random.randint(0,5)

    study=random.randint(0,12)

    previous_gpa=round(
        random.uniform(1.5,4.0),
        2
    )

    if random.random()<0.3:

        mid_percent=0

    else:

        subject_count=random.randint(4,6)

        mid_full=subject_count*30

        mid_obtained=random.randint(
            int(mid_full*0.3),
            mid_full
        )

        mid_percent=round(
            (mid_obtained/mid_full)*100,
            2
        )

    ct_percent=((ct1+ct2)/10)*100

    gpa=(

        attendance*0.02
        + ct_percent*0.02
        + study*0.10
        + mid_percent*0.015
        + previous_gpa*0.9

    )

    gpa=round(
        min(
            max(gpa/2,0),
            4
        ),
        2
    )

    data.append([

        attendance,
        ct_percent,
        study,
        mid_percent,
        previous_gpa,
        gpa

    ])

df=pd.DataFrame(

    data,

    columns=[

        "Attendance",
        "CT",
        "Study_Hours",
        "Mid_Marks",
        "Previous_GPA",
        "GPA"

    ]
)

df.to_csv(
    "student_data.csv",
    index=False
)

print(
    "3000 student records created successfully"
)