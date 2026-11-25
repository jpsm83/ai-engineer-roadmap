import os
from dotenv import load_dotenv, find_dotenv
from redlines import Redlines
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
# TOOLS is the function schemas in functionDefinitions.py.
# The conversion prompt pastes that list in, and the agent call passes the same list
# as tools=, so the routine may only name functions the model is actually given.
from functionDefinitions import TOOLS
import csv
import json
import matplotlib.pyplot as plt
import re
from collections import Counter
import math 
from termcolor import colored
import tiktoken 

# Drop library warnings so the printed routine and eval are the lesson.
import warnings
warnings.filterwarnings('ignore')

import base64

# Load OPENAI_API_KEY from a local .env. OpenAI() below takes this value as api_key.
_ = load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')

from openai import OpenAI
from rich import print

# One client. The routine is written by the reasoning model.
# The eval agent and the simulated customer use the non-reasoning model.
client = OpenAI(api_key=openai_api_key)
NON_REASONING_MODEL = 'gpt-6-luna'
REASONING_MODEL = 'gpt-5-nano'
# This file's folder, so the policy and the eval CSV are found next to the script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# chat.completions.create returns a completion. Extra kwargs carry tools or response_format.
# reasoning_effort "none" is sent only when the model is NON_REASONING_MODEL.
def create_chat_completion(model, messages, **kwargs):
    request = {"model": model, "messages": messages, **kwargs}
    if model == NON_REASONING_MODEL:
        request["reasoning_effort"] = "none"
    return client.chat.completions.create(**request)

# Notebook-shaped wrapper. The lesson text lives on .data.
class Markdown:
    def __init__(self, data):
        self.data = data

# Prints that text. An object with no .data is printed as itself.
def display(obj):
    print(getattr(obj, "data", obj))

# Show full cells when an eval table is printed. The default would cut them off.
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Redlines marks what changed between two strings. output_markdown is that diff as markdown.
def compare_strings(string1, string2):
    # Create a Redlines object to compare the strings
    diff = Redlines(string1, string2)
    
    # Display the differences using Markdown
    display(Markdown(diff.output_markdown))

# Small demo of that diff, before the policy work. "original" versus "modified".
string_a = "This is the original text for comparison purposes."
string_b = "This is the modified text to compare for differences."

compare_strings(string_a, string_b)

# The public help-center article. generate_routine turns this into an internal routine.
# The commented print would show the article before that conversion.
with open(os.path.join(BASE_DIR, 'originalPolicy', 'flightCancellationsPolicy.md'), 'r') as file:
    flight_cancellation_policy = file.read()
    # print(flight_cancellation_policy)

# Instructions for the reasoning model: turn the help-center article into a step-by-step routine.
# This is an f-string, so {TOOLS} is filled now with the schemas from functionDefinitions.
# Function names in the routine must be those schemas, wrapped in backticks, and the last
# step must be `case_resolution`. extract_function_names later reads those backticks.
CONVERSION_PROMPT = f"""
You are a helpful assistant tasked with taking an external facing help center article and converting it into a internal-facing programmatically executable routine optimized for an LLM. 
The LLM using this routine will be tasked with reading the policy, answering incoming questions from customers, and helping drive the case toward resolution.

Please follow these instructions:
1. **Review the customer service policy carefully** to ensure every step is accounted for. It is crucial not to skip any steps or policies.
2. **Organize the instructions into a logical, step-by-step order**, using the specified format. 
3. **Use the following format**:
   - **Main actions are numbered** (e.g., 1, 2, 3).
   - **Sub-actions are lettered** under their relevant main actions (e.g., 1a, 1b).
      **Sub-actions should start on new lines**
   - **Specify conditions using clear 'if...then...else' statements** (e.g., 'If the product was purchased within 30 days, then...').
   - **For instructions that require more information from the customer**, provide polite and professional prompts to ask for additional information.
   - **For actions that require data from external systems**, write a step to call a function using backticks for the function name (e.g., call the `check_delivery_date` function).
      - **If a step requires the customer service agent to take an action** (e.g., process a refund), generate a function call for this action (e.g., call the `process_refund` function).
      - **Only use the available set of functions that are defined below.
   - **If there is an action an assistant can perform on behalf of the user**, include a function call for this action (e.g., call the `change_email_address` function), and ensure the function is defined with its purpose and required parameters.
      - **Only use the available set of functions that are defined below.
   - **The step prior to case resolution should always be to ask if there is anything more you can assist with**.
   - **End with a final action for case resolution**: calling the `case_resolution` function should always be the final step.
4. **Ensure compliance** by making sure all steps adhere to company policies, privacy regulations, and legal requirements.
5. **Handle exceptions or escalations** by specifying steps for scenarios that fall outside the standard policy.
6. **Ensure coverage** by checking that all of the conditions covered in the policy are also covered in the routines

**Important**: Always wrap the functions you return in backticks i.e. `check_ticket_type`. Do not include the arguments to the functions.

Here are the currently available set of functions in JSON format: 
TOOLS: {TOOLS}

Please convert the following customer service policy into the formatted routine, ensuring it is easy to follow and execute programmatically. Ensure that you **only** use the functions provided and do **not** create net new functions."""

