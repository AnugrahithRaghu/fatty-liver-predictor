import joblib
import numpy as np

# Load model
model = joblib.load("models/fatty_liver_model.pkl")

# Example user input
# age, height, weight, bmi, waist, alcohol, activity, diet, family_history

input_data = np.array([[45, 170, 85, 29.4, 102, 2, 0, 2, 1]])

prediction = model.predict(input_data)

risk_map = {0: "Low", 1: "Moderate", 2: "High"}

print("Predicted Risk:", risk_map[prediction[0]])