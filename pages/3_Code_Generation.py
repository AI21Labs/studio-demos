import streamlit as st

from utils.completion import complete
from utils.studio_style import apply_studio_style
from constants import CODE_GENERATIONS_EXAMPLES, CODE_GENERATION_CUSTOM_PROMPT_PLACEHOLDER

preset = """Create a regular expression that extracts email addresses from strings:\nExpression: /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/gi\n\n##\n\nCreate a regular expression that validate a password contains at least 8 characters, one uppercase letter and a number:\nExpression: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$/g\n\n##\n\nCreate a regular expression that finds non-ASCII characters:\nExpression: [^\x00-\x7F]\n\n##\n\nCreate a regular expression to match HTML tags:\nExpression: /<(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>/\n\n##\n\nCreate a regular expression to validate an IP address:\nExpression: ^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$\n\n##\n\n"""
suffix = ":\nExpression:"


st.set_page_config(
    page_title="Code Generation"
)


def query(prompt):
    config = {
        "numResults": 1,
        "maxTokens": 64,
        "temperature": 0,
        "topKReturn": 0,
        "topP": 1,
        "stopSequences": ["##"]
    }
    res = complete(model_type='j1-jumbo',
                   prompt=f"{preset}{prompt}{suffix}",
                   config=config,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])
    return res["completions"][0]["data"]["text"]

def set_new_prompt():
    st.session_state["curr_prompt"] = st.session_state.prompt_select_box_key

if __name__ == '__main__':

    apply_studio_style()
    if "curr_prompt" not in st.session_state:
        st.session_state["curr_prompt"] = ""
    st.title("Regular Expression Generation")
    st.text("")
    st.text("")
    st.markdown("###### Use large-language models to transform an instruction in natural language to a regular expression (regex).")

    st.selectbox(label="Select one instruction from the drop-down menu:",
                          options=CODE_GENERATIONS_EXAMPLES, on_change=set_new_prompt, key="prompt_select_box_key").strip()

    st.session_state["prompt"] =  st.text_input(label="Type in your instruction", value=st.session_state["curr_prompt"])


    st.text("")
    if st.button(label="Generate Regex"):
        st.session_state["save_results_ind"] = []
        with st.spinner("Loading..."):
            st.session_state["result"] = {
                "completion": query(st.session_state["prompt"]),
            }
    st.text("")
    if "result" in st.session_state:
        result = st.session_state["result"]["completion"]
        st.markdown("###### Regex:")
        st.code(result)




