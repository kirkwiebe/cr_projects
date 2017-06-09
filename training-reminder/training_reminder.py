import os
from slackclient import SlackClient
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

slack_client = SlackClient(SLACK_BOT_TOKEN)

# access a spreadsheet

def getGoogleSheet():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_creds.json', scope)
    gc = gspread.authorize(credentials)
    doc = gc.open('Training Completion')
    sheet = doc.worksheet('Slackbot')
    return sheet

report_sheet = getGoogleSheet()
# get all data

def getReport(worksheet):
    list_of_lists = worksheet.get_all_values()
    return list_of_lists

data = getReport(report_sheet)

# get training name
course_name = data[1][2]

# get list of users without 'Completed' training

hudlies = []
for row in data:
    if row == data[0]:
        continue
    else:
        if row[3] != 'Completed':
            user = row[0] + ' ' + row[1]
            hudlies.append(user)

# send a message to a list of users

message = 'Please make sure to complete this week\'s training: *' + course_name + '*.'
sent_to=[]

response = slack_client.api_call('users.list')
users = response['members']
for user in users:
    realname = user['profile']['real_name']
    for hudlie in hudlies:
        if realname.startswith(hudlie): #found a match with a Hudlie
            sent_to.append(hudlie)
            user_id = user['id']
            slack_client.api_call('chat.postMessage', channel=user_id, text=message, as_user=True)
            time.sleep(1.5)

not_sent_to = [x for x in hudlies if x not in sent_to]

# prints back a message about what it did

if len(not_sent_to) == 0:
    print "Successfully sent to {} Hudlies!".format(len(hudlies))
else:
    print "Successfully sent to {} Hudlies!".format(len(sent_to))
    print "Did Not Send To", not_sent_to
