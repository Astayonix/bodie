import os
import json
import time
from slackclient import SlackClient

token = 'SLACK_OAUTH_ACCESS_TOKEN_DH'
sc = SlackClient(os.environ[token])
# print sc
if sc.rtm_connect():
    # print sc.rtm_connect()
    while True:
        new_evts = sc.rtm_read()
        # print new_evts
        for evt in new_evts:
            # print evt
            if 'type' in evt:
                # print evt
                if evt["type"] == 'message':# and 'yes' in evt:
                    message = evt['text']
                    # print message
        print sc.rtm_read()
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"