import mesop as me


@me.stateclass
class State:
  article: str = ""
  summary: str = ""


def on_article_change(e: me.InputEvent):
  me.state(State).article = e.value


def on_summarize_click(e: me.ClickEvent):
  state = me.state(State)
  # Replace this with your actual summarization logic
  state.summary = f"Summary of article: '{state.article}'"
  yield


@me.page(path="/")
def app():
  state = me.state(State)

  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      padding=me.Padding.all(24),
      gap=24,
      background="#f0f4f8",
      height="100vh",
    )
  ):
    me.text("Text Summarizer", type="headline-3")

    with me.box(
      style=me.Style(
        background="white",
        padding=me.Padding.all(16),
        border_radius=10,
        box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
      )
    ):
      me.text("Enter your article", style=me.Style(font_weight=500))
      me.textarea(
        rows=10,
        label="Article",
        on_input=on_article_change,
      )
      me.button("Summarize", on_click=on_summarize_click)
      me.text(state.summary)
