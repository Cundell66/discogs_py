import os

# import time
from flask import Flask, render_template, request, redirect
from cs50 import SQL
import requests
import random
import math

app = Flask(__name__)

db = SQL("sqlite:///vinyl_records.db")

# import secrets from .env which is not on github
app.config.from_pyfile("settings.py")

userName = os.getenv("userName")
discogsToken = os.getenv("discogsToken")
folderID = os.getenv("folderID")
totalItems = 355

# set urls for required routes
discogsURL = f"https://api.discogs.com/users/{userName}/collection/folders/{folderID}/releases?token={discogsToken}"
masterURL = "https://api.discogs.com/masters/"


# generate random number to select random title
def getRandomNumber(max):
    return math.floor(random.random() * max)


# steps used in both post and get gathered together in function
def fetchContents(itemNo, page):
    discogs = requests.get(discogsURL + "&page=" + str(page)).json()
    releases = discogs["releases"]
    totalItems = discogs["pagination"]["items"]
    contents = releases[itemNo]["basic_information"]
    idNumber = contents["master_id"]
    master = requests.get(masterURL + str(idNumber) + "?token=" + discogsToken).json()
    tracklist = master["tracklist"]
    return contents, tracklist, totalItems


def fetchAllContents():
    # Get the total number of pages
    response = requests.get(discogsURL).json()
    totalPages = response["pagination"]["pages"]

    allContents = []

    # Fetch all pages
    for page in range(1, totalPages + 1):
        response = requests.get(discogsURL + "&page=" + str(page)).json()
        releases = response["releases"]
        # Fetch and store details for each release
        for release in releases:
            contents = release["basic_information"]
            if contents["year"] == 0:
                idNumber = contents["master_id"]
                master = requests.get(
                    masterURL + str(idNumber) + "?token=" + discogsToken
                ).json()
                contents["year"] = master["year"]
            allContents.append(contents)
    return allContents


@app.route("/", methods=["GET", "POST"])
def home():
    global totalItems
    itemNo = getRandomNumber(totalItems)
    page = math.floor(itemNo / 49) + 1
    itemNo = itemNo % 49
    try:
        contents, tracklist, totalItems = fetchContents(itemNo, page)
        return render_template("index.html", contents=contents, tracklist=tracklist)
    except Exception as e:
        return render_template("index.html", contents=str(e))


@app.route("/update", methods=["GET"])
def update():
    try:
        allcontents = fetchAllContents()
        for i in range(len(allcontents)):
            contents = allcontents[i]
            release_id = contents["id"]
            existing_album = db.execute(
                "SELECT * FROM albums WHERE release_id = ?", (release_id,)
            )
            if not existing_album:
                db.execute(
                    "INSERT INTO albums (artist, artist_id, title, year, description, cover_image, genres, label, release_id, master_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    contents["artists"][0]["name"],
                    contents["artists"][0]["id"],
                    contents["title"],
                    contents["year"],
                    ",".join(contents["formats"][0]["descriptions"]),
                    contents["cover_image"],
                    contents["genres"][0],
                    contents["labels"][0]["name"],
                    contents["id"],
                    contents["master_id"],
                )
        return redirect("/collection")
    except Exception as e:
        return str(e)


@app.route("/rebuild", methods=["GET"])
def rebuild():
    try:
        db.execute("DELETE FROM albums")
        db.execute("DELETE FROM sqlite_sequence WHERE name = 'albums'")

        allcontents = fetchAllContents()
        for i in range(len(allcontents)):
            contents = allcontents[i]
            db.execute(
                "INSERT INTO albums (artist, artist_id, title, year, description, cover_image, genres, label, release_id, master_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                contents["artists"][0]["name"],
                contents["artists"][0]["id"],
                contents["title"],
                contents["year"],
                ",".join(contents["formats"][0]["descriptions"]),
                contents["cover_image"],
                contents["genres"][0],
                contents["labels"][0]["name"],
                contents["id"],
                contents["master_id"],
            )
        return redirect("/collection")
    except Exception as e:
        return str(e)


@app.route("/collection", methods=["GET"])
def collection():
    albums = db.execute("SELECT * FROM albums ORDER BY artist, year")
    return render_template("collection.html", albums=albums)


@app.route("/database", methods=["GET"])
def database():
    return render_template("database.html", result="")


@app.route("/delete", methods=["POST"])
def delete():
    album_id = request.form.get("id")
    if album_id:
        db.execute("DELETE FROM albums WHERE id = ?", album_id)
    return redirect("/collection")


@app.route("/lyrics", methods=["POST"])
def lyrics():
    bad_chars = [";", ":", "-", "!", "*", ",", "'"]
    artist = request.form.get("artist")
    title = request.form.get("title")
    print(artist, title)
    a = ""
    for i in artist:
        if i not in bad_chars:
            a += i
    t = ""
    for i in title:
        if i not in bad_chars:
            t += i
    return redirect(
        f"https://genius.com/albums/{a.replace(' ',' - ')}/{t.replace(' ',' - ')}"
    )


@app.route("/artist", methods=["POST"])
def artist():
    artist = request.form.get("artist")
    discogsURL = f"https://api.discogs.com/database/search?format=lp&artist={artist}&country=uk&token={discogsToken}"
    releases = requests.get(discogsURL).json()
    releases["results"].sort(
        key=lambda x: int(x["year"])
        if "year" in x and x["year"].isdigit()
        else float("inf")
    )
    # Filter the releases to return each title only once
    titles = set()
    unique_releases = []
    for release in releases["results"]:
        if release["title"] not in titles:
            titles.add(release["title"])
            unique_releases.append(release)

    return render_template("artist.html", releases=unique_releases, artist=artist)


@app.route("/tracks", methods=["POST"])
def tracks():
    artist = request.form.get("artist")
    cover = request.form.get("cover")
    title = request.form.get("title")
    idNumber = request.form.get("master_id")
    master = requests.get(masterURL + str(idNumber) + "?token=" + discogsToken).json()
    tracklist = master["tracklist"]
    return render_template("tracks.html", tracks=tracklist, title=title, cover=cover, artist=artist)

@app.route("/search", methods=["POST"])
def search():
    q = request.form.get("q")
    if q:
        albums = db.execute("SELECT * FROM albums WHERE artist LIKE ? ORDER BY year", "%" + q + "%")
    else:
        albums = []
    return render_template("search.html", albums=albums, q=q)
