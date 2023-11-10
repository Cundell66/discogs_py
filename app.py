import os
# import time
from flask import Flask, render_template
from cs50 import SQL
import requests
import random
import math


app = Flask(__name__)

db = SQL("sqlite:///vinyl_records.db")

# import secrets from discogs.js which is not on github
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
    master = requests.get(masterURL + str(idNumber)).json()
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
                    "INSERT INTO albums (artist, title, year, description, cover_image, genres, label, release_id, master_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    contents["artists"][0]["name"],
                    contents["title"],
                    contents["year"],
                    ",".join(contents["formats"][0]["descriptions"]),
                    contents["cover_image"],
                    contents["genres"][0],
                    contents["labels"][0]["name"],
                    contents["id"],
                    contents["master_id"],
                )
        return render_template("database.html", result="Database updated successfully")
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
                    "INSERT INTO albums (artist, title, year, description, cover_image, genres, label, release_id, master_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    contents["artists"][0]["name"],
                    contents["title"],
                    contents["year"],
                    ",".join(contents["formats"][0]["descriptions"]),
                    contents["cover_image"],
                    contents["genres"][0],
                    contents["labels"][0]["name"],
                    contents["id"],
                    contents["master_id"],
            )
        return render_template("database.html", result="Database updated successfully")
    except Exception as e:
        return str(e)


@app.route("/collection", methods=["GET"])
def collection():
    albums = db.execute("SELECT * FROM albums ORDER BY artist, year")
    return render_template("collection.html", albums=albums)


@app.route("/database", methods=["GET"])
def database():
    return render_template("database.html", result="")
