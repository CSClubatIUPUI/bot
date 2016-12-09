import re

from lib import CommandHandler

PATTERN_REGEX = r"^s\/([^\/]+)\/([^\/]+)[\/]?$"

class Command(CommandHandler):
    def __init__(self, bot):
        super().__init__(bot, PATTERN_REGEX, ["pattern", "replace"])
        self.last_messages = {}

    def handle_default(self, msg):
        if not msg.channel in self.last_messages:
            self.last_messages[msg.channel] = {}
        if re.match(PATTERN_REGEX, msg.text):
            return
        self.last_messages[msg.channel][msg.user] = msg.text

    def handle(self, msg):
        if not msg.channel in self.last_messages:
            return
        if not msg.user in self.last_messages[msg.channel]:
            return
        last_message = self.last_messages[msg.channel][msg.user]
        new_message = re.sub(msg.params["pattern"], msg.params["replace"], last_message)
        self.last_messages[msg.channel][msg.user] = new_message
        msg.reply(new_message)
