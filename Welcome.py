import streamlit as st
from utils.studio_style import apply_studio_style


if __name__ == '__main__':
    st.set_page_config(
        page_title="Welcome"
    )
    apply_studio_style()
    st.title("Welcome to AI21 Studio demos")
    st.markdown("Experience the incredible power of large language models first-hand. With these demos, you can explore a variety of unique use cases that showcase what our sophisticated technology is truly capable of. From instant content generation to a paraphraser that can rewrite any text, the world of AI text generation will be at your fingertips." )
    st.markdown("Check out the brains behind the demos here: https://www.ai21.com/studio")
    st.markdown("Please note that this is a limited demonstration of AI21 Studio's capabilities. If you're interested in learning more, contact us at studio@ai21.com")
