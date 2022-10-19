import requests
import streamlit as st

from utils.completion import _full_url
from utils.studio_style import apply_studio_style


API_KEY = st.secrets['api-keys']['ai21-algo-team-prod']


@st.cache(show_spinner=False)
def rewrite(text, api_key, intent="general", span_start=0, span_end=None, env="production"):
    url = _full_url(env, model_type='experimental', custom_model='', endpoint='rewrite')
    auth_header = f"Bearer {api_key}"
    resp = requests.post(
        url,
        headers={"Authorization": auth_header},
        json={"text": text,
              "intent": intent,
              "spanStart": span_start,
              "spanEnd": len(text) if span_end is None else span_end}
    )
    return resp.json()


def get_suggestions(text, intent='general', span_start=0, span_end=None):
    rewrite_resp = rewrite(text, intent=intent, span_start=span_start, span_end=span_end, api_key=API_KEY)
    rewritten_texts = [sug['text'] for sug in rewrite_resp['suggestions']]
    st.session_state["rewrite_rewritten_texts"] = rewritten_texts


if __name__ == '__main__':
    apply_studio_style()

    st.title("Rewrite text")
    text = st.text_input(label="Insert your text here",
                         placeholder="Let's set up a meeting to discuss opportunities using AI21 Studio",
                         value="Let's set up a meeting to discuss opportunities using AI21 Studio").strip()

    intent = st.radio(
        "Set rewrite intent 👉",
        key="intent",
        options=["general", "formal", "casual", "long", "short"],
        horizontal=True
    )

    # col1, *_ = st.columns(4)
    # with col1:
        # intent = st.selectbox(
        #     "Rewrite intent",
        #     ("general", "formal", "casual", "long", "short"),
        # )
    st.button(label="Rewrite", on_click=lambda: get_suggestions(text, intent=intent))
    if "rewrite_rewritten_texts" in st.session_state:
        st.markdown(body='* ' + '\n* '.join(st.session_state["rewrite_rewritten_texts"]))
