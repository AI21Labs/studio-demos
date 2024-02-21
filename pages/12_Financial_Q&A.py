import streamlit as st
from utils.studio_style import apply_studio_style
import requests
import time

api_key = st.secrets['api-keys']['ai21-stage-api-key']

st.set_page_config(
    page_title="Answers",
)


PH_Q = "What is Microsoft's revenue in Q1?"

COMPANY_TICKER_DICT = {"microsoft":"MSFT",
                       "apple":"AAPL",
                       "netflix":"NFLX",
                       "google":"GOOG",
                       "alphabet":"GOOG",
                       "amazon":"AMZN",
                       "meta":"META",
                       "tesla":"TSLA",
                       "nvidia":"NVDA"}

PERIOD_TYPES = ['annual', 'quarterly']

sec_label = "p72-sec-txt"


def get_ai21_answers(question,
                     model_url,
                     context=None,
                     mode="flexible",
                     labels=None,
                     ticker = None,
                     year = None,
                     period_type = None,
                     path=None,
                     api_key=api_key,
                     retrival_similarity_threshold=0.8,
                     retrival_strategy="default",
                     top_k=None):
    """
    Get AI21 answers for a given question using CA model.

    Args:
        question (str): The question to be answered.
        model_url (str): The URL of the AI model to use.
        context (str, optional): The context for the question (default: None).
        mode (str, optional): The mode for answering the question (default: "flexible").
        labels (list, optional): The labels to use for filtering the answers (default: None).
        path (str, optional): The path to the file containing additional information (default: None).
        api_key (str, optional): The API key for authentication (default: ai21.api_key).
        retrival_similarity_threshold (float, optional): The similarity threshold for retrieval (default: 0.8).
        retrival_strategy (str, optional): The retrieval strategy to use (default: "defualt").
        top_k (int, optional): The maximum number of segments to retrive (default: None).

    Returns:
        dict: The response containing the AI21 answers.

    """
    url = model_url
    curr_labels = labels+[ticker]
    if year > 0:
        year_label  = str(int(year))
        curr_labels.append(year_label)
    if period_type in PERIOD_TYPES:
        curr_labels.append(period_type)

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "question": question,
        "mode": mode,
        "labels": curr_labels,
        "path": path,
        "retrievalSimilarityThreshold": retrival_similarity_threshold,
        "retrievalStrategy": retrival_strategy,
        "top_k": top_k
    }
    try:
        time.sleep(3)
        response = requests.post(url, headers=headers, json=payload).json()
        return response
    except:
        # res = ai21.Library.Answer.execute(question=prompt)
        print(f"ERROR - Method: {path}\n Failed Q: {question}\n")
        return None


if __name__ == '__main__':

    apply_studio_style()
    st.title("Financial Q&A")

    st.write("Ask a question on top of SEC financial documents.")

    question = st.text_input(label="Question:", value=PH_Q)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        ticker = st.selectbox(label='Ticker', options=list(COMPANY_TICKER_DICT.values()))
    with col2:
        year = st.selectbox(label="Year", options=[2019,2020,2021,2022,2023])
    with col3:
        period_type = st.selectbox(label='Period Type', options=['Annual', 'Quarterly']).lower()

    if st.button(label="Answer"):
        with st.spinner("Loading..."):
            response = get_ai21_answers(question=question,
                                                labels=["p72-sec-txt"],
                                                api_key=api_key,
                                                model_url="https://api-stage.ai21.com/studio/v1/library/answer",
                                                ticker = ticker,
                                                year = year,
                                                period_type = period_type,
                                                retrival_similarity_threshold = 0.78,
                                                retrival_strategy = 'default',
                                                top_k = None)

            st.session_state["answer"] = response['answer']

    if "answer" in st.session_state:
        st.write(st.session_state['answer'])
