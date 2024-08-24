import os
from pathlib import Path


def concat_markdown_summaries():
  input_dir = Path("../gen/summarized_markdown/")
  output_file = Path("../gen/api_summary.txt")

  with output_file.open("w", encoding="utf-8") as outfile:
    for markdown_file in sorted(input_dir.glob("*.md")):
      with markdown_file.open("r", encoding="utf-8") as infile:
        file_name = markdown_file.stem
        file_segment = file_name.split("_")[-1]
        api_name = file_segment.replace("-", "_")
        outfile.write(api_name + ": " + infile.read())
        outfile.write("\n")


if __name__ == "__main__":
  concat_markdown_summaries()
