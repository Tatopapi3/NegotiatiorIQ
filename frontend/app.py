import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="NegotiateIQ", page_icon="💼", layout="centered")

st.markdown("""
<style>
    .main { max-width: 720px; }
    .stTextArea textarea { font-size: 14px; }
    .result-box { background: #0f172a; border-radius: 12px; padding: 1.5rem; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("💼 NegotiateIQ")
st.caption("AI salary negotiation coach powered by Claude + real market data")

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_negotiate, tab_free, tab_ingest = st.tabs(["💰 Salary Negotiation", "🧠 Negotiate Anything", "📥 Ingest Data"])

# ── Tab 1: Salary Negotiation ──────────────────────────────────────────────────
with tab_negotiate:
    st.subheader("Get your negotiation playbook")
    st.caption("We'll pull real market comps from our database and have Claude coach you.")

    col1, col2 = st.columns(2)
    with col1:
        role       = st.text_input("Job Title", placeholder="Senior Software Engineer")
        company    = st.text_input("Company", placeholder="Acme Corp")
        location   = st.text_input("Location", value="New York, NY")
    with col2:
        salary     = st.number_input("Offered Salary ($)", min_value=50000, max_value=1000000,
                                      value=150000, step=5000)
        years_exp  = st.number_input("Your Years of Experience", min_value=0, max_value=40, value=3)

    notes = st.text_area("Additional context (optional)",
                          placeholder="e.g. I have a competing offer from Stripe for $175k. "
                                      "I'm currently at $140k. The role is fully remote.",
                          height=80)

    if st.button("🚀 Get My Negotiation Coaching", type="primary", use_container_width=True):
        if not role or not company:
            st.warning("Please fill in at least the job title and company.")
        else:
            with st.spinner("Pulling market comps and generating your playbook..."):
                try:
                    res = requests.post(f"{API_URL}/negotiate", json={
                        "role": role,
                        "company": company,
                        "location": location,
                        "salary": salary,
                        "years_exp": years_exp,
                        "notes": notes,
                    }, timeout=60)
                    data = res.json()
                except Exception as e:
                    st.error(f"API error: {e}")
                    st.stop()

            st.success(f"Found {data['similar_jds_found']} market comps · {data['similar_profiles_found']} similar candidates")

            st.markdown("### 📊 Market Rate Assessment")
            st.markdown(data["market_rate"])

            st.markdown("### 💰 Counter-Offer Range")
            st.markdown(data["counter_range"])

            st.markdown("### ✉️ Negotiation Script")
            st.markdown(data["negotiation_script"])

            st.markdown("### 🎯 Your Leverage Points")
            st.markdown(data["key_points"])

            with st.expander("Full Claude response"):
                st.markdown(data["raw"])

# ── Tab 2: Negotiate Anything ──────────────────────────────────────────────────
with tab_free:
    st.subheader("Negotiate anything")
    st.caption("Rent, freelance rates, vendor contracts, job offers — describe your situation and get a word-for-word script.")

    situation = st.text_area(
        "Describe what you're negotiating",
        placeholder=(
            "Example: I'm a freelance developer. A client wants to pay me $75/hr for a 3-month project. "
            "I usually charge $120/hr. They said budget is tight but really need my skills in React and AI. "
            "How do I negotiate this?"
        ),
        height=160,
    )

    if st.button("🧠 Get Negotiation Script", type="primary", use_container_width=True):
        if not situation.strip():
            st.warning("Describe your negotiation situation above.")
        else:
            with st.spinner("Crafting your negotiation strategy..."):
                try:
                    res = requests.post(f"{API_URL}/negotiate/free", json={"situation": situation}, timeout=60)
                    data = res.json()
                except Exception as e:
                    st.error(f"API error: {e}")
                    st.stop()

            st.markdown("### 🎯 Strategy")
            st.markdown(data["strategy"])

            st.markdown("### ✉️ Word-for-Word Script")
            st.markdown(data["script"])

            st.markdown("### 🔑 Key Tactics")
            st.markdown(data["tactics"])

# ── Tab 3: Ingest Data ─────────────────────────────────────────────────────────
with tab_ingest:
    st.subheader("Add market data")
    col_jd, col_profile = st.columns(2)

    with col_jd:
        st.markdown("**📋 Job Description**")
        jd_title   = st.text_input("Title", key="jd_title", placeholder="Senior Engineer")
        jd_company = st.text_input("Company", key="jd_company")
        jd_loc     = st.text_input("Location", key="jd_loc", value="New York, NY")
        jd_min     = st.number_input("Min Salary", key="jd_min", value=0, step=5000)
        jd_max     = st.number_input("Max Salary", key="jd_max", value=0, step=5000)
        jd_content = st.text_area("JD Text", key="jd_content", height=120)
        if st.button("Add JD", use_container_width=True):
            if jd_title and jd_company and jd_content:
                res = requests.post(f"{API_URL}/ingest/jd", json={
                    "title": jd_title, "company": jd_company,
                    "location": jd_loc,
                    "salary_min": jd_min or None,
                    "salary_max": jd_max or None,
                    "content": jd_content,
                })
                st.success("JD ingested!") if res.ok else st.error(res.text)

    with col_profile:
        st.markdown("**👤 Candidate Profile**")
        p_title   = st.text_input("Title", key="p_title", placeholder="Senior Engineer")
        p_yrs     = st.number_input("Years Exp", key="p_yrs", value=3, min_value=0)
        p_skills  = st.text_input("Skills (comma-separated)", key="p_skills")
        p_content = st.text_area("Profile / Resume Text", key="p_content", height=120)
        if st.button("Add Profile", use_container_width=True):
            if p_title and p_content:
                res = requests.post(f"{API_URL}/ingest/profile", json={
                    "title": p_title, "years_exp": p_yrs,
                    "skills": [s.strip() for s in p_skills.split(",") if s.strip()],
                    "content": p_content,
                })
                st.success("Profile ingested!") if res.ok else st.error(res.text)
