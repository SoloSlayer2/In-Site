import streamlit as st
import requests
import base64

sessions = requests.Session()
API_BASE = "http://192.168.29.75:8000"

def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
    """
    st.markdown(bg, unsafe_allow_html=True)

set_bg(r"C:\Users\Ronit\Downloads\weather.jpg")



API_KEY = "174d93e84a8c95ab4e78e2552d5de2c2"
st.markdown(
    """
    <h1 style='text-align: center; color: white;'>🌤️ Weather</h1>
     <h4 style='text-align: center; color: white;'>Get latest weather forecast</h4>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    /* Center container */
    .search-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    /* Input box style */
    .stTextInput > div > div > input {
        border-radius: 12px;
        padding: 10px 16px;
        font-size: 1rem;
    }

    /* Custom button style */
    div.stButton > button:first-child {
        display: flex;
        justify-content: center;
        background-color: #1f6feb;
        color: white;
        border-radius: 12px;
        padding: 0.6em 1.5em;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
    }

    div.stButton > button:hover {
        background-color: #0947a7;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.25);
    }

    div.stButton > button:active {
        background-color: #4338ca;
        transform: scale(0.98);
    }
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="search-container">', unsafe_allow_html=True)
city = st.text_input("Mention city's name here", placeholder="Example -- Bhubaneshwar")
get_weather = st.button("Get Weather")
st.markdown('</div>', unsafe_allow_html=True)

if get_weather:
    if not API_KEY:
        st.error("API key is missing. Please add it in the code.")
    else:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            response = requests.get(url, params=params)
            data = response.json()

            if response.status_code == 200:

                weather = data["weather"][0]["description"].title()
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]
                icon = data["weather"][0]["icon"]

                st.subheader(f"Weather in {city}")
                st.image(f"https://openweathermap.org/img/wn/{icon}@2x.png", width=100)
                st.write(f"**Condition:** {weather}")
                st.metric("Temperature (°C)", f"{temp}", delta=f"Feels like {feels_like}")
                st.write(f"💧 Humidity: {humidity}%")
                st.write(f"🌬️ Wind Speed: {wind} m/s")

            else:
                st.error(f"Error: {data.get('message', 'Could not fetch weather data')}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

