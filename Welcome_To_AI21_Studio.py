import streamlit as st
from utils.studio_style import apply_studio_style
if __name__ == '__main__':

    apply_studio_style()
    st.title("Welcome to AI21 Studio")
    st.markdown("The following tabs allow you to navigate between demos that demonstrate our technology's capabilities." )
    st.markdown("To check out the brains behind the demos visit https://www.ai21.com/studio" )
