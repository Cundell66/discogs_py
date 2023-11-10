# discogs_py
 CS50 Discogs Collection Viewer

This is a web application that allows you to view and explore a Discogs collection folder.
It can retrieve data from the Discogs API and stores it in a local SQL folder - vinyl_records.db
It also randomly selects an entry in the specified Discogs collection folder and displays artist, title, sleeve artwork and tracklist of that random selected record.

Features
Randomly selects releases from your collection to provide a varied browsing experience
Shows the tracklist for each randomly selected release
Allows you to choose another random selection by clicking the "Random Pick" button
Clicking on Full Collection displays a table of basic information about each release in my Discogs collection
Clicking on Update accesses the Discogs API and at a rate limit of 60 calls per minute renews the whole SQL database

Technologies Used
Python
Flask
SQL
html

Getting Started
Get your Discogs API token by signing up for a free Discogs account at discogs.com. Then, create a .env file in the root directory and export your token, username and folder ID. Example:
discogsToken = "AAaAaAaAAAaaaaaaaAAAaAaaaAAaaAAaaaaAAaaa"
userName = "jackBauer"
folderID = 1111111;

Limitations:
despite storing album info at a local level the cover images are still held on Discogs servers - this can mean them failing to load or at the least being very slow.

