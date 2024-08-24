import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/text",
)
def text():
  with me.box(style=me.Style(
      background=me.theme_var("surface"),
      border_radius=12,
      padding=me.Padding.all(24),
      box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
      max_width=480,
      margin=me.Margin.symmetric(horizontal="auto", vertical=40,
  ))):
    with me.box(style=me.Style(display="flex", align_items="center", gap=12)):
      me.icon(icon="article", style=me.Style(color=me.theme_var("primary")))
      me.text(text="Elegant Card", type="headline-5", style=me.Style(
          color=me.theme_var("on-surface"),
          font_weight="bold"
      ))

    me.divider()

    me.text(text="This beautifully designed card showcases a modern approach to UI elements. With subtle shadows, rounded corners, and a consistent color palette, it provides a pleasing visual experience.",
            type="body-1", style=me.Style(
        color=me.theme_var("on-surface-variant"),
        margin=me.Margin.symmetric(vertical=16)
    ))

    with me.box(style=me.Style(display="flex", justify_content="flex-end", margin=me.Margin(top=20))):
      me.button("Learn More", on_click=card_action, type="flat", style=me.Style(
          border_radius=20,
          padding=me.Padding.symmetric(horizontal=16, vertical=8),
          background=me.theme_var("primary"),
          color=me.theme_var("on-primary"),
          text_transform="uppercase",
          letter_spacing=1
      ))

def card_action(e: me.ClickEvent):
    # Handle card action button click
    print("Card action button clicked")
