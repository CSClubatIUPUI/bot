import importlib
import os
import slackbot.bot as slackbot
from lib import Message

bot = None
last_messages = {}

class Bot:
    """
    A wrapper around the slacker and slackbot APIs.
    """
    def __init__(self, slack_bot):
        self.slackbot = slack_bot
        self.slacker = self.get_slacker()
        self.users = self.get_user_list()

    def get_user(self, user_id):
        """
        Returns a user's info from the cache.
        Fetches a user from the server if not cached.
        """
        for user in self.users:
            if user["id"] == user_id:
                return user
        self.users.append(self.slacker.users.info(user_id))
        return self.users[-1]

    def get_user_list(self):
        """
        Returns a list of all users.
        """
        response = self.slacker.users.list()
        return response.body["members"]

    def get_slacker(self):
        """
        Returns the slackbot.Bot's slacker instance.
        """
        return self.slackbot.__getattribute__("_client").webapi

class CSCBot:
    """
    Main class, handles command loading from /commands
    """
    def __init__(self):
        self.slackbot = slackbot.Bot()
        self.bot = Bot(self.slackbot)
        self.commands = []
        self.init_commands()

    def init_commands(self):
        """
        Loads command modules from /commands
        """
        command_dir = "commands/"
        command_files = os.listdir(command_dir)
        for command_file in command_files:
            if not command_file.endswith(".py"):
                continue
            command = importlib.import_module("{}{}".format(command_dir, command_file.replace(".py", "")).replace("/", ".")).Command(self)
            self.commands.append(command)

    def on_message(self, raw_msg):
        """
        Message handler that parses and passes commands.
        """
        msg = Message(raw_msg, {})
        for command in self.commands:
            if "handle_default" in dir(command):
                command.handle_default(msg)
            regex_results = command.regex.findall(msg.text)
            if len(regex_results) > 0 and len(regex_results[0]) > 0:
                for index, param_name in enumerate(command.params):
                    msg.params[param_name] = regex_results[0][index]
                command.handle(msg)

@slackbot.respond_to(r".*")
@slackbot.listen_to(r".*")
def on_default(msg):
    """
    Wrapper around CSCBot.on_message, since the slackbot module doesn't pass
        the CSCBot instance properly.
    """
    return bot.on_message(msg)

def main():
    # pylint: disable=W0603
    global bot
    bot = CSCBot()
    print("Connecting...")
    try:
        bot.slackbot.run()
    except KeyboardInterrupt:
        # slackbot throws a nasty error if you SIGINT it
        print("Exiting.")

if __name__ == "__main__":
    main()
