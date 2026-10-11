import streamlit as st
import pickle 
import warnings
import time

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Weather Predictor",
    page_icon="🌤️",
    layout="centered"
)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.main-title {
    font-size: 3.5rem;
    color: #ffffff;
    text-align: center;
    text-shadow: 2px 2px 8px #000000;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin-bottom: -10px;
}
.sub-title {
    font-size: 1.2rem;
    color: #e0e0e0;
    text-align: center;
    text-shadow: 1px 1px 5px #000000;
    margin-bottom: 30px;
    font-style: italic;
}

/* Dark Glass Form */
div[data-testid="stForm"] {
    background-color: rgba(20, 25, 30, 0.85);
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Bright white labels for the sliders */
div[data-testid="stForm"] label p {
    color: #ffffff !important;
    font-weight: 600;
    font-size: 1.1rem;
    letter-spacing: 0.5px;
}

/* Interactive Glowing Submit Button */
button[kind="primaryFormSubmit"] {
    border: none;
    background: linear-gradient(90deg, #ff8a00, #e52e71);
    color: white !important;
    font-size: 1.2rem;
    font-weight: bold;
    border-radius: 10px;
    transition: all 0.3s ease;
}
button[kind="primaryFormSubmit"]:hover {
    transform: scale(1.02);
    box-shadow: 0 0 15px rgba(229, 46, 113, 0.6);
    border: none;
}

/* Alert Boxes */
div[data-testid="stAlert"] {
    background-color: rgba(20, 25, 30, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.3) !important;
}
div[data-testid="stAlert"] p {
    color: #ffffff !important;
    font-size: 1.1rem !important;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown('<p class="main-title">🌤️ Weather Forecaster</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Slide the dials below to set the atmospheric conditions.</p>', unsafe_allow_html=True)

# The form with interactive sliders
with st.form("weather_form"):
    col1, col2 = st.columns(2)

    with col1:
        ppt = st.slider("🌧️ Precipitation (mm):", 
                        min_value=0.0, max_value=100.0, value=10.0, step=0.1, 
                        help="Drag to adjust the expected rainfall.")
        
        maxt = st.slider("🔥 Max Temperature (°C):", 
                         min_value=-30.0, max_value=60.0, value=25.0, step=0.5, 
                         help="Drag to set the peak daytime temperature.")

    with col2:
        wind = st.slider("💨 Wind Speed (km/h):", 
                         min_value=0.0, max_value=150.0, value=15.0, step=0.5, 
                         help="Drag to set the wind intensity.")
        
        mint = st.slider("❄️ Min Temperature (°C):", 
                         min_value=-30.0, max_value=60.0, value=15.0, step=0.5, 
                         help="Drag to set the lowest nighttime temperature.")

    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("✨ Predict Weather Magic", use_container_width=True)

if submit_btn:
    if mint > maxt:
        st.error("⚠️ Physics alert: Minimum temperature cannot be higher than Maximum temperature!")
    else:
        with st.spinner("Consulting the clouds... ☁️"):
            time.sleep(1.5)  
            
            try:
                with open("wp.pkl", "rb") as file:
                    wp = pickle.load(file)
                res = wp.predict([[ppt, maxt, mint, wind]])[0]
                
                st.success(f"🎯 **Expected Weather:** {str(res).title()}")
                
                prediction_lower = str(res).lower()
                if "rain" in prediction_lower or "drizzle" in prediction_lower:
                    st.info("Perfect weather to grab a cup of coffee, play some lofi beats, and read a good book! ☕📚")
                elif "sun" in prediction_lower or "clear" in prediction_lower:
                    st.balloons()
                    st.info("It's a beautiful day! Perfect for a walk outside. 🌻")
                elif "snow" in prediction_lower:
                    st.snow()
                    st.info("Time to get cozy under a heavy blanket! ❄️🛌")
                elif "cloud" in prediction_lower or "overcast" in prediction_lower:
                    st.info("A calm, cozy overcast day. Great for movie watching! 🍿☁️")
                
            except FileNotFoundError:
                st.error("Model file 'wp.pkl' not found. Please ensure it is in the same folder as this script.")
            except Exception as e:
                st.error(f"An error occurred: {e}")