# ```python
# import mesop as me

# class State:
#     left_model_name: str = "Bard"
#     right_model_name: str = "ChatGPT"
#     left_model_output: str = ""
#     right_model_output: str = ""
#     user_input: str = ""
#     rating: int = 0
#     reason: str = ""

# def on_user_input(event: me.InputEvent):
#     me.state(State).user_input = event.value

# def on_generate(event: me.ClickEvent):
#     state = me.state(State)
#     # Replace this with actual API calls to your LLM
#     state.left_model_output = f"Left model output: {state.user_input}"
#     state.right_model_output = f"Right model output: {state.user_input}"

# def on_rating_change(event: me.SelectSelectionChangeEvent):
#     me.state(State).rating = int(event.value)

# def on_reason_input(event: me.InputEvent):
#     me.state(State).reason = event.value

# @me.page(path="/", title="LLM Comparison")
# def app():
#     state = me.state(State)

#     with me.box(style=me.Style(display="flex", flex_direction="column", gap=20, padding=me.Padding.all(20))):
#         me.text("LLM Comparison", type="headline-4")

#         with me.box(style=me.Style(display="flex", gap=20)):
#             with me.box(style=me.Style(width="50%")):
#                 me.text(state.left_model_name, style=me.Style(font_weight=500))
#                 me.markdown(state.left_model_output)
#             with me.box(style=me.Style(width="50%")):
#                 me.text(state.right_model_name, style=me.Style(font_weight=500))
#                 me.markdown(state.right_model_output)

#         with me.box(style=me.Style(display="flex", flex_direction="column", gap=10)):
#             me.text("Which output is better?")
#             me.select(
#                 options=[
#                     me.SelectOption(label="Left", value="1"),
#                     me.SelectOption(label="Right", value="2"),
#                     me.SelectOption(label="Same", value="0"),
#                 ],
#                 on_selection_change=on_rating_change,
#             )
#             me.text("Reason")
#             me.textarea(on_input=on_reason_input)

#         with me.box(style=me.Style(display="flex", gap=10)):
#             me.textarea(label="Enter your prompt", rows=5, on_input=on_user_input)
#             me.button("Generate", on_click=on_generate)

#         me.text(f"Rating: {state.rating}")
#         me.text(f"Reason: {state.reason}")

# ```

# **Explanation:**

# 1. **State Class:**  A `State` class is defined to hold the application's data. This includes:
#    - `left_model_name`: The name of the left-hand side LLM.
#    - `right_model_name`: The name of the right-hand side LLM.
#    - `left_model_output`: The output from the left-hand side LLM.
#    - `right_model_output`: The output from the right-hand side LLM.
#    - `user_input`: The user's prompt input.
#    - `rating`: The user's rating of which output is better (1 for left, 2 for right, 0 for same).
#    - `reason`: The user's explanation for their rating.

# 2. **Event Handlers:** Several event handlers are defined to manage user interactions:
#    - `on_user_input`: Updates the `user_input` in the `State` when the user types into the prompt input box.
#    - `on_generate`:  Triggered when the "Generate" button is clicked. This is where you would replace the placeholder code with API calls to your chosen LLMs.
#    - `on_rating_change`: Updates the `rating` in the `State` when the user selects a rating from the dropdown.
#    - `on_reason_input`: Updates the `reason` in the `State` when the user enters text into the "Reason" textarea.

# 3. **Main App Component:** The `app` function is decorated with `@me.page(path="/", title="LLM Comparison")` to create the root component for the Mesop app. Inside the component:
#    - The UI is constructed using Mesop components: `box`, `text`, `textarea`, `button`, `select`, and `markdown`.
#    - The UI elements are dynamically populated using data from the `State` object.
#    - The event handlers are connected to the appropriate components.

# **To Use this App:**

# 1. **LLM API Integration:**  Replace the placeholder code inside the `on_generate` function with actual API calls to your chosen LLMs (Bard and ChatGPT, for example).  You'll need to obtain API keys or credentials for these services.
# 2. **Run Mesop:**  Save this code as a Python file (e.g., `llm_comparison.py`) and run it using `mesop llm_comparison.py`.  This will start a web server, and you can access the app in your browser.

# This app provides a basic framework for comparing LLM outputs. You can customize the appearance, add more features (e.g., side-by-side code execution), and integrate with different LLMs based on your needs.
