# :: maze_runner.py
################################################
# Runs the maze, using interface provided
# by maze.py.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 8 November 2018

# local imports
from maze import Maze
from maze_constants import MazeResult, MazeMove, MazeGameState


class MazeRunner(object):
    def __init__(self, uid):
        self.maze = Maze(uid)
        self.reset_maze_runner()

    """
    Resets looked at and visited squares.
    """
    def reset_maze_runner(self):
        self.tovisit = []
        self.visited = set()

    def _is_valid_move(self, move_result):
        return(
            move_result != MazeResult.WALL and
            move_result != MazeResult.OUT_OF_BOUNDS and
            self.maze.current_location() not in self.visited)

    def _is_end_square(self, move_result):
        return move_result == MazeResult.END

    def _log_square(self):
        self.tovisit.append(self.maze.current_location())

    def run(self):
        start_square = self.maze.current_location()
        self.tovisit.append(start_square)
        while self.maze.game_state() == MazeGameState.PLAYING:
            curr_square = self.tovisit.pop()
            self.visited.add(curr_square)
            if self._is_valid_move(self.maze.update(MazeMove.UP)):
                print("UP")
                self._log_square()
                self.maze.update(MazeMove.DOWN)
            elif self._is_valid_move(self.maze.update(MazeMove.DOWN)):
                print("DOWN")
                self._log_square()
                self.maze.update(MazeMove.UP)
            elif self._is_valid_move(self.maze.update(MazeMove.LEFT)):
                print("LEFT")
                self._log_square()
                self.maze.update(MazeMove.RIGHT)
            elif self._is_valid_move(self.maze.update(MazeMove.RIGHT)):
                print("RIGHT")
                self._log_square()
                self.maze.update(MazeMove.LEFT)
            else:
                print("Joke's on you... you can't move anywhere.")
                exit(1)


if __name__ == '__main__':
    print("Welcome to maze runner.")
    print("Input your UID to continue.")
    uid = input()
    mazerunner = MazeRunner(uid)
    mazerunner.run()
