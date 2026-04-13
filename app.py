from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index() -> str:
    """Homepage route"""
    return "<h1>Welkom bij de eerste flask site</h1>"

if __name__ == "__main__":
    app.run(debug=True)