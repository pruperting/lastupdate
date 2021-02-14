import subprocess
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from beets import config

import sys
import pylast

lastupdate_command = Subcommand('lastupdate', help='Update playtime based on recent lastfm activity')
def lastupdate(lib, opts, args):
    print ("This part should update playcounts")
    lastfm_update()
lastupdate_command.func = lastupdate

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
    lastfm_apikey = config['lastupdate']['apikey'].as_str()
    lastfm_network = pylast.LastFMNetwork(
    api_key=lastfm_apikey,
    )
    recent_tracks = lastfm_network.get_user(username).get_recent_tracks(limit=number)
    for i, track in enumerate(recent_tracks):
        printable = track_and_timestamp(track)
        print(str(i + 1) + " " + printable)
    return recent_tracks

def lastfm_update():
    lastfm_username = config['lastupdate']['user'].as_str()
    print(lastfm_username + " last played:")
    try:
        get_recent_tracks(lastfm_username, 200)
    except pylast.WSError as e:
        print("Error: " + str(e))

