import os
#import sys
import json
from slacker import Slacker

slack = Slacker(os.environ['SLACK_OAUTH_ACCESS_TOKEN'])

# Send a message to #team-chips-and-crisps channel
#slack.chat.post_message('#team-chips-and-crisps', 'Hello fellow slackers, this is our bot!')

#trying to prettyprint the json returned by channels
channel_obj = slack.channels.list()
channels = channel_obj.body
json_str_channel_list = json.dumps(channels)
channels = json.loads(json_str_channel_list)
print channels

# Get users list
#response = slack.users.list()
# print response
#users = response.body['members']
# for user in users:
#     print user

# Upload a file
#slack.files.upload('hello.txt')