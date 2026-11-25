import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from rich import print

# Load OPENAI_API_KEY from a local .env file into the environment.
_ = load_dotenv(find_dotenv())  # read local .env file

# Client for every chat.completions.create call below.
# api_key is the value just loaded; the SDK sends it on each request.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# One user prompt in, the assistant's reply text out.
# create() returns a completion object; the text is choices[0].message.content.
# Temperature stays commented out because gpt-5-nano only accepts its default.
def get_completion(prompt, model="gpt-5-nano"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # temperature=0,  # course uses 0 for deterministic output; gpt-5-nano only allows 1
    )
    return response.choices[0].message.content

# Lamp review read by the sentiment and extraction prompts in examples 1–6.
lamp_review = """
Needed a nice lamp for my bedroom, and this one had \
additional storage and not too high of a price point. \
Got it fast.  The string to our lamp broke during the \
transit and the company happily sent over a new one. \
Came within a few days as well. It was easy to put \
together.  I had a missing part, so I contacted their \
support and they very quickly got me the missing piece! \
Lumina seems to me to be a great company that cares \
about their customers and products!!
"""

# Examples 1–6 are unused. They all read lamp_review and tighten the answer:
# open sentiment; one word, positive or negative; up to five lowercase emotions;
# anger as yes or no; JSON "Item" and "Brand", or "unknown"; then one JSON
# with sentiment, anger as a boolean, item, and brand.
'''
# ============================== example 1 ==============================

prompt = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Review text: ```{lamp_review}```
"""
response = get_completion(prompt)
print(response)

# ============================== example 2 ==============================

prompt = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Give your answer as a single word, either "positive" \
or "negative".

Review text: ```{lamp_review}```
"""
response = get_completion(prompt)
print(response)

# ============================== example 3 ==============================

prompt = f"""
Identify a list of emotions that the writer of the \
following review is expressing. Include no more than \
five items in the list. Format your answer as a list of \
lower-case words separated by commas.

Review text: ```{lamp_review}```
"""
response = get_completion(prompt)
print(response)

# ============================== example 4 ==============================

prompt = f"""
Is the writer of the following review expressing anger?\
The review is delimited with triple backticks. \
Give your answer as either yes or no.

Review text: ```{lamp_review}```
"""
response = get_completion(prompt)
print(response)

# ============================== example 5 ==============================

prompt = f"""
Identify the following items from the review text: 
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Item" and "Brand" as the keys. 
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
  
Review text: ```{lamp_review}```
"""
response = get_completion(prompt)
print(response)

# ============================== example 6 ==============================

prompt = f"""
Identify the following items from the review text: 
- Sentiment (positive or negative)
- Is the reviewer expressing anger? (true or false)
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Anger", "Item" and "Brand" as the keys.
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
Format the Anger value as a boolean.

Review text: ```{lamp_review}```
"""
response = get_completion(prompt)
print(response)
'''

# =============================================================================
# =============================================================================
# =============================================================================

# News-style story for the topic prompts. This replaces the lamp review
# as the text the model reads. Prompts paste it in as {story}.
story = """
In a recent survey conducted by the government, 
public sector employees were asked to rate their level 
of satisfaction with the department they work at. 
The results revealed that NASA was the most popular 
department with a satisfaction rating of 95%.

One NASA employee, John Smith, commented on the findings, 
stating, "I'm not surprised that NASA came out on top. 
It's a great place to work with amazing people and 
incredible opportunities. I'm proud to be a part of 
such an innovative organization."

The results were also welcomed by NASA's management team, 
with Director Tom Johnson stating, "We are thrilled to 
hear that our employees are satisfied with their work at NASA. 
We have a talented and dedicated team who work tirelessly 
to achieve our goals, and it's fantastic to see that their 
hard work is paying off."

The survey also revealed that the 
Social Security Administration had the lowest satisfaction 
rating, with only 45% of employees indicating they were 
satisfied with their job. The government has pledged to 
address the concerns raised by employees in the survey and 
work towards improving job satisfaction across all departments.
"""

# ============================== example 7 ==============================

# Ask for five topics from the story, one or two words each, comma-separated.
# get_completion returns that list as a single string.
prompt = f"""
Determine five topics that are being discussed in the \
following text, which is delimited by triple backticks.

Make each item one or two words long. 

Format your response as a list of items separated by commas.

Text sample: ```{story}```
"""
response = get_completion(prompt)
print(response)

# Would split that comma-separated list. The result is thrown away;
# the check below uses topic_list, not whatever the model just returned.
response.split(sep=',')

# Topics this lesson will look for. The next prompt prints these names,
# and the lookup below reads the key "nasa", so the model has to answer
# with that same spelling.
topic_list = [
    "nasa", "local government", "engineering", 
    "employee satisfaction", "federal government"
]

# For each name in topic_list, ask for a line "name: 0" or "name: 1".
# 1 means the story is about that topic. The joined list is what the model sees.
prompt = f"""
Determine whether each item in the following list of \
topics is a topic in the text below, which
is delimited with triple backticks.

Give your answer as follows:
item from the list: 0 or 1

List of topics: {", ".join(topic_list)}

Text sample: ```{story}```
"""
response = get_completion(prompt)
print(response)

# Turn "topic: 0" / "topic: 1" lines into a dict.
# topic_dict['nasa'] only matches if a line used that name from topic_list.
# A 1 means the story is about NASA, so the lesson prints an alert.
topic_dict = {i.split(': ')[0]: int(i.split(': ')[1]) for i in response.split(sep='\n')}
if topic_dict['nasa'] == 1:
    print("ALERT: New NASA story!")