import streamlit as st
from constants import PRODUCT_DESCRIPTION_FEW_SHOT, DEFAULT_MODEL
from utils.completion import complete
from utils.studio_style import apply_studio_style

st.set_page_config(
    page_title="Product Description Generator",
)


def query(prompt):
    config = {
        "numResults": 1,
        "maxTokens": 240,
        "temperature": 1,
        "topKReturn": 0,
        "topP":0.98,
        "countPenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "frequencyPenalty": {
            "scale": 225,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "presencePenalty": {
            "scale": 1.2,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
      },
      "stopSequences":["##"]
    }

    res = complete(model_type=DEFAULT_MODEL,
                   prompt=prompt,
                   **config)

    return res["completions"][0]["data"]["text"]


if __name__ == '__main__':

    apply_studio_style()
    st.title("Product Description Generator")
    st.markdown("###### Create valuable marketing copy for product pages that describes your product and its benefits within seconds! Simply choose a fashion accessory, a few key features, and let our tool work its magic.")


    product_input = st.text_input("Enter the name of your product:", value="Talking Picture Oxford Flat")
    features = st.text_area("List your product features here:", value="- Flat shoes\n- Amazing chestnut color\n- Man made materials")

    prompt = PRODUCT_DESCRIPTION_FEW_SHOT + f"Product: {product_input}\nFeatures:\n{features}\nDescription:"

    if st.button(label="Generate Description"):
        st.session_state["short-form-save_results_ind"] = []
        with st.spinner("Loading..."):
            st.session_state["short-form-result"] = {
                "completion": query(prompt),
            }

    if "short-form-result" in st.session_state:
        result = st.session_state["short-form-result"]["completion"]
        st.text("")
        st.text_area("Generated Product Description", result, height=200)




