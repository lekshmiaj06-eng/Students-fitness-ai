import streamlit as st
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# 2. Setup AI Client (This is the "reliable" way that worked for you)
client = InferenceClient(api_key=API_KEY)

st.set_page_config(page_title="Student AI Fitness Pro", page_icon="🏋️")
st.title("🏋️ Student AI Fitness & Diet Pro")

# --- USER INPUT SECTION ---
st.subheader("Personal Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)

with col2:
    goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Stay Fit"])
    activity = st.selectbox("Activity Level", ["Sedentary", "Moderate", "Active"])

with col3:
    budget = st.selectbox("Monthly Food Budget", ["Low", "Medium", "High"])
    cuisine = st.text_input("Cuisine Preference", value="Indian")

# --- BMI LOGIC ---
bmi = weight / ((height/100) ** 2)
st.metric(label="Your BMI", value=f"{bmi:.1f}")

# Categorize BMI for the AI prompt
if bmi < 18.5: status = "Underweight"
elif 18.5 <= bmi <= 24.9: status = "Normal"
else: status = "Overweight"

st.subheader("Health & Safety")
col4, col5 = st.columns(2)
with col4:
    medical_info = st.text_area("Medical Conditions / Injuries", placeholder="e.g., Asthma, none...")
with col5:
    allergies = st.text_input("Food Allergies", placeholder="e.g., Peanuts, None")
    equipment = st.selectbox("Equipment", ["None", "Dumbbells", "Full Gym"])

# --- AI GENERATION ---
if st.button("Generate My Personalized Plan"):
    if not API_KEY:
        st.error("API Key missing! Add it to your .env file.")
    else:
        with st.spinner("🤖 AI is crafting your plan..."):
            prompt = f"Coach mode. Student BMI: {bmi:.1f} ({status}), Goal: {goal}, Budget: {budget}, Medical: {medical_info}, Allergies: {allergies}. Provide a 3-day workout and meal plan."
            
            try:
                # Use the same model and client method that worked for you!
                response = client.chat_completion(
                    model="meta-llama/Llama-3.2-1B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )
                plan_text = response.choices[0].message.content
                st.session_state.plan = plan_text 
                st.markdown(plan_text)
            except Exception as e:
                st.error(f"AI connection failed: {e}")

