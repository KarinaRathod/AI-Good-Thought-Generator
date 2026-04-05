import os
from dotenv import load_dotenv
import streamlit as st
import matplotlib.pyplot as plt
import datetime
import google.generativeai as genai

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# UI CONFIG
# -----------------------------
st.set_page_config(page_title="AI Good Thought Generator", layout="wide")
st.title("🧠✨ AI Good Thought Generator")
st.caption("Get personalized positive thoughts based on your mood and situation")

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "mood_data" not in st.session_state:
    st.session_state.mood_data = []

# -----------------------------
# INPUT SECTION
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    mood = st.selectbox("💭 Select Your Mood", [
        "😊 Happy",
        "😔 Sad",
        "😰 Anxious",
        "😴 Unmotivated",
        "😤 Stressed"
    ])

with col2:
    tone = st.selectbox("🎭 Select Tone", [
        "Friendly",
        "Motivational",
        "Calm",
        "Strict"
    ])

situation = st.text_area("📝 What's on your mind?", height=150)

# -----------------------------
# GENERATE THOUGHT
# -----------------------------
if st.button("✨ Generate Thought"):

    if not situation.strip():
        st.warning("⚠️ Please describe your situation")
        st.stop()

    with st.spinner("🧠 Generating meaningful thought..."):

        prompt = f"""
        User mood: {mood}
        Tone: {tone}
        Situation: {situation}

        Generate a deep, meaningful, non-generic positive thought.
        Make it:
        - Personal
        - Emotionally intelligent
        - Short (3-4 lines max)
        - Not cliché

        Avoid generic quotes.
        """

        response = model.generate_content(prompt)
        thought = response.text

        # Save history
        st.session_state.history.append({
            "time": str(datetime.datetime.now()),
            "mood": mood,
            "thought": thought
        })

        # Save mood for graph
        mood_score = {
            "😊 Happy": 5,
            "😔 Sad": 2,
            "😰 Anxious": 2,
            "😴 Unmotivated": 3,
            "😤 Stressed": 2
        }

        st.session_state.mood_data.append(mood_score[mood])

        # -----------------------------
        # DISPLAY OUTPUT
        # -----------------------------
        st.subheader("💡 Your Thought")
        st.success(thought)

# -----------------------------
# HISTORY
# -----------------------------
if st.session_state.history:
    st.subheader("📜 Thought History")

    for item in reversed(st.session_state.history[-5:]):
        st.info(f"{item['time']}\n\nMood: {item['mood']}\n\n{item['thought']}")

# -----------------------------
# MOOD TRACKER GRAPH
# -----------------------------
if len(st.session_state.mood_data) > 1:
    st.subheader("📊 Mood Trend")

    fig, ax = plt.subplots()
    ax.plot(st.session_state.mood_data, marker='o')
    ax.set_title("Mood Improvement Trend")
    ax.set_xlabel("Entries")
    ax.set_ylabel("Mood Score")

    st.pyplot(fig)

# -----------------------------
# DOWNLOAD REPORT
# -----------------------------
if st.session_state.history:

    report = "AI GOOD THOUGHT JOURNAL\n\n"

    for item in st.session_state.history:
        report += f"Time: {item['time']}\n"
        report += f"Mood: {item['mood']}\n"
        report += f"Thought: {item['thought']}\n\n"

    st.download_button(
        "📥 Download Thought Journal",
        data=report,
        file_name="thought_journal.txt"
    )