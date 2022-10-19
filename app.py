import streamlit as st
import numpy as np
import asyncio
from aiohttp import ClientSession
from utils.studio_style import apply_studio_style

import argparse
from utils.completion import complete

from utils.install_ai21_package import install_ai21_package_if_needed
install_ai21_package_if_needed(package_name="studio_chatbot", repo_ssh_url="git+ssh://git@bitbucket.org/ai21labs/studio-chatbot.git")

from studio_chatbot.constants import VOCAB_PATH

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        type=int,
                        default=8888)

    parser.add_argument('--num_results',
                        type=int,
                        default=5)

    args = parser.parse_args()
    return args


def build_generate_outline(title):
    return lambda: generate_outline(title)


def generate_outline(title):
    st.session_state['show_outline'] = True
    st.session_state['show_sections'] = False

    prompt = f"Write sections to a great blog post for the following title.\nBlog title: How to start a personal blog \nBlog sections:\n1. Pick a personal blog template\n2. Develop your brand\n3. Choose a hosting plan and domain name\n4. Create a content calendar \n5. Optimize your content for SEO\n6. Build an email list\n7. Get the word out\n\n##\n\nWrite sections to a great blog post for the following title.\nBlog title: A real-world example on Improving JavaScript performance\nBlog sections:\n1. Why I needed to Improve my JavaScript performance\n2. Three common ways to find performance issues in Javascript\n3. How I found the JavaScript performance issue using console.time\n4. How does lodash cloneDeep work?\n5. What is the alternative to lodash cloneDeep?\n6. Conclusion\n\n##\n\nWrite sections to a great blog post for the following title.\nBlog title: Is a Happy Life Different from a Meaningful One?\nBlog sections:\n1. Five differences between a happy life and a meaningful one\n2. What is happiness, anyway?\n3. Is the happiness without pleasure?\n4. Can you have it all?\n\n##\n\nWrite sections to a great blog post for the following title.\nBlog title: {title}\nBlog Sections:\n"
    config = {
        "numResults": 1,
        "maxTokens": 296,
        "temperature": 0.84,
        "topKReturn": 0,
        "topP": 1,
        "stopSequences": ["##"]
    }
    res = complete(model_type='j1-jumbo',
                   prompt=prompt,
                   config=config,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])

    st.session_state["outline"] = res["completions"][0]["data"]["text"].strip()


def generate_sections():
    st.session_state['show_sections'] = True


def build_on_next_click(section_heading, section_index, completions, arg_sorted_by_length):
    return lambda: on_next_click(section_heading, section_index, completions, arg_sorted_by_length)


def on_next_click(section_heading, section_index, completions, arg_sorted_by_length):
    new_comp_index = (st.session_state['generated_sections_data'][section_heading]["text_area_index"] + 1) % 5
    section_i_text = completions[arg_sorted_by_length[new_comp_index]]["data"]["text"]
    st.session_state['generated_sections_data'][section_heading]["text_area_index"] = new_comp_index
    st.session_state['generated_sections_data'][section_heading]["text_area_data"].text_area(label=section_heading,
                                                                                             height=300,
                                                                                             value=section_i_text,
                                                                                             key=section_index)


def build_on_prev_click(section_heading, section_index, completions, arg_sorted_by_length):
    return lambda: on_prev_click(section_heading, section_index, completions, arg_sorted_by_length)


def on_prev_click(section_heading, section_index, completions, arg_sorted_by_length):
    new_comp_index = (st.session_state['generated_sections_data'][section_heading]["text_area_index"] - 1) % 5
    section_i_text = completions[arg_sorted_by_length[new_comp_index]]["data"]["text"]
    st.session_state['generated_sections_data'][section_heading]["text_area_index"] = new_comp_index
    st.session_state['generated_sections_data'][section_heading]["text_area_data"].text_area(label=section_heading,
                                                                                             height=300,
                                                                                             value=section_i_text,
                                                                                             key=section_index)