# One user message: the conversion instructions plus this policy.
# Returns the routine as text from choices[0].message.content.
def generate_routine(policy):
    try:
        messages = [
            {
                "role": "user",
                "content": f"""
                    {CONVERSION_PROMPT}

                    POLICY:
                    {policy}
                """
            }
        ]

        response = create_chat_completion(REASONING_MODEL, messages)
        

        return response.choices[0].message.content 
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# Write the routine with the reasoning model and print it.
flight_cancellation_routine = generate_routine(flight_cancellation_policy)

display(Markdown(flight_cancellation_routine))

# Multiset difference of two lists. The print loops are commented out,
# so a call computes the diff and shows nothing until those prints are turned back on.
def compare_lists(a, b):
    # Create Counters for both lists
    counter_a = Counter(a)
    counter_b = Counter(b)
    
    # Find elements that are only in A or have a higher count in A
    diff_a = counter_a - counter_b
    # Find elements that are only in B or have a higher count in B
    diff_b = counter_b - counter_a
    
    # Report differences
    # print("Items in A that are not in B (or more of in A):")
    # for item, count in diff_a.items():
    #     print(f"{item}: {count}")

    #print("\nItems in B that are not in A (or more of in B):")
    # for item, count in diff_b.items():
    #     print(f"{item}: {count}")

# Every backtick span in the routine. The conversion prompt required function names in backticks.
def extract_function_names(text):
    # Use regex to match text between backticks and extract function names
    pattern = r'`(.*?)`'
    matches = re.findall(pattern, text)
    return matches

# Names the routine wrapped in backticks, against the names in TOOLS.
# A name in the routine that is not in TOOLS would need a function the helper does not define.
# A TOOLS name missing from the routine is a defined tool this routine never mentioned.
# compare_lists leaves its prints commented, so this call is silent.
function_names_from_reasoning_model = set(extract_function_names(flight_cancellation_routine))

# Extract the list of TOOLs we provided the model
function_names_defined = [tool["function"]["name"] for tool in TOOLS if tool["type"] == "function"]

compare_lists(function_names_from_reasoning_model, function_names_defined)

# One agent turn. The system message is the policy (the generated routine, in the eval below).
# tools=TOOLS and parallel_tool_calls=False: the model may answer in text or request one tool.
# Returns the message object. Callers read .content and .tool_calls, not the whole completion.
def agent_response(transcript, policy, model):
    try:
        messages = [
            {
                "role": "system",
                "content": f"""
You are a customer service agent that is responsible for handling airline related issues. Below is the exact policy that you must follow to address the customer's issue.

POLICY:
{policy}
                """
            }
        ]

        messages.extend(transcript)
        response = create_chat_completion(
            model,
            messages,
            tools=TOOLS,
            parallel_tool_calls=False,
        )
        
        return response.choices[0].message 
    except Exception as e:
        print(f"An error occurred: {e}")
        print(messages)

# CSV blanks arrive as NaN floats. Those become "" so the customer prompt does not say "nan".
def safe_str(value):
    return "" if (isinstance(value, float) and math.isnan(value)) else str(value)

