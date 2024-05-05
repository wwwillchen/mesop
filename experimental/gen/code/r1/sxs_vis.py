import mesop as me


@me.stateclass
class State:
  left_input: str = ""
  right_input: str = ""
  left_output: str = ""
  right_output: str = ""
  rating: int = 0
  reason: str = ""


def on_left_input_update(e: me.InputEvent):
  me.state(State).left_input = e.value


def on_right_input_update(e: me.InputEvent):
  me.state(State).right_input = e.value


def on_left_submit(e: me.ClickEvent):
  state = me.state(State)
  # Replace this with your actual LLM call
  state.left_output = f"Left LLM output for input: '{state.left_input}'"
  yield


def on_right_submit(e: me.ClickEvent):
  state = me.state(State)
  # Replace this with your actual LLM call
  state.right_output = f"Right LLM output for input: '{state.right_input}'"
  yield


def on_rating_change(e: me.SelectSelectionChangeEvent):
  me.state(State).rating = int(e.value)


def on_reason_change(e: me.InputEvent):
  me.state(State).reason = e.value


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
    me.text("LLM Comparison", type="headline-3")

    with me.box(
      style=me.Style(
        display="flex",
        flex_direction="row",
        gap=24,
      )
    ):
      with me.box(
        style=me.Style(
          width="50%",
          padding=me.Padding.all(16),
          background="white",
          border_radius=10,
          box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
        )
      ):
        me.text("Left LLM", style=me.Style(font_weight=500))
        me.textarea(
          rows=5,
          label="Input",
          on_input=on_left_input_update,
        )
        me.button("Submit", on_click=on_left_submit)
        me.text(state.left_output)
      with me.box(
        style=me.Style(
          width="50%",
          padding=me.Padding.all(16),
          background="white",
          border_radius=10,
          box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
        )
      ):
        me.text("Right LLM", style=me.Style(font_weight=500))
        me.textarea(
          rows=5,
          label="Input",
          on_input=on_right_input_update,
        )
        me.button("Submit", on_click=on_right_submit)
        me.text(state.right_output)

    with me.box(
      style=me.Style(
        display="flex",
        flex_direction="row",
        gap=24,
        align_items="center",
      )
    ):
      with me.box(
        style=me.Style(
          width="50%",
          padding=me.Padding.all(16),
          background="white",
          border_radius=10,
          box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
        )
      ):
        me.text("Rating", style=me.Style(font_weight=500))
        me.select(
          options=[
            me.SelectOption(label="1 - Much worse", value="1"),
            me.SelectOption(label="2 - Worse", value="2"),
            me.SelectOption(label="3 - Slightly worse", value="3"),
            me.SelectOption(label="4 - Same", value="4"),
            me.SelectOption(label="5 - Slightly better", value="5"),
            me.SelectOption(label="6 - Better", value="6"),
            me.SelectOption(label="7 - Much better", value="7"),
          ],
          on_selection_change=on_rating_change,
        )
      with me.box(
        style=me.Style(
          width="50%",
          padding=me.Padding.all(16),
          background="white",
          border_radius=10,
          box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
        )
      ):
        me.text("Reason", style=me.Style(font_weight=500))
        me.textarea(
          rows=3,
          on_input=on_reason_change,
          placeholder="Why is one LLM better than the other?",
        )
