import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📊 StudyHacker Dashboard")

st.header("Weekly Stats")
if st.button("Refresh Weekly Stats"):
    r = requests.get(f"{API_URL}/stats/weekly").json()
    st.json(r)

st.header("Monthly Stats")
if st.button("Refresh Monthly Stats"):
    r = requests.get(f"{API_URL}/stats/monthly").json()
    st.json(r)

st.header("Task Progress")
if st.button("Refresh Task Progress"):
    r = requests.get(f"{API_URL}/stats/tasks-progress").json()
    st.json(r)
