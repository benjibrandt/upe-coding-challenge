# :: maze_constants.py
################################################
# All the constants needed for handling the
# UPE maze coding challenge.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 8 November 2018
# https://gist.github.com/austinguo550/381d5e30d825b90900ef60fa39a806f4?fbclid=IwAR2rV-XeOuZj7NeZSuJ4tgMEXlC0Ggzv7Lha4FzfWGnr_hWDkDB8K_LanwE

from enum import Enum


class MazeMove(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class MazeState(Enum):
    WALL = "WALL"
    SUCCESS = "SUCCESS"
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"
    END = "END"