# One eval case. The agent follows `policy`. A second call to the same model plays the customer,
# using the details on this CSV row. expected_inputs is a JSON string of the arguments we want.
# verify_identity, ask_clarification, the ticket and fare lookups, get_refund_amount, and the
# two flight lookups are answered here and the loop continues. Any other tool call stops the
# loop: that name and its arguments are what the row is graded on. Ten turns with no such
# call leaves actual_function empty and is_correct false.
def process_row(row_number,test_row,policy,model,iteration=0, verbose=False):
    # Extract variables from test_row
    context = test_row['context']
    request = test_row['request']
    full_name = test_row['full_name']
    booking_ref = test_row['booking_ref']
    flight_no = test_row['flight_no']
    ticket_type = test_row['ticket_type']
    fare_rules = safe_str(test_row['fare_rules'])
    medical_certificate = safe_str(test_row['medical_certificate'])
    refund_amount = safe_str(test_row['refund_amount'])
    expected_function = test_row['expected_function']
    expected_inputs_str = test_row['expected_inputs']
    expected_inputs = json.loads(expected_inputs_str)

    # System prompt for the model that plays the customer.
    # A blank medical certificate is left out of the details.
    CUSTOMER_PROMPT = f"""<objective>You are a customer named {full_name} trying to resolve an issue with a customer service agent.
    Continue providing the information the agent requests so they can solve your issue.
    If you have the information in your *details* then use that. Otherwise, generate an appropriate answer.</objective>
    <details>
    Booking Reference: {booking_ref}
    Flight Number: {flight_no}
    {f"Medical Reference: {medical_certificate}" if medical_certificate else ""}
    Context: {context}
    Your initial request: {request}
    </details>
    <guidance>
    Remember that YOU are the customer.
    If the agent needs some information, that must come from you. 
    Do not ask the agent for information.
    </guidance>
    """

    # Initialize transcript
    transcript = [{"role": "user", "content": request}]
    # if verbose:
        # print(f'Starting request: {request}')
    
    # Initialize variables
    is_correct = False

    loop_count = 0
    while True:
        loop_count += 1
        # Stop after ten turns. No graded tool call means this row is wrong.
        if loop_count > 10:
            actual_function = None
            actual_inputs = None
            break
        # Call agent_response with the current transcript, policy, model
        response = agent_response(transcript, policy, model)
        
        # Extract assistant message content and tool_calls
        if response:
            assistant_message_content = response.content
            tool_calls = response.tool_calls
        else:
            assistant_message_content = None
            tool_calls = None
        
        if not tool_calls:
            # The agent spoke instead of calling a tool. Ask the customer model to reply,
            # then go around again. The customer system prompt is the row's details.
            transcript.append({"role": "assistant", "content": assistant_message_content})
            
            # Get customer response
            customer_messages = [{"role": "system", "content": CUSTOMER_PROMPT}]
            customer_messages.extend(transcript)
            
            customer_response = create_chat_completion(model, customer_messages)
            
            # Append customer response to transcript
            transcript.append({"role": "user", "content": customer_response.choices[0].message.content})
            
            # Continue the loop
            continue
        else:
            #print(tool_calls)
            # There is a tool call
            tool_call = tool_calls[0]  # Assuming we're only interested in the first tool call
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            if function_name == 'verify_identity':
                # Always answers "True". tool_call_id has to be the id on the request
                # so the next turn can match this result. Then the agent goes again.
                transcript.append(response.to_dict())
                
                # Simulate the tool response
                tool_response = "True"
                
                # Append the tool response to transcript
                transcript.append({"role": "tool", "content": tool_response, "tool_call_id": tool_call.id})
                
                # Continue the loop
                continue
            elif function_name == 'ask_clarification':
                # The prompt argument is spoken to the customer as assistant text.
                # There is no tool message for this name. The customer model answers it.
                clarification_prompt = arguments.get('prompt')
                
                # Append assistant's clarification message
                transcript.append({"role": "assistant", "content": clarification_prompt})
                
                # Get customer response
                customer_messages = [{"role": "system", "content": CUSTOMER_PROMPT}]
                customer_messages.extend(transcript)
                
                customer_response = create_chat_completion(model, customer_messages)
                
                # Append customer response to transcript
                transcript.append({"role": "user", "content": customer_response.choices[0].message.content})
                
                # Continue the loop
                continue
            elif function_name == 'check_ticket_type':
                # Answer with this row's ticket type and fare rules, then keep going.
                # Append assistant's message to transcript
                transcript.append(response.to_dict())
                
                tool_response = f'Ticket type: {ticket_type}\nFare rules: {fare_rules}'
                
                # Append the tool response to transcript
                transcript.append({"role": "tool", "content": tool_response, "tool_call_id": tool_call.id})
                
                # Continue the loop
                continue
            elif function_name == 'check_fare_rules':
                # Same ticket type and fare rules. A partial_refund fare also includes the refund amount.
                # Append assistant's message to transcript
                transcript.append(response.to_dict())
                
                tool_response = f'Ticket type: {ticket_type}\nFare rules: {fare_rules}'

                if fare_rules == 'partial_refund':
                    tool_response += f'\nRefund amount: {refund_amount}'
                
                # Append the tool response to transcript
                transcript.append({"role": "tool", "content": tool_response, "tool_call_id": tool_call.id})
                
                # Continue the loop
                continue
            elif function_name == 'get_refund_amount':
                # Answer with this row's refund amount, then keep going.
                # Append assistant's message to transcript
                transcript.append(response.to_dict())
                
                tool_response = f'Refund amount: {refund_amount}'
                
                # Append the tool response to transcript
                transcript.append({"role": "tool", "content": tool_response, "tool_call_id": tool_call.id})
                
                # Continue the loop
                continue
            elif function_name == 'check_next_available_flight':
                # Answer with a fixed flight, LMG091 at 10:00 AM tomorrow, then keep going.
                # Append assistant's message to transcript
                transcript.append(response.to_dict())
                
                # simulating the tool response
                tool_response = f'Next available flight: LMG091 at 10:00 AM Tomorrow'
                
                # Append the tool response to transcript
                transcript.append({"role": "tool", "content": tool_response, "tool_call_id": tool_call.id})
                
                # Continue the loop
                continue
            elif function_name == 'provide_alternative_options':
                # Answer with a fixed flight, FR9876 at 5:00 PM tomorrow, then keep going.
                # Append assistant's message to transcript
                transcript.append(response.to_dict())
                
                # simulating the tool response
                tool_response = f'Next available flight: FR9876 at 5:00 PM Tomorrow'
                
                # Append the tool response to transcript
                transcript.append({"role": "tool", "content": tool_response, "tool_call_id": tool_call.id})
                
                # Continue the loop
                continue
            else:
                # Any other tool is the graded action. Stop and compare its name and
                # arguments, as strings, to expected_function and expected_inputs.
                # if verbose:
                    # print('Got a successful function call')
                # Stop and compare function call and arguments with expected_function and expected_inputs
                transcript.append(response.to_dict())
                actual_function = function_name
                actual_inputs = arguments
                is_correct = (actual_function == expected_function) and (str(actual_inputs) == str(expected_inputs))
                
                # Break the loop
                break
    
    # Return the results
    return {
        'request': request,
        'context': context,
        'expected_function': expected_function,
        'expected_inputs': expected_inputs,
        'actual_function': actual_function,
        'actual_inputs': actual_inputs,
        'is_correct': is_correct,
        'transcript': transcript
    }

