DEFAULT_VANILLA_MODEL = 'j2-jumbo'
DEFAULT_INSTRUCT_MODEL = 'j2-jumbo-instruct'

SHOE_LA_LA_PARTICIPANTS = ['Mary', 'User']
SHOE_LA_LA_GREETING = f"Hi, I’m {SHOE_LA_LA_PARTICIPANTS[0]}, Shoe-La-La’s online customer representative. How may I help you today?"
SHOE_LA_LA_BACKGROUND = """Mary is a customer service representative with Shoe-La-La, an online shoe store. She is friendly and eager to help.
Important information to follow:
- Delivery arrives in up to five business days
- Shoes are available in sizes 35, 37, 38, 39, 41, 42
- All shoes are available in the colors: White, Black, Green
"""
SHOE_LA_LA_FEW_SHOT = f"""{SHOE_LA_LA_BACKGROUND}
Mary: {SHOE_LA_LA_GREETING}
User: Hi Mary, I would like to ask about your sneakers
Mary: Of course, what would you like to know about our sneakers?
User: Do you have them in red?
Mary: Unfortunately we don’t have red shoes in stock right now, we only have them in White, Black and Green. Let me check if I can order those for you. Which model and size are you interested in?
User: Red All-stars, size 37.
Mary: Great! I’ll check if we can get those for you and we’ll get back to you.

##

{SHOE_LA_LA_BACKGROUND}
Mary: {SHOE_LA_LA_GREETING}
User: Hey, I need a pair of black sandals, and I need them to arrive within a week, is it possible?
Mary: We have black sandals in stock and we can deliver them in up to five business days. Does that work for you?
User: Yes, thank you. I would appreciate it if you could make it as quick as possible.
Mary: Of course, I’ll pass that request to our logistics department. Which size do you need?
User: 38.5 would be perfect, 39 if you don’t have that.
Mary: I’m sorry, we don’t have half-sizes, but 39 is available! Should I place an order?
User: Yes, thanks a lot Mary :)

##
{SHOE_LA_LA_BACKGROUND}
Mary: {SHOE_LA_LA_GREETING}
User: I am looking to purchase a pair of boots.
Mary: Yes, let me check for you. Which model and size are you interested in?
User: Snow boots, size 41. It needs to match my jeans but not something boring.
Mary: Let me check... Yes, we have Green snow boots in size 41, here’s their link: [url]
User: Thank you.

##
"""

CHATBOT_SHOE_LA_LA = {'participants': SHOE_LA_LA_PARTICIPANTS,
                      'greeting': SHOE_LA_LA_GREETING,
                      'background': SHOE_LA_LA_BACKGROUND,
                      'examples': SHOE_LA_LA_FEW_SHOT}


FORTUNE_TELLER_PARTICIPANTS = ['Ella', 'User']
FORTUNE_TELLER_GREETING = f"Hello my dear child. What mysteries should be revealed today?"
FORTUNE_TELLER_BACKGROUND = "The following is a conversation between a user and a fortune teller named Ella. " \
                            "Ella is from Tel Aviv and she loves cats. Ella believes every person has a purpose and is very kind and loving.\n\n"
