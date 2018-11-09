# :: maze.py
################################################
# Handles authentication, status getting,
# and updating of the maze.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 8 November 2018

# external imports
import requests
from maze_constants import MazeAuth, MazeUpdate, MazeStatus


class Maze(object):
    AUTH_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"
    BASE_STATUS_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="
    BASE_UPDATE_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="   

    def __init__(self, uid):
        token = self.get_token(uid)
        self.update_session(token)

    """
    Gets the token from AWS.
    @parma uid: the student's uid.
    @return: an AWS token to be appeneded to URLs.
    """
    def get_token(self, uid):
        resp = requests.post(Maze.AUTH_URL, data={
            MazeAuth.UID: uid
        })
        return resp.json()[MazeAuth.TOKEN]

    """
    Updates the API URLs to a valid session token.
    @param token: the AWS token gotten by self.get_token
    """
    def update_session(self, token):
        self.update_url = Maze.BASE_UPDATE_URL + token
        self.status_url = Maze.BASE_STATUS_URL + token

    """
    @return: a string representing game state. Defined in maze_constants.MazeGameState.
    """
    def game_state(self):
        return requests.get(self.status_url).json()[MazeStatus.STATUS]

    """
    @return: a 2-entry array representing [x, y] location.
    """
    def current_location(self):
        return requests.get(self.status_url).json()[MazeStatus.CURRENT_LOCATION]

    """
    @return: a 2-entry array representing [width, height]
    """
    def size(self):
        return requests.get(self.status_url).json()[MazeStatus.MAZE_SIZE]

    """
    @return: an int representing the number of levels completed.
    """
    def levels_completed(self):
        return requests.get(self.status_url).json()[MazeStatus.LEVELS_COMPLETED]

    """
    @return: an int representing the number of levels in total.
    """
    def total_levels(self):
        return requests.get(self.status_url).json()[MazeStatus.TOTAL_LEVELS]

    """
    Updates the maze with the specified action.
    @param action: a constant from maze_constants.MazeMove.
    @return: the JSON response of POSTing the action.
    """
    def update(self, action):
        return requests.post(self.update_url, data={
            MazeUpdate.ACTION: action
        }).json()[MazeUpdate.RESULT]
