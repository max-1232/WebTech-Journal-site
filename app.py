from flask import Flask

app = Flask(__name__)

@app.route("/")
def index() -> str:
    """Homepage route"""
    return "<h1>Welkom bij mijn Flask app!<h1>"

if __name__ == "__main__":
    app.run(debug=True)