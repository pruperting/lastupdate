# lastupdate
Beets plugin to sync playdate from lastfm with local library.

# A Note

I am in no way a programmer, at best, I am a googler and cut and paster, so, expect bad code and no structure


This is a work-in-progress plugin for Beets that will pull a list of your 200 most recently played tracks from lastfm and then tries to update a played date field in beets with the played time of each of the 200 tracks. 
If the played date is newer than the current one (or it doesnt exist) for each track, it will also increment the playcount.
All this is to make the smartplaylist plugin more useful, so you can create smartplaylists based on how long ago a track was last played.

Eventually I plan to build this out into its own program to manage and create smartplaylists, including a music catagorisation tool that suggests songs that are similiar based on audio characteristics.

# Configuration
You need to add lastupdate to your plugins list in beets' config.yaml and then also the following to specify your username and API key
`
lastupdate:
    user: YOURLASTFMUSERNAME
    apikey: YOURLASTFMAPIKEY`

# Usage

To use run `beet lastupdate` (python3 only at this stage)

# Current Status
2021-02-14 Born on valentines day, love at first site. Currently, all this plugin does is get your last 200 played tracks and splits out the timestamp, artist and title into rows - but thats a start!

