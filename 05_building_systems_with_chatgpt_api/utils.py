import json
import os
from collections import defaultdict
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
from rich import print

_ = load_dotenv(find_dotenv())

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PRODUCTS_FILE = Path(__file__).with_name("products.json")


def get_completion_from_messages(messages,
                                 model="gpt-5-nano",
                                 temperature=1,
                                 max_completion_tokens=5000):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens,
    )
    return response.choices[0].message.content


def get_products():
    with open(PRODUCTS_FILE, "r") as file:
        return json.load(file)


def get_products_and_category():
    products_by_category = defaultdict(list)
    for product_info in get_products().values():
        category = product_info.get("category")
        name = product_info.get("name")
        if category and name:
            products_by_category[category].append(name)
    return dict(products_by_category)


def get_product_by_name(name):
    return get_products().get(name)


def get_products_by_category(category):
    return [product for product in get_products().values() if product["category"] == category]


def find_category_and_product_only(user_input, products_and_category):
    delimiter = "####"
    system_message = f"""
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Output a python list of objects, where each object has \
the following format:
    'category': <one of Computers and Laptops, \
    Smartphones and Accessories, \
    Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, \
    Audio Equipment, Cameras and Camcorders>,
OR
    'products': <a list of products that must be found in the allowed products below>

Where the categories and products must be found in \
the customer service query.
If a product is mentioned, it must be associated with \
the correct category in the allowed products list below.
If no products or categories are found, output an \
empty list.

Allowed products:
{json.dumps(products_and_category, indent=2)}

Only output the list of objects, with nothing else.
"""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_input}{delimiter}"},
    ]
    return get_completion_from_messages(messages)


def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        cleaned = input_string.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()
        cleaned = cleaned.replace("'", '"')
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None


def generate_output_string(data_list):
    output_string = ""

    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data:
                for product_name in data["products"]:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                for product in get_products_by_category(data["category"]):
                    output_string += json.dumps(product, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string


def get_products_from_query(user_msg):
    """Extract mentioned categories and products from a customer query."""
    return find_category_and_product_only(user_msg, get_products_and_category())


def get_mentioned_product_info(data_list):
    """Look up catalog details for extracted products and categories."""
    product_info = []

    if data_list is None:
        return product_info

    for data in data_list:
        try:
            if "products" in data:
                for product_name in data["products"]:
                    product = get_product_by_name(product_name)
                    if product:
                        product_info.append(product)
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                product_info.extend(get_products_by_category(data["category"]))
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return product_info


def answer_user_msg(user_msg, product_info):
    """Answer a customer query using retrieved product information."""
    delimiter = "####"
    system_message = """
You are a customer service assistant for a large electronic store. \
Respond in a friendly and helpful tone, with concise answers. \
Make sure to ask the user relevant follow-up questions.
"""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_msg}{delimiter}"},
        {"role": "assistant", "content": f"Relevant product information:\n{product_info}"},
    ]
    return get_completion_from_messages(messages)
