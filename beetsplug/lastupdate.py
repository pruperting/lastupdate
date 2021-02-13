import subprocess
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand

import sys
import pylast

API_KEY = "c3e3a25d7295d0e9b712c5ad9f5fa319"
API_SECRET = "4417c92a23d24dfa2515540c3f69aad5"
lastfm_username = "prupertplum"
# You can use either use the password, or find the hash once and use that
lastfm_password_hash = pylast.md5("nU65Kj8E2V9T!N2")

lastfm_network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=lastfm_username,
    password_hash=lastfm_password_hash,
)


lastupdate_command = Subcommand('lsupdate', help='Update playtime based on recent lastfm activity')
def last_update(lib, opts, args):
    print "This part should update playcounts"
    lastfm_upddate()
lastupdate_command.func = last_update

class SuperPlug(BeetsPlugin):
    def commands(self):
        return [lastupdate_command]

def track_and_timestamp(track):
    return f"{track.timestamp}\t{track.track}"


def print_track(track):
    print(track_and_timestamp(track))

TRACK_SEPARATOR = " - "


def split_artist_track(artist_track):
    artist_track = artist_track.replace(" – ", " - ")
    artist_track = artist_track.replace("“", '"')
    artist_track = artist_track.replace("”", '"')

    (artist, track) = artist_track.split(TRACK_SEPARATOR)
    artist = artist.strip()
    track = track.strip()
    print("Artist:\t\t'" + artist + "'")
    print("Track:\t\t'" + track + "'")

    # Validate
    if len(artist) == 0 and len(track) == 0:
        sys.exit("Error: Artist and track are blank")
    if len(artist) == 0:
        sys.exit("Error: Artist is blank")
    if len(track) == 0:
        sys.exit("Error: Track is blank")

    return (artist, track)

def get_recent_tracks(username, number):
    recent_tracks = lastfm_network.get_user(username).get_recent_tracks(limit=number)
    for i, track in enumerate(recent_tracks):
        printable = track_and_timestamp(track)
        print(str(i + 1) + " " + printable)
    return recent_tracks

def lastfm_upddate():
    print(lastfm_username + " last played:")
    self._log.debug(u'Getting recently played tracks', item)
    try:
        get_recent_tracks(lastfm_username, 200)
    except pylast.WSError as e:
        print("Error: " + str(e))

