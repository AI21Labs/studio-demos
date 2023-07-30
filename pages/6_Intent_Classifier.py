import asyncio
import math
import streamlit as st
from constants import DEFAULT_MODEL
from utils.completion import async_complete, tokenize
import re


OTHER_THRESHOLD = 0.2

st.set_page_config(
    page_title="Intent Classifier",
)


def generate_response(prompt, delay):
    config = {"maxTokens": 0, "temperature": 1}
    res = async_complete(model_type=DEFAULT_MODEL,
                         prompt=prompt,
                         config=config, delay=delay)
    return res


def batch_responses(prompts, delay=0.25):
    delay = delay if len(prompts) >= 5 else 0 # may deal with less than 5 requests in 1 second
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    group = asyncio.gather(*[generate_response(p, i*delay) for i, p in enumerate(prompts)])
    results = loop.run_until_complete(group)
    loop.close()
    return results


if __name__ == "__main__":
    st.title("Text Classifier")
    instruction = "Classify the following question into one of the following classes:"
    st.write(instruction)

    st.session_state['classes'] = st.text_area(label='Classes', value="Parking\nFood/Restaurants\nRoom Facilities\nSpa\nTransport", height=180)
    st.session_state['classes'] = re.sub('\n+', '\n', st.session_state['classes'])

    st.session_state['question'] = st.text_input(label="Question", value="How to get from the airport?")

    if st.button('Classify'):
        prompt = f"{instruction}\n{st.session_state['classes']}\n\nQuestion:\n{st.session_state['question']}\n\nClass:\n"
        num_tokens = len(tokenize(prompt))
        responses = batch_responses([prompt + c for c in st.session_state['classes'].split('\n')])
        results = {}
        for i, r in enumerate(responses):
            token_list = [t['generatedToken'] for t in r['prompt']['tokens'][num_tokens:] if t['generatedToken']['token'] != '<|newline|>']
            class_name = ''.join([t['token'] for t in token_list]).replace('▁', ' ')
            sum_logprobs = sum([t['logprob'] for t in token_list])
            results[class_name] = round(math.exp(sum_logprobs), 2)

        results['Other'] = 1 - sum(results.values())

        sorted_results = {k: v for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True)}
        for name, prob in sorted_results.items():
            st.write(name, round(prob, 2))

