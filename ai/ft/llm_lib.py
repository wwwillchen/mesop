import datetime
import os
import re
from os import getenv
from typing import Literal, NamedTuple

import anthropic
import google.generativeai as genai
from openai import OpenAI

SYSTEM_INSTRUCTION_PART_1_PATH = "prompts/mesop_overview.txt"
SYSTEM_INSTRUCTION_PART_2_PATH = "prompts/mini_docs.txt"

with open(SYSTEM_INSTRUCTION_PART_1_PATH) as f:
  SYSTEM_INSTRUCTION_PART_1 = f.read()

with open(SYSTEM_INSTRUCTION_PART_2_PATH) as f:
  SYSTEM_INSTRUCTION_PART_2 = f.read()

SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTION_PART_1 + SYSTEM_INSTRUCTION_PART_2
PROMPT_PATH = "prompts/revise_prompt.txt"

with open(PROMPT_PATH) as f:
  REVISE_APP_BASE_PROMPT = f.read().strip()


class ApplyPatchResult(NamedTuple):
  has_error: bool
  result: str


def apply_patch(original_code: str, patch: str) -> ApplyPatchResult:
  # flash does some weird formatting.
  patch = patch.replace("```diff", "").replace("```", "")
  # Extract the diff content
  diff_pattern = r"<<<<<<< ORIGINAL(.*?)=======\n(.*?)>>>>>>> UPDATED"
  matches = re.findall(diff_pattern, patch, re.DOTALL)
  patched_code = original_code
  if len(matches) == 0:
    print("[WARN] No diff found:", patch)
    return ApplyPatchResult(True, "WARN: NO_DIFFS_FOUND")
  for original, updated in matches:
    original = original.strip()
    updated = updated.strip()

    # Replace the original part with the updated part
    new_patched_code = patched_code.replace(original, updated, 1)
    if new_patched_code == patched_code:
      return ApplyPatchResult(True, "WARN: DID_NOT_APPLY_PATCH")
    patched_code = new_patched_code

  return ApplyPatchResult(False, patched_code)


def adjust_mesop_app(
  code: str,
  msg: str,
  model=Literal[
    "gemini-pro",
    "gemini-flash",
    "deepseek",
    "sonnet",
    "gpt-4o-mini",
    "gpt-4o-mini-ft",
    "gpt-4o",
  ],
) -> str:
  if model == "deepseek":
    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=getenv("OPEN_ROUTER_API_KEY"),
    )
    return adjust_mesop_app_openai_client(
      code, msg, client, model="deepseek/deepseek-coder"
    )
  elif model.startswith("gpt-4o-mini"):
    client = OpenAI(
      api_key=getenv("OPENAI_API_KEY"),
    )
    if model.endswith("-ft"):
      model = "ft:gpt-4o-mini-2024-07-18:personal::9yoxJtKf"
    return adjust_mesop_app_openai_client(code, msg, client, model=model)
  elif model == "gpt-4o":
    client = OpenAI(
      api_key=getenv("OPENAI_API_KEY"),
    )
    return adjust_mesop_app_openai_client(
      code, msg, client, model="gpt-4o-2024-08-06"
    )
  elif model == "sonnet":
    return adjust_mesop_app_anthropic_client(
      code, msg, model="claude-3-5-sonnet-20240620"
    )
  raise Exception(f"Unknown model: {model}")


def adjust_mesop_app_gemini(code: str, msg: str, model: str) -> str:
  model = make_gemini_model(model=model)
  response = model.generate_content(
    REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
      "<APP_CHANGES>", msg
    ),
    request_options={"timeout": 120},
    safety_settings=safety_settings,
    generation_config=generation_config,
  )

  llm_output = response.text.strip()
  print("[INFO] LLM output:", llm_output)
  return llm_output


# Fireworks client
# client = OpenAI(
#     base_url = "https://api.fireworks.ai/inference/v1",
#     api_key=getenv("FIREWORKS_API_KEY"),
# )

# Groq client
# client = OpenAI(
#     base_url="https://api.groq.com/openai/v1",
#     api_key=getenv("GROQ_API_KEY")
# )

# ollama client
# client = OpenAI(
#     base_url = 'http://localhost:11434/v1',
#     api_key='ollama', # required, but unused
# )

# together client
# client = OpenAI(
#   api_key=os.environ.get("TOGETHER_API_KEY"),
#   base_url="https://api.together.xyz/v1",
# )


def adjust_mesop_app_anthropic_client(code: str, msg: str, model: str) -> str:
  client = anthropic.Anthropic()

  client.beta.prompt_caching.messages.create(
    model=model,
    max_tokens=8_000,
    system=[
      {
        "type": "text",
        "text": SYSTEM_INSTRUCTION,
        "cache_control": {"type": "ephemeral"},
      }
    ],
    messages=[
      {
        "role": "user",
        "content": REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
          "<APP_CHANGES>", msg
        ),
      },
    ],
  )


def adjust_mesop_app_openai_client(
  code: str, msg: str, client: OpenAI, model: str
) -> str:
  completion = client.chat.completions.create(
    model=model,
    max_tokens=10_000,
    messages=[
      {
        "role": "system",
        "content": SYSTEM_INSTRUCTION,
      },
      {
        "role": "user",
        "content": REVISE_APP_BASE_PROMPT.replace("<APP_CODE>", code).replace(
          "<APP_CHANGES>", msg
        ),
      },
    ],
  )
  print("[INFO] LLM output:", completion.choices[0].message.content)
  llm_output = completion.choices[0].message.content
  return llm_output
