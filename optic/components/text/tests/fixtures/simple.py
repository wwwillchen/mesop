import optic as op


@op.page(path="/components/text/tests/fixtures/simple")
def text():
    op.text(text="Hello, world!")
