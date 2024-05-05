import mesop as me


@me.stateclass
class State:
  model1_input: str = ""
  model2_input: str = ""
  model1_response: str = ""
  model2_response: str = ""
  rating: int = 0
  reason: str = ""
  model1_selected: str = "gpt-3.5-turbo"
  model2_selected: str = "text-davinci-003"
  show_model1_code: bool = False
  show_model2_code: bool = False
  show_rating: bool = False


@me.page(path="/llm_compare", title="LLM Compare")
def page():
  state = me.state(State)
  with me.box(style=_STYLE_CONTAINER):
    with me.box(style=_STYLE_MAIN_HEADER):
      with me.box(style=_STYLE_TITLE_BOX):
        me.text(
          state.title,
          type="headline-6",
          style=me.Style(line_height="24px", margin=me.Margin(bottom=0)),
        )

    with me.box(style=_STYLE_MAIN_COLUMN):
      with me.box(style=_STYLE_INPUT_COLUMN):
        with me.box(style=_STYLE_MODEL_SELECTION):
          me.text("Model 1", style=_STYLE_MODEL_LABEL)
          me.select(
            options=[
              me.SelectOption(label="Chat-GPT Turbo", value="gpt-3.5-turbo"),
              me.SelectOption(
                label="Text-Davinci-003", value="text-davinci-003"
              ),
            ],
            style=_STYLE_MODEL_SELECT,
            value=state.model1_selected,
            on_selection_change=on_model1_select,
          )
          icon_button(
            icon="code",
            tooltip="Show code",
            label="Code",
            on_click=on_click_show_model1_code,
          )
        with me.box(style=_STYLE_INPUT_AREA):
          me.textarea(
            label="Model 1 Prompt",
            key=f"model1-{state.clear_prompt_count}",
            on_input=on_model1_input,
            style=_STYLE_INPUT_WIDTH,
          )
          me.button(
            label="Submit", type="flat", on_click=on_click_submit_model1
          )
          me.button(label="Clear", on_click=on_click_clear_model1)

      with me.box(style=_STYLE_INPUT_COLUMN):
        with me.box(style=_STYLE_MODEL_SELECTION):
          me.text("Model 2", style=_STYLE_MODEL_LABEL)
          me.select(
            options=[
              me.SelectOption(label="Chat-GPT Turbo", value="gpt-3.5-turbo"),
              me.SelectOption(
                label="Text-Davinci-003", value="text-davinci-003"
              ),
            ],
            style=_STYLE_MODEL_SELECT,
            value=state.model2_selected,
            on_selection_change=on_model2_select,
          )
          icon_button(
            icon="code",
            tooltip="Show code",
            label="Code",
            on_click=on_click_show_model2_code,
          )
        with me.box(style=_STYLE_INPUT_AREA):
          me.textarea(
            label="Model 2 Prompt",
            key=f"model2-{state.clear_prompt_count}",
            on_input=on_model2_input,
            style=_STYLE_INPUT_WIDTH,
          )
          me.button(
            label="Submit", type="flat", on_click=on_click_submit_model2
          )
          me.button(label="Clear", on_click=on_click_clear_model2)

      # Model Response Column
      with me.box(style=_STYLE_RESPONSE_COLUMN):
        with me.box(
          style=_STYLE_RESPONSE_AREA,
          key="model1_code_box",
          display="block" if state.show_model1_code else "none",
        ):
          me.markdown(
            _GPT_CODE_TEXT.format(
              content=state.model1_input, model=state.model1_selected
            )
          )
        with me.box(
          style=_STYLE_RESPONSE_AREA,
          key="model2_code_box",
          display="block" if state.show_model2_code else "none",
        ):
          me.markdown(
            _GPT_CODE_TEXT.format(
              content=state.model2_input, model=state.model2_selected
            )
          )
        with me.box(
          style=_STYLE_RESPONSE_AREA,
          key="model1_response_box",
          display="block" if state.model1_response else "none",
        ):
          me.markdown(state.model1_response)
        with me.box(
          style=_STYLE_RESPONSE_AREA,
          key="model2_response_box",
          display="block" if state.model2_response else "none",
        ):
          me.markdown(state.model2_response)

      # Rating
      with me.box(
        style=_STYLE_RATING_AREA,
        display="block" if state.show_rating else "none",
      ):
        me.text("Which response is better?")
        with me.box(style=me.Style(display="flex")):
          me.radio(
            options=[
              me.RadioOption(label="Model 1", value="1"),
              me.RadioOption(label="Model 2", value="2"),
            ],
            on_change=on_rating_change,
            value=str(state.rating),
          )
        me.textarea(
          label="Why?",
          on_input=on_reason_change,
          value=state.reason,
          style=_STYLE_INPUT_WIDTH,
        )
        with me.box(
          style=me.Style(
            display="flex",
            justify_content="space-between",
          )
        ):
          me.button(
            label="Submit", type="flat", on_click=on_click_submit_rating
          )
          me.button(label="Clear", type="flat", on_click=on_click_clear_rating)


# HELPERS


@me.component
def icon_button(*, icon: str, label: str, tooltip: str, on_click: Callable):
  """Icon button with text and tooltip."""
  with me.content_button(on_click=on_click):
    with me.tooltip(message=tooltip):
      with me.box(style=me.Style(display="flex")):
        me.icon(icon=icon)
        me.text(
          label, style=me.Style(line_height="24px", margin=me.Margin(left=5))
        )


