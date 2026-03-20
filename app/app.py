import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("models/fatty_liver_model.pkl")

st.title("Fatty Liver Risk Predictor 🩺")

# --------- BASIC INPUTS ---------
age = st.slider("Age", 18, 70)
height = st.slider("Height (cm)", 140, 200)
weight = st.slider("Weight (kg)", 40, 120)

# BMI calculation
bmi = weight / ((height / 100) ** 2)
st.write("BMI:", round(bmi, 2))

# --------- WAIST AUTO-FILL SYSTEM ---------
st.subheader("Waist Input (Auto from Jeans Size) 👖")

# Initialize session state
if "waist" not in st.session_state:
    st.session_state.waist = 70

# Jeans selection
jeans_size = st.selectbox(
    "Select your jeans size (optional)",
    ["None"] + [str(s) for s in range(26, 54, 2)]
)

# If jeans selected → update waist
if jeans_size != "None":
    st.session_state.waist = round(int(jeans_size) * 2.54)

# Waist slider (auto-updated)
waist = st.slider(
    "Waist Circumference (cm)",
    60, 130,
    value=st.session_state.waist
)

# Show message
if jeans_size != "None":
    st.success(f"Auto-filled waist: {waist} cm")

# --------- OTHER INPUTS ---------
alcohol = st.selectbox("Alcohol Consumption", ["None", "Moderate", "High"])
activity = st.selectbox("Physical Activity", ["Low", "Medium", "High"])
diet = st.selectbox("Diet Type", ["Healthy", "Mixed", "Junk"])
family_history = st.selectbox("Family History", ["No", "Yes"])

# --------- ENCODING ---------
alcohol_map = {"None": 0, "Moderate": 1, "High": 2}
activity_map = {"Low": 0, "Medium": 1, "High": 2}
diet_map = {"Healthy": 0, "Mixed": 1, "Junk": 2}
family_map = {"No": 0, "Yes": 1}

# --------- PREDICTION ---------
# --------- PREDICTION ---------
if st.button("Predict"):
    input_data = np.array([[
        age, height, weight, bmi, waist,
        alcohol_map[alcohol],
        activity_map[activity],
        diet_map[diet],
        family_map[family_history]
    ]])

    prediction = model.predict(input_data)[0]

    risk_map = {0: "Low", 1: "Moderate", 2: "High"}
    result = risk_map[prediction]

    st.subheader(f"Risk Level: {result}")

    # --------- EXPLANATION LOGIC ---------
    reasons = []

    if bmi > 30:
        reasons.append("High BMI (Obesity)")
    elif bmi > 25:
        reasons.append("Overweight (BMI > 25)")

    if waist > 100:
        reasons.append("High Waist Circumference")

    if alcohol == "High":
        reasons.append("High Alcohol Consumption")
    elif alcohol == "Moderate":
        reasons.append("Moderate Alcohol Intake")

    if activity == "Low":
        reasons.append("Low Physical Activity")

    if diet == "Junk":
        reasons.append("Unhealthy Diet (Junk Food)")

    if family_history == "Yes":
        reasons.append("Family History of Liver Disease")

    if age > 50:
        reasons.append("Age > 50")

    # --------- SHOW EXPLANATION ---------
    if result == "High":
        st.error("⚠️ High Risk Detected")

    elif result == "Moderate":
        st.warning("⚠️ Moderate Risk")

    else:
        st.success("✅ Low Risk")

    # Show reasons
    if reasons:
        st.markdown("### 🔍 Why this result?")
        for r in reasons:
            st.write("•", r)

    # --------- RECOMMENDATIONS ---------
    st.markdown("### 💡 Recommendations")

    if result == "High":
        st.write("• Reduce alcohol consumption")
        st.write("• Follow a healthy diet")
        st.write("• Exercise regularly")
        st.write("• Consult a doctor if needed")

    elif result == "Moderate":
        st.write("• Maintain a balanced diet")
        st.write("• Stay physically active")
        st.write("• Monitor your weight")

    else:
        st.write("• Maintain your healthy lifestyle 👍")