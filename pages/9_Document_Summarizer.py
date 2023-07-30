import streamlit as st
from ai21.errors import UnprocessableEntity

from utils.studio_style import apply_studio_style
from constants import ai21, SUMMARIZATION_URL, SUMMARIZATION_TEXT

st.set_page_config(
    page_title="Document Summarizer",
)


@st.cache_data(show_spinner=False)
def get_summary(source, sourceType):
    try:
        response = ai21.Summarize.execute(source=source, sourceType=sourceType.upper())
        st.session_state["summary"] = response['summary']
    except UnprocessableEntity:
        st.session_state["summary"] = None


if __name__ == '__main__':
    apply_studio_style()

    st.title("Document Summarizer")
    st.write(
        "Effortlessly transform lengthy material into a focused summary. Whether it’s an article, research paper or even your own notes -  this tool will sum up the key points!")
    sourceType = st.radio(label="Source type", options=['Text', 'URL'])
    if sourceType == 'Text':
        source = st.text_area(label="Paste your text here:",
                              height=400,
                              value=SUMMARIZATION_TEXT).strip()
    else:
        source = st.text_input(label="Paste your URL here:",
                               value=SUMMARIZATION_URL).strip()

    st.button(label="Summarize 📝️", on_click=get_summary, args=(source, sourceType))

    if "summary" in st.session_state:
        if st.session_state["summary"] is None:
            st.write('Text is too long for the document summarizer, please try the segment summarizer instead.')
        else:
            st.text_area(label="Summary", height=250, value=st.session_state["summary"])

