import asyncio
import os
import requests
import streamlit as st
from aiohttp import ClientSession

_env2base = {
    "staging": "https://api-stage.ai21.com/studio/v1",
    "production": "https://api.ai21.com/studio/v1"
}


def _full_url(env, model_type, custom_model, endpoint):
    return os.path.join(_env2base[env], model_type, custom_model or '', endpoint)


async def async_complete(model_type, prompt, config, api_key, custom_model=None, env='production', delay=0):
    async with ClientSession() as session:
        url = _full_url(env, model_type, custom_model, endpoint='complete')
        auth_header = f"Bearer {api_key}"
        res = await session.post(
            url,
            headers={"Authorization": auth_header},
            json={"prompt": prompt, **config}
        )
        res = await res.json()
        return res


async def async_tokenize(text, api_key, env='production', delay=0):
    async with ClientSession() as session:
        await asyncio.sleep(delay)
        url = _full_url(env, '', '', endpoint='tokenize')
        auth_header = f"Bearer {api_key}"
        res = await session.post(
            url,
            headers={"Authorization": auth_header},
            json={"text": text}
        )
        res = await res.json()
        return res


def complete(model_type, prompt, config, api_key, custom_model=None, env='production'):
    url = _full_url(env, model_type, custom_model, endpoint='complete')
    auth_header = f"Bearer {api_key}"
    resp = requests.post(
        url,
        headers={"Authorization": auth_header},
        json={"prompt": prompt, **config}
    )
    return resp.json()


async def req(s, prompt, num_results):
    async with ClientSession() as session:
        config = {
            "numResults": num_results,
            "maxTokens": 256,
            "temperature": 0.0,
            "topKReturn": 0,
            "topP": 1,
            "logitBias": {"<|endoftext|>": -2.5},
            "countPenalty": {
                "scale": 0,
                "applyToNumbers": False,
                "applyToPunctuations": False,
                "applyToStopwords": False,
                "applyToWhitespaces": False,
                "applyToEmojis": False
            },
            "frequencyPenalty": {
                "scale": 185,
                "applyToNumbers": False,
                "applyToPunctuations": False,
                "applyToStopwords": False,
                "applyToWhitespaces": False,
                "applyToEmojis": False
            },
            "presencePenalty": {
                "scale": 0.4,
                "applyToNumbers": False,
                "applyToPunctuations": False,
                "applyToStopwords": False,
                "applyToWhitespaces": False,
                "applyToEmojis": False
            },
            "stopSequences": ["##"]
        }

        response = complete(model_type='experimental/j1-grande-instruct',
                            prompt=prompt,
                            config=config,
                            api_key=st.secrets['api-keys']['ai21-algo-team-prod'])

        return response