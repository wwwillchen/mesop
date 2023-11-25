import optic as op


@op.stateclass
class State:
    string: str = "a"


@op.on(op.ChangeEvent)
def change(action: op.ChangeEvent):
    state = op.state(State)
    state.string = action.value


@op.page(path="/components/text_input/e2e/text_input_app")
def app():
    op.text_input(label="Hello, world!", on_change=change)
    state = op.state(State)
    op.text(text=state.string)
