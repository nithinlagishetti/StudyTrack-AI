import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

FEATURES = [
    "Age",
    "Study_Hours_Per_Day",
    "Preferred_Study_Time",
    "Attendance_Percentage",
    "Sleep_Hours"
]

def clean_data(df):
    df = df.copy()

    if "Name" in df.columns:
        df.drop(columns=["Name"], inplace=True)

    for col in df.columns:
        if df[col].dtype == "object":
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].mean(), inplace=True)

    le = LabelEncoder()
    df["Preferred_Study_Time"] = le.fit_transform(df["Preferred_Study_Time"])

    return df

def train_model(df):
    X = df[FEATURES]
    y = df["Marks"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = LinearRegression()
    model.fit(X_train, y_train)

    accuracy = r2_score(y_test, model.predict(X_test))

    return model, scaler, accuracy, FEATURES
