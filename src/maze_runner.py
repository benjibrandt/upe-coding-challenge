# :: maze_runner.py
################################################
# Runs the maze, using interface provided
# by maze.py.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 8 November 2018

# local imports
from maze import Maze
from maze_constants import MazeResult, MazeMove, MazeGameState, MazeCoord, Bearings


class Square(object):
    def __init__(self, coordinates, type, dir):
        self.coordinates = coordinates
        self.type = type
        self.dir = dir


class MazeRunner(object):
    def __init__(self, uid):
        self.maze = Maze(uid)
        self.reset_maze_runner()

    def __debug_game_status(self):
        print("==== game_status ====")
        print("Size: {}".format(self.maze.size()))
        print("Game Sate: {}".format(self.maze.game_state()))
        print("Total levels: {}".format(self.maze.total_levels()))
        print("Levels completed: {}".format(self.maze.levels_completed()))
        print("====")

    """
    Resets looked at and visited squares.
    """
    def reset_maze_runner(self):
        self.tovisit = []
        self.visited = set()

    def _valid_move(self, move_result):
        return move_result != MazeResult.WALL and move_result != MazeResult.OUT_OF_BOUNDS
    
    def _pledge_algo(self, init_dir, dest):
        #print("<--- PLEDGE ALGO --->")
        bearing = -1
        direction = init_dir
        #print("dir: {}".format(direction))
        #print("start lock: {}".format(self.maze.current_location()))
        while bearing != 0 and self.maze.current_location() != dest:
            #print("bearing: {}".format(bearing))
            changedDirectionPurposefully = False
            while(self._valid_move(self.maze.update(direction))) and self.maze.current_location() != dest:
                #print("---> loc before move: {}".format(self.maze.current_location()))
                clwdir = self._get_clockwise_direction(direction)
                #print("``` attempting to move clockwise ```")
                #print("``` clwdir: {}```".format(clwdir))
                if self._valid_move(self.maze.update(clwdir)):
                    #print("moved clockwise")
                    #print("---> clwdir: {}".format(clwdir))
                    direction = clwdir
                    #print("~~~~=> new direction: {}".format(direction))
                    #print(")))=> bearing-pre: {}".format(bearing))
                    bearing += 1
                    #print("(((=> bearing-post: {}".format(bearing))
                    changedDirectionPurposefully = True
                    break
                #print("broke out")
            if not changedDirectionPurposefully:
                bearing -= 1
                direction = self._get_counter_clockwise_direction(direction)

    def _is_end_square(self, move_result):
        return move_result == MazeResult.END

    def _log_square(self):
        if self.maze.current_location() not in self.visited:
            self.tovisit.append(self.maze.current_location())

    """
    Places all valid squares adjacent to the current square into the tovisit stack.
    curr_square: the square we're currently sitting on according to the AWS API.
    @return: maze_constants.MazeMove.FOUND_END if end square is found, maze_constants.MazeMove.LOGGED otherwise.
    """
    def _log_adjacent_squares(self):
        #print("self.maze.current_location() @ start of log: {}".format(self.maze.current_location()))
        up = self.maze.update(MazeMove.UP)
        if up == MazeResult.END: return MazeMove.FOUND_END
        elif self._valid_move(up):
            self._log_square()
            self.maze.update(MazeMove.DOWN)
        down = self.maze.update(MazeMove.DOWN)
        if down == MazeResult.END: return MazeMove.FOUND_END
        elif self._valid_move(down):
            self._log_square()
            self.maze.update(MazeMove.UP)
        left = self.maze.update(MazeMove.LEFT)
        if left == MazeResult.END: return MazeMove.FOUND_END
        elif self._valid_move(left):
            self._log_square()
            self.maze.update(MazeMove.RIGHT)
        right = self.maze.update(MazeMove.RIGHT)
        if right == MazeResult.END: return MazeMove.FOUND_END
        elif self._valid_move(right):
            self._log_square()
            self.maze.update(MazeMove.LEFT)
        return MazeMove.LOGGED

    def _get_adjacent_squares(self):
        adj_squares = []

        coord = (-1, -1)
        up = self.maze.update(MazeMove.UP)
        if self._valid_move(up):
            coord = self.maze.current_location()
            self.maze.update(MazeMove.DOWN)
        adj_squares.append(Square(coord, up, MazeMove.UP))

        coord = (-1, -1)
        down = self.maze.update(MazeMove.DOWN)
        if self._valid_move(down):
            coord = self.maze.current_location()
            self.maze.update(MazeMove.UP)
        adj_squares.append(Square(coord, down, MazeMove.DOWN))

        coord = (-1, -1)
        left = self.maze.update(MazeMove.LEFT)
        if self._valid_move(left):
            coord = self.maze.current_location()
            self.maze.update(MazeMove.RIGHT)
        adj_squares.append(Square(coord, left, MazeMove.LEFT))

        coord = (-1, -1)
        right = self.maze.update(MazeMove.RIGHT)
        if self._valid_move(right):
            coord = self.maze.current_location()
            self.maze.update(MazeMove.LEFT)
        adj_squares.append(Square(coord, right, MazeMove.RIGHT))

        return adj_squares

    def _get_counter_clockwise_direction(self, curr_dir):
        if curr_dir == MazeMove.DOWN:
            return MazeMove.RIGHT
        elif curr_dir == MazeMove.UP:
            return MazeMove.LEFT
        elif curr_dir == MazeMove.LEFT:
            return MazeMove.DOWN
        elif curr_dir == MazeMove.RIGHT:
            return MazeMove.UP
        else:
            return None

    def _get_clockwise_direction(self, curr_dir):
        if curr_dir == MazeMove.DOWN:
            return MazeMove.LEFT
        elif curr_dir == MazeMove.UP:
            return MazeMove.RIGHT
        elif curr_dir == MazeMove.LEFT:
            return MazeMove.UP
        elif curr_dir == MazeMove.RIGHT:
            return MazeMove.DOWN
        else:
            return None

    def _get_opposite_direction(self, curr_dir):
        if curr_dir == MazeMove.DOWN:
            return MazeMove.UP
        elif curr_dir == MazeMove.UP:
            return MazeMove.DOWN
        elif curr_dir == MazeMove.LEFT:
            return MazeMove.RIGHT
        elif curr_dir == MazeMove.RIGHT:
            return MazeMove.LEFT
        else:
            return None

    """
    Moves from the current square (gotten by self.maze.current_location()) to the square indicated by dest.
    @param dest: a tuple with the (x, y) coordinates of the square you wish to move to.
    @end: a call to self.maze.current_location() will yield the coordinates indicated by param dest.
    """
    def _move_to(self, dest):
        curr_square = self.maze.current_location()
        while curr_square != dest:
            while dest[MazeCoord.X] != curr_square[MazeCoord.X]:
                if curr_square[MazeCoord.X] > dest[MazeCoord.X]:
                    direction = MazeMove.LEFT
                    if self.maze.update(direction) != MazeResult.SUCCESS:
                        self._pledge_algo(self._get_counter_clockwise_direction(direction), dest)
                    curr_square = self.maze.current_location()
                else:  # curr_square[MazeCoord.X] < dest[MazeCoord.X]:
                    direction = MazeMove.RIGHT
                    if self.maze.update(direction) != MazeResult.SUCCESS:
                        self._pledge_algo(self._get_counter_clockwise_direction(direction), dest)
                    curr_square = self.maze.current_location()
            while dest[MazeCoord.Y] != curr_square[MazeCoord.Y]:
                if curr_square[MazeCoord.Y] > dest[MazeCoord.Y]:
                    direction = MazeMove.UP
                    if self.maze.update(direction) != MazeResult.SUCCESS:
                        self._pledge_algo(self._get_counter_clockwise_direction(direction), dest)
                    curr_square = self.maze.current_location()
                else:  # curr_square[MazeCoord.Y] < dest[MazeCoord.Y]
                    direction = MazeMove.DOWN
                    if self.maze.update(direction) != MazeResult.SUCCESS:
                        self._pledge_algo(self._get_counter_clockwise_direction(direction), dest)
                    curr_square = self.maze.current_location()


    """
    basically, we need to store a 'moves made to get here' thing when recording a square for encounter,
    so we can successfully re-create a path back to the square, because this API shit is stupid.
    More or less, we should just need to check the given coordinate against our current coordinate, calculate
    moves back to there, and continue trying moves.
    """
    def run(self):
        self.__debug_game_status()
        start_square = self.maze.current_location()
        self.tovisit.append(start_square)
        #print("start_square: {}".format(start_square))
        while self.maze.game_state() == MazeGameState.PLAYING:
            curr_square = self.tovisit.pop()
            #print("~~~~~~")
            #print("curr_square: {}".format(curr_square))
            #print("self.maze.current_location(): {}".format(self.maze.current_location()))
            #print("----")
            self._move_to(curr_square)
            #print("<<<< moved >>>>>")
            #print("self.maze.current_location(): {}".format(self.maze.current_location()))
            #print("<<<<<>>>>>")
            if self._log_adjacent_squares() == MazeMove.FOUND_END:
                print("<<< found the end! >>>")
                self.__debug_game_status()
                self.reset_maze_runner()
                start_square = self.maze.current_location()
                self.tovisit.append(start_square)
                continue
            #print(self.tovisit)
            #print("----")
            #print("~~~~~~")
            self.visited.add(curr_square)


if __name__ == '__main__':
    print("Welcome to maze runner.")
    print("Input your UID to continue.")
    uid = input()
    mazerunner = MazeRunner(uid)
    mazerunner.run()
