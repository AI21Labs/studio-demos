import streamlit as st

from utils.completion import complete
from utils.studio_style import apply_studio_style

preset = """Create a regular expression that extracts email addresses from strings:\nExpression: /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/gi\n\n##\n\nCreate a regular expression that validate a password contains at least 8 characters, one uppercase letter and a number:\nExpression: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$/g\n\n##\n\nCreate a regular expression that finds non-ASCII characters:\nExpression: [^\x00-\x7F]\n\n##\n\nCreate a regular expression to match HTML tags:\nExpression: /<(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>/\n\n##\n\nCreate a regular expression to validate an IP address:\nExpression: ^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$\n\n##\n\nCreate a regular expression checks if a date is entered in 'YYYY–MM–DD' format:\nExpression:"""
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
    res = complete(model_type=st.session_state['model'],
                   prompt=few_shot_prompt,
                   config=config,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])
    return res["completions"][0]["data"]["text"]



if __name__ == '__main__':

    apply_studio_style()
    st.title("Regular Expression Generation")

    st.markdown("#### Model")
    st.session_state['model'] = st.selectbox(label="Model",
                                             options=['j1-jumbo', 'experimental/j1-grande-instruct', 'j1-grande',
                                                      'j1-large'])

    st.markdown("#### Regex Few-Shot Prompt")
    few_shot_prompt = st.text_area(label="Insert your regex instruction:", placeholder="",
                          value=preset).strip()

    if st.button(label="Generate Regex"):
        st.session_state["save_results_ind"] = []
        with st.spinner("Loading..."):
            st.session_state["result"] = {
                "completion": query(preset),
            }

    if "result" in st.session_state:
        st.subheader("Completion:")
        result = st.session_state["result"]["completion"]
        st.code(result)




