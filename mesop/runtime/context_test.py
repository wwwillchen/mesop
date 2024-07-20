import pytest

from mesop.runtime.context import Context


def test_context_do_not_share_properties():
  print("classvars", vars(Context))
  c1 = Context(get_handler=lambda x: None, states={})
  c2 = Context(get_handler=lambda x: None, states={})
  print("c1", vars(c1))
  for key in c1.__dict__:
    if c1.__dict__[key] not in (None, False, True):
      assert c1.__dict__[key] is not c2.__dict__[key]

  assert False


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