_GPT_CODE_TEXT = """
python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="{model}",
  messages=[
    {{
      "role": "user",
      "content": "{content}"
    }}
  ],
  temperature=0.7,
  max_tokens=1024,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
)
print(response.choices[0].message.content)
```
""".strip()


# Event Handlers


def on_model1_input(e: me.InputEvent):
  state = me.state(State)
  state.model1_input = e.value


def on_model2_input(e: me.InputEvent):
  state = me.state(State)
  state.model2_input = e.value


def on_model1_select(e: me.SelectSelectionChangeEvent):
  """Event to select model 1."""
  state = me.state(State)
  state.model1_selected = e.value


def on_model2_select(e: me.SelectSelectionChangeEvent):
  """Event to select model 2."""
  state = me.state(State)
  state.model2_selected = e.value


def on_click_show_model1_code(e: me.ClickEvent):
  """Opens/Closes code for model 1."""
  state = me.state(State)
  state.show_model1_code = not state.show_model1_code


def on_click_show_model2_code(e: me.ClickEvent):
  """Opens/Closes code for model 2."""
  state = me.state(State)
  state.show_model2_code = not state.show_model2_code


def on_click_submit_model1(e: me.ClickEvent):
  """Submits prompt for model 1."""
  state = me.state(State)
  state.model1_response = "Response will be displayed here."
  yield


def on_click_submit_model2(e: me.ClickEvent):
  """Submits prompt for model 2."""
  state = me.state(State)
  state.model2_response = "Response will be displayed here."
  yield


def on_click_clear_model1(e: me.ClickEvent):
  state = me.state(State)
  state.clear_prompt_count += 1
  state.model1_input = ""
  state.model1_response = ""


def on_click_clear_model2(e: me.ClickEvent):
  state = me.state(State)
  state.clear_prompt_count += 1
  state.model2_input = ""
  state.model2_response = ""


def on_click_clear_rating(e: me.ClickEvent):
  state = me.state(State)
  state.rating = 0
  state.reason = ""


def on_click_submit_rating(e: me.ClickEvent):
  state = me.state(State)
  state.show_rating = False
  me.text(
    f"Thank you for the rating! You rated Model {state.rating} as better."
  )
  if state.reason:
    me.text(f"Your reason: {state.reason}")


def on_rating_change(e: me.RadioChangeEvent):
  state = me.state(State)
  state.rating = int(e.value)


def on_reason_change(e: me.InputEvent):
  state = me.state(State)
  state.reason = e.value


# STYLES


_STYLE_CONTAINER = me.Style(
  display="grid",
  grid_template_columns="5fr 2fr",
  grid_template_rows="auto 5fr",
  height="100vh",
)

_STYLE_MAIN_HEADER = me.Style(
  border=_DEFAULT_BORDER, padding=me.Padding.all(15)
)

_STYLE_MAIN_COLUMN = me.Style(
  border=_DEFAULT_BORDER,
  padding=me.Padding.all(15),
  overflow_y="scroll",
)

_STYLE_CONFIG_COLUMN = me.Style(
  border=_DEFAULT_BORDER,
  padding=me.Padding.all(15),
  overflow_y="scroll",
)

_STYLE_TITLE_BOX = me.Style(display="inline-block")

_STYLE_CONFIG_HEADER = me.Style(
  border=_DEFAULT_BORDER, padding=me.Padding.all(10)
)

_STYLE_STOP_SEQUENCE_CHIP = me.Style(margin=me.Margin.all(3))

_STYLE_MODAL_CONTAINER = me.Style(
  background="#fff",
  margin=me.Margin.symmetric(vertical="0", horizontal="auto"),
  width="min(1024px, 100%)",
  box_sizing="content-box",
  height="100vh",
  overflow_y="scroll",
  box_shadow=("0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"),
)

_STYLE_MODAL_CONTENT = me.Style(margin=me.Margin.all(30))

_STYLE_CODE_BOX = me.Style(
  font_size=13,
  margin=me.Margin.symmetric(vertical=10, horizontal=0),
  padding=me.Padding.all(10),
  border=me.Border.all(me.BorderSide(color="#e0e0e0", width=1, style="solid")),
)

_STYLE_INPUT_COLUMN = me.Style(
  display="grid",
  grid_template_rows="1fr 6fr",
  gap=15,
)

_STYLE_RESPONSE_COLUMN = me.Style(
  display="grid",
  grid_template_rows="1fr 1fr 5fr 5fr",
  gap=15,
)

_STYLE_MODEL_SELECTION = me.Style(
  display="flex", justify_content="space-between"
)
_STYLE_MODEL_LABEL = me.Style(font_weight="bold")
_STYLE_MODEL_SELECT = me.Style(width="100%")

_STYLE_INPUT_AREA = me.Style(display="flex", flex_direction="column", gap=10)
_STYLE_INPUT_WIDTH = me.Style(width="100%")

_STYLE_RESPONSE_AREA = me.Style(
  width="100%",
  padding=me.Padding.all(10),
  border=me.Border.all(me.BorderSide(color="#e0e0e0", width=1, style="solid")),
)

_STYLE_RATING_AREA = me.Style(
  display="grid",
  grid_template_rows="auto 1fr",
  gap=10,
  padding=me.Padding(top=20),
)

_DEFAULT_PADDING = me.Padding.all(15)
_DEFAULT_BORDER = me.Border.all(
  me.BorderSide(color="#e0e0e0", width=1, style="solid")
)
