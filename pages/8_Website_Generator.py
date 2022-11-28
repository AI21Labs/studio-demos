import streamlit as st
from constants import WEBSITE_DESCRIPTION_FEW_SHOT, WEBSITE_HEADLINE_FEW_SHOT
from utils.completion import complete
from utils.studio_style import apply_studio_style

st.set_page_config(
    page_title="Website Generator",
)


def query(prompt, stopSequences=["##"]):
    config = {
        "numResults": 1,
        "maxTokens": 240,
        "temperature": 0.7,
        "topKReturn": 0,
        "topP":0.98,
        "countPenalty": {
            "scale": 0.4,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
      "stopSequences":stopSequences
    }

    res = complete(model_type="j1-jumbo",
                   prompt=prompt,
                   config=config,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])

    return res["completions"][0]["data"]["text"]


if __name__ == '__main__':

    apply_studio_style()
    st.title("Website Generator")
    st.markdown("###### Create valuable marketing copy for your business page that describes your business and its benefits within seconds! Simply give a few details about your business, and let our tool work its magic.")

    business_name = st.text_input("Enter your business' name:", value="Home Painters")
    location = st.text_input("Enter your business' location:", value="Memphis, Tennessee")
    services = st.text_area("List your business services here:", value="- Interior & Exterior Painting\n- Staining\n- Removal, Cleanup, Retexture, Repainting")
    highlights = st.text_area("Do you want to highlight some benefits of your business?", value="- Over 15 years of experience\n- 5 years guarantee")

    prompt = WEBSITE_DESCRIPTION_FEW_SHOT + f"Name of Business: {business_name}\nLocation: {location}\nServices:\n{services}\n\nImportant Company Highlights:\n{highlights}\n\nDescription:\n"

    if st.button(label="Generate Website Description"):
        st.session_state["short-form-save_results_ind"] = []
        with st.spinner("Loading..."):
            st.session_state["short-form-result"] = {
                "completion": query(prompt).strip(),
            }
            result = st.session_state["short-form-result"]["completion"]
            headline_prompt = WEBSITE_HEADLINE_FEW_SHOT + f'Name of Business: {business_name}\n\nDescription:\n{result}\n\nHeadline:\n'
            st.session_state["headline"] = {
                "completion": query(headline_prompt, stopSequences=['\n']),
            }

    if "short-form-result" in st.session_state:
        if "headline" in st.session_state:
            st.text_input("Generated Headline", st.session_state['headline']['completion'])
        else:
            st.text("")
        st.text_area("Generated Website Description", st.session_state["short-form-result"]["completion"], height=200)

