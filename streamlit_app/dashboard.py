import streamlit as st
import socketio
import pandas as pd
import requests

# Initialize SocketIO client
sio = socketio.Client()

# Function to fetch data from the Flask app
def fetch_data():
    response = requests.get('http://127.0.0.1:5000/data')
    return response.json()

# Shared state to store CSV data
if 'csv_data' not in st.session_state:
    st.session_state.csv_data = fetch_data()

# Function to handle SocketIO events
@sio.on('csv_update')
def handle_csv_update(data):
    # Update the session state with the new data
    st.session_state.csv_data = data
    st.experimental_rerun()  # Rerun the Streamlit app to update the UI

# Connect to the Flask-SocketIO server
try:
    sio.connect('http://127.0.0.1:5000')
except Exception as e:
    st.error(f"Failed to connect to SocketIO server: {e}")

# Streamlit app
st.title("CSV Data Dashboard")

# Display the CSV data
if isinstance(st.session_state.csv_data, list):
    # Convert the list of dictionaries to a DataFrame for display
    df = pd.DataFrame(st.session_state.csv_data)
    st.table(df)
else:
    st.write("No data available yet.")

# Disconnect SocketIO when the Streamlit app stops
if sio.connected:
    sio.disconnect()