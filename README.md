# Digital Shadow AI 👤🛡️

An AI-powered digital footprint and privacy audit engine. It analyzes unstructured textual data using rule-based PII heuristic pattern matching and Generative AI (Gemini 3.8 Flash) to profile OSINT vulnerability exposure.

## Features
- **Deterministic PII Scanning:** Instant detection of emails, phone numbers, UPI handles, and sensitive routine keywords.
- **Cognitive Footprint Profiling:** Gemini 3.8 Flash infers behavioural habits, living conditions, and digital persona.
- **Privacy Scorecard:** Computes quantitative risk scores (0-100%).

## Setup & Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Run Streamlit app: `streamlit run app.py`
3. Add `GEMINI_API_KEY` to Streamlit Secrets for live demo functionality.
