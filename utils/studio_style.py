import streamlit as st

def apply_studio_style():
    st.markdown(
        """
       
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.image("./assets/studio_logo.svg")