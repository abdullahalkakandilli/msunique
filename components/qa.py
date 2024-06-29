import streamlit as st
from utils.ip_checker import get_remote_ip


def app(session_state):
    ip = get_remote_ip()

    with st.sidebar:
        st.info(f"Ip address: {ip}")

    st.info('Q&A session will be reset if you leave the page', icon="ℹ️")
