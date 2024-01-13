import streamlit as st
import pandas as pd
import altair as alt
import speech_recognition as sr
import tempfile
from st_audiorec import st_audiorec

st.set_page_config(layout="wide")
# Set the title and description of your Streamlit app
st.title("Voice-Controlled CSV Data Visualization App")
st.write("Upload a CSV file and use voice commands to interact with the data.")

# Initialize the speech recognition recognizer
r = sr.Recognizer()

# Initialize the df variable as None
df = None

# Initialize session_state with an empty array
if 'chart_commands' not in st.session_state:
    st.session_state.chart_commands = []

# Create a layout with columns for positioning elements
col1, col2 = st.columns([6, 6])  # Adjust column widths as needed

# Element 1: File uploader in the upper part with more width
with col1:
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

# Element 2: Voice recorder in the upper part with more width
with col2:
    st.write("Press the 'Record' button and speak your command (ex., `Show me this data in a line chart`)...")
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        st.write("Recording stopped.")
        st.write("Recognizing command...")
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with audio_file as f:
            f.write(wav_audio_data)
        with sr.AudioFile(audio_file.name) as source:
            try:
                audio_data = r.record(source)
                command = r.recognize_google(audio_data)
                st.write(f"Recognized command: {command}")
                st.session_state.chart_commands.append(command)
            except sr.UnknownValueError:
                st.write("Sorry, I couldn't understand the command. Please try again.")

# Render charts in a single column underneath
st.write("Charts:")
charts_col1, charts_col2 = st.columns(2)
for chart_command in st.session_state.chart_commands:
    if "pie chart" in chart_command:
        # Create a pie chart using Altair
        chart = alt.Chart(df).mark_circle().encode(
            x='X Axis',  # Replace 'Category' with your category column name
            size='Y Axis',  # Replace 'Value' with your value column name
            color='Category:N'
        ).properties(
            width=1000,  # Adjust width as needed
            height=400
        )
        with charts_col1:
            st.altair_chart(chart, use_container_width=True)

    elif "line chart" in chart_command:
        # Create a line chart using Altair
        chart = alt.Chart(df).mark_line().encode(
            x='X Axis',  # Replace 'Date' with your x-axis column name
            y='Y Axis'  # Replace 'Value' with your y-axis column name
        ).properties(
            width=1000,  # Adjust width as needed
            height=400
        )
        with charts_col2:
            st.altair_chart(chart, use_container_width=True)

    elif "bar chart" in chart_command:
        # Create a bar chart using Altair
        chart = alt.Chart(df).mark_bar().encode(
            x='X Axis',  # Replace 'Category' with your category column name
            y='Y Axis',  # Replace 'Value' with your value column name
            color='Category:N'
        ).properties(
            width=1000,  # Adjust width as needed
            height=400
        )
        with charts_col1:
            st.altair_chart(chart, use_container_width=True)
