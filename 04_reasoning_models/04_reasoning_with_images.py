import os
from dotenv import load_dotenv, find_dotenv
import json

# Warning control
import warnings
warnings.filterwarnings('ignore')

import base64

# Import OpenAI key
_ = load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')

from openai import OpenAI

client = OpenAI(api_key=openai_api_key)
NON_REASONING_MODEL = 'gpt-6-luna'
REASONING_MODEL = 'gpt-5-nano'

def create_chat_completion(model, messages, **kwargs):
    request = {"model": model, "messages": messages, **kwargs}
    if model == NON_REASONING_MODEL:
        request["reasoning_effort"] = "none"
    return client.chat.completions.create(**request)

image_filepath = 'data/org_chart_sample.png'
print(f"[image] {image_filepath}")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

#print(response.choices[0].message.content)

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

response = reasoning_model_vision(file_path=image_filepath
                     ,prompt='What is this?'
                     ,model=REASONING_MODEL)

print(response.choices[0].message.content)

structured_prompt = ("<instructions>You are a consulting assistant who processes org data. "
                     "Extract the org hierarchy from the image you're provided in a structured format. "
                     "The structure should be returned in JSON containing:\n"
                     "- arbitrary ID of the person that you can generate\n"
                     "- name of the person\n"
                     "- role of the person\n"
                     "- an array of IDs they report to\n"
                     "- an array of IDs that report to them"
                     "</instructions>")

# print(structured_prompt)

reasoning_model_response = reasoning_model_vision(file_path=image_filepath
                        ,model=REASONING_MODEL
                        ,prompt=structured_prompt
                        ,json_mode=True)

print(reasoning_model_response.choices[0].message.content)

cleaned_json = reasoning_model_response.choices[0].message.content.replace('```json','').replace('```','')

org_data = json.loads(cleaned_json)

print(json.dumps(org_data, indent=2))

analysis_prompt = ("<instructions>You are an org chart expert assistant. Your role is to"
                   "answer any org chart questions with your org data.</instructions>\n"
                   f"<org_data>{org_data}</org_data>\n")

messages = [{
    "role": "user",
    "content": analysis_prompt + "<question>Who has the highest ranking reports, and which manager has the most reports?</question>"
}]

response = create_chat_completion(REASONING_MODEL, messages)

print(response.choices[0].message.content)

image_filepath = 'data/erd-relation-order.png'

print(f"[image] {image_filepath}")