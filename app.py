from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index() -> str:
    """Homepage route"""
    return render_template("index.html", title="Welkom")

@app.route("/informatie")
def info() -> str:
    return '<h1>Dit hebben we jou te bieden:</h1><p>Piano, gitaar, drums, zang</p>'

@app.route("/contact")
def contact() -> str:
    return "<h1>Neem contact op</h1><p>Email: info@session.nl</p>"

@app.route("/cursist/<naam>")
def cursist(naam: str) -> str:
    return f"<h1>Dit is de pagina van {naam}</h1>"

if __name__ == "__main__":
    app.run(debug=True)