import ai21
import streamlit as st

ai21.api_key = st.secrets['api-keys']['ai21-algo-team-prod']

DEFAULT_MODEL = 'j2-ultra'

SUMMARIZATION_URL = "https://www.ai21.com/blog/announcing-ai21-studio-and-jurassic-1"
SUMMARIZATION_TEXT = '''Perhaps no other crisis in modern history has had as great an impact on daily human existence as COVID-19. And none has forced businesses throughout the world to accelerate their evolution as their leaders worked to respond and recover on the way to thriving in the postpandemic environment.

Deloitte Private’s latest global survey of private enterprises reveals that executives in every region used the crisis as a catalyst, accelerating change in virtually all aspects of how we work and live. They stepped up their digital transformation through greater technology investment and deployment. In-progress initiatives were pushed toward completion, while those that were on the drawing board came to life. They sought out new partnerships and alliances. They pursued new opportunities to strengthen their supply networks and grow markets. They increased efforts to understand their purpose beyond profits, seeking new ways to grow sustainably and strengthen trust with their employees, customers, and other key stakeholders. They also embraced new possibilities in how and where work gets done.
'''

CLASSIFICATION_FEWSHOT="""Classify the following news article into one of the following topics:
1. World
2. Sports
3. Business
4. Science and Technology
Title:
Astronomers Observe Collision of Galaxies, Formation of Larger
Summary:
An international team of astronomers has obtained the clearest images yet of the merger of two distant clusters of galaxies, calling it one of the most powerful cosmic events ever witnessed.
The topic of this article is:
Science and Technology

===

Classify the following news article into one of the following topics:
1. World
2. Sports
3. Business
4. Science and Technology
Title:
Bomb Explodes Near U.S. Military Convoy (AP)
Summary:
AP - A car bomb exploded early Sunday near a U.S. military convoy on the road leading to Baghdad's airport, Iraqi police said, and a witness said two Humvees were destroyed.
The topic of this article is:
World

===

Classify the following news article into one of the following topics:
1. World
2. Sports
3. Business
4. Science and Technology
Title:
Maradona goes to Cuba
Summary:
The former Argentine football star, Diego Armando Maradona, traveled on Monday to Cuba to continue his treatment against his addiction to drugs.
The topic of this article is:
Sports

===

Classify the following news article into one of the following topics:
1. World
2. Sports
3. Business
4. Science and Technology
Title:
Duke earnings jump in third quarter
Summary:
Duke Energy Corp. reports third-quarter net income of  $389 million, or 41 cents per diluted share, sharply above earnings of  $49 million, or 5 cents per diluted share, in the same period last year.
The topic of this article is:
Business

===

"""

CLASSIFICATION_PROMPT="""Classify the following news article into one of the following topics:
1. World
2. Sports
3. Business
4. Science and Technology"""

CLASSIFICATION_TITLE = "D.C. Unveils Stadium Plan"

CLASSIFICATION_DESCRIPTION = "Rumors spread that Major League Baseball is edging closer to moving the Expos to Washington as D.C. officials announce plans for a stadium on the Anacostia waterfront."

PRODUCT_DESCRIPTION_FEW_SHOT = '''Write product descriptions for fashion eCommerce site based on a list of features.
Product: On Every Spectrum Fit and Flare Dress
Features:
- Designed by Retrolicious
- Stretch cotton fabric
- Side pockets
- Rainbow stripes print
Description: In a bold rainbow-striped print, made up of exceptionally vibrant hues, this outstanding skater dress from Retroliciousis on every spectrum of vintage-inspired style. Made from a stretchy cotton fabric and boasting a round neckline, a sleeveless fitted bodice, and a gathered flare skirt with handy side pockets, this adorable fit-and-flare dress is truly unique and so retro-chic.

##

Write product descriptions for fashion eCommerce site based on a list of features.
Product: Camp Director Crossbody Bag
Features:
- Black canvas purse
- Rainbow space print
- Leather trim
- Two securely-zipped compartments
Description: Take a bit of camp charm with you wherever you go with this black canvas purse! Adorned with a rainbow space motif print, black faux-leather trim, two securely-zipped compartments, and adjustable crossbody strap, this ModCloth-exclusive bag makes sure you command a smile wherever you wander.

##

Write product descriptions for fashion eCommerce site based on a list of features.'''

