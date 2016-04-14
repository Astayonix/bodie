#import sys
import os
import json
from slacker import Slacker
from random import choice

slack = Slacker(os.environ['SLACK_OAUTH_ACCESS_TOKEN'])

# prettyprint the json returned by channels
# pp_json = json.dumps(channel_list, sort_keys=False, indent=4, separators=(',',':'))
# print pp_json

def teamChannelSet ():
    """Creates a set of all public channels on a given Slack team"""
    slack_public_channels_set = set()
    ugly_channel_list = slack.channels.list().body
    channels = ugly_channel_list['channels']
    for channel in channels:
        slack_public_channels_set.add(str(unicode(channel['id'])))
    return slack_public_channels_set

channel_list = list(teamChannelSet())
#print channel_list

def teamMemberSet():
    """Creates a set of all public channel members on a given Slack team"""
    slack_public_channels_users_set = set()
    ugly_channel_list = slack.channels.list().body
    channels = ugly_channel_list['channels']
    for channel in channels:
        members_list = channel['members']
        for member in members_list:
            slack_public_channels_users_set.add(str(unicode(member)))
    return slack_public_channels_users_set

member_list = list(teamMemberSet())
#print member_list

def teamChannelUserDict(member_list):
    """Creates a dictionary of all users and the public channels they belong to on a given Slack team"""
    public_channels_and_users_dict = {}
    member_list = member_list
    ugly_channel_list = slack.channels.list().body
    channels = ugly_channel_list['channels']
    for member in member_list:
        public_channels_and_users_dict[member] = []
    for member in member_list:
        for channel in channels:
            channel_members = channel['members']
            channel_id = channel['id']
            for channel_member in channel_members:
                if member == channel_member:
                    public_channels_and_users_dict[member].append(channel_id)
    return public_channels_and_users_dict

channel_user_dict = teamChannelUserDict(member_list)
#print channel_user_dict

def teamUserLocationDict(member_list):
    """Creates a dictionary of all non-deleted, non-bot users and their associated location information.
    {Slack User_ID: [User's Real First and Last Name, User's Time Zone, User's Time Zone Label]}"""
    user_location_dict = {}
    member_list = member_list
    ugly_user_list = slack.users.list().body
    users = ugly_user_list['members']
    for member in member_list:
        user_location_dict[member] = []
    for member in member_list:
        for user in users:
            if user['deleted'] == False:
                if user['is_bot'] == False:
                    user_id = user['id']
                    user_real_name = user['real_name']
                    if user_real_name == "":
                        user_real_name = "my friend"
                    user_tz = user['tz']
                    user_tz_label = user['tz_label']
                    if member == user_id:
                        user_location_dict[member].append(user_real_name)
                        user_location_dict[member].append(user_tz)
                        user_location_dict[member].append(user_tz_label)
    return user_location_dict

user_location_info_dict = teamUserLocationDict(member_list)
# print user_location_info_dict

def playerSelectLocAgnDeptAgn(member_list, user_location_info_dict):
    """Selects 2 non-deleted, non-bot users to play a game regardless of their user location or department channel.
    Location agnostic, department agnostic""" 
    player_list = []
    user_location_info_dict = user_location_info_dict
    member_list = member_list
    if len(member_list) >= 2:
        player1 = choice(member_list)
        member_list[:] = [player for player in member_list if (player != player1)]
        if len(member_list) >= 1:
            player2 = choice(member_list)
            if (player1 != player2) and (player1 and player2 in user_location_info_dict.keys()):
                player_list.append(player1)
                player_list.append(player2)
                return player_list
        else:
            print "There are not enough people on this team to choose 2 players!"
            return player_list
    else:
        print "There are not enough people on this team to choose 2 players!"
        return player_list

# player_list = playerSelectLocAgnDeptAgn(member_list, user_location_info_dict)
# print player_list

player_list = ['U0YLNJNQ2']#,'U0YKH3LF7', 'U0YMFJAF4', 'U0YKWGAN9', 'U0YHWCPQB'] #me, yvonne, jake, heidi, iona

def gameAnnounce(player_list, user_location_info_dict):
    if player_list != []:
        user_location_info_dict = user_location_info_dict
        player_list = player_list
        for player in player_list:
            player_id = player
            player_name = user_location_info_dict[player][0]
            player_tz = user_location_info_dict[player][1]
            player_tz_name = user_location_info_dict[player][2]
            dm_channel_id = slack.im.open(player).body['channel']['id']
            slack.chat.post_message(
                dm_channel_id,
                "Hi there! :smile:  You've been working hard and look like you could use a short break.",
                as_user=False,
                username='Bodie',
                icon_emoji=':break:'
                )
            slack.chat.post_message(
                dm_channel_id,
                "Would you like to play a game, %s? :sparkles:  Type /Yes to start playing!" % (player_name),
                as_user=False,
                username='Bodie',
                icon_emoji=':break:'
                )

game_accept_list = gameAnnounce(player_list, user_location_info_dict)

# Send a message to #team-chips-and-crisps channel
# slack.chat.post_message('team-chips-and-crisps', 'Hello there!  Are you ready for a game, Xiomara?', as_user=False, username='Bodie')

# Get users list
#response = slack.users.list()
# print response
#users = response.body['members']
# for user in users:
#     print user

# Upload a file
#slack.files.upload('hello.txt')