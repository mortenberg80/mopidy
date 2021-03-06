import asynchat
import logging

from mopidy import get_mpd_protocol_version, config
from mopidy.exceptions import MpdAckError
from mopidy.mpd.handler import MpdHandler

logger = logging.getLogger(u'mpd.session')

def indent(string, places=4, linebreak=config.MPD_LINE_TERMINATOR):
    lines = string.split(linebreak)
    if len(lines) == 1:
        return string
    result = u''
    for line in lines:
        result += linebreak + ' ' * places + line
    return result

class MpdSession(asynchat.async_chat):
    def __init__(self, server, client_socket, client_address, backend,
            handler_class=MpdHandler):
        asynchat.async_chat.__init__(self, sock=client_socket)
        self.server = server
        self.client_address = client_address
        self.input_buffer = []
        self.set_terminator(config.MPD_LINE_TERMINATOR.encode(
            config.MPD_LINE_ENCODING))
        self.handler = handler_class(session=self, backend=backend)
        self.send_response(u'OK MPD %s' % get_mpd_protocol_version())

    def do_close(self):
        logger.info(u'Closing connection with [%s]:%s', *self.client_address)
        self.close_when_done()

    def do_kill(self):
        self.server.do_kill()

    def collect_incoming_data(self, data):
        self.input_buffer.append(data)

    def found_terminator(self):
        data = ''.join(self.input_buffer).strip()
        self.input_buffer = []
        input = data.decode(config.MPD_LINE_ENCODING)
        logger.debug(u'Input: %s', indent(input))
        self.handle_request(input)

    def handle_request(self, input):
        try:
            response = self.handler.handle_request(input)
            self.handle_response(response)
        except MpdAckError, e:
            logger.warning(e)
            return self.send_response(u'ACK %s' % e)

    def handle_response(self, response):
        self.send_response(config.MPD_LINE_TERMINATOR.join(response))

    def send_response(self, output):
        logger.debug(u'Output: %s', indent(output))
        output = u'%s%s' % (output, config.MPD_LINE_TERMINATOR)
        data = output.encode(config.MPD_LINE_ENCODING)
        self.push(data)

    def stats_uptime(self):
        return self.server.uptime
