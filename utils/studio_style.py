import streamlit as st

def apply_studio_style():
    st.markdown(
        """
        <link href="//db.onlinewebfonts.com/c/9e00143409affcb46a1ae58634aa64be?family=Sofia+Pro" rel="stylesheet" type="text/css"/>
        <style>
            @import url(//db.onlinewebfonts.com/c/9e00143409affcb46a1ae58634aa64be?family=Sofia+Pro);
            @font-face {
              font-family: 'Sofia Pro';
              font-style: normal;
              font-weight: 700;
              src: src: url("//db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.eot"); src: url("//db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.eot?#iefix") format("embedded-opentype"), url("//db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.woff2") format("woff2"), url("//db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.woff") format("woff"), url("//db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.ttf") format("truetype"), url("//db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.svg#Sofia Pro") format("svg"); 
              unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
            }

            html, body, [class*="css"]  {
            font-family: 'Sofia Pro';
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.image("./assets/studio_logo.svg")