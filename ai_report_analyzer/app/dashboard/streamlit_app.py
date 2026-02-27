import streamlit as st
import pandas as pd
import requests
import os

API_URL = os.getenv("API_URL", "http://api:8000")

st.set_page_config(page_title="AI Report Analyzer", layout="wide")

st.title("Intelligent Business Report Analyzer")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    with st.spinner("Processing data..."):
        files = {"file": uploaded_file.getvalue()}
        try:
            response = requests.post(f"{API_URL}/upload", files=files)
            if response.status_code == 200:
                data = response.json()
                st.success("Report Analyzed Successfully")
                st.json(data["insights"])
            else:
                st.error("Failed to process report")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")

st.divider()

st.subheader("Historical Reports")

try:
    resp = requests.get(f"{API_URL}/reports")
    if resp.status_code == 200:
        reports = resp.json()
        if reports:
            df_reports = pd.DataFrame(reports)
            st.dataframe(df_reports)
        else:
            st.info("No reports found")
except:
    st.info("Waiting for API service")