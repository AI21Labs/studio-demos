import streamlit as st

from utils.completion import complete, tokenize
from utils.studio_style import apply_studio_style
from constants import OBQA_CONTEXT, OBQA_QUESTION, OBQA_MODEL

st.set_page_config(
    page_title="OpenBookQA",
)

max_tokens = 2048 - 200

def query(prompt, **kwargs):
    config = {
        "numResults": 1,
        "maxTokens": 200,
        "temperature": 0,
        **kwargs
    }
    res = complete(model_type='j1-grande-v2',
                   custom_model=OBQA_MODEL,
                   prompt=prompt,
                   config=config,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])
    return res["completions"][0]["data"]["text"]


if __name__ == '__main__':

    apply_studio_style()
    st.title("Open Book Question Answering")

    st.write("Ask a question on a given context.")

    obqa_context = st.text_area(label="Context:", value=OBQA_CONTEXT, height=300)
    obqa_question = st.text_input(label="Question:", value=OBQA_QUESTION)
    obqa_prompt = f"question:\n{obqa_question}\n\ncontext:\n{obqa_context}\n\nquestion:\n{obqa_question}\nanswer:\n"

    if st.button(label="Answer"):
        with st.spinner("Loading..."):
            num_tokens = len(tokenize(obqa_prompt, api_key=st.secrets['api-keys']['ai21-algo-team-prod']))
            if num_tokens > max_tokens:
                st.write("Text is too long. Input is limited up to 2048 tokens. Try using a shorter text.")
                if 'obqa_answer' in st.session_state:
                    del st.session_state['completions']
            else:
                st.session_state["obqa_answer"] = query(obqa_prompt)

    if "obqa_answer" in st.session_state:
        st.write(f"Answer: {st.session_state['obqa_answer']}")
        if st.session_state['obqa_answer'] == "Answer not in document":
            if st.button(label="Force answer"):
                with st.spinner("Loading..."):
                    st.session_state["obqa_force_answer"] = query(obqa_prompt, logitBias={"▁Answer": -1000})
            if "obqa_force_answer" in st.session_state:
                st.write(f"Answer: {st.session_state['obqa_force_answer']}")
