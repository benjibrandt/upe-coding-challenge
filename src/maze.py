# :: maze.py
################################################
# Handles authentication, status getting,
# and updating of the maze.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 8 November 2018

# external imports
import requests
from maze_constants import MazeAuth, MazeUpdate, MazeStatus, MazeMove


class Location(object):
    def __init__(self, coordinate_pair):
        """
        @param coordinate_pair: a tuple in the form (x, y)
        """
        self.x, self.y = coordinate_pair

    def move(self, direction, paces=1):
        """
        Updates the stored location via a move in direction for paces.

        @param direction: direction from maze_constants.MazeMove
        @param paces: the number of 'steps' to take in the given direction. Must be an int >= 0.
        @return: True if the move succeeds, False otherwise.
        """
        if paces < 0: return False
        if direction == MazeMove.RIGHT: self.x += paces
        elif direction == MazeMove.LEFT: self.x -= paces
        elif direction == MazeMove.UP: self.y -= paces
        elif direction == MazeMove.DOWN: self.y += paces
        else: return False
        return True

    def peek(self, direction, paces=1):
        """
        Determines what a move in direction for paces would yield, and retruns that.
        Does NOT modify the stored location.

        @param direction: direction from maze_constants.MazeMove
        @param paces: the number of 'steps' to take in the given direction. Must be an int >= 0.
        @return: a tuple containing the potential location if a valid move, None otherwise.
        """
        if paces < 0: return None
        x, y = self.x, self.y
        if direction == MazeMove.RIGHT: x += paces
        elif direction == MazeMove.LEFT: x -= paces
        elif direction == MazeMove.UP: y -= paces
        elif direction == MazeMove.DOWN: y += paces
        else: return None
        return Location((x, y))

    def set_location(self, new_location):
        """
        @param new_location: a tuple in the form (x, y).
        """
        self.x, self.y = new_location


class Maze(object):
    AUTH_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"
    BASE_STATUS_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="
    BASE_UPDATE_URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="   

    def __init__(self, uid):
        """
        @param uid: a 9-digit UCLA ID number.
        """
        token = self.get_token(uid)
        self.update_session(token)

    def get_token(self, uid):
        """
        Gets the token from AWS.
        @parma uid: the student's uid.
        @return: an AWS token to be appeneded to URLs.
        """
        req = requests.post(Maze.AUTH_URL, data={
            MazeAuth.UID: uid
        })
        if req.status_code != requests.codes.ok:
            print("ERROR: authentication request rejected. Status code {}".format(req.status_code))
            exit(1)
        else:
            return req.json()[MazeAuth.TOKEN]

    def update_session(self, token):
        """
        Updates the API URLs to a valid session token.
        @param token: the AWS token gotten by self.get_token
        """
        self.update_url = Maze.BASE_UPDATE_URL + token
        self.status_url = Maze.BASE_STATUS_URL + token

    def game_state(self):
        """
        @return: a string representing game state. Defined in maze_constants.MazeGameState.
        """
        req = requests.get(self.status_url)
        if req.status_code != requests.codes.ok:
            print("ERROR: game state request rejected. Status code {}".format(req.status_code))
            exit(1)
        else:
            return req.json()[MazeStatus.STATUS]

    def current_location(self):
        """
        @return: a tuple representing [x, y] location.
        """
        req = requests.get(self.status_url)
        if req.status_code != requests.codes.ok:
            print("ERROR: maze location request rejected. Status code {}".format(req.status_code))
            exit(1)
        else:
            return Location(tuple(req.json()[MazeStatus.CURRENT_LOCATION]))

    def size(self):
        """
        @return: a tuple representing [width, height]
        """
        req = requests.get(self.status_url)
        if req.status_code != requests.codes.ok:
            print("ERROR: maze size request rejected. Status code {}".format(req.status_code))
            exit(1)
        else:
            return tuple(req.json()[MazeStatus.MAZE_SIZE])

    def levels_completed(self):
        """
        @return: an int representing the number of levels completed.
        """
        req = requests.get(self.status_url)
        if req.status_code != requests.codes.ok:
            print("ERROR: levels completed request rejected. Status code {}".format(req.status_code))
            exit(1)
        else:
            return req.json()[MazeStatus.LEVELS_COMPLETED]

    def total_levels(self):
        """
        @return: an int representing the number of levels in total.
        """
        req = requests.get(self.status_url)
        if req.status_code != requests.codes.ok:
            print("ERROR: total levels request rejected. Status code {}".format(req.status_code))
            exit(1)
        else:
            return req.json()[MazeStatus.TOTAL_LEVELS]
   
    def update(self, action):
        """
        Updates the maze with the specified action.
        @param action: a constant from maze_constants.MazeMove.
        @return: the JSON response of POSTing the action.
        """
        req = requests.post(self.update_url, data={
            MazeUpdate.ACTION: action
        })
        if req.status_code != requests.codes.ok:
            print("ERROR: update request rejected. Status code {}".format(req.status_code))
            exit(1)
        else:
            return req.json()[MazeUpdate.RESULT]
