# -*- coding: utf-8 -*-
import subprocess
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from beets import config
from beets import dbcore
from beets import library
from beets.dbcore import types
import sys
import pylast

lastupdate_command = Subcommand('lastupdate', help='Update playtime based on recent lastfm activity')
def lastupdate(lib, opts, args):
    print ("This part updates playtimes")
    lastfm_update(lib)
lastupdate_command.func = lastupdate

class SuperPlug(BeetsPlugin):
    item_types = {
        'play_count':  types.INTEGER,
        'last_played': library.DateType(),
        'rating':      types.FLOAT,
    }
    def commands(self):
        return [lastupdate_command]

TRACK_SEPARATOR = " - "

total_updated = 0
total_found = 0
total_notupdated = 0

def split_artist_track(artisttitle):
    artisttitle = artisttitle.replace(" – ", " - ")
    artisttitle = artisttitle.replace("“", '"')
    artisttitle = artisttitle.replace("”", '"')

    (artist, title) = artisttitle.split(TRACK_SEPARATOR)
    artist = artist.strip()
    title = title.strip()
    # Validate
    if len(artist) == 0 and len(title) == 0:
        sys.exit("Error: Artist and title are blank")
    if len(artist) == 0:
        sys.exit("Error: Artist is blank")
    if len(title) == 0:
        sys.exit("Error: Title is blank")
    return (artist, title)



def process_tracks(lib, timestamp, artist, title, process):
    global total_updated
    global total_found
    global total_notupdated
    #total = len(tracks)
    # First try to query by musicbrainz's trackid
    #if trackid:
    #    song = lib.items(
    #        dbcore.query.MatchQuery('mb_trackid', trackid)
    #    ).get()

    # If not, try just artist/title
    query = dbcore.AndQuery([
        dbcore.query.SubstringQuery('artist', artist),
        dbcore.query.SubstringQuery('title', title)
    ])
    song = lib.items(query).get()
    # Last resort, try just replacing to utf-8 quote
    if song is None:
        title = title.replace("'", u'\u2019')
        query = dbcore.AndQuery([
            dbcore.query.SubstringQuery('artist', artist),
            dbcore.query.SubstringQuery('title', title)
        ])
        song = lib.items(query).get()

    if song is not None:
        if  process == 1:
            total_found += 1
            count = int(song.get('play_count', 0))
            lastplayed = int(song.get('last_played', 0))
            if int(timestamp) > lastplayed:
                count += 1
                song['play_count'] = count
                song['last_played'] = timestamp
                song.store()
                total_updated += 1
                print(str(song) + " updated with new last played of " + str(timestamp) + " and playcount of " + str(count))
            else:
                total_notupdated += 1
        if  process == 2:
            total_found += 1
            song['rating'] = 1
            song.store()
            total_updated += 1
            print(str(song) + " updated with rating of 1")
            
    return total_updated, total_found, total_notupdated

def get_recent_tracks(lib, username, rnumber):
    lastfm_apikey = config['lastupdate']['apikey'].as_str()
    lastfm_network = pylast.LastFMNetwork(
    api_key=lastfm_apikey,
    )
    recent_tracks = lastfm_network.get_user(username).get_recent_tracks(limit=rnumber)
    for i, track in enumerate(recent_tracks):
        timestamp = f"{track.timestamp}"
        artisttitle = f"{track.track}"
        artist,title = split_artist_track(artisttitle)
        process_tracks(lib, timestamp, artist, title, process=1)
    print("total found " + str(total_found) + " total updated " + str(total_updated) + " total not updated " + str(total_notupdated))
    return recent_tracks


def get_loved_tracks(lib, username, lnumber):
    lastfm_apikey = config['lastupdate']['apikey'].as_str()
    lastfm_network = pylast.LastFMNetwork(
    api_key=lastfm_apikey,
    )
    loved_tracks = lastfm_network.get_user(username).get_loved_tracks(limit=lnumber)
    for i, track in enumerate(loved_tracks):
        artisttitle = f"{track.track}"
        artist,title = split_artist_track(artisttitle)
        timestamp = "0" #hacky way of re-using process_tracks
        process_tracks(lib, timestamp, artist, title, process=2)
    print("total found " + str(total_found) + " total updated " + str(total_updated) + " total not updated " + str(total_notupdated))
    return loved_tracks

def lastfm_update(lib):
    lastfm_username = config['lastupdate']['user'].as_str()
    try:
        print(lastfm_username + " last played:")
        rtrackcount = config['lastupdate']['recent_trackcount'].get()
        get_recent_tracks(lib, lastfm_username, rtrackcount)
        total_updated = 0
        total_found = 0
        total_notupdated = 0
        print(lastfm_username + " loved tracks:")
        ltrackcount = config['lastupdate']['loved_trackcount'].get()
        get_loved_tracks(lib, lastfm_username, ltrackcount)
    except pylast.WSError as e:
        print("Error: " + str(e))

