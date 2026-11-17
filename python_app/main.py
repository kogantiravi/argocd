import os
from flask import Flask, make_response

app = Flask(__name__)

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World2 10:04")
    response = make_response(f"Hello {name}!")
    
    # Add custom headers here
    response.headers["X-Custom-Header"] = "MyValue_ravi"
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
