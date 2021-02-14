# lastupdate
Beets plugin to sync playdate from lastfm with local library.

# A Note
I am in no way a programmer, at best, I am a googler and cut and paster, so, expect bad code and worse logic.

This is a work-in-progress plugin for Beets that will pull a list of your recently played tracks from lastfm and then tries to update a played date field `last_played` (as used by the mpdstats plugin) in beets with the played time of each of the tracks. If the played date is newer than the current one (or it doesnt exist) for each track, it will also increment the playcount.
All this is to make the smartplaylist plugin more useful, so you can create smartplaylists based on how long ago a track was last played.

Eventually I plan to build this out into its own program to manage and create smartplaylists, including a music catagorisation tool that suggests songs that are similiar based on audio characteristics. But that is a while off.

# Configuration
You need to add `lastupdate` to your plugins list in beets' config.yaml and then also add a new lastupdate section:
```
lastupdate:
    user: YOURLASTFMUSERNAME
    apikey: YOURLASTFMAPIKEY
    trackcount: HOW_MANY_LASTFMPLAYS_TO_PROCESS
```
# Usage
To use run `beet lastupdate` (python3 only at this stage).
The idea is you run this regularly (nightly) to keep your beets database in sync with your playcounts.

# To Do
I wrote this primarily to make the smartplaylist plugin more useful, but I suspect it wont work very well with the last_played field as it has no way of comparing that against the time when the playlists are updated. So I'll likely need to modify that plugin so this new field is useful.

# Current Status
2021-02-14 Born on valentines day, love at first site. Currently, all this plugin does is get your last 200 played tracks and splits out the timestamp, artist and title into rows - but thats a start!
2021-02-14 Well, its later on and after some Valentines day chocolate, I've actually got a working plugin. Its ugly as sin as the commit says, but it works with new plays and then doesn't overright when run again. It's really kinda neat.

