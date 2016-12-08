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
    # 曲の一覧を取得
    rows = g.db.execute("select mu.music, ar.artist, fe.feeling \
                         from ns_music mu, ns_artist ar, ns_feeling fe \
                         where mu.artist=ar.id and mu.feeling=fe.id \
                         order by ar.artist;")
    for row in rows.fetchall():
        music_lists.append({"music": row["music"],
                           "artist": row["artist"],
                           "feeling": row["feeling"]})
    return render_template("show_music_all.html", lists=music_lists)


@app.route("/regist")
def regist():
    lists = [[], [],[]]
    
    # アーティスト情報をリストへ格納
    ar_rows = g.db.execute("select id, artist from ns_artist order by artist;")
    for ar_row in ar_rows.fetchall():
        lists[0].append({"id": ar_row["id"], "artist": ar_row["artist"]})

    # feeling情報をリストへ格納
    fe_rows = g.db.execute("select id, feeling from ns_feeling;")
    for fe_row in fe_rows.fetchall():
        lists[1].append({"id": fe_row["id"], "feeling": fe_row["feeling"]})

    # country情報をリストへ格納
    co_rows = g.db.execute("select id, country from ns_country")
    for co_row in co_rows.fetchall():
        lists[2].append({"id": co_row["id"], "country": co_row["country"]})
    # 登録画面へ遷移
    return render_template("regist.html", lists=lists)


@app.route("/regist/music", methods=["GET", "POST"])
def regist_music():
    if request.method == "POST":
        # 未記入がある場合はリダイレクト
        if not request.form["music"] or \
           not request.form["artist"] or \
           not request.form["feeling"]:
           flash("未記入の項目があります")
           return redirect(url_for("regist"))

        # 登録処理を行う
        else:
            sql = text("insert into ns_music (music, artist, feeling) \
                        values (:music, :artist, :feeling)")
            g.db.execute(sql,
                         music = request.form["music"],
                         artist = request.form["artist"],
                         feeling = request.form["feeling"])
            flash("登録が完了しました")
            return redirect(url_for("regist"))

    # 直リンクの場合はリダイレクト
    else:
        return redirect(url_for("regist"))


@app.route("/regist/artist", methods=["GET", "POST"])
def regist_artist():
    if request.method == "POST":
        # 未記入がある場合はリダイレクト
        if not request.form["new_artist"] or \
           not request.form["new_country"]:
            flash("未記入の項目があります")
            return redirect(url_for("regist"))

        # 登録処理を行う
        else:
            sql = text("insert into ns_artist (artist, country) \
                        values (:artist, :country);")
            g.db.execute(sql,
                         artist = request.form["new_artist"],
                         country = request.form["new_country"])
            flash("登録が完了しました")
            return redirect(url_for("regist"))

    # 直リンクの場合はリダイレクト
    else:
        return redirect(url_for("regist"))


@app.route("/")
def random_music():
    row = g.db.execute("select mu.music, ar.artist \
                         from ns_music mu, ns_artist ar \
                         where mu.artist = ar.id \
                         order by random() limit 1;")
    return render_template("random_music.html", row=row.fetchone())


if __name__ == "__main__":
    app.run()
