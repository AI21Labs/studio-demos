import streamlit as st
from constants import DEFAULT_MODEL
from utils.completion import complete, tokenize
from utils.studio_style import apply_studio_style
import re

st.set_page_config(
    page_title="Marketing Generator",
)

max_tokens = 2048 - 200

MODEL_CONF = {
    "maxTokens": 200,
    "temperature": 0.8,
    "numResults": 16
    # "logitBias": {'<|endoftext|>': -5}
}

TOKENS_LIMITS = {
    "pitch": (20, 150),
}

WORDS_LIMIT = {
    "pitch": (150, 200),
}

title_placeholder = "PetSmart Charities® Commits $100 Million to Improve Access to Veterinary Care"
article_placeholder = """The inability of many families to access veterinary care is a pressing issue facing animal welfare nationally. To combat this, PetSmart Charities announced a commitment of $100 million over the next five years to help break down the geographic, cultural, language and financial barriers that prevent pets from receiving the veterinary care they need to thrive.  
Zora is a lovable pug whose owner knew something was wrong with her breathing, but was struggling to find a vet that would provide non-routine care at low cost. Despite the challenges of transitioning from homelessness and landing in the hospital himself, Zora’s owner found someone to take her to a free clinic offered by Ruthless Kindness, a PetSmart Charities grantee. Thanks to the care she received, Zora and her owner are now thriving together.
Veterinary access impacts the animal welfare industry and individual families in every community in the country. More than 70 percent of homes in the United States now include pets, but 50 million pets in the U.S. lack even basic veterinary care, including spay/neuter surgeries, annual exams and vaccinations. Without regular veterinary care, minor pet health issues often become bigger, costlier problems; and preventable diseases can be passed on to people and other animals. Pet parents may be forced to relinquish their beloved furry family members to already overcrowded animal shelters or be forced to watch them suffer when they can't access treatment. With pets being universally recognized as beloved family members, the challenges posed by an inability to access veterinary care can have a profound impact. 
PetSmart Charities estimates it would cost more than $20 billion annually to bridge the gap for pets in need of veterinary care at standard veterinary prices. More needs to be done to expand availability of lower-cost services, ensure access for remote and bilingual communities and ensure there are enough veterinarians able to perform a variety of services through clinics and urgent care centers. To help lead the charge, the nonprofit is taking a leadership role in marshaling partners and stakeholders to develop and execute solutions to solving the gap in veterinary care access. 
""The challenges facing the veterinary care system are vast and varied and no single organization can solve them alone,"" said Aimee Gilbreath, president of PetSmart Charities. ""Through PetSmart Charities' commitment, we plan to invest further in our partners and build new alliances to innovate solutions across the entire system — while also funding long-term solutions already in place such as low-cost vet clinics and veterinary student scholarships. We're confident this approach will produce sustainable change within the veterinary care industry. Our best friends deserve access to adequate health care like any family members."" 

Barriers to Veterinary Care
While affordability remains the most prominent barrier to veterinary care, additional challenges contribute to the current veterinary care gap, including:
Veterinary Shortage: With pet ownership steadily on the rise, a 33% increase in pet healthcare service spending is expected over the next 10 years. 90 million U.S. households now include pets, but the number of nationwide veterinarians has increased by just 2.7 percent each year since 2007. To meet the growing need for veterinary care, an additional 41,000 veterinarians would be needed by 2030. 
Veterinary Deserts and Cultural Inclusion: Within rural and underserved regions, veterinary practices are difficult to find close-by, making trips to the veterinarian costly and sometimes impossible. Additionally, as veterinarians are currently listed among the top five least diverse professions, cultural and language divides can often occur between clients and veterinarians, discouraging some pet parents from seeking care. 
Economic Challenges: The cost of veterinary care has spiked 10 percent in the last year alone and amidst the ongoing housing crisis and economic uncertainty, 63 percent of pet parents find it difficult to cover surprise vet expenses.
Regulatory Challenges: Nationwide, fragmented and varied veterinary regulations pose challenges to the development of easy, efficient and consistent solutions such as telemedicine. 
How PetSmart Charities Will Innovate Solutions
Through a $100 million commitment in funding over the next five years, PetSmart Charities will take a multifaceted approach to improve access to adequate veterinary care for all pets, including:
Funding solutions across the system of veterinary care – from investing in new and more affordable types of clinics to working directly with providers to help them overcome challenges in care delivery.
Supporting innovative solutions such as new telehealth care and delayed payment models that reduce and help manage the cost of care for pet parents.
Partnering with universities and thought leaders to research the evolving needs of pets while developing innovative, cost-effective ways to deliver care.
Awarding scholarships to veterinary students pursuing community-based practices and establishing a training program for Master's-level veterinary practitioners to offer basic care at affordable prices.
Expanding access to lower-cost veterinary care through sustainable nonprofit clinics.
Developing community-based models led by local changemakers to improve access to veterinary care to underserved communities through an emphasis on their unique challenges.
For more information on how PetSmart Charities is working to expand access to veterinary care nationwide or to help support initiatives like this for pets and their families, visit petsmartcharities.org. 

About PetSmart Charities®
PetSmart Charities is committed to making the world a better place for pets and all who love them. Through its in-store adoption program in all PetSmart® stores across the U.S. and Puerto Rico, PetSmart Charities helps up to 600,000 pets connect with loving families each year. PetSmart Charities also provides grant funding to support organizations that advocate and care for the well-being of all pets and their families. PetSmart Charities' grants and efforts connect pets with loving homes through adoption, improve access to affordable veterinary care and support families in times of crises with access to food, shelter and disaster response. Each year, millions of generous supporters help pets in need by donating to PetSmart Charities directly at PetSmartCharities.org, while shopping at PetSmart.com, and by using the PIN pads at checkout registers inside PetSmart® stores. In turn, PetSmart Charities efficiently uses more than 90 cents of every dollar donated to fulfill its role as the leading funder of animal welfare in North America, granting more than $500 million since its inception in 1994. Independent from PetSmart LLC, PetSmart Charities is a 501(c)(3) organization that has received the Four-Star Rating from Charity Navigator for the past 18 years in a row – placing it among the top one percent of rated charities. To learn more visit www.petsmartcharities.org."""


