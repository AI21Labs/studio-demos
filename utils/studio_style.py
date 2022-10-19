import streamlit as st

def apply_studio_style():
    st.markdown(
        """
        <style>
         @import url(http://db.onlinewebfonts.com/c/9e00143409affcb46a1ae58634aa64be?family=Sofia+Pro);
         @font-face {font-family: "Sofia Pro";
}

			html, body, [class*="css"]  {
			font-family: 'Sofia Pro';
			}
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.image("./assets/studio_logo.svg")