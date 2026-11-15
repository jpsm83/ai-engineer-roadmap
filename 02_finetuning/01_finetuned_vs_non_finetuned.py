"""Compare a base model with a chat/fine-tuned model on the same prompts.

This course example sends each prompt to a non-fine-tuned Llama 2 model and to
the chat version, so their answers can be compared side by side.

It needs real Lamini credentials in the repository-root .env file.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
import lamini
from lamini import BasicModelRunner

## Load the shared .env from the repository root, regardless of the current
## working directory.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

## Configure the Lamini client with the URL and API key from the environment.
lamini.api_url = os.getenv("POWERML__PRODUCTION__URL")
lamini.api_key = os.getenv("POWERML__PRODUCTION__KEY")

if (
    not lamini.api_url
    or not lamini.api_key
    or lamini.api_url.strip().lower() == "none"
    or lamini.api_key.strip().lower() == "none"
):
    raise RuntimeError(
        "Missing or placeholder Lamini credentials. Set real values for "
        "POWERML__PRODUCTION__URL and POWERML__PRODUCTION__KEY in the .env "
        "file at the repository root."
    )

## BasicModelRunner wraps a hosted model behind a simple callable interface.
## This first model is the base Llama 2 model, without chat fine-tuning.
non_finetuned = BasicModelRunner("meta-llama/Llama-2-7b-hf")

## Send the same kinds of prompts to the base model.
non_finetuned_output = non_finetuned("Tell me how to train my dog to sit")

print(non_finetuned_output)

print(non_finetuned("What do you think of Mars?"))

print(non_finetuned("taylor swift's best friend"))

print(non_finetuned("""Agent: I'm here to help you with your Amazon deliver order.
Customer: I didn't get my item
Agent: I'm sorry to hear that. Which item was it?
Customer: the blanket
Agent:"""))

## The -chat model has been fine-tuned to follow instructions and hold a
## conversation, so its answers should be more useful on these prompts.
finetuned_model = BasicModelRunner("meta-llama/Llama-2-7b-chat-hf")

finetuned_output = finetuned_model("Tell me how to train my dog to sit")

print(finetuned_output)

## [INST] ... [/INST] is the instruction format used by Llama 2 chat models.
## Sending the same format to the base model shows that it was not trained on it.
print(finetuned_model("[INST]Tell me how to train my dog to sit[/INST]"))

print(non_finetuned("[INST]Tell me how to train my dog to sit[/INST]"))

print(finetuned_model("What do you think of Mars?"))

print(finetuned_model("taylor swift's best friend"))

## A multi-turn dialogue prompt: the chat model should continue the Agent turn.
print(finetuned_model("""Agent: I'm here to help you with your Amazon deliver order.
Customer: I didn't get my item
Agent: I'm sorry to hear that. Which item was it?
Customer: the blanket
Agent:"""))