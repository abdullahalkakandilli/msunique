import streamlit as st
from utils.ip_checker import get_remote_ip


def app(session_state):
    ip = get_remote_ip()
    with st.sidebar:
        st.info(f"Ip address: {ip}")

    st.markdown(
        """
        Welcome to Sweephy  dashboard ! \n
        This dashboard shows 
            """
    )

    company = st.selectbox("Company", ["IBM", "SIEMENS"])
