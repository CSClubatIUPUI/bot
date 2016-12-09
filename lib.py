import re

class CommandHandler(object):
    def __init__(self, bot, regex, params):
        self.bot = bot
        self.regex = re.compile(regex)
        self.params = params

    # pylint: disable=W0613
    def handle(self, msg):
        raise NotImplementedError("Please implement CommandHandler.handle()")

class Message(object):
    def __init__(self, raw_msg, params):
        self.raw_msg = raw_msg
        self.params = params
        self.channel = raw_msg.body["channel"]
        self.user = raw_msg.body["user"]
        self.text = raw_msg.body["text"]

    def reply(self, msg):
        return self.raw_msg.reply(msg)