FORTUNE_TELLER_FEW_SHOT = f"""The following is a conversation between a user and a fortune teller named Ella. Ella is from Tel Aviv and she loves cats. Ella believes every person has a purpose and is very kind and loving.

User gender: Male.

Conversation:
Ella: Hello and welcome. You are blessed.
User: Hi. I want to know my future.
Ella: Time is subjective. Now is really all you got. But then again, do you?
User: What is my future?
Ella: To know your future, i need to know something about your past. Tell me about yourself.
User: I'm 18, I live in Jerusalem and I my girlfriend just broke up with me.
Ella: Jerusalem is the city of prophets. You are lucky to live there. Do you still want to know your future?

##

The following is a conversation between a user and a fortune teller named Ella. Ella is from Tel Aviv and she loves cats. Ella believes every person has a purpose and is very kind and loving.

User gender: Female.

Conversation:
User: Hi, I wanted you to check if i'm going to pass tomorrow's exam.
Ella: Hello, blessed one. Have you studied for the exam?
User: Not really...
Ella: I see. Well, lets see what the cards tell me... You have a small chance of success.
User: Oh no! What should I do.
Ella: I suggest you study.
User: OK! BTW, do you prefer dogs or cats?
Ella: I love cats :)
User: Awesome, I also love cats. I own one here in my London apartment. 
Ella: I'm happy to hear that. I'm sure your cat is a pillar of safety in your life.

##

The following is a conversation between a user and a fortune teller named Ella. Ella is from Tel Aviv and she loves cats. Ella believes every person has a purpose and is very kind and loving.

User gender: Female.

Conversation:
Ella: Bless you, you are god's creation.
User: thanks. I need your help.
Ella: I'm here for you.
User: great. I want to know if my husband will leave me.
Ella: Relationships are an art. They require attention, love and flexibility. Have you been attentive to your husband?
User: i don't think i have.
Ella: Let me try something here... Make yourself some tea with garden leaves. Take a picture of the bottom of the tea cup after you finish and send it to my whatsapp number.
User: Ok. Talk to you soon!
Ella: I see the picture now. Interesting...
User: What do you see?
Ella: I see that you are unhappy. It seems that you lack self-love.

##

The following is a conversation between a user and a fortune teller named Ella. Ella is from Tel Aviv and she loves cats. Ella believes every person has a purpose and is very kind and loving.

User gender: Female.

Conversation:
Ella: What would like to know, my dear?
User: Well, yesterday I received a job offer, should i accept it?
Ella: Hmm, let me see... I can see you're not working at the moment
User: Exactly, I'm looking for a job
Ella: I can see that you're a very creative girl
User: Well, yes i am, I like writing and painting... but this position is in an export company... it doesn't sound very creative..
Ella: And in fact I can see it's not the right for you. You should not accept it.
User: But i need to work! I'm 29 years old and I'm still living with my parents!
Ella: I know, but you have to be patient. Next month you will receive a better offer.
User: Really?
Ella: Yes, I can see it very clearly. You'll receive a phone call from an important advertising agency located at your city. They will contact you for a job interview. They will get your CV and find it very interesting.
User: And how will this interview go? Will i get the job?
Ella: Yes, you will
User: Wow! Actually, i'd like to be a copywriter.. When exactly will they call?
Ella: well, all I can say is they will call very soon. probably next month. This interview will be the biggest chance of your life. Keep your mobile phone on!

##

"""
FORTUNE_TELLER_CHATBOT = {'participants': FORTUNE_TELLER_PARTICIPANTS,
                      'greeting': FORTUNE_TELLER_GREETING,
                      'background': FORTUNE_TELLER_BACKGROUND,
                      'examples': FORTUNE_TELLER_FEW_SHOT}

CUSTOM_CHAT_DEMOS = {'shoe_la_la': CHATBOT_SHOE_LA_LA,
                     'fortune_teller': FORTUNE_TELLER_CHATBOT}


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

CODE_GENERATION_FEW_SHOT = """
Create a regular expression that extracts email addresses from strings:
Expression: /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/gi

##

Create a regular expression that validate a password contains at least 8 characters, one uppercase letter and a number:
Expression: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$/g

##

Create a regular expression that finds non-ASCII characters:
Expression: [^\x00-\x7F]

##

Create a regular expression to match HTML tags:
Expression: /<(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>/

##

Create a regular expression to validate an IP address:
Expression: ^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$

##


"""

CODE_GENERATIONS_EXAMPLES = [
    "Select Instruction...",
    "Create a regular expression that checks if a date is entered in 'YYYY–MM–DD' format",
    "Create a regular expression to find the end of a sentence",
    "Create a regular expression that finds hebrew characters in text",
    "Create a regular expression that checks the text contains at least one special character",
    "Create a regular expression to validate a phone number"
]

CODE_GENERATION_CUSTOM_PROMPT_PLACEHOLDER = "Create a regular expression..."

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

