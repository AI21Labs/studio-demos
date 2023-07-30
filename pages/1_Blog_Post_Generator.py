import streamlit as st
import numpy as np
import asyncio
from constants import DEFAULT_MODEL
from utils.studio_style import apply_studio_style
import argparse
from utils.completion import complete, async_complete
from utils.completion import paraphrase_req

st.set_page_config(
    page_title="Blog Post Generator",
)


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


def build_prompt(title, sections, section_heading):
    sections_text = '\n'.join(sections)
    prompt = f"Write a descriptive section in a blog post according to the following details.\n\nBlog Title:\n{title}\n\nBlog Sections:\n{sections_text}\n\nCurrent Section Heading:\n{section_heading}\n\nCurrent Section Text:\n"
    return prompt

def generate_sections_content(num_results, sections, title):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    config = {
        "numResults": num_results,
        "maxTokens": 256,
        "minTokens": 10,
        "temperature": 0.7,
        "topKReturn": 0,
        "topP": 1,
        "stopSequences": []
    }
    group = asyncio.gather(*[async_complete(DEFAULT_MODEL, build_prompt(title, sections, s), config) for s in sections])
    results = loop.run_until_complete(group)
    loop.close()
    return results

def build_generate_outline(title):
    return lambda: generate_outline(title)


def generate_outline(title):
    st.session_state['show_outline'] = True
    st.session_state['show_sections'] = False

    res = _generate_outline(title)

    st.session_state["outline"] = res["completions"][0]["data"]["text"].strip()


def _generate_outline(title):
    prompt = f"Write sections to a great blog post for the following title.\nBlog title: How to start a personal blog \nBlog sections:\n1. Pick a personal blog template\n2. Develop your brand\n3. Choose a hosting plan and domain name\n4. Create a content calendar \n5. Optimize your content for SEO\n6. Build an email list\n7. Get the word out\n\n##\n\nWrite sections to a great blog post for the following title.\nBlog title: A real-world example on Improving JavaScript performance\nBlog sections:\n1. Why I needed to Improve my JavaScript performance\n2. Three common ways to find performance issues in Javascript\n3. How I found the JavaScript performance issue using console.time\n4. How does lodash cloneDeep work?\n5. What is the alternative to lodash cloneDeep?\n6. Conclusion\n\n##\n\nWrite sections to a great blog post for the following title.\nBlog title: Is a Happy Life Different from a Meaningful One?\nBlog sections:\n1. Five differences between a happy life and a meaningful one\n2. What is happiness, anyway?\n3. Is the happiness without pleasure?\n4. Can you have it all?\n\n##\n\nWrite sections to a great blog post for the following title.\nBlog title: {title}\nBlog Sections:\n"
    config = {
        "numResults": 1,
        "maxTokens": 296,
        "temperature": 0.84,
        "topKReturn": 0,
        "topP": 1,
        "stopSequences": ["##"]
    }
    res = complete(model_type=DEFAULT_MODEL,
                   prompt=prompt,
                   **config)
    return res


def generate_sections():
    st.session_state['show_sections'] = True


def build_on_next_click(section_heading, section_index, completions, arg_sorted_by_length):
    return lambda: on_next_click(section_heading, section_index, completions, arg_sorted_by_length)


def on_next_click(section_heading, section_index, completions, arg_sorted_by_length):
    st.session_state['show_paraphrase'][section_heading] = False
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
    st.session_state['show_paraphrase'][section_heading] = False

    new_comp_index = (st.session_state['generated_sections_data'][section_heading]["text_area_index"] - 1) % 5
    section_i_text = completions[arg_sorted_by_length[new_comp_index]]["data"]["text"]
    st.session_state['generated_sections_data'][section_heading]["text_area_index"] = new_comp_index
    st.session_state['generated_sections_data'][section_heading]["text_area_data"].text_area(label=section_heading,
                                                                                             height=300,
                                                                                             value=section_i_text,
                                                                                             key=section_index)


def get_event_loop(title, sections, num_results):
    st.session_state['show_sections'] = True



    for s in sections:
        st.session_state['generated_sections_data'][s] = {}
        st.session_state['show_paraphrase'][s] = False

    # perform request, actually generate sections
    results = generate_sections_content(num_results, sections, title)

    # moved these lines here to detach st code from logic
    for i, s in enumerate(sections):
        response_json = results[i]
        section_completions = response_json["completions"]  # gets the generated candidates of the current completion
        st.session_state['generated_sections_data'][s]["completions"] = section_completions

    # rank/filter
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

        st.session_state['generated_sections_data'][s]["rewrites"] = ["" for c in range(len(section_completions))]


