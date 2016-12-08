import re
import slackbot.bot as slackbot

bot = None
last_messages = {}

PATTERN_ALL = r".*"
PATTERN_REGEX = r"^s\/([^\/]+)\/([^\/]+)[\/]?$"

class Message:
    def __init__(self, raw_msg):
        self.channel = raw_msg.body["channel"]
        self.user = raw_msg.body["user"]
        self.text = raw_msg.body["text"]

class Bot:
    def __init__(self, slack_bot):
        self.slackbot = slack_bot
        self.slacker = self.get_slacker()
        self.users = self.get_user_list()

    def get_user(self, user_id):
        for user in self.users:
            if user["id"] == user_id:
                return user
        self.users.append(self.slacker.users.info(user_id))
        return self.users[-1]

    def get_user_list(self):
        response = self.slacker.users.list()
        return response.body["members"]

    def get_slacker(self):
        return self.slackbot.__getattribute__("_client").webapi

class CSCBot:
    def __init__(self):
        self.slackbot = slackbot.Bot()
        self.bot = Bot(self.slackbot)

    def on_message(self, raw_msg):
        msg = Message(raw_msg)
        if not msg.channel in last_messages:
            last_messages[msg.channel] = {}
        if not re.match(PATTERN_REGEX, msg.text):
            last_messages[msg.channel][msg.user] = msg.text

    def on_regex(self, raw_msg, pattern, replace):
        msg = Message(raw_msg)
        if not msg.channel in last_messages:
            return
        if not msg.user in last_messages[msg.channel]:
            return
        last_message = last_messages[msg.channel][msg.user]
        new_message = re.sub(pattern, replace, last_message)
        last_messages[msg.channel][msg.user] = new_message
        raw_msg.reply(new_message)

# Necessary because slackbot doesn't pass `self` to methods
@slackbot.respond_to(PATTERN_ALL)
@slackbot.listen_to(PATTERN_ALL)
def on_default(msg):
    return bot.on_message(msg)

@slackbot.respond_to(PATTERN_REGEX)
@slackbot.listen_to(PATTERN_REGEX)
def on_regex(msg, pattern, replace):
    return bot.on_regex(msg, pattern, replace)

def main():
    # pylint: disable=W0603
    global bot
    bot = CSCBot()
    print("Connecting...")
    try:
        bot.slackbot.run()
    except KeyboardInterrupt:
        print("Exiting.")

if __name__ == "__main__":
    main()
