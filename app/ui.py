import requests
import streamlit as st
st.set_page_config(page_title="Agentic Data Engineering Copilot", layout="wide")
st.title("🚨 Agentic Data Engineering Copilot")
st.caption("Multi-agent investigation + MCP-style operational tools + human approval")
incident = st.text_area("Incident", "customer_orders_daily failed at 03:17 UTC after a schema change. Investigate and propose a remediation.")
approved = st.checkbox("Approve side-effecting remediation ticket creation")
if st.button("Investigate"):
    r = requests.post("http://api:8000/investigate", json={"incident": incident, "approved": approved}, timeout=180)
    r.raise_for_status()
    x = r.json()
    st.subheader("Root Cause")
    st.write(x.get("rca"))
    st.subheader("Remediation")
    st.write(x.get("remediation"))
    st.subheader("Report")
    st.code(x.get("report", ""))
