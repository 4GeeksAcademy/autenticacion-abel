import os
import sys

from app import app

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3001, debug=False, use_reloader=False)
