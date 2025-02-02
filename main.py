# main.py
import streamlit as st
from components import dashboard, qa

PAGES = {"Assistant report": dashboard, "Q&A": qa}


def main():
    st.set_page_config(
        page_title='Swisshacks-AI',
        page_icon="LogoLeaf.png",
        layout='wide',
        initial_sidebar_state='auto',
    )
    st.sidebar.title(
        'Sweephy - Swisshacks Microsoft / Unique Challenge - AI Innovation in Finance'
    )
    selection = st.sidebar.radio("", list(PAGES.keys()))

    if "visited_pages" not in st.session_state:
        st.session_state.visited_pages = []

    if selection not in st.session_state.visited_pages:
        st.session_state.visited_pages.append(selection)

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app(st.session_state)


if __name__ == "__main__":
    main()
