PROMPT_INSTRUCTIONS = """
Your task is to write a Mesop app.

Instructions:
1. For the @me.page decorator, leave it empty like this `@me.page()`
2. Event handler functions cannot use lambdas. You must use functions.
3. Event handle functions only pass in the event type. They do not accept extra parameters.
4. For padding, make sure to use the the `me.Padding` object rather than a string or int.
5. For margin, make sure to use the the `me.Margin` object rather than a string or int.
6. For border, make sure to use the the `me.Border` and `me.BorderSide` objects rather than a string.
7. For buttons, prefer using type="flat", especially if it is the primary button.
8. Only output the python code.

Here is a description of the app I want you to write:

"""

# The GitHub discussions seems too noisy and adds a lot of tokens
# (e.g. release notes, back and forth with answering questions)
# so it's not being used for now.
# with open("gen/prompt_context/discussions.txt", encoding="utf-8") as file:
#   discussions = file.read()

with open("gen/prompt_context/api_docs.txt", encoding="utf-8") as file:
  api_docs = file.read()

SYSTEM_PROMPT = api_docs + PROMPT_INSTRUCTIONS
print(SYSTEM_PROMPT)
