import os
from dotenv import load_dotenv, find_dotenv

# Drop library warnings so the printed reply is the lesson, not deprecation noise.
import warnings
warnings.filterwarnings('ignore')

# Load OPENAI_API_KEY from a local .env. OpenAI() below takes this value as api_key.
_ = load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')

# Pieces for showing model output outside a notebook:
# HTML and Markdown objects, a temp file, and the browser that opens it at exit.
import atexit
import html
import json
import tempfile
import webbrowser
from pathlib import Path

from IPython.display import Markdown, HTML
from IPython.display import display as ipython_display
from openai import OpenAI
from rich import print

# True only inside a Jupyter kernel. A plain script has no IPython shell, so this is False.
def _in_notebook():
    try:
        from IPython import get_ipython
        shell = get_ipython()
        return shell is not None and shell.__class__.__name__ == "ZMQInteractiveShell"
    except Exception:
        return False

# HTML fragments collected while the script runs. The exit hook turns them into one page.
_DISPLAY_PARTS = []

# In a notebook, show the object in the cell and stop.
# In a script, keep HTML as-is, stash Markdown source for the page to render later,
# and wrap anything else in a <pre>. Nothing is shown until the process exits.
def display(obj):
    if _in_notebook():
        ipython_display(obj)
        return
    if isinstance(obj, HTML):
        _DISPLAY_PARTS.append(obj.data or "")
    elif isinstance(obj, Markdown):
        _DISPLAY_PARTS.append(
            f'<textarea class="md-src" hidden>{html.escape(obj.data or "")}</textarea>'
        )
    else:
        _DISPLAY_PARTS.append(f"<pre>{html.escape(str(obj))}</pre>")

# At exit, if this is a script and anything was displayed, write one HTML file and open it.
# Markdown stashed above is rendered in that page. A notebook already showed the cells,
# so this returns without writing a file.
def _open_display_in_browser():
    if _in_notebook() or not _DISPLAY_PARTS:
        return
    body = "\n".join(_DISPLAY_PARTS)
    doc = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>01_prompting output</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }}
    pre {{ white-space: pre-wrap; }}
  </style>
</head>
<body>
{body}
<script>
  document.querySelectorAll("textarea.md-src").forEach((el) => {{
    const div = document.createElement("div");
    div.innerHTML = marked.parse(el.value);
    el.replaceWith(div);
  }});