async def req(s, prompt, num_results):
    async with ClientSession() as session:
        prompt = prompt + s + "\n\nCurrent Section Text:\n"
        config = {
            "numResults": num_results,
            "maxTokens": 256,
            "minTokens": 10,
            "temperature": 0.7,
            "topKReturn": 0,
            "topP": 1,
            "stopSequences": []
        }
        response = complete(model_type='j1-grande',
                            custom_model='long-form-70-0005-40-epochs',
                            prompt=prompt,
                            config=config,
                            api_key=st.secrets['api-keys']['ai21-algo-team-prod'])

        return response


def get_event_loop(sections, prompt, num_results):
    st.session_state['show_sections'] = True

    for s in sections:
        st.session_state['generated_sections_data'][s] = {}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    group = asyncio.gather(*[req(s, prompt, num_results) for s in sections])

    results = loop.run_until_complete(group)
    loop.close()

    for i, s in enumerate(sections):
        response_json = results[i]
        section_completions = response_json["completions"]
        st.session_state['generated_sections_data'][s]["completions"] = section_completions

        lengths = []
        for c in range(len(section_completions)):
            l = len(section_completions[c]["data"]["text"])
            lengths.append(l)

        arg_sort = np.argsort(lengths)
        index = 2
        st.session_state['generated_sections_data'][s]["text_area_index"] = index
        st.session_state['generated_sections_data'][s]["arg_sort"] = arg_sort


def build_event_loop(sections, prompt, num_results):
    return lambda: get_event_loop(sections, prompt, num_results)


def build_event_loop_one_section(section, prompt, num_results):
    return lambda: get_event_loop([section], prompt, num_results)


def on_outline_change():
    st.session_state['show_sections'] = False


if __name__ == '__main__':

    apply_studio_style()

    args = get_args()
    num_results = args.num_results

    # Initialization
    if 'show_outline' not in st.session_state:
        st.session_state['show_outline'] = False

    if 'show_sections' not in st.session_state:
        st.session_state['show_sections'] = False

    if 'generated_sections_data' not in st.session_state:
        st.session_state['generated_sections_data'] = {}

    st.title("Generate a Blog Post")
    st.text(f"VOCAB_PATH={VOCAB_PATH}")
    st.markdown("#### Blog Title")
    title = st.text_input(label="Write your blog post title", placeholder="",
                          value="5 Strategies to overcome writer's block").strip()
    st.markdown("#### Blog Outline")
    st.button(label="Generate Outline", on_click=build_generate_outline(title))

    if st.session_state['show_outline']:
        text_area_outline = st.text_area(label="", height=250, value=st.session_state["outline"],
                                         on_change=on_outline_change)
        sections = text_area_outline.split("\n")
        prompt = f"Write a descriptive section in a blog post according to the following details.\n\nBlog Title:\n{title}\n\nBlog Sections:\n{text_area_outline}\n\nCurrent Section Heading:\n"

        st.markdown("#### Blog Sections")
        st.button(label="Generate Sections", on_click=build_event_loop(sections, prompt, num_results))

        if st.session_state['show_sections']:
            st.markdown(f"**{title}**")
            for s in sections:
                st.session_state['generated_sections_data'][s]["text_area_data"] = st.empty()
                st.session_state['generated_sections_data'][s]["cols"] = st.empty()

            all_sections_data = st.session_state['generated_sections_data']
            for i, s in enumerate(st.session_state['generated_sections_data'].keys()):
                index = st.session_state['generated_sections_data'][s]["text_area_index"]
                section_completions = all_sections_data[s]["completions"]
                arg_sort = st.session_state['generated_sections_data'][s]["arg_sort"]

                section_i_text = section_completions[index]["data"]["text"]

                st.session_state['generated_sections_data'][s]["text_area_data"].text_area(label=s, height=300,
                                                                                           value=section_i_text, key=s)
                col1, col2, col3, col4 = st.session_state['generated_sections_data'][s]["cols"].columns(
                    [0.5, 0.5, 4, 4])

                with col1:
                    st.button("<", on_click=build_on_prev_click(s, i, section_completions, arg_sort), key=f"<{str(i)}")
                with col2:
                    st.button(">", on_click=build_on_next_click(s, i, section_completions, arg_sort), key=f">{str(i)}")
                with col3:
                    st.button("Generate Again", on_click=build_event_loop_one_section(s, prompt, num_results), key=f"again-{str(i)}")