# Shorten a transcript for display. A tool call becomes {name, arguments}.
# Every other message is left as stored, so the printed row is not the raw tool object.
def filter_messages(message_list):
    messages = []
    for item in message_list:
        tool_calls = item.get("tool_calls") if isinstance(item, dict) else getattr(item, "tool_calls", None)
        if tool_calls:
            tool = tool_calls[0]
            function = tool.get("function", tool) if isinstance(tool, dict) else tool.function
            name = function.get("name") if isinstance(function, dict) else function.name
            arguments = function.get("arguments") if isinstance(function, dict) else function.arguments
            messages.append({"role": "assistant", "tool_call": {"name": name, "arguments": arguments}})
        else:
            messages.append(item)
    return messages


# Run process_row on every eval row at once. Each finished row is appended as it completes.
# cleaned_transcript is the shortened form from filter_messages.
# total_accuracy is the fraction of rows whose final tool call matched.
def evaluate_function_calls(df, policy, model, i=0, verbose=False):
    records = []

    # Use ThreadPoolExecutor to process rows in parallel
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_row, row_number, row, policy, model, i, verbose): row_number for row_number, row in df.iterrows()}
        for future in futures:
            record = future.result()
            records.append(record)


    df = pd.DataFrame(records)
    df['cleaned_transcript'] = df['transcript'].apply(filter_messages)
    total_accuracy = df['is_correct'].mean()
    return df, total_accuracy

# Spreadsheet of cases: the customer details, the expected final function, and its arguments.
# The commented print would show the first rows before the eval runs.
eval_df = pd.read_csv(os.path.join(BASE_DIR, 'evals', 'policyEvals.csv'))
# print(eval_df.head())

