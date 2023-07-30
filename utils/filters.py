import re

CHAR_LIMIT = {
    "Twitter": (30, 280),
    "Linkedin": (100, 1500),
}

def anonymize(text):
    text = re.sub(r'https?:\/\/.*', '[URL]', text)
    return re.sub(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', '[EMAIL]', text)


def is_duplicate_prefix(input_text, output_text, th=0.7):
    input_words = input_text.strip().split()
    output_words = output_text.strip().split()
    if len(input_words) == 0 or len(output_words) == 0:
        return True
    output_prefix = output_words[:len(input_words)]
    overlap = set(output_prefix) & set(input_words)
    return len(overlap) / len(output_prefix) > th


def apply_filters(completion, prompt, media):
    min_length, max_length = CHAR_LIMIT[media]
    text = completion['data']['text']
    return completion["finishReason"]["reason"] == "endoftext" \
                       and min_length <= len(text) <= max_length \
                       and not is_duplicate_prefix(text, prompt) \
                       and "[" not in text and "]" not in text


def filter_duplicates(completions):
    results = list()
    for curr in completions:
        if not any(is_duplicate_prefix(r, curr) for r in results):
            results.append(curr)
    return results


def remove_utf_emojis(s):
    return re.sub(r'<0x([0-9A-Fa-f]+)>', "", s)