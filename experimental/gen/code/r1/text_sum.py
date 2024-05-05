import mesop as me


@me.stateclass
class State:
  input_text: str = ""
  summary: str = ""


def on_input_text_change(e: me.InputEvent):
  me.state(State).input_text = e.value


def on_summarize_click(e: me.ClickEvent):
  state = me.state(State)
  # Replace this with your actual text summarization logic
  state.summary = "Summary of: " + state.input_text
  # Note: You'd need to implement a summarization function here
  # You can use libraries like `transformers` or `sumy` for this


@me.page(path="/")
def app():
  state = me.state(State)
  with me.box(style=me.Style(padding=me.Padding.all(24))):
    me.text("Text Summarizer", type="headline-3")
    me.textarea(label="Enter text", rows=10, on_input=on_input_text_change)
    me.button("Summarize", on_click=on_summarize_click)
    me.text("Summary:", style=me.Style(font_weight=500))
    me.textarea(value=state.summary, readonly=True)
