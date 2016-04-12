#import sys
import os
import json
from slacker import Slacker
from random import choice

slack = Slacker(os.environ['SLACK_OAUTH_ACCESS_TOKEN'])

# prettyprint the json returned by channels
# pp_channel = json.dumps(channel_list, sort_keys=False, indent=4, separators=(',',':'))
# print pp_channel

def teamChannelList ():
    """Creates a set of all public channels on a given Slack team"""
    slack_public_channels_set = set()
    ugly_channel_list = slack.channels.list().body
    channels = ugly_channel_list['channels']
    for channel in channels:
        slack_public_channels_set.add(str(unicode(channel['id'])))
    print slack_public_channels_set
    return slack_public_channels_set

teamChannelList()

def teamMemberList():
    """Creates a set of all public channel members on a given Slack team"""
    slack_public_channels_users_set = set()
    ugly_channel_list = slack.channels.list().body
    channels = ugly_channel_list['channels']
    for channel in channels:
        members_list = channel['members']
        for member in members_list:
            slack_public_channels_users_set.add(str(unicode(member)))
    print slack_public_channels_users_set
    return slack_public_channels_users_set

teamMemberList()

# Send a message to #team-chips-and-crisps channel
slack.chat.post_message('team-chips-and-crisps', 'Hello there!  Are you ready for a game, %s?' % (choice(slack_public_channels_users_set)), as_user=False, username='Bodie')

# Get users list
#response = slack.users.list()
# print response
#users = response.body['members']
# for user in users:
#     print user

# Upload a file
#slack.files.upload('hello.txt')