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

# Custom CSS for modern Light Dashboard UI
st.markdown("""
<style>
    /* Background */
    .stApp {
        background: linear-gradient(180deg, #4b92db 0%, #68a7ec 120px, #f4f7fb 120px, #f4f7fb 100%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Header title */
    .main-title {
        color: white;
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: -25px;
        margin-bottom: 25px;
        letter-spacing: -0.5px;
    }
    
    /* Card Container */
    .dashboard-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #edf2f7;
        margin-bottom: 20px;
    }
    
    /* Card Header */
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1a202c;
        margin: 0;
    }
    .card-btn {
        background: #111827;
        color: white;
        font-size: 0.78rem;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
    }
    .card-btn-light {
        background: #f3f4f6;
        color: #374151;
        font-size: 0.78rem;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #e5e7eb;
    }
    
    /* List item row */
    .list-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #f3f4f6;
        font-size: 0.88rem;
    }
    .list-row:last-child {
        border-bottom: none;
    }
    .badge-high {
        color: #ef4444;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-med {
        color: #f59e0b;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-low {
        color: #10b981;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    /* Hide default elements */
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
        st.success("✅ Gemini Active")

# Main Page Title
st.markdown("<div class='main-title'>Digital Footprint Tracker</div>", unsafe_allow_html=True)

# Top Section: Privacy Index & Privacy AI
col_top1, col_top2 = st.columns([1, 1.4])

with col_top1:
    st.markdown("""
    <div class='dashboard-card'>
        <div style='color: #6b7280; font-size: 0.85rem; font-weight: 500;'>Privacy Index</div>
        <div style='font-size: 1.8rem; font-weight: 800; color: #111827; margin: 4px 0 14px 0;'>Average</div>
        <div style='display: flex; gap: 8px;'>
            <div style='height: 6px; flex: 1; background: #3b82f6; border-radius: 4px;'></div>
            <div style='height: 6px; flex: 1; background: #60a5fa; border-radius: 4px;'></div>
            <div style='height: 6px; flex: 1; background: #93c5fd; border-radius: 4px;'></div>
            <div style='height: 6px; flex: 1; background: #e5e7eb; border-radius: 4px;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_top2:
    st.markdown("<div class='dashboard-card' style='padding-bottom: 12px;'>", unsafe_allow_html=True)
    st.markdown("<div style='color: #111827; font-size: 0.95rem; font-weight: 700; margin-bottom: 8px;'>Get personalized insights with Privacy AI</div>", unsafe_allow_html=True)
    ai_col1, ai_col2 = st.columns([4, 1])
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
                resp = model.generate_content(f"Analyze this privacy issue and suggest immediate fix: {query}")
                st.info(f"🤖 **Privacy AI:** {resp.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please configure your Gemini API Key in Streamlit Secrets.")

# Middle Section: Data Breaches & Permission Risks
m_col1, m_col2 = st.columns(2)

with m_col1:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-header'>
            <span class='card-title'>12 Data Breaches</span>
            <span class='card-btn'>Resolve all</span>
        </div>
        <div class='list-row'>
            <span><b>Google</b></span>
            <span style='color: #6b7280;'>2 days ago</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span><b>United Healthcare</b></span>
            <span style='color: #6b7280;'>2 days ago</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span><b>Meta</b></span>
            <span style='color: #6b7280;'>7 days ago</span>
            <span class='badge-med'>• Medium</span>
        </div>
        <div class='list-row'>
            <span><b>AT&T</b></span>
            <span style='color: #6b7280;'>10 days ago</span>
            <span class='badge-low'>• Low</span>
        </div>
        <div class='list-row'>
            <span><b>Ticketmaster</b></span>
            <span style='color: #6b7280;'>10 days ago</span>
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
            <span>📁 Google Drive</span>
            <span style='color: #6b7280;'>Files</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span>💳 Amazon</span>
            <span style='color: #6b7280;'>Payment</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span>📍 Google Chrome</span>
            <span style='color: #6b7280;'>Location</span>
            <span class='badge-high'>• High</span>
        </div>
        <div class='list-row'>
            <span>👥 Spotify</span>
            <span style='color: #6b7280;'>Contacts</span>
            <span class='badge-med'>• Medium</span>
        </div>
        <div class='list-row'>
            <span>🎙️ LinkedIn</span>
            <span style='color: #6b7280;'>Microphone</span>
            <span class='badge-med'>• Medium</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Bottom Section: Graphs (Suspicious Logins & Accounts Breakdown)
b_col1, b_col2 = st.columns(2)

with b_col1:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-header'>
            <span class='card-title'>13 Suspicious Logins</span>
            <span class='card-btn-light'>Review all</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Bar Chart with Plotly
    days = ['Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue']
    counts = [2, 5, 8, 2, 2, 3, 4]
    
    fig_bar = go.Figure(data=[
        go.Bar(
            x=days, 
            y=counts, 
            marker_color='#6b8afd',
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
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor='#f3f4f6', zeroline=False),
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
    
    # Donut Chart with Plotly
    labels = ['Social media', 'Finance', 'E-commerce', 'Work & productivity', 'Personal', 'Other']
    values = [280, 190, 130, 90, 60, 46]
    colors = ['#f87171', '#fbbf24', '#34d399', '#60a5fa', '#a78bfa', '#38bdf8']
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.6,
        marker=dict(colors=colors),
        textinfo='none'
    )])
    fig_donut.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=190,
        legend=dict(orientation="v", x=1.05, y=0.5, font=dict(size=10)),
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
