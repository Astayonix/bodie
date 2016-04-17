#import sys
import os
import json
import time
from random import choice
from slackclient import SlackClient
from datetime import datetime

slack = SlackClient(os.environ['SLACK_OAUTH_ACCESS_TOKEN_DH'])

# prettyprint the json returned by channels
# pp_json = json.dumps(channel_list, sort_keys=False, indent=4, separators=(',',':'))
# print pp_json

def teamDict():
    """Creates a dictionary of Slack team information
    {Slack Team_ID: [Slack team name, slack team domain]}"""

    slack_team_dictionary = {}
    ugly_team_json = slack.api_call('team.info')
    teams = ugly_team_json['team']
    team = teams['id']
    name = teams['name']
    domain = teams['domain']
    slack_team_dictionary[team] = []
    slack_team_dictionary[team].append(name)
    slack_team_dictionary[team].append(domain)
    return slack_team_dictionary

team_dict = teamDict()
#print team_dict

def teamChannelSet ():
    """Creates a set of all public channel ids on a given Slack team"""
    slack_public_channels_set = set()
    ugly_channel_list = slack.api_call('channels.list')
    channels = ugly_channel_list['channels']
    for channel in channels:
        slack_public_channels_set.add(channel['id'])
    return slack_public_channels_set

channel_list = list(teamChannelSet())
#print channel_list

def teamMemberSet():
    """Creates a set of all public channel member ids on a given Slack team"""
    slack_public_channels_users_set = set()
    ugly_channel_list = slack.api_call('channels.list')
    channels = ugly_channel_list['channels']
    for channel in channels:
        members_list = channel['members']
        for member in members_list:
            slack_public_channels_users_set.add(member)
    return slack_public_channels_users_set

member_list = list(teamMemberSet())
#print member_list

def teamChannelUserDict(member_list):
    """Creates a dictionary of all users and the public channels they belong to on a given Slack team
    {Slack User_ID: [Slack Channel_ID 1, Slack Channel_ID 2, ... Slack Channel_ID n]"""
    public_channels_and_users_dict = {}
    member_list = member_list
    ugly_channel_list = slack.api_call('channels.list')
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
    ugly_user_list = slack.api_call('users.list')
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

user_location_dict = teamUserLocationDict(member_list)
#print user_location_dict

def playerSelectLocAgnDeptAgn(member_list, user_location_dict):
    """Returns a list of 2 randomly chosen non-deleted, non-bot users to play a game regardless of their user location or department channel.
    Location agnostic, department agnostic""" 
    player_list = []
    user_location_dict = user_location_dict
    member_list = member_list
    if len(member_list) >= 2:
        player1 = choice(member_list)
        member_list[:] = [player for player in member_list if (player != player1)]
        if len(member_list) >= 1:
            player2 = choice(member_list)
            if (player1 != player2) and (player1 and player2 in user_location_dict.keys()):
                player_list.append(player1)
                player_list.append(player2)
                return player_list
        else:
            print "There are not enough people on this team to choose 2 players!"
            return player_list
    else:
        print "There are not enough people on this team to choose 2 players!"
        return player_list

player_list_locagn_deptagn = playerSelectLocAgnDeptAgn(member_list, user_location_dict)
print player_list_locagn_deptagn

# player_list = ['U0YLNJNQ2']#,'U0YKH3LF7', 'U0YMFJAF4', 'U0YKWGAN9', 'U0YHWCPQB'] #me, yvonne, jake, heidi, iona

def gameAnnounce(player_list, user_location_info_dict):
    if player_list != []:
        player_response_list = []
        user_location_info_dict = user_location_info_dict
        player_list = player_list
        for player in player_list:
            player_id = player
            player_name = user_location_info_dict[player][0]
            player_tz = user_location_info_dict[player][1]
            player_tz_name = user_location_info_dict[player][2]
            dm_channel_id = slack.api_call('im.open', user = player)['channel']['id']
            slack.api_call(
                'chat.postMessage',
                channel = dm_channel_id,
                text = "Hi there! :smile:  You've been working hard and look like you could use a short break.",
                # attachments = [{:}, {:}],
                as_user = False,
                username = 'Bodie',
                icon_emoji = ':bodie:'
                )
            slack.api_call(
                'chat.postMessage',
                channel = dm_channel_id,
                text = "Would you like to play a game, %s? :sparkles:  Type 'gimmeabreak' to start playing!" % (player_name),
                as_user=False,
                username='Bodie',
                icon_emoji=':bodie:'
                )
            if slack.rtm_connect():
                while True:
                    new_evts = slack.rtm_read()
                    for evt in new_evts:
                        if ('type' and 'text' in evt) and ('is_ephemeral' not in evt):
                            if evt['type'] == 'message':# and 'yes' in evt:
                                # pp_json = json.dumps(evt, sort_keys=False, indent=4, separators=(',',':'))
                                # print pp_json
                                # evt_dt_fmt = '%Y-%m-%d;%H:%M:%S'
                                evt_text = evt['text']
                                evt_type = evt['type']
                                evt_user = evt['user']
                                evt_channel = evt['channel']
                                evt_ts = evt['ts']
                                # evt_time_stamp = datetime.strptime(evt_ts, evt_dt_fmt)
                                print evt_channel, evt_user, evt_type, evt_text, evt_ts
                                if ('gimmeabreak' in evt_text.lower()) and (evt_user == player) and (evt_channel == dm_channel_id):
                                    print "yes"
                                    player_response_list.append('y')
                                    break
                                else:
                                    print "no"
                                    player_response_list.append('n')
                                    break
                    time.sleep(1)
            else:
                print "Connection Failed, invalid token?"
    return player_response_list
                
game_accept_list = gameAnnounce(player_list_locagn_deptagn, user_location_dict)
print game_accept_list

# Upload a file
#slack.files.upload('hello.txt')