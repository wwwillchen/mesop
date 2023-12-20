from pydantic import validate_arguments

import mesop.components.sidenav.sidenav_pb2 as sidenav_pb
from mesop.component_helpers import insert_composite_component


@validate_arguments
def sidenav(
  *,
  key: str | None = None,
):
  """
  This function creates a sidenav.

  Args:
      label: The text to be displayed
  """
  return insert_composite_component(
    key=key,
    type_name="sidenav",
    proto=sidenav_pb.SidenavType(),
  )
