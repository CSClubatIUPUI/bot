# CS Bot

This is the bot that lives on the CS Club's Slack.

## Running

You'll need Python 3.1+ and a [Slack API token](https://api.slack.com/tokens).

Run `pip install slackbot`.

Create a file named `config.json`, and write the following to it:

```json
{
  "api_key": "whatever your API token is"
}
```

Run `python cscbot.py`. It should print "Connecting..." and start listening as
the user you generated the API token for.

## Extending

Create a Python file in the `commands` directory. This file must export a class
named `Command`, which must extend the `lib.CommandHandler` class. The `Command`
class must take a single `bot` parameter (of type `cscbot.CSCBot`) and construct
its superclass by passing the `bot` parameter, along with a regex pattern (as a
string, not compiled) to trigger the command on, and a list of regex
parameter names.

The `Command` class must implement a method named `handle`, which accepts a
single `msg` parameter, of type `lib.Message`. The `msg` parameter will have a
`params` attribute, which will map `Command.params` to the regex matches of
`msg.text`.
