# :: maze.py
################################################
# Handles authentication, status getting,
# and updating of the maze.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 8 November 2018

# external imports
import requests


class Maze(object):
    AUTH_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"
    STAT_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="
    UPDATE_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="   

    def __init__(self, uid):
        token = self.__authenticate(uid)
        self.update_url = self.UPDATE_URL + token
        self.stat_url = self.STAT_URL + token

    # @param uid: the student's uid
    # @return: the auth token given by the AWS API, based on UID
    def __authenticate(self, uid):
        req = requests.get(self.AUTH_URL)
        return req.token

    def status(self):
        return requests.get(self.stat_url)

    def update(self, action):
        return requests.post(self.update_url, data={
            "action": action
        })
