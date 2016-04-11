import os
#import sys
from slacker import Slacker

slack = Slacker(os.environ['SLACK_OAUTH_ACCESS_TOKEN'])

# Send a message to #team-chips-and-crisps channel
#slack.chat.post_message('#team-chips-and-crisps', 'Hello fellow slackers, this is our bot!')
channel_list = slack.channels.info() 
print channel_list.body
# Get users list
#response = slack.users.list()
# print response
#users = response.body['members']
# for user in users:
#     print user

# Upload a file
#slack.files.upload('hello.txt')