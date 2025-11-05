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

set_bg(r"C:\Users\Ronit\Downloads\Newschecker.jpg")

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
    <h1 style='text-align: center; color: white;'>📝 News Checker</h1>
    <h4 style='text-align: center; color: white;'>News verification tool to check the authenticity of news articles.</h4>
    """,
    unsafe_allow_html=True
)
st.write("---")
text_input = st.text_area(label="Type your news here...", placeholder="Example -- Trump is now president of mars.")
if st.button("Check News"):
    input_text = text_input.strip()
    if input_text == "":
        st.warning("Please enter some text to check.")
    else:
        with st.spinner("Checking news..."):
            payload = {"news": input_text}
            try:
                response = sessions.post(f"{API_BASE}/news/verify", json=payload)
                if response.status_code == 200:
                    res = response.json()
                    result=res["data"]["result"]
                    verdict = res["data"]["verdict"]

                    if verdict == "True":
                        st.markdown("<p style='color:limegreen; font-weight:600;'>✅ The news is Real.</p>", unsafe_allow_html=True)

                    elif verdict == "Partially True":
                        st.markdown("<p style='color:orange; font-weight:600;'>🟠 The news is Partially True.</p>", unsafe_allow_html=True)

                    elif verdict == "False":
                        st.markdown("<p style='color:red; font-weight:600;'>❌ The news is Fake.</p>", unsafe_allow_html=True)

                    else:
                        st.markdown("<p style='color:gray;'>⚪ Unable to determine verdict.</p>", unsafe_allow_html=True)    
                    st.markdown(f"{result}")

                else:
                    st.error("Error from server. Please try again later.")
            except Exception as e:
                st.error(f"An error occurred: {e}")