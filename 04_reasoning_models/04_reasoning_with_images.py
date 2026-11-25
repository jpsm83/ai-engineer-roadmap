import os
from dotenv import load_dotenv, find_dotenv
# json parses the org-chart reply once the model returns it.
import json

# Drop library warnings so the printed answers are the lesson.
import warnings
warnings.filterwarnings('ignore')

# base64 turns the PNG bytes into the string the image part of a message needs.
import base64

# Load OPENAI_API_KEY from a local .env. OpenAI() below takes this value as api_key.
_ = load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')

from openai import OpenAI
from rich import print

# One client. Both vision calls and the follow-up question use the reasoning model.
# create_chat_completion turns reasoning off only for the non-reasoning name, which this file does not call.
client = OpenAI(api_key=openai_api_key)
NON_REASONING_MODEL = 'gpt-6-luna'
REASONING_MODEL = 'gpt-5-nano'

# chat.completions.create returns a completion. Extra kwargs carry response_format
# when a call wants JSON. reasoning_effort "none" is sent only for NON_REASONING_MODEL.
def create_chat_completion(model, messages, **kwargs):
    request = {"model": model, "messages": messages, **kwargs}
    if model == NON_REASONING_MODEL:
        request["reasoning_effort"] = "none"
    return client.chat.completions.create(**request)

# Org chart the first two calls look at. The print is so you can see which file was sent.
image_filepath = 'data/org_chart_sample.png'
print(f"[image] {image_filepath}")

# Read the PNG and return the base64 text. The caller wraps it as a data URL.
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Would print a reply's text. Left commented; the first live print is the "What is this?" answer.
#print(response.choices[0].message.content)

# Send one user message whose content is a text part plus an image part.
# The image is a data URL built from encode_image. json_mode adds response_format
# json_object, so the model must return JSON. The return value is the full completion;
# callers read the text at choices[0].message.content.
def reasoning_model_vision(file_path,prompt,model,json_mode=False):

    base64_image = encode_image(file_path)

    if json_mode:

        response = create_chat_completion(
            model=model,
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}]}],
            response_format={ "type": "json_object" }
        )

    else:
        
        response = create_chat_completion(
            model=model,
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}]}],
        )

    return response

# Free-text look at the org chart. The printed string is the reply, not the completion object.
response = reasoning_model_vision(file_path=image_filepath
                     ,prompt='What is this?'
                     ,model=REASONING_MODEL)

print(response.choices[0].message.content)

# Extraction instructions. The model invents an id per person; "report to" and
# "that report to them" are arrays of those same ids, so the graph can be followed later.
structured_prompt = ("<instructions>You are a consulting assistant who processes org data. "
                     "Extract the org hierarchy from the image you're provided in a structured format. "
                     "The structure should be returned in JSON containing:\n"
                     "- arbitrary ID of the person that you can generate\n"
                     "- name of the person\n"
                     "- role of the person\n"
                     "- an array of IDs they report to\n"
                     "- an array of IDs that report to them"
                     "</instructions>")

# Would print the extraction instructions before the call. Left commented.
# print(structured_prompt)

# Same image, now with json_mode so the reply is a JSON object.
reasoning_model_response = reasoning_model_vision(file_path=image_filepath
                        ,model=REASONING_MODEL
                        ,prompt=structured_prompt
                        ,json_mode=True)

print(reasoning_model_response.choices[0].message.content)

# Drop a markdown fence if the model wrapped the JSON, then parse it.
cleaned_json = reasoning_model_response.choices[0].message.content.replace('```json','').replace('```','')

org_data = json.loads(cleaned_json)

print(json.dumps(org_data, indent=2))

# No image on this turn. The question is answered from org_data pasted into the prompt:
# who has the highest ranking reports, and which manager has the most reports.
analysis_prompt = ("<instructions>You are an org chart expert assistant. Your role is to"
                   "answer any org chart questions with your org data.</instructions>\n"
                   f"<org_data>{org_data}</org_data>\n")

messages = [{
    "role": "user",
    "content": analysis_prompt + "<question>Who has the highest ranking reports, and which manager has the most reports?</question>"
}]

# Text-only completion. The printed answer is choices[0].message.content.
response = create_chat_completion(REASONING_MODEL, messages)

print(response.choices[0].message.content)

# Replaces the org-chart path above with the ERD image.
# This file prints that new path and does not send the image.
image_filepath = 'data/erd-relation-order.png'

print(f"[image] {image_filepath}")