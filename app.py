import streamlit as st
import pickle
import pandas as pd
import easyocr
import re
import cv2
import numpy as np


# Load Model
with open("rfu_model.pkl", "rb") as f:
    model = pickle.load(f)


st.title("Anemia Detection App")
st.subheader("Upload CBC Report Image")


uploaded_img = st.file_uploader("Upload CBC Image", type=["jpg", "jpeg", "png"])


reader = easyocr.Reader(["en"])


def extract_values(text):
    values = {}

    def find(pattern, key):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            values[key] = float(match.group(1))

    find(r"hemoglobin[^0-9]*([\d\.]+)", "Hemoglobin")
    find(r"mcv[^0-9]*([\d\.]+)", "MCV")
    find(r"mch[^0-9]*([\d\.]+)", "MCH")
    find(r"mchc[^0-9]*([\d\.]+)", "MCHC")

    return values


if "extracted" not in st.session_state:
    st.session_state.extracted = {}


# OCR RUN
if uploaded_img is not None and not st.session_state.extracted:

    file_bytes = np.frombuffer(uploaded_img.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(img, caption="Uploaded Report", width=420)

    with st.spinner("Extracting values..."):
        result = reader.readtext(img, detail=0)
        text = " ".join(result)
        st.session_state.extracted = extract_values(text)



st.write("### CBC Values")

# Pre-fill with OCR values or allow manual input
hemoglobin = st.number_input("Hemoglobin", value=st.session_state.extracted.get("Hemoglobin", 0.0))
mcv = st.number_input("MCV", value=st.session_state.extracted.get("MCV", 0.0))
mch = st.number_input("MCH", value=st.session_state.extracted.get("MCH", 0.0))
mchc = st.number_input("MCHC", value=st.session_state.extracted.get("MCHC", 0.0))

gender = st.selectbox("Gender", ["Male", "Female"])
gender_val = 1 if gender == "Male" else 0


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
