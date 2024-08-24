"""
Summarizes the extracted markdown into one sentence.
"""

import os
import time

import google.generativeai as genai


PROMPT = """UI Framework Documentation Summarizer
You are an AI assistant tasked with creating a brief summary of a markdown document describing an API for a UI framework. This summary will help another AI system quickly determine if the API is relevant for code generation tasks.
Input
You will receive the contents of a markdown document describing the API.
Output
Provide a concise summary of the document in 1 sentence focusing on what the API is relevant is for."""


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # type: ignore

model = genai.GenerativeModel("gemini-1.5-flash-latest")


def generate_refined_text(content: str):
  max_retries = 2
  backoff_factor = 2
  for attempt in range(max_retries):
    try:
      response = model.generate_content(PROMPT + "\n\n" + content)  # type: ignore
      return response.text
    except Exception as e:
      if attempt == max_retries - 1:
        raise
      wait_time = backoff_factor**attempt
      print(
        f"Attempt {attempt + 1} failed. Retrying in {wait_time} seconds...", e
      )
      time.sleep(wait_time)


def process_files():
  input_dir = "../gen/extracted_markdown"
  output_dir = "../gen/summarized_markdown"

  # Create output directory if it doesn't exist
  os.makedirs(output_dir, exist_ok=True)

  for filename in os.listdir(input_dir):
    if filename.endswith(".md"):
      input_path = os.path.join(input_dir, filename)
      output_path = os.path.join(output_dir, filename)

      print(f"Processing {filename}...")

      with open(input_path, encoding="utf-8") as infile:
        content = infile.read()

      try:
        refined_content = generate_refined_text(content)
        assert refined_content is not None

        with open(output_path, "w", encoding="utf-8") as outfile:
          outfile.write(refined_content)

        print(f"Refined content written to {output_path}")

      except Exception as e:
        print(f"Error processing {filename}: {e!s}")


if __name__ == "__main__":
  process_files()
