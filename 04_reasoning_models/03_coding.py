import os
from dotenv import load_dotenv, find_dotenv

# Drop library warnings so the printed rewrite is the lesson.
import warnings
warnings.filterwarnings('ignore')

# Load OPENAI_API_KEY from a local .env. OpenAI() below takes this value as api_key.
_ = load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')

from openai import OpenAI
from rich import print

# One client. The live call uses the non-reasoning model.
# create_chat_completion turns reasoning off only for that name.
client = OpenAI(api_key=openai_api_key)
NON_REASONING_MODEL = 'gpt-6-luna'
REASONING_MODEL = 'gpt-5-nano'

# chat.completions.create returns a completion. Extra kwargs are accepted and unused in this file.
# reasoning_effort "none" is sent only when the model is NON_REASONING_MODEL.
def create_chat_completion(model, messages, **kwargs):
    request = {"model": model, "messages": messages, **kwargs}
    if model == NON_REASONING_MODEL:
        request["reasoning_effort"] = "none"
    return client.chat.completions.create(**request)

# One user prompt in, the reply text out. That text is choices[0].message.content.
def get_chat_completion(model, prompt):
    """
    Calls the OpenAI API to get a chat completion.

    :param model: The model to use for the completion.
    :param prompt: The prompt to send to the model.
    :return: The completion response from the model.
    """
    response = create_chat_completion(
        model,
        [{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

# A React interview-form prompt stays in this unused string so it does not call the API.
# Inside it, the non-reasoning call is commented out. The reasoning-model call would
# print that model's reply. The prompt asks for code only: a component named
# FeedbackForm that starts with "use client".
'''
react_demo_prompt = """Create an elegant, delightful React component for an Interview Feedback Form where:

1. The interviewer rates candidates across multiple dimensions using rubrics
2. Each rating must include specific evidence/examples
3. The final recommendation should auto-calculate based on a weighted scoring system
4. The UI should guide interviewers to give specific, behavioral feedback

The goal is to enforce structured, objective feedback gathering. A smart model should:
- Create a thoughtful rubric structure
- Add helpful prompts/placeholders
- Build in intelligent validation

Make sure to
 - Call the element FeedbackForm
 - Start the code with "use client"

Respond with the code only! Nothing else!"""

# non_reasoning_model_code = get_chat_completion(NON_REASONING_MODEL, react_demo_prompt)

# print(non_reasoning_model_code)

reasoning_model_code = get_chat_completion(REASONING_MODEL, react_demo_prompt)

print(reasoning_model_code)
'''

# A tangled process_orders, given to the model as source to clean.
# The comments inside this string are part of the code the model sees.
code_snippet = """
def process_orders(orders_list, settings={}, debug=False, notify_customer=True):
    results = []
    errors = []
    notifications = []
    # Process all orders
    for i in range(0, len(orders_list)):
        # Get order
        order = orders_list[i]
        try:
            # Validate order has required fields
            if 'id' in order and 'items' in order and 'customer' in order:
                # Check customer info
                if 'email' in order['customer'] and 'name' in order['customer']:
                    # Validate items
                    items_valid = True
                    total = 0
                    # Check each item
                    for item in order['items']:
                        if not ('product_id' in item and 'quantity' in item):
                            items_valid = False
                            errors.append(f"Invalid item in order {order['id']}")
                            if debug == True:
                                print(f"Debug: Invalid item found in order {order['id']}")
                        else:
                            # Calculate total
                            if 'price' in item:
                                total = total + (item['quantity'] * item['price'])
                            else:
                                items_valid = False
                                errors.append(f"Missing price in order {order['id']}")
                    # Process if items valid
                    if items_valid == True:
                        # Apply any discounts from settings
                        if settings != {} and 'discount' in settings:
                            total = total * (1 - settings['discount'])
                        # Create processed order
                        processed = {
                            'order_id': order['id'],
                            'customer_name': order['customer']['name'],
                            'customer_email': order['customer']['email'],
                            'total': total,
                            'items_count': len(order['items'])
                        }
                        results.append(processed)
                        # Send notification
                        if notify_customer == True:
                            try:
                                # Create notification
                                notification = {
                                    'to': order['customer']['email'],
                                    'subject': 'Order Processed',
                                    'total': total
                                }
                                notifications.append(notification)
                                if debug == True:
                                    print(f"Debug: Notification queued for order {order['id']}")
                            except Exception as e:
                                errors.append(f"Notification failed for order {order['id']}")
                else:
                    errors.append(f"Invalid customer data in order {order['id']}")
            else:
                errors.append(f"Missing required fields in order {order['id']}")
        except Exception as e:
            # Add general error
            errors.append(f"Error processing order {order['id']}: {str(e)}")
            if debug == True:
                print(f"Debug: Error processing order {order['id']}: {str(e)}")

    # Print debug summary
    if debug == True:
        print(f"Debug: Processed {len(results)} orders with {len(errors)} errors")
        print(f"Debug: Queued {len(notifications)} notifications")

    return {
        "processed_orders": results,
        "errors": errors,
        "notifications": notifications
    }
"""

# Ask the non-reasoning model for a rewrite, and print only that text.
prompt = f"""I have some code that I'd like you to clean up and improve. Return only the updated code that fixes the issues: {code_snippet}"""
non_reasoning_model_code = get_chat_completion(NON_REASONING_MODEL, prompt)
print(non_reasoning_model_code)

# The same rewrite on the reasoning model, then a third call that compares the two,
# stay in this unused string so this run only shows the non-reasoning rewrite.
'''
reasoning_model_code = get_chat_completion(REASONING_MODEL, prompt)
print(reasoning_model_code)

result = get_chat_completion(REASONING_MODEL,f"which code is better and why? Option 1: {non_reasoning_model_code}... or Option 2: {reasoning_model_code}")
print(result)
'''