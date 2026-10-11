import streamlit as st
import pickle 
import warnings
import time
import random

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Weather Predictor",
    page_icon="🌤️",
    layout="centered"
)



def change_bg(url):
    """Injects CSS to dynamically change the background image with a smooth override"""
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("{url}") !important;
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def create_rain():
    rain_html = """
    <style>
    .raindrop {
        position: fixed;
        top: -10vh;
        font-size: 1.5rem;
        z-index: 9999; /* Kept in front to look like drops on the screen */
        animation: rain-fall linear forwards;
    }
    @keyframes rain-fall {
        0% { transform: translateY(-10vh); opacity: 1; }
        100% { transform: translateY(110vh); opacity: 0; }
    }
    </style>
    """
    for _ in range(50):  
        left = random.randint(0, 100)
        duration = random.uniform(0.8, 1.5)
        delay = random.uniform(0, 2)
        rain_html += f"<div class='raindrop' style='left: {left}vw; animation-duration: {duration}s; animation-delay: {delay}s;'>💧</div>"
    st.markdown(rain_html, unsafe_allow_html=True)

def create_clouds():
    cloud_html = """
    <style>
    .cloud {
        position: fixed;
        left: -15vw;
        font-size: 4rem;
        z-index: 0; /* Pushed behind the glass form */
        animation: cloud-drift linear forwards;
        opacity: 0.85;
    }
    @keyframes cloud-drift {
        0% { transform: translateX(-10vw); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateX(110vw); opacity: 0; }
    }
    </style>
    """
    for _ in range(15):  
        top = random.randint(0, 70)
        duration = random.uniform(4, 8)
        delay = random.uniform(0, 1.5)
        cloud_html += f"<div class='cloud' style='top: {top}vh; animation-duration: {duration}s; animation-delay: {delay}s;'>☁️</div>"
    st.markdown(cloud_html, unsafe_allow_html=True)

def create_sun():
    sun_html = """
    <style>
    .sun-wrapper {
        position: fixed;
        z-index: 0; /* FIXED: Pushed to the background layer */
        animation: sun-rise 2.5s ease-out forwards;
    }
    .css-sun {
        width: 130px;
        height: 130px;
        background: radial-gradient(circle, #fff3c9 0%, #ffd700 40%, #ff8c00 100%);
        border-radius: 50%;
        box-shadow: 0 0 40px 20px rgba(255, 215, 0, 0.5);
        animation: sun-pulse 2.5s infinite alternate;
    }
    @keyframes sun-rise {
        0% { bottom: -20vh; left: -10vw; opacity: 0; transform: scale(0.5); }
        100% { bottom: 65vh; left: 8vw; opacity: 1; transform: scale(1); }
    }
    @keyframes sun-pulse {
        0% { box-shadow: 0 0 40px 20px rgba(255, 215, 0, 0.5); transform: scale(1); }
        100% { box-shadow: 0 0 65px 35px rgba(255, 215, 0, 0.8); transform: scale(1.03); }
    }
    </style>
    <div class="sun-wrapper">
        <div class="css-sun"></div>
    </div>
    """
    st.markdown(sun_html, unsafe_allow_html=True)

# --- Main Default Background and Styling ---
page_bg_img = """
<style>
/* Default Sunset Background */
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
    position: relative; /* Ensures z-index works */
    z-index: 10; /* Keeps form above the sun/clouds */
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
    position: relative; /* Ensures z-index works */
    z-index: 10; /* Keeps alerts above the sun/clouds */
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
                    change_bg("https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=2000&auto=format&fit=crop")
                    create_rain() 
                    st.info("Perfect weather to grab a cup of coffee, play some lofi beats, and read a good book! ☕📚")
                    
                elif "sun" in prediction_lower or "clear" in prediction_lower:
                    change_bg("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop")
                    create_sun() 
                    st.info("It's a beautiful day! Perfect for a walk outside. 🌻")
                    
                elif "snow" in prediction_lower:
                    change_bg("https://images.unsplash.com/photo-1483664852095-d6cc6870702d?q=80&w=2000&auto=format&fit=crop")
                    st.snow() 
                    st.info("Time to get cozy under a heavy blanket! ❄️🛌")
                    
                elif "cloud" in prediction_lower or "overcast" in prediction_lower:
                    change_bg("https://images.unsplash.com/photo-1499956827185-0d63ee78a910?q=80&w=2000&auto=format&fit=crop")
                    create_clouds() 
                    st.info("A calm, cozy overcast day. Great for movie watching! 🍿☁️")
                
            except FileNotFoundError:
                st.error("Model file 'wp.pkl' not found. Please ensure it is in the same folder as this script.")
            except Exception as e:
                st.error(f"An error occurred: {e}")