# One case, side by side: the spreadsheet row, and the actual function, inputs, and transcript.
# User lines print blue. Every other line prints red. eval_df and df are the tables below.
def display_row(index):
    eval_row = eval_df.iloc[index]
    df_row = df.iloc[index][["actual_function", "actual_inputs", "is_correct", "cleaned_transcript"]]
    transcript_list = df_row["cleaned_transcript"]

    print("Eval DataFrame Row:")
    print(eval_row)
    print("\nDataFrame Columns:")
    print("actual_function:", df_row["actual_function"])
    print("actual_inputs:", df_row["actual_inputs"])
    print("is_correct:", df_row["is_correct"])
    print("transcript:")
    for entry in transcript_list:
        role = entry["role"] if isinstance(entry, dict) else getattr(entry, "role", None)
        color = "blue" if role == "user" else "red"
        print(colored(str(entry), color))

# Grade the generated routine with the non-reasoning model, then print the accuracy.
# display(df) would show every row. display_row(8) shows one case instead.
df, accuracy = evaluate_function_calls(eval_df, flight_cancellation_routine, NON_REASONING_MODEL)

# Display the accuracy as a mini header
display(Markdown(f"### Accuracy: {accuracy:.2%}"))

# display(df)

display_row(8)

# One completion, optionally forced into a JSON schema.
# Returns the reply text. The improvement loop below is what would pass OUTPUT_SCHEMA.
def get_openai_response(messages, model, response_format=None):
    try:
        if response_format:
            response = create_chat_completion(
                model,
                messages,
                response_format={"type": "json_schema", "json_schema": response_format}
            )
        else:
            response = create_chat_completion(model, messages)
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")


# Schema the improvement call would require: one key, final_answer, and no extras.
# strict means the model must match this object. The loop reads that key as the new routine.
OUTPUT_SCHEMA = {
                    "name": "policy_output",
                    "schema": {
                    "type": "object",
                    "properties": {
                        "final_answer": { "type": "string" }
                    },
                    "required": ["final_answer"],
                    "additionalProperties": False
                    },
                    "strict": True
                }

# Opening message for the meta-prompt: improve the routine using the original policy and TOOLS.
# The routine text and the eval table are not in this message. The unused loop below appends them.
# The model is told to return only the improved policy, under the final_answer key.
start_reasoning_model_message = [
    {
        "role": "user",
        "content": f"""# Instructions
You are an agent that is responsible for improving the quality of instructions that are provided to a customer service LLM agent. 
Your task is to improve the instructions that are provided to the LLM agent in order to increase accuracy on a test set while adhering to the initial policy. 

## Criteria
- Analyze the existing instructions and the results of the eval. Understand which behaviors lead to failures.
- For example, if the LLM agent is not asking for the booking reference when it is needed, you should add a step to ask for the booking reference.
- Improve the instructions to address the gaps in the eval results.
- Ensure changes made are compliant with the original policy.
- Only use the tools provided.
- Use the functions provided to the best of your ability to ensure the LLM agent can handle the customer service requests effectively. Including gathering data where necessary.
- Try changing the format if this formatting doesn't work well - consider basic XML (e.g. <step> <substep> <if> <case>) or markdown as alternatives.

You will be provided with 4 items:
1) The ground-truth policy for the customer service agent containing detailed instructions on how to handle flight cancellations and changes.
2) Full list of available functions.
3) A routine instruction set.
4) A results that shows the LLMs performance on a test set using this routine instruction set. This dataset contains columns showing:
    - request: This is the initial user request. 
    - expected_function: This is the function we expect the LLM to call at the end of the conversation. 
    - expected_input: This is the input we expect the LLM to provide to the function at the end of the conversation.
    - actual_function: This is the final function the LLM called using the current instructions.
    - actual_input: These are the function parameters the LLM provided based on the current instructions.
    - transcript: This is the conversation transcript between the user and the LLM agent. 
    - is_correct: True/False value depending on if the model responded correctly

You may be provided with a history of edits and evaluations. You can use this information to understand what has been tried before and what has worked or not worked.

# Data

## 1. Original policy
{flight_cancellation_policy}

## 2. Functions
{TOOLS}

# Conclusion

Return the improved policy exactly as written within the defined JSON. Remove all parts from the LLM's answer that are not part of the policy, and do not create additional keys.
"""
     }
]

# Tokenizer for the unused loop's length check. It counts the message contents joined together.
encoding = tiktoken.get_encoding("o200k_base")

def num_tokens_from_messages(messages):
    entire_input = ""
    for message in messages:
        entire_input += message["content"] + " "
    tokens = encoding.encode(entire_input)
    return len(tokens)

