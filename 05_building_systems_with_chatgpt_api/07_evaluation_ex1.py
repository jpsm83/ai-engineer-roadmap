import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import utils
from rich import print

# Panel chat UI. extension() loads the widgets used at the bottom.
import panel as pn  # GUI
pn.extension()

# Load OPENAI_API_KEY from a local .env file into the environment.
_ = load_dotenv(find_dotenv())  # read local .env file

# Client for the moderation calls and the two chat calls in one turn.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chat call for the customer reply and for the yes/no check.
# messages in, assistant text out. max_completion_tokens also counts
# reasoning tokens on gpt-5-nano.
def get_completion_from_messages(messages,
                                 model="gpt-5-nano",
                                 temperature=1,
                                 max_completion_tokens=5000):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens,  # includes reasoning tokens on gpt-5-nano
    )
    return response.choices[0].message.content

# System of chained prompts for processing the user query
# One turn of the chain from the earlier lessons: moderate the input,
# extract products, look them up, answer, moderate the answer, then ask
# the model if the answer is good enough.
# user_input is this turn's question. all_messages is history from
# earlier turns. The return is (reply text, updated history).

def process_user_message(user_input, all_messages, debug=True):
    # ``` wraps the customer text in the answer prompt below.
    delimiter = "```"

    # Step 1: Check input to see if it flags the Moderation API or is a prompt injection
    # moderations.create scores the raw input. results[0].flagged is the
    # boolean. A flagged input returns a refusal and leaves history as it was.
    # The heading also names prompt injection. This function does not run that check.
    response = client.moderations.create(model="omni-moderation-latest", input=user_input)

    moderation_output = response.results[0]

    if moderation_output.flagged:
        print("Step 1: Input flagged by Moderation API.")
        return "Sorry, we cannot process this request.", all_messages

    if debug: print("Step 1: Input passed moderation check.")
    
    # utils.find_category_and_product_only sends the query plus the catalog
    # to a model and returns text shaped like a list of category or product
    # objects. The commented print would show that text.
    category_and_product_response = utils.find_category_and_product_only(user_input, utils.get_products_and_category())
    #print(print(category_and_product_response)

    # Step 2: Extract the list of products
    # utils.read_string_to_list turns that text into a Python list,
    # or None if it is missing or not JSON. The lookup below still
    # runs on that None. The commented print would show the list.
    category_and_product_list = utils.read_string_to_list(category_and_product_response)
    #print(category_and_product_list)

    if debug: print("Step 2: Extracted list of products.")

    # Step 3: If products are found, look them up
    # utils.generate_output_string looks those names up and returns the
    # matching catalog entries as JSON text.
    product_information = utils.generate_output_string(category_and_product_list)

    if debug: print("Step 3: Looked up product information.")

    # Step 4: Answer the user question
    # messages is only this turn: store-assistant instructions, the query
    # wrapped in ```, and an assistant turn that already holds the product
    # JSON. The model is called on all_messages + messages, so it sees
    # earlier turns first and this turn after them.
    system_message = f"""
    You are a customer service assistant for a large electronic store. \
    Respond in a friendly and helpful tone, with concise answers. \
    Make sure to ask the user relevant follow-up questions.
    """

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
        {'role': 'assistant', 'content': f"Relevant product information:\n{product_information}"}
    ]

    final_response = get_completion_from_messages(all_messages + messages)

    if debug:print("Step 4: Generated response to user question.")

    # History grows by this turn's user message and the product-info
    # assistant message, not the system line (messages[1:]). The real
    # reply is appended later, in collect_messages.
    all_messages = all_messages + messages[1:]

    # Step 5: Put the answer through the Moderation API
    # Same moderation call as step 1, this time on the reply text.
    # flagged replaces the reply with a refusal. History still includes this turn.
    response = client.moderations.create(model="omni-moderation-latest", input=final_response)

    moderation_output = response.results[0]

    if moderation_output.flagged:
        if debug: print("Step 5: Response flagged by Moderation API.")
        return "Sorry, we cannot provide this information.", all_messages

    if debug: print("Step 5: Response passed moderation check.")

    # Step 6: Ask the model if the response answers the initial user query well
    # Reuses the system_message variable from step 4, the store-assistant
    # instructions. The user turn holds the question and the reply.
    # That question does not demand the letter Y. Step 7 still treats
    # that letter as approval. evaluation_response is the text that comes back.
    user_message = f"""
    Customer message: {delimiter}{user_input}{delimiter}
    Agent response: {delimiter}{final_response}{delimiter}

    Does the response sufficiently answer the question?
    """

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    evaluation_response = get_completion_from_messages(messages)

    if debug: print("Step 6: Model evaluated the response.")

    # Step 7: If yes, use this answer; if not, say that you will connect the user to a human
    # "Y" anywhere in the evaluation text keeps final_response. Anything
    # else returns the handoff sentence. Both returns include the updated history.
    if "Y" in evaluation_response:  # Using "in" instead of "==" to be safer for model output variation (e.g., "Y." or "Yes")
        if debug: print("Step 7: Model approved the response.")
        return final_response, all_messages
    else:
        if debug: print("Step 7: Model disapproved the response.")
        neg_str = "I'm unable to provide the information you're looking for. I'll connect you with a human representative for further assistance."
        return neg_str, all_messages

# One-shot CLI demo (commented out so this file opens the dashboard):
# A single question, empty history. Left commented so running the file
# starts the chat UI below instead of answering once and exiting.
# user_input = "tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tell me about your tvs"
# response,_ = process_user_message(user_input,[])
# print(response)

# Function that collects user and assistant messages over time
# Runs when the button is clicked. inp.value_input is the submitted
# text. An empty box returns without calling the model. Setting
# inp.value to '' clears the box for the next turn.
# context is the running transcript the model reads. panels is only
# what the page shows. Those two stores are not the same list.

def collect_messages(debug=False):
    user_input = inp.value_input
    if debug: print(f"User Input = {user_input}")
    if user_input == "":
        return
    inp.value = ''
    global context
    # The commented call is an earlier signature that passed the catalog
    # in. The live call lets process_user_message load products itself.
    # It returns the reply and the updated history. The reply is then
    # appended as an assistant turn, so the next click still sees it.
    #response, context = process_user_message(user_input, context, utils.get_products_and_category(),debug=True)
    response, context = process_user_message(user_input, context, debug=False)
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(user_input, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)

# Chat with the chatbot!
# context starts as one system turn. panels collects the visible rows.
# inp is the text box. The button is bound to collect_messages, and
# the panel below redraws when that function returns a column of rows.

panels = [] # collect display 

context = [ {'role':'system', 'content':"You are Service Assistant"} ]  

inp = pn.widgets.TextInput( placeholder='Enter text here…')

button_conversation = pn.widgets.Button(name="Service Assistant")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

# In a notebook, a bare `dashboard` is enough to render. From a .py file
# you need .show() to start a local server and open the browser.
# .show() serves this dashboard on port 5006. That is why this file
# is not run while it is being commented.
dashboard.show(port=5006)