OBQA_CONTEXT = """Large Language Models
Introduction to the core of our product

Natural language processing (NLP) has seen rapid growth in the last few years since large language models (LLMs) were introduced. Those huge models are based on the Transformers architecture, which allowed for the training of much larger and more powerful language models.
We divide LLMs into two main categories, Autoregressive and Masked LM (language model). In this page we will focus on Autoregressive LLMs, as our language models, Jurassic-1 series, belongs to this category.

⚡ The task: predict the next word
Autoregressive LLM is a neural network model composed from billions of parameters. It was trained on a massive amount of texts with one goal: to predict the next word, based on the given text. By repeating this action several times, every time adding the prediction word to the provided text, you will end up with a complete text (e.g. full sentences, paragraphs, articles, books, and more). In terms of terminology, the textual output (the complete text) is called a completion while the input (the given, original text) is called prompt.

🎓 Added value: knowledge acquisition
Imagine you had to read all of Shakespeare's works repeatedly to learn a language. Eventually, you would be able to not only memorize all of his plays and poems, but also imitate his writing style.
In similar fashion, we trained the LLMs by supplying them with many textual sources. This enabled them to gain an in-depth understanding of English as well as general knowledge.

🗣️ Interacting with Large Language Models
The LLMs are queried using natural language, also known as prompt engineering. 
Rather than writing lines of code and loading a model, you write a natural language prompt and pass it to the model as the input.

⚙️ Resource-intensive
Data, computation, and engineering resources are required for training and deploying large language models. LLMs, such as our Jurassic-1 models, play an important role here, providing access to this type of technology to academic researchers and developers.

Tokenizer & Tokenization

Now that you know what large language models are, you must be wondering: “How does a neural network use text as input and output?”.

The answer is: Tokenization 🧩
Any language can be broken down into basic pieces (in our case, tokens). Each of those pieces is translated into its own vector representation, which is eventually fed into the model. For example:
Each model has its own dictionary of tokens, which determines the language it "speaks". Each text in the input will be decomposed into these tokens, and every text generated by the model will be composed of them.
But how do we break down a language? Which pieces are we choosing as our tokens? There are several approaches to solve this:

🔡 Character-level tokenization
As a simple solution, each character can be treated as its own token. By doing so, we can represent the entire English language with just 26 characters (okay, double it for capital letters and add some punctuation). This would give us a small token dictionary, thereby reducing the width we need for those vectors and saving us some valuable memory. However, those tokens don’t have any inherent meaning - we all know what the meaning of “Cat” is, but what is the meaning of “C”? The key to understanding language is context. Although it is clear to us readers that a "Cat" and a "Cradle" have different meanings, for a language model with this tokenizer - the "C" is the same.

🆒 Word-level tokenization
Another approach we can try is breaking our text into words, just like in the example above ("I want to break free").
Now, every token has a meaning that the model can learn and use. We are gaining meaning, but that requires a much larger dictionary. Also, it raises another question: what about words stemming from the same root-word like ”helped”, “helping”, and “helpful”? In this approach each of these words will get a different token with no inherent relation between them, whereas for us readers it's clear that they all have a similar meaning.
Furthermore, words may have fundamentally different meanings when strung together - for instance, my run-down car isn't running anywhere. What if we went a step further?

💬 Sentence-level tokenization
In this approach we break our text into sentences. This will capture meaningful phrases! However, this would result in an absurdly large dictionary, with some tokens being so rare that we would require an enormous amount of data to teach the model the meaning of each token.

🏅 Which is best?
Each method has pros and cons, and like any real-life problem, the best solution involves a number of compromises. AI21 Studio uses a large token dictionary (250K), which contains some from every method: separate characters, words, word parts such as prefixes and suffixes, and many multi-word tokens."""

OBQA_QUESTION = "Which tokenization methods are there?"

DOC_QA = "What would you like to know?"
