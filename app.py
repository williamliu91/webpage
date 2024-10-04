import streamlit as st
import home
import about
import contact

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "About", "Contact"])

# Navigation logic
if page == "Home":
    home.app()
elif page == "About":
    about.app()
elif page == "Contact":
    contact.app()
