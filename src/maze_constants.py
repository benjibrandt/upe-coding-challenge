# :: maze_constants.py
################################################
# All the constants needed for handling the
# UPE maze coding challenge.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 8 November 2018
# https://gist.github.com/austinguo550/381d5e30d825b90900ef60fa39a806f4?fbclid=IwAR2rV-XeOuZj7NeZSuJ4tgMEXlC0Ggzv7Lha4FzfWGnr_hWDkDB8K_LanwE


class MazeMove(object):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    FOUND_END = 1
    LOGGED = 0


class MazeUpdate(object):
    RESULT = "result"
    ACTION = "action"


class MazeResult(object):
    WALL = "WALL"
    SUCCESS = "SUCCESS"
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"
    END = "END"


class MazeGameState(object):
    GAME_OVER = "GAME_OVER"
    NONE = "NONE"
    FINISHED = "FINISHED"
    PLAYING = "PLAYING"


class MazeStatus(object):
    MAZE_SIZE = "maze_size"
    CURRENT_LOCATION = "current_location"
    STATUS = "status"
    LEVELS_COMPLETED = "levels_completed"
    TOTAL_LEVELS = "total_levels"


class MazeAuth(object):
    TOKEN = "token"
    UID = "uid"


class MazeCoord(object):
    X = 0
    Y = 1


class MazeMaterials(object):
    END = 2
    WALL = 1
    PATH = 0
    FOG = -1
