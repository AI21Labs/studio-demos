import requests
import streamlit as st
from aiohttp import ClientSession

API_KEY = st.secrets['api-keys']['ai21-algo-team-prod']


def obqa(context, question):
    endpoint = "https://api.ai21.com/studio/v1/experimental/open-book-qa"
    auth_header = "Bearer " + API_KEY
    res = requests.post(endpoint,
                        headers={"Authorization": auth_header},
                        json={"context": context, "question": question})
    res = res.json()
    return res["answer"]


def segment(source, sourceType):
    resp = requests.post(
        "https://api.ai21.com/studio/v1/segmentation",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "source": source,
            "sourceType": sourceType
        }
    )

    if resp.status_code != 200:
        raise Exception(f"Segmentation request failed with status {resp.status_code}")

    segments = [x['segmentText'] for x in resp.json()['segments'] if x["segmentType"] in ["normal_text", "normal_text_short"]]
    return segments


async def paraphrase_req(sentence, tone):
    async with ClientSession() as session:
        res = await session.post(
            "https://api.ai21.com/studio/v1/experimental/rewrite",
            headers={f"Authorization": f"Bearer {st.secrets['api-keys']['ai21-algo-team-prod']}"},
            json={
                "text": sentence,
                "intent": tone.lower(),
                "spanStart": 0,
                "spanEnd": len(sentence)
            }
        )
        res = await res.json()
        return res
