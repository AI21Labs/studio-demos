import requests
import streamlit as st
from constants import ai21

API_KEY = st.secrets['api-keys']['ai21-algo-team-prod']


def answer(context, question):
    endpoint = "https://api.ai21.com/studio/v1/experimental/answer"
    auth_header = "Bearer " + API_KEY
    res = requests.post(endpoint,
                        headers={"Authorization": auth_header},
                        json={"context": context, "question": question})
    res = res.json()
    return res["answer"]


def segment(source, sourceType):
    resp = ai21.Segmentation.execute(source=source, sourceType=sourceType)
    segments = [x['segmentText'] for x in resp.json()['segments'] if x["segmentType"] in ["normal_text", "normal_text_short"]]
    return segments
