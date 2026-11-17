import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World2 10:04")
    return f"Hello {name}!"
    return body, 200, {"X-Custom-Header": "ravi_header"}

if __name__ == "__main__":
    # Local development fallback
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
