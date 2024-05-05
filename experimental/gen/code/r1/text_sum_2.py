import mesop as me


@me.stateclass
class State:
  input_text: str = ""
  summary_text: str = ""


def on_input(event: me.InputEvent):
  me.state(State).input_text = event.value


def on_summarize(event: me.ClickEvent):
  state = me.state(State)
  # Replace this with your actual summarization logic
  state.summary_text = "This is a placeholder summary."
  # ...


@me.page(path="/summarize", title="Text Summarization Tool")
def app():
  state = me.state(State)
  with me.box(style=me.Style(padding=me.Padding.all(24), background="#f0f4f8")):
    me.text("Text Summarization Tool", type="headline-3")
    me.textarea(
      label="Enter your article:",
      rows=10,
      on_input=on_input,
      style=me.Style(width="100%"),
    )
    me.button("Summarize", on_click=on_summarize, color="primary")
    me.box(style=me.Style(height=16))
    me.text("Summary:", style=me.Style(font_weight=500))
    me.textarea(
      value=state.summary_text,
      rows=5,
      readonly=True,
      style=me.Style(width="100%"),
    )