def anonymize(text):
    text = re.sub(r'https?:\/\/.*', '[URL]', text)
    return re.sub(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', '[EMAIL]', text)


def generate(prompt, category, max_retries=2):
    min_length, max_length = WORDS_LIMIT[category]
    completions_filtered = []
    try_count = 0
    MODEL_CONF['minTokens'], MODEL_CONF['maxTokens'] = TOKENS_LIMITS[category]
    while not len(completions_filtered) and try_count < max_retries:
        res = complete(model_type=DEFAULT_MODEL, prompt=prompt, **MODEL_CONF)
        completions_filtered = [comp['data']['text'] for comp in res['completions']
                                if comp["finishReason"]["reason"] == "endoftext"
                                and min_length <= len(comp['data']['text'].split()) <= max_length]
        try_count += 1
    st.session_state["completions"] = [anonymize(i) for i in completions_filtered]


def on_next():
    st.session_state['index'] = (st.session_state['index'] + 1) % len(st.session_state['completions'])


def on_prev():
    st.session_state['index'] = (st.session_state['index'] - 1) % len(st.session_state['completions'])


def toolbar():
    cols = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])
    with cols[1]:
        if st.button(label='<', key='prev'):
            on_prev()
    with cols[2]:
        st.text(f"{st.session_state['index'] + 1}/{len(st.session_state['completions'])}")
    with cols[3]:
        if st.button(label='>', key='next'):
            on_next()


if __name__ == '__main__':
    apply_studio_style()
    st.title("Marketing Generator")

    st.session_state['title'] = st.text_input(label="Title", value=title_placeholder).strip()
    st.session_state['article'] = st.text_area(label="Article", value=article_placeholder, height=500).strip()

    domain = st.radio(
        "Select domain of reporter 👉",
        options=['Technology', 'Healthcare', 'Venture Funding', 'Other'],
    )

    if domain == 'Other':
        instruction = "Write a pitch to reporters persuading them why they should write about this for their publication."
    else:
        instruction = f"Write a pitch to reporters that cover {domain} stories persuading them why they should write about this for their publication."
    suffix = "Email Introduction"
    prompt = f"{instruction}\nTitle: {st.session_state['title']}\nPress Release:\n{st.session_state['article']}\n\n{suffix}:\n"
    category = 'pitch'

    if st.button(label="Compose"):
        with st.spinner("Loading..."):
            num_tokens = len(tokenize(prompt))
            if num_tokens > max_tokens:
                st.write("Text is too long. Input is limited up to 2048 tokens. Try using a shorter text.")
                if 'completions' in st.session_state:
                    del st.session_state['completions']
            else:
                generate(prompt, category=category)
                st.session_state['index'] = 0

    if 'completions' in st.session_state:
        if len(st.session_state['completions']) == 0:
            st.write("Please try again 😔")

        else:
            curr_text = st.session_state['completions'][st.session_state['index']]
            st.subheader(f'Generated Email')
            st.text_area(label="", value=curr_text.strip(), height=400)
            st.write(f"Number of words: {len(curr_text.split())}")
            if len(st.session_state['completions']) > 1:
                toolbar()
