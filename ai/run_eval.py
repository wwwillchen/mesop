"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import concurrent.futures
import os

import google.generativeai as genai
from eval_model import EvalQuestion, eval_questions
from llm import generate_mesop_app, get_or_create_cache
from prompt import SYSTEM_PROMPT

EVAL_RUN_NAME = "r3"

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 32768,
  "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction=SYSTEM_PROMPT,
)


eval_dir = f"gen/eval/{EVAL_RUN_NAME}"
if not os.path.exists(eval_dir):
  os.makedirs(eval_dir)


def process_eval_question(eval_question: EvalQuestion):
  # chat_session = model.start_chat()
  try:
    response_text = generate_mesop_app(
      eval_question.question,
      model_name="gemini-1.5-flash",
      api_key=os.environ["GEMINI_FREE_API_KEY"],
    )
    # response_text = response.text
  except Exception as e:
    response_text = str(e)

  print(response_text)
  with open(
    f"{eval_dir}/{eval_question.name}.md", "w", encoding="utf-8"
  ) as output_file:
    output_file.write(response_text)


genai.configure(api_key=os.environ["GEMINI_FREE_API_KEY"])
get_or_create_cache()
print("start async")
# do this synchronously
# for eval_question in eval_questions[:2]:
#   process_eval_question(eval_question)
# get_or_create_cache()
with concurrent.futures.ThreadPoolExecutor() as executor:
  # Update this to how ever many eval questions you want to run:
  executor.map(process_eval_question, eval_questions[:5])
