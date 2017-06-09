import os
import time
import datetime
import gspread
import rollcall_behavior
from slackclient import SlackClient
from oauth2client.service_account import ServiceAccountCredentials

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">:"
COMMAND = "do your thing"

# instantiate Slack clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# obtain Google sheets credentials and open the spreadsheet
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('rollcall_creds.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1UuD0q08bbdMjnJrb85Uwfbb46SCJWIWkHi1JH-9QA_0/edit#gid=1528692932")

# listen for and handle the commands
def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "That's not my thing. Use the *" + COMMAND + \
               "* command."
    if command.startswith(COMMAND):
        # function gets all names for the day
        rollcall_behavior.get_all_names()
        # creating list
        input_list = rollcall_behavior.get_all_names.names_list
        # function reduces list
        rollcall_behavior.get_current_shifts(input_list)
        # creating new list that removes names
        output_list = rollcall_behavior.get_current_shifts.answer
        # formatting function
        slack_client.api_call("chat.postMessage", channel=channel,
                                  text="The following *{}* people should be logged in to phones:".format(len(output_list)), as_user=True)
        for name in output_list:
            slack_client.api_call("chat.postMessage", channel=channel,
                                      text=name, as_user=True)
    else:
        slack_client.api_call("chat.postMessage", channel=channel,
                                  text=response, as_user=True)


    # slack_client.api_call("chat.postMessage", channel=channel,
                          #text=response, as_user=True)

    # for name in rollcall_behavior.get_current_shifts(input_list):
    #    print name


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("rollcall connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
