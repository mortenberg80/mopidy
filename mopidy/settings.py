CONSOLE_LOG_FORMAT = u'%(levelname)-8s %(asctime)s [%(threadName)s] %(name)s\n  %(message)s'
MPD_LINE_ENCODING = u'utf-8'
MPD_LINE_TERMINATOR = u'\n'
MPD_SERVER_HOSTNAME = u'localhost'
MPD_SERVER_PORT = 6600

BACKEND=u'mopidy.backends.despotify.DespotifyBackend'
#BACKEND=u'mopidy.backends.libspotify.LibspotifyBackend'

SPOTIFY_USERNAME = u''
SPOTIFY_PASSWORD = u''

try:
    from mopidy.local_settings import *
except ImportError:
    pass

