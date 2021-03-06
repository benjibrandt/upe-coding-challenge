# :: maze_runner.py
################################################
# Runs the maze, using interface provided
# by maze.py.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 8 November 2018

# local imports
from maze import Maze
from maze_constants import MazeResult, MazeMove, MazeGameState, MazeMaterials


class MazeRunner(object):
    def __init__(self, uid):
        """
        @param uid: a 9-digit UCLA student ID.
        """
        self.maze = Maze(uid)
        self.reset_maze_runner()

    def report_game_status(self):
        """
        prints the relevant status information about the in-progress sovling session.
        """
        print("==== game_status ====")
        print("Game Sate: {}".format(self.maze.game_state()))
        print("=====================")

    def reset_maze_runner(self):
        """
        Resets the maze runner to its initial, pre-solving state (though UID is left intact).
        """
        self.maze_size = (0, 0)
        """
        maze_tracker is our own, internal representation of the maze, so we don't have to
        constantly consult the API.
        
        Contained values can be any value in maze_constants.MazeMaterials.
        """
        self.maze_tracker = [[]]
        self.current_location = (-1, -1)

    def _valid_move(self, move_result):
        """
        Checks if the move made was a valid one.

        @param curr_dir: a maze_constants.MazeMove value.
        @return: True if a successful move (into the end or ordinary path) was made, false otherwise.
        """
        return move_result != MazeResult.WALL and move_result != MazeResult.OUT_OF_BOUNDS

    def _make_move(self, direction):
        """
        Attempts to make the move in the given direction with as little AWS communication if possible.
        Will check to see if the intended destination has been cached.
            If cached: determines if move will be successful, and only contacts AWS if it will be.
            If not: contacts the AWS API to attempt a move.
        Local trackers such as maze_tracker and current_location will be updated appropriately.

        @param direction: a value from maze_constants.MazeMove
        @return: any value in maze_constants.MazeResult.
        """
        peek_loc = self.current_location.peek(direction)
        if (self.maze.current_location().x, self.maze.current_location().y) != (self.current_location.x, self.current_location.y):
            exit(1)
        if not self._in_bounds(peek_loc):
            return MazeResult.OUT_OF_BOUNDS
        cached_loc = self.maze_tracker[peek_loc.y][peek_loc.x]
        if cached_loc != MazeMaterials.FOG:
            if cached_loc != MazeMaterials.WALL:
                self.current_location.move(direction)
                self.maze.update(direction)
                return MazeResult.SUCCESS  # need to indicate successful move into cached loc
            else:
                return MazeResult.WALL
        else:
            move_result = self.maze.update(direction)
            if self._valid_move(move_result):
                self.current_location.move(direction)
            if move_result != MazeResult.OUT_OF_BOUNDS:
                update_loc = self.current_location if move_result != MazeResult.WALL else peek_loc
                self._update_maze_tracker(update_loc, self._get_equivalent_maze_material(move_result))
            return move_result

    def _pledge_algo(self, init_dir):
        bearing = -1
        direction = self._get_counter_clockwise_direction(init_dir)
        while True:
            decrementedBearing = False
            move = self._make_move(direction)
            if move == MazeResult.END:
                return True
            if not self._valid_move(move):
                decrementedBearing = True
                bearing -= 1
            if bearing == 0:
                break
            clwdir = self._get_clockwise_direction(direction)
            move = self._make_move(clwdir)
            if self._valid_move(move):
                if move == MazeResult.END:
                    return True
                direction = clwdir
                bearing += 1
            else:
                if decrementedBearing:
                    direction = self._get_counter_clockwise_direction(direction)
        return False

    def _get_counter_clockwise_direction(self, curr_dir):
        """
        @param curr_dir: a maze_constants.MazeMove value.
        @return: the direction that is 90 degree counter-clockwise rotation of the one supplied.
        """
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
        """
        @param curr_dir: a maze_constants.MazeMove value.
        @return: the direction that is the 90 degree clockwise rotation of the one supplied.
        """
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
        """
        @param curr_dir: a maze_constants.MazeMove value.
        @return: the direction that is the logical opposite of the one supplied.
        """
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

    def _in_bounds(self, location):
        """
        Determines if the location is in bounds according to the current maze.

        @param location: a maze.Location object.
        """
        maze_sz_x, maze_sz_y = self.maze_size
        return location.x < maze_sz_x and location.x >= 0 and location.y < maze_sz_y and location.y >= 0

    def _update_maze_tracker(self, location, value):
        """
        Updates the internal maze tracker at location with value.

        @param location: the location to be updated. Must be in-bounds for the current maze.
        @param value: the value to update that location with. Must be in maze_constants.MazeMaterials.
        @return: True if update succeeded, False otherwise.
        """
        if not self._in_bounds(location) or value not in vars(MazeMaterials).values():
            return False

        self.maze_tracker[location.y][location.x] = value
        return True

    def _get_equivalent_maze_material(self, move_result):
        """
        Finds the corrollary between maze_constants.MazeResult and maze_constants.MazeMaterials.

        @param move_result: a value in maze_constants.MazeResult.
        @return: the proper maze material, or None if move_result is invalid (either not in MazeResult, or OUT_OF_BOUNDS).
        """
        if move_result == MazeResult.END:
            return MazeMaterials.END
        elif move_result == MazeResult.OUT_OF_BOUNDS:
            return None
        elif move_result == MazeResult.SUCCESS:
            return MazeMaterials.PATH
        elif move_result == MazeResult.WALL:
            return MazeMaterials.WALL
        else:
            return None
    
    def run_pure_pledge(self):
        self.report_game_status()
        init_dir = MazeMove.DOWN  # arbitrary
        level_total = self.maze.total_levels()
        completed_total = self.maze.levels_completed()
        while completed_total != level_total and self.maze.game_state() == MazeGameState.PLAYING:
            self.current_location = self.maze.current_location()
            self.maze_size = self.maze.size()
            maze_size_x, maze_size_y = self.maze_size
            self.maze_tracker = [[MazeMaterials.FOG for x in range(maze_size_x)] for y in range(maze_size_y)] 
            self.maze_tracker[self.current_location.y][self.current_location.x] = MazeMaterials.PATH
            while True:
                maze_move = self._make_move(init_dir)
                if maze_move != MazeResult.SUCCESS:
                    if maze_move == MazeResult.END:
                        print("<<< found the end! >>>")
                        self.report_game_status()
                        completed_total = self.maze.levels_completed()
                        break
                    elif self._pledge_algo(init_dir):
                        print("<<< found the end! >>>")
                        self.report_game_status()
                        completed_total = self.maze.levels_completed()
                        break

if __name__ == '__main__':
    print("Welcome to maze runner.")
    print("Input your UID to continue.")
    uid = input()
    mazerunner = MazeRunner(uid)
    mazerunner.run_pure_pledge()
    print("Solved!")
