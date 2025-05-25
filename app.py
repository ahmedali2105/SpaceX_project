import streamlit as st
import joblib
import numpy as np
import os

# 1. Check if model exists
MODEL_PATH = "models/launch_success.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("""
    Model file not found! Please ensure:
    1. You have a 'models' folder
    2. It contains 'launch_success.pkl'
    3. The file is committed to GitHub
    """)
    st.stop()

# 2. Load Model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"Failed to load model: {str(e)}")
    st.stop()

# Rest of your app code...
st.set_page_config(...)
