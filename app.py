import streamlit as st
import re
import google.generativeai as genai

st.set_page_config(
    page_title="Digital Shadow AI",
    page_icon="👤",
    layout="wide"
)

def scan_pii_entities(text):
    patterns = {
        "Email Address": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "Phone Number": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "UPI ID": r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}",
        "Date of Birth / Date": r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b",
        "Credit / Debit Card Pattern": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "IP Address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    }
    
    findings = []
    risk_points = 0
    
    for label, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            findings.append({"entity": label, "count": len(matches), "samples": matches[:2]})
            risk_points += len(matches) * 20

    sensitive_keywords = [
        "password", "pin", "otp", "secret", "home address", "living alone",
        "bank account", "salary", "routine", "vacation until", "out of town"
    ]
    found_keywords = [kw for kw in sensitive_keywords if kw in text.lower()]
    risk_points += len(found_keywords) * 15
    
    total_score = min(risk_points, 100)
    return findings, found_keywords, total_score

def analyze_with_gemini(api_key, text):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")
        
        prompt = f'''
        You are a Cyber Threat Intelligence and OSINT Privacy Expert.
        Analyze the following text (social media bio, status, chat history, or personal log) to identify what digital footprint and psychological vulnerabilities it reveals:
        
        "{text}"
        
        Provide the response in the exact structured format:
        PERSONA: [A 2-sentence description of what an attacker or data broker can infer about this person's habits, wealth, location, routine, or vulnerabilities]
        EXPOSURE_LEVEL: [Low/Moderate/Critical]
        LEAKED_INTENT: [Bullet points or comma-separated list of non-obvious inferences like daily schedule, family members, location routines]
        DEFENSE_TIP: [2 concrete actionable steps to minimize this digital shadow]
        '''
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"GenAI Analysis unavailable: {str(e)}"

# Read API Key from secrets if configured
configured_key = st.secrets.get("GEMINI_API_KEY", "")

st.title("👤 Digital Shadow AI — Digital Footprint & Privacy Exposure Engine")
st.markdown("A cognitive security engine detecting PII leaks, behavioural profiling exposure, and digital footprint risks.")

with st.sidebar:
    st.header("⚙️ Engine Settings")
    if configured_key:
        st.success("✅ System API Key configured")
        active_api_key = configured_key
    else:
        active_api_key = st.text_input("Gemini API Key", type="password", help="Enter Google Gemini API Key")
        
    st.markdown("---")
    st.markdown("### Threat Engine Layers:")
    st.markdown("1. **Rule-Based Heuristic Scanner:** Real-time PII & Sensitive pattern identifier.")
    st.markdown("2. **Gemini 3.8 Flash:** Behavioral OSINT persona profiling & risk extraction.")

user_text = st.text_area(
    "Paste Social Media Bio, Tweet, Daily Log, or Text Message to evaluate digital exposure:",
    height=160,
    placeholder="e.g., Working from Starbucks on Ring Road every evening! Live alone with my dog. Reach me at rahul99@gmail.com or GPay at 9876543210..."
)

if st.button("Evaluate Digital Shadow", type="primary"):
    if not user_text.strip():
        st.warning("Please enter text to inspect.")
    else:
        findings, keywords, risk_score = scan_pii_entities(user_text)
        
        st.markdown("---")
        st.subheader("📊 Exposure Metrics")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Direct Data Leak Score", f"{risk_score}%")
        
        if risk_score > 60:
            severity = "Critical Risk"
        elif risk_score > 25:
            severity = "Moderate Exposure"
        else:
            severity = "Low Risk"
            
        c2.metric("Exposure Status", severity)
        c3.metric("Direct PII Entities Found", len(findings) + len(keywords))
        
        st.markdown("### 🔍 Extracted PII Entities & Contextual Markers")
        if findings or keywords:
            for item in findings:
                st.error(f"⚠️ **{item['entity']} Detected:** Found {item['count']} instance(s)")
            if keywords:
                st.warning(f"⚠️ **Sensitive Operational Keywords:** {', '.join(keywords)}")
        else:
            st.success("No standard PII (Email, Phone, UPI) detected by heuristic scanner.")
            
        st.markdown("---")
        st.subheader("🧠 GenAI Threat Actor Profiling (Digital Shadow)")
        
        if active_api_key:
            with st.spinner("Compiling digital footprint persona with Gemini 3.8 Flash..."):
                gemini_output = analyze_with_gemini(active_api_key, user_text)
                st.info(gemini_output)
        else:
            st.info("💡 Add your Gemini API Key in Streamlit Secrets or Sidebar to view OSINT persona analysis and defense recommendations.")
