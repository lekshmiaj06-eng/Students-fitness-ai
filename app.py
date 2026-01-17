import streamlit as st
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# 1. Load the secret key from the .env file
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# 2. Setup AI Client (Using a highly stable model)
client = InferenceClient(api_key=API_KEY)

# 3. UI Design
st.set_page_config(page_title="Student AI Fitness", layout="wide")
st.title("🏋️‍♂️ Student AI Fitness & Diet Planner")

# User Input Section
col1, col2 = st.columns(2)
with col1:
    goal = st.selectbox("Your Fitness Goal", ["Weight Loss", "Muscle Gain", "Stay Fit"])
    cuisine = st.text_input("Cultural Food Preference", "Indian")
with col2:
    budget = st.selectbox("Budget", ["Budget-Friendly (Student)", "Moderate", "High"])
    equipment = st.text_input("Available Equipment", "None / Bodyweight")

# 4. Generate Plan
if st.button("Generate My Personalized Plan"):
    if not API_KEY:
        st.error("API Key not found! Please check your .env file.")
    else:
        prompt = f"As a student fitness coach, create a 1-day workout and meal plan. Goal: {goal}. Cuisine: {cuisine}. Budget: {budget}. Equipment: {equipment}. Keep it very cheap and dorm-friendly."
        
        with st.spinner("🤖 AI is crafting your plan..."):
            try:
                # Using a very reliable model for student projects
                response = client.chat_completion(
                    model="meta-llama/Llama-3.2-1B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800
                )
                st.success("Plan Ready!")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Something went wrong: {e}")