import streamlit as st
from streamlit_chat import message
from typing import List, Dict
from constants import CUSTOM_CHAT_DEMOS

from utils.completion import complete
from utils.studio_style import apply_studio_style

st.set_page_config(
    page_title="Conversational AI",
)


def message_to_string(message: Dict[str, str]) -> str:
    return [f"{k}: {v}" for k, v in message.items()][0]


def messages_to_string(messages: List[Dict[str, str]]) -> str:
    messages_parsed_dicts = [message_to_string(message) for message in messages]
    messages_parsed = '\n'.join(messages_parsed_dicts)
    return messages_parsed


def query(prompt):
    config = {
        "numResults": 1,
        "maxTokens": 50,
        "temperature": 0.8,
        "topKReturn": 0,
        "topP": 0.9,
        "stopSequences": [f"{st.session_state['bot_name']}:", f"{st.session_state['user_name']}:", "##"]
    }
    res = complete(model_type=st.session_state['fortune_teller_model'],
                   prompt=prompt,
                   config=config,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])
    return res


def six_lines():
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")


def add_response():
    prompt = st.session_state['fewshot'] + \
             st.session_state['background'] + \
             messages_to_string(st.session_state.messages) + \
             f"\n{st.session_state['bot_name']}:"
    output = query(prompt)
    output_text = output['completions'][0]['data']['text'].strip()
    st.session_state.messages.append({st.session_state['bot_name']: output_text})


def add_input():
    input_text = st.session_state.text_input
    st.session_state.messages.append({st.session_state['user_name']: input_text})
    add_response()
    st.session_state['text_input'] = ""


def regenerate_completion():
    st.session_state.messages.pop(-1)
    add_response()


def reset_chat():
    st.session_state['text_input'] = ""
    st.session_state['messages'] = []
    st.session_state.messages.append({st.session_state['bot_name']: st.session_state['greeting']})


def get_message_text(i):
    return list(st.session_state['messages'][i].values())[0]


def init_demo(custom_demo):
    if custom_demo in CUSTOM_CHAT_DEMOS:
        st.session_state['custom_participants'] = CUSTOM_CHAT_DEMOS[custom_demo]['participants']
        st.session_state['custom_greeting'] = CUSTOM_CHAT_DEMOS[custom_demo]['greeting']
        st.session_state['custom_background'] = CUSTOM_CHAT_DEMOS[custom_demo]['background']
        st.session_state['custom_examples'] = CUSTOM_CHAT_DEMOS[custom_demo]['examples']
    else:
        st.session_state['custom_participants'] = ['Bot', 'User']
        st.session_state['custom_greeting'] = f"Hi, I'm {st.session_state['custom_participants'][0]}"
        st.session_state['custom_background'] = "Bot is a helpful friendly chatbot"
        st.session_state['custom_examples'] = ""


if __name__ == '__main__':

    apply_studio_style()
    custom_demo = "fortune_teller"
    init_demo(custom_demo)
    st.session_state['fortune_teller_model'] = 'experimental/j1-grande-instruct'
    st.session_state['bot_name'] = st.session_state['custom_participants'][0]
    st.session_state['user_name'] = st.session_state['custom_participants'][1]
    st.session_state['fewshot'] = st.session_state['custom_examples']
    st.session_state['background'] = st.session_state['custom_background']

    st.session_state['greeting'] = st.session_state['custom_greeting']

    st.title("Conversational AI")
    st.write("We see conversational AI in your future and so does Ella, our AI fortune teller! This interactive demo illustrates how our model can be used to create a realistic conversational experience.")
    st.write("Curious to hear your fortune? Ask Ella anything and she'll consult her crystal ball 🔮")

    if 'messages' not in st.session_state:
        reset_chat()
    if 'display' not in st.session_state:
        st.session_state['display'] = {}

    st.write("--------------------------------")

    if custom_demo == "fortune_teller":
        st.session_state['user_gender'] = st.radio("Select your gender:", ('Female', 'Male', 'Other'), horizontal=True)
        st.session_state['background'] += f"User gender: {st.session_state['user_gender']}.\n\n"

    st.subheader("Chat")
    st.session_state['display'][0] = {}
    st.session_state['display'][0]["cols"] = st.empty()
    col1, col2 = st.session_state['display'][0]["cols"].columns([9, 1.5])
    with col1:
        message(get_message_text(0), is_user=True, key=str(0) + '_user', avatar_style='bottts', seed=12)
    total_messages = len(st.session_state['messages'])
    for i in range(1, total_messages, 2):
        st.session_state['display'][i] = {}
        st.session_state['display'][i]["cols"] = st.empty()
        col1, col2, col3, col4 = st.session_state['display'][i]["cols"].columns([9, 0.5, 0.5, 0.5])
        with col1:
            message(get_message_text(i), key=str(i) + '_user', avatar_style='avataaars', seed=23)
            message(get_message_text(i+1), is_user=True, key=str(i+1), avatar_style='bottts', seed=12)
        if i == total_messages-2:
            with col3:
                six_lines()
                if st.button(label="Regenerate", key=str(i) + "regen"):
                    regenerate_completion()
                    st.experimental_rerun()
    st.text_input(label="Discover what your future holds by asking Ella your questions here:", on_change=add_input, key='text_input')

    st.write("--------------------------------")
    if st.button(label="Reset conversation", on_click=reset_chat):
        st.experimental_rerun()

