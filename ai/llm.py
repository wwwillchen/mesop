import datetime
import time

import google.generativeai as genai
from google.generativeai import caching

with open("./gen/prompt_context/prompt.txt") as f:
  SYSTEM_INSTRUCTION = f.read()


generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 32768,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]


def make_model(api_key: str, model_name: str) -> genai.GenerativeModel:
  genai.configure(api_key=api_key)

  cache = get_or_create_cache()
  model = genai.GenerativeModel.from_cached_content(cached_content=cache)
  return model
  # return genai.GenerativeModel(
  #   model_name=model_name,
  #   system_instruction=SYSTEM_INSTRUCTION,
  #   safety_settings=safety_settings,
  #   generation_config=generation_config,
  # )


def get_or_create_cache() -> caching.CachedContent:
  # prompt: get or create a cache
  cache_list = list(caching.CachedContent.list())
  if cache_list:
    cache_list[0]
    assert cache_list[0].display_name == "mesop_context"

    cache = cache_list[0]
    print("reuse existing cache", cache)
  else:
    cache = create_cache()
    print("create new cache", cache)
  return cache


def create_cache() -> caching.CachedContent:
  # Create a cache with a 5 minute TTL
  return caching.CachedContent.create(
    model="models/gemini-1.5-flash-001",
    display_name="mesop_context",  # used to identify the cache
    system_instruction=SYSTEM_INSTRUCTION,
    ttl=datetime.timedelta(minutes=60),
  )


def generate_mesop_app(msg: str, model_name: str, api_key: str) -> str:
  model = make_model(api_key, model_name)
  start_time = time.time()
  response = model.generate_content(
    msg,
    request_options={"timeout": 120},
    safety_settings=safety_settings,
    generation_config=generation_config,
  )
  end_time = time.time()
  print(f"Time taken: {end_time - start_time} seconds")
  return response.text
