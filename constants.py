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

CUSTOM_CHAT_DEMOS = {'shoe_la_la': CHATBOT_SHOE_LA_LA}


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

CLASSIFICATION_SUMMARY = "Rumors spread that Major League Baseball is edging closer to moving the Expos to Washington as D.C. officials announce plans for a stadium on the Anacostia waterfront."