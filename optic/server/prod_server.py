import os
from flask import send_file
from .server import app, port
from rules_python.python.runfiles import runfiles  # type: ignore
from werkzeug.utils import safe_join


def get_path(path: str) -> str:
    p = runfiles.Create().Rlocation(safe_join("optic/web/src/app", path))
    print("**path", p)
    return p


@app.route("/")
def serve_root():
    return send_file(get_path("index.html"))


@app.route("/<path:path>")
def serve_file(path: str):
    if is_file_path(path):
        return send_file(get_path(path))
    else:
        return send_file(get_path("index.html"))


def run():
    app.run(host="0.0.0.0", port=port, use_reloader=False)


def is_file_path(path: str) -> bool:
    _, last_segment = os.path.split(path)
    return "." in last_segment


if __name__ == "__main__":
    run()
