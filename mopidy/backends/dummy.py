from mopidy.backends import BaseBackend

class DummyBackend(BaseBackend):
    def __init__(self, *args, **kwargs):
        super(DummyBackend, self).__init__(*args, **kwargs)

    def url_handlers(self):
        return [u'dummy:']

    def _next(self):
        return True

    def _pause(self):
        return True

    def _play(self):
        return True

    def _play_id(self, songid):
        return True

    def _play_pos(self, songpos):
        return True

    def _previous(self):
        return True

    def _resume(self):
        return True
