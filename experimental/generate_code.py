"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import re
from dataclasses import dataclass

import google.generativeai as genai

print(genai.__version__)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  # "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

# chat_session = model.start_chat()

with open("experimental/gen/prompt_preamble.txt") as file:
  prompt_preamble = file.read()


@dataclass
class Example:
  name: str
  prompt: str


def remove_code_block_markers(markdown_text: str):
  # This regex matches triple backticks followed optionally by 'python' and any whitespace, then captures everything until the closing triple backticks
  pattern = r"```python\s*(.*?)```"
  # Replace the matched pattern with just the captured group, effectively removing the backticks and language identifier
  cleaned_text = re.sub(pattern, r"\1", markdown_text, flags=re.DOTALL)
  return cleaned_text


with open("experimental/example_inputs.txt") as file:
  examples = [Example(*line.strip().split("|")) for line in file.readlines()]

INSTRUCTIONS = """
You are an expert Python developer and a world-class frontend engineer.

Follow these guidelines carefully:
- Do NOT be lazy. Fully write the code.
- Do NOT import any libraries except for mesop.
- Do NOT output anything EXCEPT for code. Do NOT output anything AFTER the code.
- Make it visually appealing.

Follow the following instructions and create a Mesop app.
""".strip()

for example in examples[2:3]:
  prompt = prompt_preamble + "\n" + INSTRUCTIONS + "\n" + example.prompt
  # print(prompt)
  response = model.generate_content(prompt, request_options={"timeout": 300})
  # response = chat_session.send_message(prompt)

  print(response.text)

  with open(f"experimental/gen/code/r2/{example.name}.py", "w") as file:
    file.write(remove_code_block_markers(response.text))

# print(chat_session.history)
