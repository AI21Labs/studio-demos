import asyncio
from aiohttp import ClientSession
from constants import ai21
import streamlit as st

api_key = st.secrets['api-keys']['ai21-algo-team-prod']

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
    res = ai21.Tokenization.execute(text=text)
    return [i['token'] for i in res['tokens']]


def complete(model_type, prompt, **config):
    return ai21.Completion.execute(model=model_type, prompt=prompt, **config)


async def paraphrase_req(sentence, tone):
    async with ClientSession() as session:
        res = await session.post(
            "https://api.ai21.com/studio/v1/paraphrase",
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
