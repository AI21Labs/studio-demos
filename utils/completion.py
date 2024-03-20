import asyncio
from aiohttp import ClientSession
from constants import client
import streamlit as st

api_key = st.secrets['api-keys']['ai21-api-key']

endpoint = lambda model_type: f"https://api.ai21.com/studio/v1/{model_type}/complete"


async def async_complete(model_type, prompt, config, delay=0):
    async with ClientSession() as session:
        await asyncio.sleep(delay)
        auth_header = f"Bearer {api_key}"
        res = await session.post(
            endpoint(model_type),
            headers={"Authorization": auth_header},
            json={"prompt": prompt, **config}
        )
        res = await res.json()
        return res


def tokenize(text):
    res = client.count_tokens(text)
    return res


async def paraphrase_req(sentence, tone):
    async with ClientSession() as session:
        res = await session.post(
            "https://api.ai21.com/studio/v1/paraphrase",
            headers={f"Authorization": f"Bearer {st.secrets['api-keys']['ai21-api-key']}"},
            json={
                "text": sentence,
                "intent": tone.lower(),
                "spanStart": 0,
                "spanEnd": len(sentence)
            }
        )
        res = await res.json()
        return res
