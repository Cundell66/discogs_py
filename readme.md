# CS50 Discogs Collection Viewer

#### Video Demo:  https://youtu.be/Ugz9eQc3_8I
#### Description:

## CS50 Discogs Collection Viewer

This is a web application that allows you to view and explore a Discogs collection folder.
It can retrieve data from the Discogs API and stores it in a local SQL folder - vinyl_records.db
It also randomly selects an entry in the specified Discogs collection folder and displays artist, title, sleeve artwork and tracklist of that random selected record.

### Features
On launch the app randomly selects a release from the collection folder to provide a varied listening experience.
It displays the Cover Image, Artist Name, Album Title, Year of Release, Label, Genre and the tracklist for the randomly selected release each page allows you to choose another random selection by clicking the **Random Pick** button on the Navigation Bar.
Clicking on **Full Collection** on the Navigation Bar displays a table of releases containing basic information - Cover Image, Artist Name, Album Title, Year of Release, Label, Genre - about each release in the selected Discogs folder.
Clicking on **Update Database** calls the Discogs API and checks for any new additions to to be inserted into the SQL database, when the update is complete the new collection page will be displayed
Clicking on **Rebuild Database** is the nuclear option and deletes all rows in the table albums and resets the SQL_sequence too, it then accesses the Discogs API and inserts all the albums in the selected folder.
Alongside every cover image are two buttons, the **Delete Album** button removes the entry from the SQL database, whilst the **Wiki Discography** button attempts to access the relevant Wikipedia page.
An artist search from the navigation bar retrieves all matches and partial matches from the database.
On the collection and search pages there are links to:
 the Genius lyrics site page for the album if there, 
 the wikipedia discography page, 
 a remove album link which will renove the album from the local database but not the collection folder on discogs.
 Clicking in the album title will open a page containing the tracklisting 
 and clicking on the artist name will reveal all the releases in the discogs database for that artist relased in the uk.

### Technologies Used
Python,
Flask,
SQL.
html,
CS50

### Getting Started
You can clone this repository. If you wish to access your own record collection you will need to get your Discogs API token by signing up for a free Discogs account at discogs.com.
Then, create a .env file in the root directory and store your token, username and folder ID. Example:
discogsToken = "AAaAaAaAAAaaaaaaaAAAaAaaaAAaaAAaaaaAAaaa"
userName = "jackBauer"
folderID = 1111111;

### Limitations:
Despite storing album info at a local level the cover images are still held on Discogs servers - this can mean them failing to load or at the least being very slow.



This is a web application that allows you to view and explore a Discogs collection folder.
It can retrieve data from the Discogs API and stores it in a local SQL folder - vinyl_records.db
It also randomly selects an entry in the specified Discogs collection folder and displays artist, title, sleeve artwork and tracklist of that random selected record.

Features
Randomly selects releases from your collection to provide a varied listening experience
Shows the tracklist for each randomly selected release
Allows you to choose another random selection by clicking the "Random Pick" button
Clicking on Full Collection displays a table of basic information about each release in my Discogs collection
Clicking on Update Database accesses the Discogs API and adds any new additions to the folder
Clicking on Rebuild Database accesses the Discogs API and at a rate limit of 60 calls per minute renews the whole SQL database
An artist search from the navigation bar retrieves all matches and partial matches from the database.
On the collection and search pages there are links to:
 the Genius lyrics site page for the album if there, 
 the wikipedia discography page, 
 a remove album link which will renove the album from the local database but not the collection folder on discogs.
 Clicking in the album title will open a page containing the tracklisting 
 and clicking on the artist name will reveal all the releases in the discogs database for that artist relased in the uk.


Technologies Used
Python
Flask
SQL
html
jinja

Getting Started
Get your Discogs API token by signing up for a free Discogs account at discogs.com. Then, create a .env file in the root directory and export your token, username and folder ID. Example:
discogsToken = "AAaAaAaAAAaaaaaaaAAAaAaaaAAaaAAaaaaAAaaa"
userName = "jackBauer"
folderID = 1111111;

Limitations:
despite storing album info at a local level the cover images are still held on Discogs servers - this can mean them failing to load or at the least being very slow.

