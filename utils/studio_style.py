import streamlit as st

def apply_studio_style():
    st.markdown(
        """
       
        <style>
        @font-face {font-family: "Sofia Pro";
    src: url("http://db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.eot"); /* IE9*/
    src: url("http://db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.eot?#iefix") format("embedded-opentype"), /* IE6-IE8 */
    url("http://db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.woff2") format("woff2"), /* chrome firefox */
    url("http://db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.woff") format("woff"), /* chrome firefox */
    url("http://db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.ttf") format("truetype"), /* chrome firefox opera Safari, Android, iOS 4.2+*/
    url("http://db.onlinewebfonts.com/t/9e00143409affcb46a1ae58634aa64be.svg#Sofia Pro") format("svg"); /* iOS 4.1- */
}

			html, body, [class*="css"]  {
			font-family: 'Sofia Pro';
			}
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.image("./assets/studio_logo.svg")