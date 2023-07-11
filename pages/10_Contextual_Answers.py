import streamlit as st
from utils.completion import tokenize
from utils.studio_style import apply_studio_style
from constants import OBQA_CONTEXT, OBQA_QUESTION, ai21

st.set_page_config(
    page_title="Answers",
)

max_tokens = 2048 - 200


if __name__ == '__main__':

    apply_studio_style()
    st.title("Contextual Answers")

    st.write("Ask a question on a given context.")

    context = st.text_area(label="Context:", value=OBQA_CONTEXT, height=300)
    question = st.text_input(label="Question:", value=OBQA_QUESTION)

    if st.button(label="Answer"):
        with st.spinner("Loading..."):
            num_tokens = len(tokenize(context + question))
            if num_tokens > max_tokens:
                st.write("Text is too long. Input is limited up to 2048 tokens. Try using a shorter text.")
                if 'answer' in st.session_state:
                    del st.session_state['completions']
            else:
                response = ai21.Experimental.answer(context=context, question=question)
                st.session_state["answer"] = response['answer']

    if "answer" in st.session_state:
        st.write(st.session_state['answer'])
