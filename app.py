import streamlit as st
import pickle
import pandas as pd

# Load Model
with open("rfu_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Anemia Detection App")
st.subheader("Enter CBC Values Manually")

# CBC Inputs
hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=0.0, step=0.1)
mcv = st.number_input("MCV (fL)", min_value=0.0, step=0.1)
mch = st.number_input("MCH (pg)", min_value=0.0, step=0.1)
mchc = st.number_input("MCHC (g/dL)", min_value=0.0, step=0.1)

# Gender
gender = st.selectbox("Gender", ["Male", "Female"])
gender_val = 1 if gender == "Male" else 0

# Predict Button
if st.button("Predict Anemia"):

    df = pd.DataFrame({
        "Gender": [gender_val],
        "Hemoglobin": [hemoglobin],
        "MCH": [mch],
        "MCHC": [mchc],
        "MCV": [mcv]
    })

    pred = model.predict(df)[0]

    if pred == 1:
        st.error("⚠️ Patient HAS Anemia")
    else:
        st.success("✔️ Patient does NOT have Anemia")