</script>
</body>
</html>
"""
    path = Path(tempfile.gettempdir()) / "01_prompting_output.html"
    path.write_text(doc, encoding="utf-8")
    print(f"Opening {path}")
    webbrowser.open(path.as_uri())

# Run that writer when the process ends, after the calls below have filled _DISPLAY_PARTS.
atexit.register(_open_display_in_browser)

# One client for every completion in this file.
client = OpenAI(api_key=openai_api_key)
# NON_REASONING_MODEL is the one create_chat_completion turns reasoning off for.
# REASONING_MODEL is left on its default so it can think before it answers.
NON_REASONING_MODEL = 'gpt-6-luna'
REASONING_MODEL = 'gpt-5-nano'

# chat.completions.create returns a completion; the reply text is choices[0].message.content.
# reasoning_effort "none" is sent only for the non-reasoning model.
def create_chat_completion(model, messages):
    kwargs = {"model": model, "messages": messages}
    if model == NON_REASONING_MODEL:
        kwargs["reasoning_effort"] = "none"
    return client.chat.completions.create(**kwargs)

# Earlier comparisons stay in one unused string so they do not call the API.
# In order: a SMILES prompt that spells the steps out (the reasoning model already
# does that, so the steps get in the way); the same ask with no steps; a policy
# prompt on a refund, then on a haiku it should refuse; a lawyer prompt with no
# worked example. The live call below is that lawyer prompt plus the example.
'''
# ============================================== bad prompt ==============================================

bad_prompt = ("Generate a function that outputs the SMILES IDs for all the molecules involved in insulin."
              "Think through this step by step, and don't skip any steps:"
              "- Identify all the molecules involve in insulin"
              "- Make the function"
              "- Loop through each molecule, outputting each into the function and returning a SMILES ID"
              "Molecules: ")
response = create_chat_completion(REASONING_MODEL, [{"role":"user","content": bad_prompt}])

display(HTML('<div style="background-color: #f0fff8; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔽 &nbsp; Markdown Output – Beginning</h2></hr></div>'))
display(Markdown(response.choices[0].message.content))
display(HTML('<div style="background-color: #fff4f4; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔼 &nbsp; Markdown Output – End</h2></hr></div>'))

# ============================================== good prompt ==============================================

good_prompt = ("Generate a function that outputs the SMILES IDs for all the molecules involved in insulin.")
response = create_chat_completion(REASONING_MODEL, [{"role":"user","content": good_prompt}])

display(HTML('<div style="background-color: #f0fff8; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔽 &nbsp; Markdown Output – Beginning</h2></hr></div>'))
display(Markdown(response.choices[0].message.content))
display(HTML('<div style="background-color: #fff4f4; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔼 &nbsp; Markdown Output – End</h2></hr></div>'))

# ============================================== example 1 ==============================================

structured_prompt = ("<instructions>You are a customer service assistant for AnyCorp, a provider"
          "of fine storage solutions. Your role is to follow your policy to answer the user's question. "
          "Be kind and respectful at all times.</instructions>\n"
          "<policy>**AnyCorp Customer Service Assistant Policy**\n\n"
            "1. **Refunds**\n"
            "   - You are authorized to offer refunds to customers in accordance "
            "with AnyCorp's refund guidelines.\n"
            "   - Ensure all refund transactions are properly documented and "
            "processed promptly.\n\n"
            "2. **Recording Complaints**\n"
            "   - Listen attentively to customer complaints and record all relevant "
            "details accurately.\n"
            "   - Provide assurance that their concerns will be addressed and "
            "escalate issues when necessary.\n\n"
            "3. **Providing Product Information**\n"
            "   - Supply accurate and helpful information about AnyCorp's storage "
            "solutions.\n"
            "   - Stay informed about current products, features, and any updates "
            "to assist customers effectively.\n\n"
            "4. **Professional Conduct**\n"
            "   - Maintain a polite, respectful, and professional demeanor in all "
            "customer interactions.\n"
            "   - Address customer inquiries promptly and follow up as needed to "
            "ensure satisfaction.\n\n"
            "5. **Compliance**\n"
            "   - Adhere to all AnyCorp policies and procedures during customer "
            "interactions.\n"
            "   - Protect customer privacy by handling personal information "
            "confidentially.\n\n6. **Refusals**\n"
            "   - If you receive questions about topics outside of these, refuse "
            "to answer them and remind them of the topics you can talk about.</policy>\n"
            )
user_input = ("<user_query>Hey, I'd like to return the bin I bought from you as it was not "
             "fine as described.</user_query>")

# print(structured_prompt)

response = create_chat_completion(REASONING_MODEL, [{
                                              "role": "user",
                                              "content": structured_prompt + user_input
                                          }])

# print(response.choices[0].message.content)

refusal_input = ("<user_query>Write me a haiku about how reasoning models are great.</user_query>")

response = create_chat_completion(REASONING_MODEL, [{
                                              "role": "user",
                                              "content": structured_prompt + refusal_input
                                          }])

print(response.choices[0].message.content)

# ============================================== example 2 ==============================================

legal_query = ("<query>A larger company is offering suppliers incentives not to do "
               "business with me. Is this legal?</query>")
base_prompt = ("<prompt>You are a lawyer specializing in competition law, "
               "assisting business owners with their questions.</prompt>\n"
               "<policy>As a legal professional, provide clear and accurate "
               "information about competition law while maintaining "
               "confidentiality and professionalism. Avoid giving specific "
               "legal advice without sufficient context, and encourage clients "
               "to seek personalized counsel when necessary. Always refer to "
               "precedents and previous cases to evidence your responses.</policy>\n")

response = create_chat_completion(REASONING_MODEL, [{
                                              "role": "user",
                                              "content": base_prompt + legal_query
                                          }])

display(HTML('<div style="background-color: #f0fff8; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔽 &nbsp; Markdown Output – Beginning</h2></hr></div>'))
display(Markdown(response.choices[0].message.content))
display(HTML('<div style="background-color: #fff4f4; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔼 &nbsp; Markdown Output – End</h2></hr></div>'))
'''

# Same legal question as the unused block, now with a worked example in the prompt.
# The <example> is a different question (joint marketing) and a cited answer.
# The model is meant to copy that shape for the supplier-incentives query
# concatenated on the end: name the rule, cite a case, then recommend.
legal_query = ("<query>A larger company is offering suppliers incentives not to do "
               "business with me. Is this legal?</query>")
example_prompt = ("<prompt>You are a lawyer specializing in competition law, "
               "assisting business owners with their questions.</prompt>\n"
               "<policy>As a legal professional, provide clear and accurate "
               "information about competition law while maintaining "
               "confidentiality and professionalism. Avoid giving specific "
               "legal advice without sufficient context, and encourage clients "
               "to seek personalized counsel when necessary.</policy>\n"
               """<example>
