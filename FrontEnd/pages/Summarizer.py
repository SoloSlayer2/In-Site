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

set_bg(r"C:\Users\Ronit\Downloads\sum.jpg")

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
        border: 2px solid #1f6feb;
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

st.markdown(
    """
    <h1 style='text-align: center; color: white;'>📰 Summarizer</h1>
    <h4 style='text-align: center; color: white;'>Summarize news articles.</h4>
    """,
    unsafe_allow_html=True
)
st.write("---")
text_input = st.text_area(label="What do you wanna know today?", placeholder="Example -- Premier League standings today.")
if st.button("Summarize News"):
    input_text = text_input.strip()
    if input_text == "":
        st.warning("Please enter some news to check.")
    else:
        with st.spinner("Fetching news..."):
            payload = {"query": input_text}
            try:
                response = sessions.post(f"{API_BASE}/news/summarize", json=payload)
                if response.status_code == 200:
                    res = response.json()
                    st.subheader("Summary:")
                    result = res["data"]["summary"]
                    st.markdown(f"{result}")
                else:
                    st.error("Error from server. Please try again later.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                