import streamlit as st
import requests

st.title("Test App")
st.write("Hello World!")

if st.button("Test API"):
    try:
        response = requests.get("http://localhost:8000/health")
        st.write("Status:", response.status_code)
        st.json(response.json())
    except Exception as e:
        st.error(f"Error: {e}")
