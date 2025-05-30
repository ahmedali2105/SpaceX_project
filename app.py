import streamlit as st
import joblib
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier

# Set page config
st.set_page_config(page_title="🚀 SpaceX Launch Success Predictor", layout="centered")
st.title("🚀 SpaceX Launch Success Predictor")

st.markdown("""
Enter all launch parameters to predict whether the SpaceX launch will be successful.
""")

# 1. Handle Model Loading
MODEL_PATH = "models/launch_success.pkl"

@st.cache_resource
def load_model():
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # If no model exists, create a simple demo model
    if not os.path.exists(MODEL_PATH):
        st.warning("Using demo model - predictions may be less accurate")
        model = RandomForestClassifier()
        
        # Create dummy data for demo purposes
        X_demo = np.random.rand(100, 10)
        y_demo = np.random.randint(0, 2, 100)
        model.fit(X_demo, y_demo)
        
        # Save demo model
        joblib.dump(model, MODEL_PATH)
        return model
    
    # Load real model if exists
    return joblib.load(MODEL_PATH)

model = load_model()

# 2. Input fields (unchanged)
rocket_encoded = st.selectbox("🚀 Rocket (Encoded)", options=[0, 1, 2], format_func=lambda x: f"Rocket {x}")
launchpad_encoded = st.selectbox("🛰️ Launchpad (Encoded)", options=[0, 1, 2], format_func=lambda x: f"Launchpad {x}")
payload_mass = st.number_input("📦 Payload Mass (kg)", min_value=0.0, max_value=50000.0, value=6000.0)
temperature = st.number_input("🌡️ Temperature (°C)", min_value=-100.0, max_value=100.0, value=25.0)
humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
wind_speed = st.number_input("💨 Wind Speed (m/s)", min_value=0.0, max_value=100.0, value=5.0)
year = st.number_input("📅 Year", min_value=2002, max_value=2030, value=2020)
month = st.number_input("📆 Month", min_value=1, max_value=12, value=6)
day = st.number_input("📅 Day", min_value=1, max_value=31, value=15)
hour = st.number_input("⏰ Hour", min_value=0, max_value=23, value=13)

# 3. Prediction
if st.button("Predict Launch Success"):
    try:
        input_data = np.array([[rocket_encoded, launchpad_encoded, payload_mass,
                              temperature, humidity, wind_speed,
                              year, month, day, hour]])
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        if prediction == 1:
            st.success(f"✅ Predicted: **Successful Launch** with {probability * 100:.2f}% confidence.")
        else:
            st.error(f"❌ Predicted: **Failed Launch** with {(1 - probability) * 100:.2f}% confidence.")
            
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Developed by Syed Ahmed Ali | Powered by Machine Learning")
