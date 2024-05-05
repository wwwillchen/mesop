import mesop as me


@me.stateclass
class State:
  uploaded_image: str = ""
  selected_style: str = "None"
  styled_image: str = ""


def on_image_upload(e: me.UploadEvent):
  state = me.state(State)
  state.uploaded_image = (
    f"data:{e.file.mime_type};base64,{e.file.getvalue().decode('base64')}"
  )


def on_style_change(e: me.SelectSelectionChangeEvent):
  me.state(State).selected_style = e.value


def on_apply_style(e: me.ClickEvent):
  state = me.state(State)
  # Replace this with your actual style transfer logic
  state.styled_image = f"Styled image with {state.selected_style} style"
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
    me.text("Image Style Transfer", type="headline-3")

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
        me.text("Upload Image", style=me.Style(font_weight=500))
        me.uploader(label="Choose Image", on_upload=on_image_upload)
        if state.uploaded_image:
          me.image(src=state.uploaded_image, style=me.Style(width="100%"))

      with me.box(
        style=me.Style(
          width="50%",
          padding=me.Padding.all(16),
          background="white",
          border_radius=10,
          box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
        )
      ):
        me.text("Select Style", style=me.Style(font_weight=500))
        me.select(
          options=[
            me.SelectOption(label="None", value="None"),
            me.SelectOption(label="Monet", value="Monet"),
            me.SelectOption(label="Van Gogh", value="Van Gogh"),
            # ... add more styles
          ],
          on_selection_change=on_style_change,
        )
        me.button("Apply Style", on_click=on_apply_style)
        if state.styled_image:
          me.image(src=state.styled_image, style=me.Style(width="100%"))