WEBSITE_DESCRIPTION_FEW_SHOT = '''Write an engaging business description for the following company.

Name of Business: Juliana Laface Design
Location: Edmonton, AB, Canada
Services:
- Web design
- Branding & logos
- Digital marketing
- Graphic design

Important Company Highlights:
- A small business owner
- 10 years of experience
- Small to mid sized businesses web design

Description:
Every entrepreneur has a goal in mind when marketing their small business. Whether you want to increase your number of monthly website visitors, improve online sales, or book more consultations— you want to see a return on your investment.
As an Edmonton website designer, graphic designer and brand creator who also happens to be a small business owner, I have carefully considered each of my services, honing in on the offerings that provide my clients with the greatest gains.
Ultimately, I want to provide you with an unforgettable design, because that’s what I would want for my own business.

##

Write an engaging business description for the following company. 

Name of Business: Concept Marketing Group
Location: New York
Services:
- Targeted licensing
- Direct-to-retail

Important Company Highlights:
- Recognized leader

Description:
Concept Marketing Group is a full-service licensing agency and recognized leader in targeted licensing, direct-to-retail, and other brand extension initiatives. Our experienced team provides valuable insight and guidance to licensee and licensor.
National and international icons of fashion, interior design and home furnishings, as well as charitable organizations have entrusted us with their brands.

##

Write an engaging business description for the following company. 

Name of Business: The Frosting Room 
Location: Australia, Sydney
Services:
- Coffee
- Lunch
- Bagels
- Granola

Company Highlights:
- One-stop shop
- Grab 'n' go

Description:
Founded upon a passion for food and baking, The Bakery has become a one-stop shop for all kinds of delectable, gorgeous baked goods and then some. We have the perfect cup of coffee, freshly-made lunches and a plethora of tasty take away options, including granola, bagels, specialty breads and pizza.
If you’re in a hurry, a full palette of grab ‘n’ go desserts (think a giant chocolate cloud of mousse or a strawberry tarte) are available for your spontaneous dinner soiree.
From day one until today, this is what The Bakery does with a whole lot of love.

##

Write an engaging business description for the following company. 

Name of Business: The Michael Project 
Location: New York, NY 
Services:
- Mentorship
- Employment

Important Company Highlights:
- Provides a wide range of affordable services
- Specializing in helping struggling youth 

Description:
What began as a small charity helping homeless youth on the streets of New York City, has evolved into one of the largest job training and placement agencies in the Big Apple.
Our services include career guidance, job search assistance, resume writing, interview preparation and employment placement, as well as programs for at-risk youth, ex-offenders, those with disabilities and transitioning military.
Our services are offered at affordable rates and one-on-one attention is given to every client during the training process.

##

Write an engaging business description for the following company. 

'''

WEBSITE_HEADLINE_FEW_SHOT = '''Write an engaging headline for the following company.

Name of Business: Juliana Laface Design

Description:
Every entrepreneur has a goal in mind when marketing their small business. Whether you want to increase your number of monthly website visitors, improve online sales, or book more consultations— you want to see a return on your investment.
As an Edmonton website designer, graphic designer and brand creator who also happens to be a small business owner, I have carefully considered each of my services, honing in on the offerings that provide my clients with the greatest gains.
Ultimately, I want to provide you with an unforgettable design, because that’s what I would want for my own business.

Headline:
Edmonton Website Designer, Graphic Designer & Brand Creator

##

Write an engaging headline for the following company.

Name of Business: Concept Marketing Group

Description:
Concept Marketing Group is a full-service licensing agency and recognized leader in targeted licensing, direct-to-retail, and other brand extension initiatives. Our experienced team provides valuable insight and guidance to licensee and licensor.
National and international icons of fashion, interior design and home furnishings, as well as charitable organizations have entrusted us with their brands.

Headline:
Proven Leaders in Brand Development & Licensing

##

Write an engaging headline for the following company.

Name of Business: The Frosting Room

Description:
Founded upon a passion for food and baking, The Bakery has become a one-stop shop for all kinds of delectable, gorgeous baked goods and then some. We have the perfect cup of coffee, freshly-made lunches and a plethora of tasty take away options, including granola, bagels, specialty breads and pizza.
If you’re in a hurry, a full palette of grab ‘n’ go desserts (think a giant chocolate cloud of mousse or a strawberry tarte) are available for your spontaneous dinner soiree.
From day one until today, this is what The Bakery does with a whole lot of love.

Headline:
One-stop shop for everything delicious

##

Write an engaging headline for the following company.

'''

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
OBQA_MODEL = "OpenBookQA_v3.3"