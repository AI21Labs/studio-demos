import streamlit as st
from utils.completion import complete
from utils.studio_style import apply_studio_style
from constants import CLASSIFICATION_FEWSHOT, CLASSIFICATION_PROMPT, CLASSIFICATION_TITLE, CLASSIFICATION_DESCRIPTION, \
    DEFAULT_MODEL

st.set_page_config(
    page_title="Topic Classifier",
)


def query(prompt):
    config = {
        "numResults": 1,
        "maxTokens": 5,
        "temperature": 0,
        "stopSequences": ["==="]
    }
    res = complete(model_type=st.session_state['classification_model'],
                   prompt=prompt,
                   **config)
    return res["completions"][0]["data"]["text"]


if __name__ == '__main__':

    apply_studio_style()
    st.title("The Topic Classifier")
    st.write("Read any interesting news lately? Let's see if our topic classifier can skim through it and identify whether its category is sports, business, world news, or science and technology.")
    st.session_state['classification_model'] = DEFAULT_MODEL

    st.text(CLASSIFICATION_PROMPT)
    classification_title = st.text_input(label="Title:", value=CLASSIFICATION_TITLE)
    classification_description = st.text_area(label="Description:", value=CLASSIFICATION_DESCRIPTION, height=100)

    if st.button(label="Classify"):
        with st.spinner("Loading..."):
            classification_prompt = f"{CLASSIFICATION_PROMPT}\nTitle:\n{classification_title}" \
                                    f"Description:\n{classification_description}The topic of this article is:\n"
            st.session_state["classification_result"] = query(CLASSIFICATION_FEWSHOT + classification_prompt)

    if "classification_result" in st.session_state:
        st.subheader(f"Topic: {st.session_state['classification_result']}")
