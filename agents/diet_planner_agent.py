import streamlit as st
import os
import json
import matplotlib.pyplot as plt
import re
from dotenv import load_dotenv
#from langchain_groq import ChatGroq

os.environ["Dietician Agent"] = "Dietician Agent"

# Load environment variables
load_dotenv()

# Initialize the Groq LLM
#llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7, max_retries=2)
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")


def calculate_bmr(age, gender, height, weight):
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161


def calculate_tdee(bmr, activity_level):
    multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9,
    }
    return bmr * multipliers.get(activity_level, 1.2)


def adjust_calories_for_goal(tdee, goal):
    if goal == "Lose Weight":
        return tdee - 500
    elif goal == "Gain Weight":
        return tdee + 500
    elif goal == "Build Strength / Muscle":
        return tdee + 250
    else:
        return tdee


def get_goal_specific_guidelines(goal):
    guidelines = {
        "Lose Weight": """- Focus on low-calorie, high-volume foods.
- Avoid added sugars and ultra-processed foods.
- Prioritize fiber-rich foods for satiety.
- Grocery list: leafy greens, chicken breast, lentils, quinoa, low-fat dairy, berries.
""",
        "Gain Weight": """- Include calorie-dense healthy foods.
- Eat more frequently.
- Prioritize complex carbs and healthy fats.
- Grocery list: oats, peanut butter, bananas, salmon, whole wheat bread, olive oil.
""",
        "Build Strength / Muscle": """- High protein intake (1.6–2.2g/kg bodyweight).
- Moderate carbs for workout energy.
- Include healthy fats for hormones.
- Grocery list: eggs, Greek yogurt, chicken, salmon, sweet potatoes, brown rice, broccoli.
""",
        "Maintain Weight": """- Balanced macronutrient split (50% carbs, 25% protein, 25% fats).
- Focus on whole, unprocessed foods.
- Grocery list: fruits, vegetables, fish, chicken, rice, beans, nuts.
""",
    }
    return guidelines.get(goal, "")


def plot_macros_chart(macros):
    labels = list(macros.keys())
    values = list(macros.values())
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)


def run_diet_planner_agent():
    st.subheader("🥗 Personalized Diet Planner")

    with st.form("diet_form"):
        age = st.number_input("Age", 5, 100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)")
        weight = st.number_input("Weight (kg)")
        activity = st.selectbox(
            "Activity Level",
            ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
        )
        goal = st.selectbox(
            "What is your goal?",
            [
                "Lose Weight",
                "Maintain Weight",
                "Gain Weight",
                "Build Strength / Muscle",
            ],
        )
        dietary_preference = st.selectbox(
            "Dietary Preference",
            ["Vegetarian", "Semi-Vegetarian", "Non-Vegetarian"],
        )
        submitted = st.form_submit_button("Generate Diet Plan")

    if submitted:
        bmr = calculate_bmr(age, gender, height, weight)
        tdee = calculate_tdee(bmr, activity)
        target_calories = adjust_calories_for_goal(tdee, goal)
        goal_guidelines = get_goal_specific_guidelines(goal)

        prompt = f"""
You are a certified dietician. ONLY return valid JSON.
Do NOT include any extra text before or after the JSON.

User profile:
- Age: {age}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- Activity Level: {activity}
- Fitness Goal: {goal}
- Calculated BMR: {bmr:.0f} kcal
- Calculated TDEE: {tdee:.0f} kcal
- Target Calories per day: {target_calories:.0f} kcal
- Dietary Preference: {dietary_preference}

Goal-specific dietary guidelines:
{goal_guidelines}

Return exactly this JSON structure (no commentary, no markdown):
{{
    "daily_plan": [
        {{
            "day": "Day 1",
            "meals": [
                {{"meal": "Breakfast", "description": "...", "calories": 350}},
                {{"meal": "Snack 1", "description": "...", "calories": 150}},
                {{"meal": "Lunch", "description": "...", "calories": 500}},
                {{"meal": "Snack 2", "description": "...", "calories": 150}},
                {{"meal": "Dinner", "description": "...", "calories": 500}}
            ],
            "total_calories": 1650,
            "macros": {{"protein_g": 120, "carbs_g": 180, "fats_g": 50}}
        }}
    ],
    "grocery_list": ["item1", "item2", "item3"]
}}
"""

        try:
            ai_response = llm.invoke(prompt)
            # Extract ai_response content text if it has a .content attribute
            if hasattr(ai_response, "content"):
                raw_result = ai_response.content
            else:
                raw_result = str(ai_response)

            # Try to extract JSON if extra text is present
            json_match = re.search(r"\{.*\}", raw_result, re.DOTALL)
            if json_match:
                raw_result = json_match.group(0)

            try:
                data = json.loads(raw_result)
            except json.JSONDecodeError:
                st.error("AI did not return valid JSON, even after cleanup.")
                st.code(raw_result, language="json")
                return

            st.success(f"Your 1-Day Meal Plan for {goal}")
            for day in data.get("daily_plan", []):
                st.markdown(
                    f"### {day.get('day', 'Day')}\nTotal: {day.get('total_calories', 0)} kcal"
                )
                for meal in day.get("meals", []):
                    st.markdown(
                        f"**{meal.get('meal', '')}**: {meal.get('description', '')} ({meal.get('calories', 0)} kcal)"
                    )

                st.subheader(f"Macronutrient Breakdown - {day.get('day', 'Day')}")
                macros = {
                    "Protein": day.get("macros", {}).get("protein_g", 0),
                    "Carbs": day.get("macros", {}).get("carbs_g", 0),
                    "Fats": day.get("macros", {}).get("fats_g", 0),
                }
                plot_macros_chart(macros)

            st.subheader("🛒 Grocery List")
            for item in data.get("grocery_list", []):
                st.markdown(f"- {item}")

        except Exception as e:
            st.error(f"Error generating diet plan: {e}")


if __name__ == "__main__":
    run_diet_planner_agent()
