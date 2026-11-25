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
# temperature is accepted but not sent: that argument stays commented out
# because gpt-5-nano only allows its default.
def get_completion(prompt, model="gpt-5-nano", temperature=1):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # temperature=temperature,  # course uses 0–2; gpt-5-nano only allows default 1
    )
    return response.choices[0].message.content

# Written here as "negative", not computed in this file. That value
# selects the apology branch. Prompts paste these in as {sentiment} and
# {review}, so those spellings have to match these two names.
# given the sentiment from the lesson on "inferring",
# and the original customer message, customize the email
sentiment = "negative"

# review for a blender
review = f"""
So, they still had the 17 piece system on seasonal \
sale for around $49 in the month of November, about \
half off, but for some reason (call it price gouging) \
around the second week of December the prices all went \
up to about anywhere from between $70-$89 for the same \
system. And the 11 piece system went up around $10 or \
so in price also from the earlier sale price of $29. \
So it looks okay, but if you look at the base, the part \
where the blade locks into place doesn’t look as good \
as in previous editions from a few years ago, but I \
plan to be very gentle with it (example, I crush \
very hard items like beans, ice, rice, etc. in the \
blender first then pulverize them in the serving size \
I want in the blender then switch to the whipping \
blade for a finer flour, and use the cross cutting blade \
first when making smoothies, then use the flat blade \
if I need them finer/less pulpy). Special tip when making \
smoothies, finely cut and freeze the fruits and \
vegetables (if using spinach-lightly stew soften the \
spinach then freeze until ready for use-and if making \
sorbet, use a small to medium sized food processor) \
that you plan to use that way you can avoid adding so \
much ice if at all-when making your smoothie. \
After about a year, the motor was making a funny noise. \
I called customer service but the warranty expired \
already, so I had to buy another one. FYI: The overall \
quality has gone done in these types of products, so \
they are kind of counting on brand recognition and \
consumer loyalty to maintain sales. Got it in about \
two days.
"""

# Example 1 is the same reply prompt, stored unused.
# Example 2 is the call that runs.
'''
# ============================== example 1 ==============================

prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
Review sentiment: {sentiment}
"""
response = get_completion(prompt)
print(response)
'''

# ============================== example 2 ==============================

# Customer-service reply. The prompt thanks the customer, and if sentiment
# is negative it apologizes and points them to customer service.
# temperature=1 is passed in, but get_completion does not forward it.
prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
Review sentiment: {sentiment}
"""
response = get_completion(prompt, temperature=1)
print(response)