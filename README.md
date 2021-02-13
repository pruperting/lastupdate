# lastupdate
Beets plugin to sync playdate from lastfm with local library.

This pulls a list of your 200 most recently played files and then tries to update a played date field in beets with the played time of each of the 200 tracks. 
If the played date is newer than the current one (or it doesnt exist) for each track, it will also increment the playcount.
All this is to make the smartplaylist plugin more useful.

Eventually I plan to build this out into its own program to manage and create smartplaylists, including a music catagorisation tool that suggests songs that are similiar based on audio characteristics.
