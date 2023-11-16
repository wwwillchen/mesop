import protos.ui_pb2 as pb
from optic.component_helpers import insert_component


def foo_bar(*, foo: str):
    """
    This function creates a button component with a label and an on_click event.

    Args:
        label (str): The text to be displayed on the button.
        on_click (Callable[..., Any]): The function to be called when the button is clicked.
    """
    insert_component(
        data=pb.ComponentData(
            foo_bar=pb.FooBarComponent(
                foo=foo,
            )
        )
    )
