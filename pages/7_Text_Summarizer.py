import requests
import streamlit as st

from utils.completion import _full_url
from utils.studio_style import apply_studio_style

PLACEHOLDER_TEXT = '''Perhaps no other crisis in modern history has had as great an impact on daily human existence as COVID-19. And none has forced businesses throughout the world to accelerate their evolution as their leaders worked to respond and recover on the way to thriving in the postpandemic environment.

Deloitte Private’s latest global survey of private enterprises reveals that executives in every region used the crisis as a catalyst, accelerating change in virtually all aspects of how we work and live. They stepped up their digital transformation through greater technology investment and deployment. In-progress initiatives were pushed toward completion, while those that were on the drawing board came to life. They sought out new partnerships and alliances. They pursued new opportunities to strengthen their supply networks and grow markets. They increased efforts to understand their purpose beyond profits, seeking new ways to grow sustainably and strengthen trust with their employees, customers, and other key stakeholders. They also embraced new possibilities in how and where work gets done.
'''

API_KEY = st.secrets['api-keys']['ai21-algo-team-prod']

st.set_page_config(
    page_title="Text Summarizer",
)


@st.cache(show_spinner=False)
def summarize(text, api_key, env="production"):
    url = _full_url(env, model_type='experimental', custom_model='', endpoint='summarize')
    auth_header = f"Bearer {api_key}"
    resp = requests.post(
        url,
        headers={"Authorization": auth_header},
        json={"text": text}
    )
    return resp.json()


def get_summary(text):
    summarize_resp = summarize(text, api_key=API_KEY)
    summary = summarize_resp['summaries'][0]['text'].strip()
    st.session_state["summarize_summary"] = summary


if __name__ == '__main__':
    apply_studio_style()

    st.title("Text Summarizer")
    st.write("Effortlessly transform lengthy material into a focused summary. Whether it’s an article, research paper or even your own notes -  this tool will sum up the key points!")
    text = st.text_area(label="Paste your text here:",
                        height=400,
                        value=PLACEHOLDER_TEXT).strip()

    st.button(label="Summarize 📝️", on_click=get_summary, args=(text,))

    if "summarize_summary" in st.session_state:
        st.text_area(label="Summary", height=150, value=st.session_state["summarize_summary"])

