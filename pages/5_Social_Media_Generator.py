from constants import *
from utils.completion import complete
from utils.filters import *
from utils.studio_style import apply_studio_style

MODEL_CONF = {
    "maxTokens": 200,
    "temperature": 0.8,
    "numResults": 16
    # "logitBias": {'<|endoftext|>': -5}
}


def create_prompt(media, article):
    post_type = "tweet" if media == "Twitter" else "Linkedin post"
    instruction = f"Write a {post_type} touting the following press release."
    return f"{instruction}\nArticle:\n{article}\n\n{post_type}:\n"


def generate(article, media, max_retries=2, top=3):
    prompt = create_prompt(media, article)
    completions_filtered = []
    try_count = 0
    while not len(completions_filtered) and try_count < max_retries:
        res = complete(model_type=DEFAULT_MODEL, prompt=prompt, **MODEL_CONF)
        completions_filtered = [comp['data']['text'] for comp in res['completions']
                                if apply_filters(comp, article, media)]
        try_count += 1
    res = filter_duplicates(completions_filtered)[:top]
    return [remove_utf_emojis(anonymize(i)) for i in res]


def on_next():
    st.session_state['index'] = (st.session_state['index'] + 1) % len(st.session_state['completions'])


def on_prev():
    st.session_state['index'] = (st.session_state['index'] - 1) % len(st.session_state['completions'])


def toolbar():
    cols = st.columns([0.35, 0.1, 0.1, 0.1, 0.35])
    with cols[1]:
        st.button(label='<', key='prev', on_click=on_prev)
    with cols[2]:
        st.text(f"{st.session_state['index'] + 1}/{len(st.session_state['completions'])}")
    with cols[3]:
        st.button(label="\>", key='next', on_click=on_next)
    with cols[4]:
        st.button(label="🔄", on_click=lambda: compose())


def extract():
    with st.spinner("Summarizing article..."):
        try:
            st.session_state['article'] = ai21.Summarize.execute(source=st.session_state['url'], sourceType='URL')['summary']
        except:
            st.session_state['article'] = False


def compose():
    with st.spinner("Generating post..."):
        st.session_state["completions"] = generate(st.session_state['article'], media=st.session_state['media'])
        st.session_state['index'] = 0


if __name__ == '__main__':
    apply_studio_style()
    st.title("Social Media Generator")

    st.session_state['url'] = st.text_input(label="Enter your article URL",
                                            value=st.session_state.get('url', 'https://www.ai21.com/blog/announcing-ai21-studio-and-jurassic-1')).strip()

    if st.button(label='Summarize'):
        extract()

    if 'article' in st.session_state:
        if not st.session_state['article']:
            st.write("This article is not supported, please try another one")

        else:
            st.text_area(label='Summary', value=st.session_state['article'], height=200)

            st.session_state['media'] = st.radio(
                "Compose a post for this article for 👉",
                options=['Twitter', 'Linkedin'],
                horizontal=True
            )

            st.button(label="Compose", on_click=lambda: compose())

    if 'completions' in st.session_state:
        if len(st.session_state['completions']) == 0:
            st.write("Please try again 😔")

        else:
            curr_text = st.session_state['completions'][st.session_state['index']]
            st.text_area(label="Your awesome generated post", value=curr_text.strip(), height=200)
            if len(st.session_state['completions']) > 1:
                toolbar()
