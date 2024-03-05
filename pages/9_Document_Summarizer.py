import streamlit as st
from ai21.errors import UnprocessableEntity

from utils.studio_style import apply_studio_style
from constants import client, SUMMARIZATION_URL, SUMMARIZATION_TEXT

st.set_page_config(
    page_title="Document Summarizer",
)

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

    if st.button(label="Answer"):
        with st.spinner("Loading..."):
            try:
                response = client.summarize.create(source=source, source_type=sourceType.upper())
                st.text_area(label="Summary", height=250, value=response.summary)
            except UnprocessableEntity:
                st.write('Text is too long for the document summarizer, please try the segment summarizer instead.')
