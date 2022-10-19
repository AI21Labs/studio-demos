import streamlit as st

from utils.completion import complete
from utils.studio_style import apply_studio_style
from constants import CLASSIFICATION_FEWSHOT, CLASSIFICATION_PROMPT


def query(prompt):
    config = {
        "numResults": 1,
        "maxTokens": 5,
        "temperature": 0,
        "stopSequences": ["==="]
    }
    res = complete(model_type=st.session_state['model'],
                   prompt=prompt,
                   config=config,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])
    return res


if __name__ == '__main__':

    apply_studio_style()
    st.title("Topic Classification")

    st.subheader("Model")
    st.session_state['model'] = st.selectbox(label="Select your preferred AI21 model",
                                             options=['j1-jumbo', 'experimental/j1-grande-instruct', 'j1-grande', 'j1-large'])

    classification_prompt = st.text_area(label="Classification instruction:", value=CLASSIFICATION_PROMPT, height=300)

    if st.button(label="Classify"):
        with st.spinner("Loading..."):
            st.session_state["result"] = query(CLASSIFICATION_FEWSHOT + classification_prompt)

    st.write(classification_prompt)
    if "result" in st.session_state:
        st.subheader("Completion:")
        st.write(st.session_state["result"])