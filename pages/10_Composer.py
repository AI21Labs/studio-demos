import streamlit as st
from utils.completion import complete
from utils.studio_style import apply_studio_style

st.set_page_config(
    page_title="Composer",
)

PROMPT_EXAMPLES = {
    "any": "Write a silly story about a pig who wants to be a superhero",
    "story": "Write a silly story about a pig who wants to be a superhero",
    "email": "Write an email to the HR manager, requesting the next available position",
    "poem": "Write a poem about returning to Kent",
    "press release": "Write a press release from the chair of the Human Rights Committee condemning the violations of human rights and censorship in North Korea",
    "blogpost": "Write a blogpost about how to start a personal blog",
    "invitation": "Invite Julie to the office Christmas party",
    "joke": "Tell me a joke about dogs",
    "abstract": "Write an abstract for an article about the importance of nutrition to health",
    "pitch": "Write a pitch about an AI-based writing assistant"
}


MODEL_CONF = {
    "maxTokens": 512,
    "temperature": 0.8,
    # "logitBias": {'<|endoftext|>': -5}
}

LENGTH_LIMITS = {
    "any": (0, 10000),
    "poem": (50, 100),
    "email": (50, 150),
    "blogpost": (300, 500),
    "story": (100, 400),
    "press release": (100, 400),
    "invitation": (50, 150),
    "abstract": (100, 200),
    "pitch": (150, 500),
    "joke": (50, 150)
}


def generate(text, category, model_type="experimental/j1-compose", max_retries=10):
    min_length, max_length = LENGTH_LIMITS[category]
    completions_filtered = []
    try_count = 0
    while not len(completions_filtered) and try_count < max_retries:
        res = complete(model_type=model_type,
                   prompt=text,
                   config=MODEL_CONF,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])
        completion_texts = [comp['data']['text'] for comp in res['completions']]
        completions_filtered = [t for t in completion_texts if min_length <= len(t.split()) <= max_length]
        try_count += 1
    st.session_state["prompt"] = text
    st.session_state["completion"] = completions_filtered[0]


if __name__ == '__main__':

    apply_studio_style()
    st.title("Composer")
    st.markdown("###### Compose any valuable content, from blogposts to emails! It can be any type of content from the list below, or any other composition you desire. Simply describe what you want to compose, and let our tool work its magic.")

    content_type = st.selectbox(
        "Select content type 👉",
        key="content_type",
        options=list(LENGTH_LIMITS.keys()),
    )

    prompt = st.text_input(label="What should the model write about?",
                     value=PROMPT_EXAMPLES[content_type],
                     placeholder=content_type).strip()

    if st.button(label="Compose"):
        with st.spinner("Loading..."):
            generate(prompt, category=content_type)

        st.write(st.session_state['completion'])
