import streamlit as st

from utils.completion import complete
from utils.studio_style import apply_studio_style




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

    res = complete(model_type="j1-jumbo",
                   prompt=prompt,
                   config=config,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])

    return res["completions"][0]["data"]["text"]



if __name__ == '__main__':

    apply_studio_style()
    st.title("Product Description Generation")
    st.markdown("###### Generates product description for fashion eCommerce site based on a list of features")


    product_input = st.text_input("Product", value="Talking Picture Oxford Flat")
    features = st.text_area("Features", value="- Flat shoes\n- Amazing chestnut color\n- Man made materials")


    prompt = f"Write product descriptions for fashion eCommerce site based on a list of features.\nProduct: On Every Spectrum Fit and Flare Dress\nFeatures:\n- Designed by Retrolicious\n- Stretch cotton fabric\n- Side pockets\n- Rainbow stripes print\nDescription: In a bold rainbow-striped print, made up of exceptionally vibrant hues, this outstanding skater dress from Retroliciousis on every spectrum of vintage-inspired style. Made from a stretchy cotton fabric and boasting a round neckline, a sleeveless fitted bodice, and a gathered flare skirt with handy side pockets, this adorable fit-and-flare dress is truly unique and so retro-chic.\n\n##\n\nWrite product descriptions for fashion eCommerce site based on a list of features.\nProduct: Camp Director Crossbody Bag\nFeatures:\n- Black canvas purse\n- Rainbow space print\n- Leather trim\n- Two securely-zipped compartments\nDescription: Take a bit of camp charm with you wherever you go with this black canvas purse! Adorned with a rainbow space motif print, black faux-leather trim, two securely-zipped compartments, and adjustable crossbody strap, this ModCloth-exclusive bag makes sure you command a smile wherever you wander.\n\n##\n\nWrite product descriptions for fashion eCommerce site based on a list of features.\nProduct: {product_input}\nFeatures:\n{features}\nDescription:"



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