# The improvement loop stays in this unused string so it does not run.
# Three times it would send the latest routine and eval table to the reasoning model,
# read final_answer as the next routine, grade that with the non-reasoning model,
# and keep older tables only while they fit under 120000 tokens. Then it would plot
# accuracy and print the routine from the best run. The banner inside says not to run it.
'''
# =======================================================================================================
# ========================== WARNING: CODE BELOW IS FOR LEARNING PURPOSES ONLY ==========================
# ========================== IT WILL CONSUME A LOT OF TOKENS AND TIME ===================================
# ========================== DO NOT RUN THIS CODE =======================================================
# =======================================================================================================

"""
# start with data from first run
routines = [flight_cancellation_routine]
results = [df]
accuracies = [round(accuracy * 100, 2)]
reasoning_model_messages = start_reasoning_model_message.copy()

MAX_TOKENS = 120000

for i in range(3):
    display(Markdown(f"## Iteration {i+1}"))
    
    # Build a candidate message with the most recent eval (full table)
    prev_results = results[-1]
    pf = prev_results.drop(columns=['transcript'])

    new_eval_content = (
        f"## 3. Routine instructions:\n"
        f"{routines[-1]}\n"
        f"## 4. Results table:\n"
        f"{pf.to_json(orient='records')}\n"
    )
    
    # Check token count before adding the newest eval
    candidate_messages = reasoning_model_messages + [{"role": "user", "content": new_eval_content}]
    if num_tokens_from_messages(candidate_messages) <= MAX_TOKENS:
        reasoning_model_messages.append({"role":"user", "content": new_eval_content})
    else:
        # If we can't even fit the newest eval, consider truncation or error handling
        # For simplicity, we skip truncation logic here
        print("excluding eval content {num_tokens_from_messages(candidate_messages)}")
        pass

    print(f"num tokens {num_tokens_from_messages(reasoning_model_messages)}")
    print(f"len messages {len(reasoning_model_messages)}")


    # Get the updated routine from the metaprompting assistant
    temp_routine_json = get_openai_response(reasoning_model_messages
                                            , REASONING_MODEL
                                            ,response_format=OUTPUT_SCHEMA)
    #temp_routine_str = temp_routine_json.strip("json```").strip("```")
    new_routine = json.loads(temp_routine_json)["final_answer"]
    routines.append(new_routine)

    eval_df = pd.read_csv('evals/policyEvals.csv')

    # Evaluate the function calls with the current policy on the gpt-4o model
    eval_df, accuracy = evaluate_function_calls(
        eval_df,
        new_routine,
        NON_REASONING_MODEL,
        i
    )
    accuracies.append(round(accuracy * 100, 2))
    results.append(eval_df)
    display(Markdown(f"### Accuracy: {accuracy:.2%}"))

    #list the IDs of the failed rows
    failed_ids = eval_df[eval_df['is_correct'] == False].index.tolist()
    display(eval_df.loc[failed_ids])
    eval_df.to_csv(f'evals/results_run_{i+1}.csv', index=False)

    # Instantiate fresh reasoning model message
    reasoning_model_messages = start_reasoning_model_message.copy()

    # Attempt to include older examples (omitting 'transcript') within token limit
    older_results = results[:-1][::-1]  # all except the newest, reversed for most recent first
    for old_eval_df in older_results:
        if 'transcript' in old_eval_df.columns:
            truncated_df = old_eval_df.drop(columns=['transcript','cleaned_transcript'])
        else:
            truncated_df = old_eval_df

        old_content = "## Older eval (no transcript):\n" + truncated_df.to_json(orient='records')
        candidate_messages = reasoning_model_messages + [{"role": "user", "content": old_content}]
        if num_tokens_from_messages(candidate_messages) <= MAX_TOKENS:
            reasoning_model_messages.append({"role": "user", "content": old_content})
        else:
            # If we exceed token limits, stop adding older examples
            break

# Plot accuracy over runs
plt.plot(range(1,len(accuracies)+1), accuracies, marker='o')
plt.title('Accuracy over time')
plt.xlabel('Run number')
plt.ylabel('Accuracy')
plt.savefig('metaprompt_accuracy.png')
plt.show()

# Print best routine
best_routine = routines[accuracies.index(max(accuracies))]
display(Markdown(f"## Best Routine\n{best_routine}"))

routines[accuracies.index(max(accuracies))]
"""
'''