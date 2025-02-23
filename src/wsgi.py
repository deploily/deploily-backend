# -*- coding: utf-8 -*-

import os

from app import app


def is_debug_mode():
    """Get app debug status."""
    debug = os.environ.get("FLASK_DEBUG")
    if not debug:
        return os.environ.get("FLASK_ENV") == "development"
    return debug.lower() not in ("0", "false", "no")


FLASK_DEBUG = is_debug_mode()
FLASK_RUN_PORT = os.getenv("FLASK_RUN_PORT", "5000")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_RUN_PORT, debug=FLASK_DEBUG)
