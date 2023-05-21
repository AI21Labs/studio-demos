import streamlit as st
from utils.studio_style import apply_studio_style
from constants import ai21

st.set_page_config(
    page_title="Rewrite Tool",
)


def get_suggestions(text, intent='general', span_start=0, span_end=None):
    rewrite_resp = ai21.Paraphrase.execute(text=text, intent=intent, spanStart=span_start, spanEnd=span_end or len(text))
    rewritten_texts = [sug['text'] for sug in rewrite_resp['suggestions']]
    st.session_state["rewrite_rewritten_texts"] = rewritten_texts


def show_next(cycle_length):
    # From streamlit docs: "When updating Session state in response to events, a callback function gets executed first, and then the app is executed from top to bottom."
    # This means this function just needs to update the current index. The text itself would be shown since the entire app is executed again
    curr_index = st.session_state["rewrite_curr_index"]
    next_index = (curr_index + 1) % cycle_length
    st.session_state["rewrite_curr_index"] = next_index


def show_prev(cycle_length):
    curr_index = st.session_state["rewrite_curr_index"]
    prev_index = (curr_index - 1) % cycle_length
    st.session_state["rewrite_curr_index"] = prev_index


if __name__ == '__main__':
    apply_studio_style()

    st.title("The Rewrite Tool")
    st.write("Rephrase with ease! Find fresh new ways to reword your sentences with an AI writing companion that paraphrases & rewrites any text. Select rewrite suggestions that clearly convey your ideas with a range of different tones to choose from.")
    text = st.text_area(label="Write your text here to see what the rewrite tool can do:",
                         max_chars=500,
                         placeholder="Let's set up a meeting to discuss opportunities using AI21 Studio",
                         value="Let's set up a meeting to discuss opportunities using AI21 Studio").strip()

    intent = st.radio(
        "Set your tone 👉",
        key="intent",
        options=["general", "formal", "casual", "long", "short"],
        horizontal=True
    )

    st.button(label="Rewrite ✍️", on_click=lambda: get_suggestions(text, intent=intent))
    if "rewrite_rewritten_texts" in st.session_state:
        suggestions = st.session_state["rewrite_rewritten_texts"]

        ph = st.empty()
        if "rewrite_curr_index" not in st.session_state:
            st.session_state["rewrite_curr_index"] = 0
        curr_index = st.session_state["rewrite_curr_index"]
        ph.text_area(label="Suggestions", value=suggestions[curr_index])

        col1, col2, col3, *_ = st.columns([1, 1, 1, 10])
        with col1:
            st.button("<", on_click=show_prev, args=(len(suggestions),))
        with col2:
            st.markdown(f"{curr_index+1}/{len(suggestions)}")
        with col3:
            st.button(">", on_click=show_next, args=(len(suggestions),))

