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


@app.route("/all")
def show_music_all():
    music_lists = []
    rows = g.db.execute("select music.music, artist.artist, feeling.feeling \
                         from ns_music music, ns_artist artist, ns_feeling feeling \
                         where music.artist=artist.id and music.feeling=feeling.id")
    for row in rows.fetchall():
        music_lists.append({"music": row["music"],
                           "artist": row["artist"],
                           "feeling": row["feeling"]})


    return render_template("show_music_all.html", lists=music_lists)


if __name__ == "__main__":
    app.run()
