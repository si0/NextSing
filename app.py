from flask import Flask, g, request, render_template, url_for, redirect, flash
from sqlalchemy import create_engine, text


DEBUG = True
SECRET_KEY = "fwewppwf@@fkpw"
app = Flask(__name__)
app.config.from_object(__name__)
engine = create_engine("postgres://database@localhost/nextsing")


# DBリクエスト前に接続
@app.before_request
def before_request():
    g.db = engine.connect()


# DBリクエスト後に切断
@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