def build_event_loop(title, section_heading, num_results):
    return lambda: get_event_loop(title, section_heading, num_results)


def build_event_loop_one_section(title, section, num_results):
    return lambda: get_event_loop(title, [section], num_results)


def on_outline_change():
    st.session_state['show_sections'] = False


def paraphrase(text, tone, times):
    len_text = len(text)
    entire_text = text
    for i in range(times):
        if len_text > 500:
            sentences = text.split(".")
        else:
            sentences = [text]

        filtered_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            len_sent = len(sentence)
            if len_sent > 1:
                filtered_sentences.append(sentence)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        group = asyncio.gather(*[paraphrase_req(sentence, tone) for sentence in filtered_sentences])

        results = loop.run_until_complete(group)
        loop.close()

        final_text = []
        for r in results:
            sugg = r["suggestions"][0]["text"]
            final_text.append(sugg)

        entire_text = ". ".join(final_text)
        entire_text = (entire_text + ".").replace(",.", ".").replace("?.", ".").replace("..", ".")

        text = entire_text
        len_text = len(entire_text)

    return entire_text

def on_paraphrase_click(s, tone, times):

    all_sections_data = st.session_state['generated_sections_data']

    index = st.session_state['generated_sections_data'][s]["text_area_index"]
    section_completions = all_sections_data[s]["completions"]

    sec_text = section_completions[index]["data"]["text"]
    paraphrased_section = paraphrase(sec_text, tone, times)



    st.session_state['generated_sections_data'][s]["rewrites"][index] = paraphrased_section
    st.session_state['show_paraphrase'][s] = True

def build_paraphrase(s, tone, times):
    return lambda: on_paraphrase_click(s, tone, times)


def on_heading_change():
    st.session_state['show_sections'] = False


def on_title_change():
    st.session_state['show_sections'] = False


if __name__ == '__main__':
    args = get_args()
    apply_studio_style()
    num_results = args.num_results

    # Initialization
    if 'show_outline' not in st.session_state:
        st.session_state['show_outline'] = False

    if 'show_sections' not in st.session_state:
        st.session_state['show_sections'] = False

    if 'show_paraphrase' not in st.session_state:
        st.session_state['show_paraphrase'] = {}

    if 'generated_sections_data' not in st.session_state:
        st.session_state['generated_sections_data'] = {}

    st.title("Blog Post Generator")
    st.markdown("Using only a title, you can instantly generate an entire article with the click of a button! Simply select your topic and this tool will create an engaging article from beginning to end.")
    st.markdown("#### Blog Title")
    title = st.text_input(label="Write the title of your article here:", placeholder="",
                          value="5 Strategies to overcome writer's block").strip()
    st.markdown("#### Blog Outline")
    st.text("Click the button to generate the blog outline")
    st.button(label="Generate Outline", on_click=build_generate_outline(title))

    sections = []
    if st.session_state['show_outline']:
        text_area_outline = st.text_area(label="", height=250, value=st.session_state["outline"],
                                         on_change=on_outline_change)
        sections = text_area_outline.split("\n")
        st.text("Unsatisfied with the generated outline? Click the 'Generate Outline' button again to re-generate it, or edit it inline.")

        st.markdown("#### Blog Sections")
        st.text("Click the button to effortlessly generate an outline for your blog post:")
        st.button(label="Generate Sections", on_click=build_event_loop(title, sections, num_results))

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

            section_text_area_value = st.session_state['generated_sections_data'][s]["rewrites"][index] if st.session_state['show_paraphrase'][s] == True else  section_completions[
                                                                                                            index]["data"]["text"]
            section_i_text = st.session_state['generated_sections_data'][s]["text_area_data"].text_area(label=s,
                                                                                                        height=300,
                                                                                                        value=section_text_area_value,
                                                                                                        key="generated-section"+s)
            st.session_state['generated_sections_data'][s]["completions"][index]["data"]["text"] = section_i_text
            col1, col2, col3, col4, col5, col6 = st.session_state['generated_sections_data'][s]["cols"].columns(
                [0.2, 0.2, 0.06, 0.047, 0.05, 0.4])

            with col1:
                st.button("Generate Again", on_click=build_event_loop_one_section(title, s, num_results),
                          key="generate-again-" + s)

            with col2:
                st.button("Paraphrase", on_click=build_paraphrase(s, tone="general", times=1),
                          key="paraphrase-button-" + s)


            with col3:
                st.button("<", on_click=build_on_prev_click(s, i, section_completions, arg_sort), key="<" + s)


            with col4:
                st.text(f"{index+1}/{num_results}")

            with col5:
                st.button(">", on_click=build_on_next_click(s, i, section_completions, arg_sort), key=">" + s)

