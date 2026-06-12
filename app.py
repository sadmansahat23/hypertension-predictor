import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Hypertension Predictor",
    page_icon="🫀",
    layout="centered"
)

model = joblib.load("hypertension_model.pkl")

st.title("Hypertension Risk Prediction")

age = st.number_input("Age", 18, 100, 40)
salt = st.number_input("Salt Intake", 0.0, 20.0, 5.0)
stress = st.number_input("Stress Score", 1, 10, 5)
sleep = st.number_input("Sleep Duration", 1.0, 12.0, 7.0)
bmi = st.number_input("BMI", 10.0, 50.0, 25.0)

bp_history = st.selectbox(
    "BP History",
    ["Hypertension", "Normal", "Prehypertension"]
)

medication = st.selectbox(
    "Medication",
    ["None", "Beta Blocker", "Diuretic", "Other"]
)

family_history = st.selectbox(
    "Family History",
    ["No", "Yes"]
)

exercise = st.selectbox(
    "Exercise Level",
    ["High", "Moderate", "Low"]
)

smoking = st.selectbox(
    "Smoking Status",
    ["Non-Smoker", "Smoker"]
)

if st.button("Predict"):

    data = {
        'Age':[age],
        'Salt_Intake':[salt],
        'Stress_Score':[stress],
        'Sleep_Duration':[sleep],
        'BMI':[bmi],

        'BP_History_Normal':[1 if bp_history=="Normal" else 0],
        'BP_History_Prehypertension':[1 if bp_history=="Prehypertension" else 0],

        'Medication_Beta Blocker':[1 if medication=="Beta Blocker" else 0],
        'Medication_Diuretic':[1 if medication=="Diuretic" else 0],
        'Medication_Other':[1 if medication=="Other" else 0],

        'Family_History_Yes':[1 if family_history=="Yes" else 0],

        'Exercise_Level_Low':[1 if exercise=="Low" else 0],
        'Exercise_Level_Moderate':[1 if exercise=="Moderate" else 0],

        'Smoking_Status_Smoker':[1 if smoking=="Smoker" else 0]
    }

    patient = pd.DataFrame(data)

    prediction = model.predict(patient)

    probability = model.predict_proba(patient)

    risk = probability[0][1] * 100

    st.write(f"Risk Score: {risk:.2f}%")

    if risk > 70:
        st.error(f"🔴 High Risk ({risk:.2f}%)")

    elif risk > 40:
        st.warning(f"🟡 Moderate Risk ({risk:.2f}%)")

    else:
        st.success(f"🟢 Low Risk ({risk:.2f}%)")
