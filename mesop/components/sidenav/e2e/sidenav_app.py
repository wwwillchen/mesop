import mesop as me


@me.page(path="/components/sidenav/e2e/sidenav_app")
def app():
  me.text("main area")
  with me.sidenav():
    me.text("sidenav")
