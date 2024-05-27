import mesop as me

@me.page(path="/diff_edge_case")
def app():
    me.text("diff_edge_case")
    me.radio(options=[me.RadioOption(label="1", value="1",),
                      me.RadioOption(label="2", value="2",)], on_change=on_change)
    if me.state(State).value == "1":
        me.checkbox("checked")
    else: 
        me.checkbox("unchecked")


@me.stateclass
class State:
    value: str ="1"

def on_change(e: me.RadioChangeEvent):
    me.state(State).value = e.value
