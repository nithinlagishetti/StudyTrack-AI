def recommend(row):
    tips = []

    if row["Sleep_Hours"] < 6:
        tips.append("Increase sleep hours")

    if row["Study_Hours_Per_Day"] < 2:
        tips.append("Increase daily study time")

    if row["Attendance_Percentage"] < 75:
        tips.append("Improve attendance")

    if not tips:
        return "Healthy study habits – keep it up"

    return "; ".join(tips)