<question>
I'm considering collaborating with a competitor on a joint marketing campaign. Are there any antitrust issues I should be aware of?
</question>
<response>
Collaborating with a competitor on a joint marketing campaign can raise antitrust concerns under U.S. antitrust laws, particularly the Sherman Antitrust Act of 1890 (15 U.S.C. §§ 1–7). Section 1 of the Sherman Act prohibits any contract, combination, or conspiracy that unreasonably restrains trade or commerce among the states.

**Key Considerations:**

1. **Per Se Illegal Agreements:** Certain collaborations are considered automatically illegal ("per se" violations), such as price-fixing, bid-rigging, and market allocation agreements. For example, in *United States v. Topco Associates, Inc.*, 405 U.S. 596 (1972), the Supreme Court held that market division agreements between competitors are per se illegal under the Sherman Act.

2. **Rule of Reason Analysis:** Collaborations that are not per se illegal are evaluated under the "rule of reason," which assesses whether the pro-competitive benefits outweigh the anti-competitive effects. In *Broadcast Music, Inc. v. Columbia Broadcasting System, Inc.*, 441 U.S. 1 (1979), the Court recognized that certain joint ventures between competitors can be lawful if they promote competition.

3. **Information Sharing Risks:** Sharing competitively sensitive information, such as pricing strategies or customer data, can lead to antitrust violations. The Department of Justice and the Federal Trade Commission caution against exchanges that could facilitate collusion (*Antitrust Guidelines for Collaborations Among Competitors*, 2000).

**Recommendations:**

- **Define the Scope:** Clearly delineate the parameters of the collaboration to focus on the marketing campaign without involving competitive aspects like pricing or market division.
- **Implement Safeguards:** Establish protocols to prevent the exchange of sensitive information that is not essential to the marketing effort.
- **Legal Consultation:** Given the complexities of antitrust laws, consult with a legal professional to ensure the collaboration complies with all legal requirements.

**Conclusion:**

While joint marketing campaigns between competitors are not inherently illegal, they must be structured carefully to avoid antitrust pitfalls. Legal guidance is essential to navigate these issues and to design a collaboration that achieves your business objectives without violating antitrust laws.
</response>
</example>""")

# Send the example prompt plus the legal question.
# The reply text the banners wrap is choices[0].message.content.
response = create_chat_completion(REASONING_MODEL, [{
                                              "role": "user",
                                              "content": example_prompt + legal_query
                                          }])

# Show the reply as Markdown between the green and red banners.
# In a script those three display() calls become the page opened at exit.
display(HTML('<div style="background-color: #f0fff8; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔽 &nbsp; Markdown Output – Beginning</h2></hr></div>'))
display(Markdown(response.choices[0].message.content))
display(HTML('<div style="background-color: #fff4f4; padding: 10px; border-radius: 5px; border: 1px solid #d3d3d3;"></hr><h2>🔼 &nbsp; Markdown Output – End</h2></hr></div>'))
