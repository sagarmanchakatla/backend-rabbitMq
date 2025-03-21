import streamlit as st
import requests
import time

def fetch_data():
    response = requests.get('http://localhost:5000/data')
    return response.json()

st.title("CSV Data Dashboard")

# Polling mechanism to update the dashboard
while True:
    data = fetch_data()
    st.table(data)
    time.sleep(5)  # Poll every 5 seconds