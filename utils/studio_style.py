import streamlit as st

def apply_studio_style():
    st.markdown(
        """
       
        <style>
            @import url("//hello.myfonts.net/count/3caa3a");
            @font-face {
              font-family: 'SofiaPro';
              font-style: normal;
              font-weight: 700;
              src: url('assets/font.woff2') format('woff2'), url('assets/font.woff') format('woff');
            }

            html, body, [class*="css"]  {
            font-family: 'SofiaPro';
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.image("./assets/studio_logo.svg")