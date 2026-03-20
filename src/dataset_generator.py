import random
import pandas as pd

def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

def generate_data(n=1000):
    data = []

    for _ in range(n):
        age = random.randint(18, 70)
        height = random.randint(150, 190)
        weight = random.randint(45, 110)

        bmi = calculate_bmi(weight, height)
        waist = random.randint(70, 120)

        alcohol = random.choice(["None", "Moderate", "High"])
        activity = random.choice(["Low", "Medium", "High"])
        diet = random.choice(["Healthy", "Mixed", "Junk"])
        family_history = random.choice(["Yes", "No"])

        score = 0

        if bmi > 30:
            score += 3
        elif bmi > 25:
            score += 2

        if waist > 100:
            score += 3

        if alcohol == "High":
            score += 3
        elif alcohol == "Moderate":
            score += 1

        if activity == "Low":
            score += 2

        if diet == "Junk":
            score += 2

        if family_history == "Yes":
            score += 2

        if age > 50:
            score += 2

        if score <= 3:
            risk = "Low"
        elif score <= 7:
            risk = "Moderate"
        else:
            risk = "High"

        data.append([
            age, height, weight, bmi, waist,
            alcohol, activity, diet, family_history, risk
        ])

    columns = [
        "age", "height", "weight", "bmi", "waist",
        "alcohol", "activity", "diet", "family_history", "risk"
    ]

    return pd.DataFrame(data, columns=columns)


# Generate dataset
df = generate_data(1000)

# Save to CSV
df.to_csv("data/fatty_liver_dataset.csv", index=False)

print("Dataset created successfully ✅")