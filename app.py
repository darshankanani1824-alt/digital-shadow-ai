import streamlit as st
import plotly.graph_objects as go
import google.generativeai as genai

# Page Config
st.set_page_config(
    page_title="Digital Footprint Tracker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for forcing pristine light SaaS card UI
st.markdown("""
<style>
    /* Background styling */
    .stApp {
        background: linear-gradient(180deg, #4b92db 0%, #68a7ec 140px, #f4f7fb 140px, #f4f7fb 100%) !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Force main container padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Header title */
    .main-title {
        color: #ffffff !important;
        text-align: center;
        font-size: 2.3rem;
        font-weight: 700;
        margin-top: -15px;
        margin-bottom: 30px;
        letter-spacing: -0.5px;
    }
    
    /* Dashboard Cards */
    .dashboard-card {
        background: #ffffff !important;
        border-radius: 18px !important;
        padding: 22px 24px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
        border: 1px solid #eef2f6 !important;
        margin-bottom: 20px;
    }
    
    /* Card Headers */
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    .card-title {
        font-size: 1.18rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
        margin: 0;
    }
    .card-btn {
        background: #111827 !important;
        color: #ffffff !important;
        font-size: 0.8rem;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 600;
    }
    .card-btn-light {
        background: #f3f4f6 !important;
        color: #374151 !important;
        font-size: 0.8rem;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #e5e7eb;
    }
    
    /* List Item Row */
    .list-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 11px 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.92rem;
    }
    .list-row:last-child {
        border-bottom: none;
    }
    .item-name {
        color: #1e293b !important;
        font-weight: 600;
    }
    .item-time {
        color: #64748b !important;
        font-size: 0.86rem;
    }
    
    /* Badges */
    .badge-high {
        color: #ef4444 !important;
        font-weight: 700;
        font-size: 0.84rem;
    }
    .badge-med {
        color: #f59e0b !important;
        font-weight: 700;
        font-size: 0.84rem;
    }
    .badge-low {
        color: #10b981 !important;
        font-weight: 700;
        font-size: 0.84rem;
    }

    /* Style the input inside card */
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 10px 14px !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🌐 Navigation")
    menu = st.radio("", ["🏠 Home", "👤 Accounts", "🛡️ Permissions", "👁️ Monitoring", "💻 Devices"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### ⚙️ Engine Settings")
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Gemini API Key", type="password")
    else:
        st.success("✅ System API Key Active")

# Main Header
st.markdown("<div class='main-title'>Digital Footprint Tracker</div>", unsafe_allow_html=True)

# Top Row
col_top1, col_top2 = st.columns([1, 1.4])

with col_top1:
    st.markdown("""
    <div class='dashboard-card' style='height: 125px;'>
        <div style='color: #64748b; font-size: 0.85rem; font-weight: 600;'>Privacy Index</div>
        <div style='font-size: 1.85rem; font-weight: 800; color: #0f172a; margin: 4px 0 12px 0;'>Average</div>
        <div style='display: flex; gap: 8px;'>
            <div style='height: 6px; flex: 1; background: #2563eb; border-radius: 4px;'></div>
            <div style='height: 6px; flex: 1; background: #3b82f6; border-radius: 4px;'></div>
            <div style='height: 6px; flex: 1; background: #93c5fd; border-radius: 4px;'></div>
            <div style='height: 6px; flex: 1; background: #e2e8f0; border-radius: 4px;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_top2:
    st.markdown("""
    <div class='dashboard-card' style='height: 125px;'>
        <div style='color: #0f172a; font-size: 0.95rem; font-weight: 700; margin-bottom: 8px;'>Get personalized insights with Privacy AI</div>
    """, unsafe_allow_html=True)
    ai_col1, ai_col2 = st.columns([4, 1.2])
    with ai_col1:
        query = st.text_input("Ask anything to Privacy AI", placeholder="Ask anything to Privacy AI...", label_visibility="collapsed")
    with ai_col2:
        ask_clicked = st.button("Analyze →", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if ask_clicked and query:
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.8-flash")
            with st.spinner("AI analyzing threat footprint..."):
                resp = model.generate_content(f"Analyze this privacy issue concisely: {query}")
                st.info(f"🤖 **Privacy AI:** {resp.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please configure your Gemini API Key in Streamlit Secrets.")

# Middle Row: Data Breaches & Permission Risks
m_col1, m_col2 = st.columns(2)

with m_col1:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-header'>
            <span class='card-title'>12 Data Breaches</span>
            <span class='card-btn'>Resolve all</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>Google</span>
            <span class='item-time'>2 days ago</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>United Healthcare</span>
            <span class='item-time'>2 days ago</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>Meta</span>
            <span class='item-time'>7 days ago</span>
            <span class='badge-med'>• Medium</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>AT&T</span>
            <span class='item-time'>10 days ago</span>
            <span class='badge-low'>• Low</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>Ticketmaster</span>
            <span class='item-time'>10 days ago</span>
            <span class='badge-low'>• Low</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-header'>
            <span class='card-title'>15 Permission Risks</span>
            <span class='card-btn-light'>Review all</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>📁 Google Drive</span>
            <span class='item-time'>Files</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>💳 Amazon</span>
            <span class='item-time'>Payment</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>📍 Google Chrome</span>
            <span class='item-time'>Location</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>👥 Spotify</span>
            <span class='item-time'>Contacts</span>
            <span class='badge-med'>• Medium</span>
        </div>
        <div class='list-row'>
            <span class='item-name'>🎙️ LinkedIn</span>
            <span class='item-time'>Microphone</span>
            <span class='badge-med'>• Medium</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Bottom Row: Graphs
b_col1, b_col2 = st.columns(2)

with b_col1:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-header'>
            <span class='card-title'>13 Suspicious Logins</span>
            <span class='card-btn-light'>Review all</span>
        </div>
    """, unsafe_allow_html=True)
    
    days = ['Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue']
    counts = [2, 5, 8, 2, 2, 3, 4]
    
    fig_bar = go.Figure(data=[
        go.Bar(
            x=days, 
            y=counts, 
            marker_color='#60a5fa',
            marker_line_width=0,
            text=counts,
            textposition='auto',
        )
    ])
    fig_bar.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=190,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False, showline=False, tickfont=dict(color='#64748b')),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', zeroline=False, tickfont=dict(color='#64748b')),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with b_col2:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-header'>
            <span class='card-title'>796 Accounts</span>
            <span class='card-btn-light'>View details</span>
        </div>
    """, unsafe_allow_html=True)
    
    labels = ['Social media', 'Finance', 'E-commerce', 'Work & productivity', 'Personal', 'Other']
    values = [280, 190, 130, 90, 60, 46]
    colors = ['#f87171', '#fbbf24', '#34d399', '#60a5fa', '#a78bfa', '#38bdf8']
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.62,
        marker=dict(colors=colors),
        textinfo='none'
    )])
    fig_donut.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=190,
        legend=dict(orientation="v", x=1.05, y=0.5, font=dict(size=11, color='#334155')),
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
