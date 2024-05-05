import mesop as me

# from transformers import pipeline


@me.stateclass
class State:
  text_input: str = ""
  sentiment: str = ""
  score: float = 0.0


# sentiment_model = pipeline("sentiment-analysis")


def analyze_sentiment(text):
  return "toxic", 1.0
  # result = sentiment_model(text)[0]
  # return result['label'], result['score']


def on_text_input(e: me.InputEvent):
  state = me.state(State)
  state.text_input = e.value


def on_analyze_click(e: me.ClickEvent):
  state = me.state(State)
  state.sentiment, state.score = analyze_sentiment(state.text_input)


@me.page(path="/sentiment", title="Sentiment Analysis Demo")
def app():
  state = me.state(State)

  with me.box(
    style=me.Style(
      padding=me.Padding(top=50, left=100, right=100, bottom=50),
      background="#E3F2FD",
    )
  ):
    with me.box(
      style=me.Style(
        background="white",
        padding=me.Padding.all(24),
        border_radius=10,
        box_shadow="0 4px 6px rgba(0,0,0,0.1)",
      )
    ):
      me.text(
        "Sentiment Analysis",
        type="headline-3",
        style=me.Style(margin=me.Margin(bottom=16)),
      )
      me.text(
        "Enter some text and click 'Analyze Sentiment' to predict if the sentiment is positive or negative.",
        style=me.Style(color="#666"),
      )

      me.box(style=me.Style(height=24))

      me.textarea(
        on_input=on_text_input,
        placeholder="Enter text here...",
        rows=5,
        max_rows=10,
        style=me.Style(width="100%", font_size=18),
      )

      me.box(style=me.Style(height=24))

      with me.box(
        style=me.Style(
          display="flex", flex_direction="row", justify_content="center"
        )
      ):
        me.button(
          "Analyze Sentiment",
          on_click=on_analyze_click,
          style=me.Style(
            background="#2196F3",
            color="white",
            border_radius=20,
            padding=me.Padding(left=24, right=24, top=12, bottom=12),
            font_size=18,
          ),
        )

      me.box(style=me.Style(height=32))

      if state.sentiment:
        sentiment_color = (
          "#4CAF50" if state.sentiment == "POSITIVE" else "#F44336"
        )
        with me.box(style=me.Style(text_align="center")):
          me.text(
            state.sentiment,
            style=me.Style(
              font_weight=700, font_size=24, color=sentiment_color
            ),
          )
          me.text(
            f"Confidence: {state.score:.3f}", style=me.Style(color="#666")
          )
