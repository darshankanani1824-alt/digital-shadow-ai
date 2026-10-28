import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Digital Footprint Tracker", page_icon="🌐", layout="wide")

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .stApp { background: #f3f6fb; }
    .hero {
        background: linear-gradient(180deg, #4a90e2, #6aa9ee);
        padding: 40px 20px; border-radius: 14px; text-align: center;
        color: white; margin-bottom: 24px;
    }
    .hero h1 { color: white; margin: 0; font-size: 2.4rem; }
    .card {
        background: white; padding: 20px 24px; border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 16px; color: #111;
    }
    .card h3 { margin-top: 0; color: #111; }
    .row { display: flex; justify-content: space-between; padding: 10px 0;
           border-bottom: 1px solid #eee; color: #222; }
    .High { color: #e53935; font-weight: 600; }
    .Medium { color: #fb8c00; font-weight: 600; }
    .Low { color: #43a047; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sample data ----------
BREACHES = [
    ("Google", "2 days ago", "High"),
    ("United Healthcare", "2 days ago", "High"),
    ("Meta", "7 days ago", "Medium"),
    ("AT&T", "10 days ago", "Low"),
    ("Ticketmaster", "10 days ago", "Low"),
]
PERMISSIONS = [
    ("📁 Google Drive", "Files", "High"),
    ("💳 Amazon", "Payment", "High"),
    ("📍 Google Chrome", "Location", "High"),
    ("👥 Spotify", "Contacts", "Medium"),
    ("🎙️ LinkedIn", "Microphone", "Medium"),
]
ACCOUNTS = [
    ("Gmail", "Active", "Low"),
    ("Facebook", "Active", "Medium"),
    ("Instagram", "Active", "Medium"),
    ("LinkedIn", "Active", "Low"),
    ("Old Forum Account", "Inactive 3 yrs", "High"),
]
LOGINS = [
    ("Mumbai, India", "Chrome / Windows", "Today"),
    ("Moscow, Russia", "Unknown device", "Yesterday"),
    ("Berlin, Germany", "Firefox / Linux", "3 days ago"),
]
DEVICES = [
    ("Windows Laptop", "Chrome", "Active now"),
    ("Android Phone", "Google App", "2 hours ago"),
    ("Unknown Device", "Unknown Browser", "5 days ago"),
]

MODEL_NAME = "gemini-2.5-flash"


# ---------- Sidebar ----------
st.sidebar.title("🌐 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "👤 Accounts", "🛡️ Permissions", "👁️ Monitoring", "💻 Devices"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Engine Settings")

# Key priority: Streamlit secrets -> sidebar input
default_key = ""
try:
    default_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    default_key = ""

api_key = st.sidebar.text_input("Gemini API Key", value=default_key, type="password")


# ---------- Gemini helper (cached so same query does not waste quota) ----------
@st.cache_data(show_spinner=False, ttl=3600)
def get_ai_insight(key: str, query: str) -> str:
    genai.configure(api_key=key)
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = f"""
You are a privacy and cybersecurity assistant.
The user wants privacy insights about: "{query}".
Give a short answer with these sections:
1. Risk level (Low / Medium / High)
2.
