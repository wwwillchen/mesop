import mesop as me


@me.page(path="/")
def app():
  with me.box(
    style=me.Style(
      background="#f0f4f8",
      height="100vh",
      display="grid",
      grid_template_rows="1fr 8fr",
      gap="24px",
    )
  ):
    header()
    main_area()


def header():
  with me.box(
    style=me.Style(
      background="#fff",
      border_radius="12px",
      box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
      padding=me.Padding.all(24),
    )
  ):
    me.text("LLM Playground", type="headline-4")


def main_area():
  with me.box(
    style=me.Style(
      background="#fff",
      border_radius="12px",
      box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
      padding=me.Padding.all(24),
      display="grid",
      grid_template_columns="1fr 1fr",
      gap="24px",
    )
  ):
    left_panel()
    right_panel()


def left_panel():
  with me.box(
    style=me.Style(display="flex", flex_direction="column", gap="16px")
  ):
    me.text("Input", style=me.Style(font_weight=500))
    me.textarea(
      rows=10,
      style=me.Style(width="100%"),
      placeholder="Enter your prompt here...",
    )
    me.button(
      "Send",
      color="primary",
      type="flat",
      style=me.Style(padding=me.Padding.all(16), font_size="18px"),
    )


def right_panel():
  with me.box(
    style=me.Style(display="flex", flex_direction="column", gap="16px")
  ):
    me.text("Output", style=me.Style(font_weight=500))
    me.markdown(
      """
# Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Maecenas sed diam eget risus varius blandit sit amet non magna.

Donec sed odio dui. Maecenas faucibus mollis interdum.
Duis mollis, est non commodo luctus, nisi erat porttitor ligula,
eget lacinia odio sem nec elit. Maecenas sed diam eget risus varius
blandit sit amet non magna. Donec ullamcorper nulla non metus
auctor fringilla. Aenean eu leo quam.
      """,
      style=me.Style(height="calc(100% - 64px)", overflow_y="auto"),
    )
