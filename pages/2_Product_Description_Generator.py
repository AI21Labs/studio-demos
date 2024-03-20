import streamlit as st
from constants import PRODUCT_DESCRIPTION_FEW_SHOT, DEFAULT_MODEL
from utils.studio_style import apply_studio_style
from constants import client
from ai21.models import Penalty

st.set_page_config(
    page_title="Product Description Generator",
)


def query(prompt):

    res = client.completion.create(
        model=DEFAULT_MODEL,
        prompt=prompt,
        num_results=1,
        max_tokens=240,
        temperature=1,
        top_k_return=0,
        top_p=0.98,
        count_penalty=Penalty(
            scale=0,
            apply_to_emojis=False,
            apply_to_numbers=False,
            apply_to_stopwords=False,
            apply_to_punctuation=False,
            apply_to_whitespaces=False,
        ),
        frequency_penalty=Penalty(
            scale=225,
            apply_to_emojis=False,
            apply_to_numbers=False,
            apply_to_stopwords=False,
            apply_to_punctuation=False,
            apply_to_whitespaces=False,
        ),
        presence_penalty=Penalty(
            scale=1.2,
            apply_to_emojis=False,
            apply_to_numbers=False,
            apply_to_stopwords=False,
            apply_to_punctuation=False,
            apply_to_whitespaces=False,
        )
    )

    return res.completions[0].data.text


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
