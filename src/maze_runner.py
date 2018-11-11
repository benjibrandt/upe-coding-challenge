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
        Prints the relevant status information about the in-progress sovling session.
        """
        print("==== game_status ====")
        print("Size: {}".format(self.maze.size()))
        print("Game Sate: {}".format(self.maze.game_state()))
        print("Total levels: {}".format(self.maze.total_levels()))
        print("Levels completed: {}".format(self.maze.levels_completed()))
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

    def _pledge_algo(self, init_dir):
        
        #print("<--- PLEDGE ALGO --->")
        bearing = -1
        direction = init_dir
        #print("dir: {}".format(direction))
        #print("start lock: {}".format(self.maze.current_location()))
        move = self.maze.update(direction)
        while bearing != 0 and move != MazeResult.END:
            move = self.maze.update(direction)
            #print("bearing: {}".format(bearing))
            changedDirectionPurposefully = False
            while(self._valid_move(move)) and move != MazeResult.END:
                #print("---> loc before move: {}".format(self.maze.current_location()))
                clwdir = self._get_clockwise_direction(direction)
                #print("``` attempting to move clockwise ```")
                #print("``` clwdir: {}```".format(clwdir))
                move = self.maze.update(clwdir)
                if self._valid_move(move):
                    #print("moved clockwise")
                    #print("---> clwdir: {}".format(clwdir))
                    direction = clwdir
                    #print("~~~~=> new direction: {}".format(direction))
                    #print(")))=> bearing-pre: {}".format(bearing))
                    bearing += 1
                    #print("(((=> bearing-post: {}".format(bearing))
                    changedDirectionPurposefully = True
                    break
                move = self.maze.update(direction)
                #print("broke out")
            if not changedDirectionPurposefully:
                bearing -= 1
                direction = self._get_counter_clockwise_direction(direction)
        return True

    def _is_end_square(self, move_result):
        """
        @param move_result: a maze_constants.MazeResult value.
        """
        return move_result == MazeResult.END

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
        return location.x < maze_sz_x or location.x >= 0 or location.y < maze_sz_y or location.y >= 0

    def _update_maze_tracker(self, location, value):
        """
        Updates the internal maze tracker at location with value.

        @param location: the location to be updated. Must be in-bounds for the current maze.
        @param value: the value to update that location with. Must be in maze_constants.MazeMaterials.
        @return: True if update succeeded, False otherwise.
        """
        if not self._in_bounds(location) or value not in vars(MazeMaterials).values():
            return False

        self.maze_tracker[location.x][location.y] = value
        return True
    
    def run_pure_pledge(self):
        self.report_game_status()
        init_dir = MazeMove.DOWN  # arbitrary
        while self.maze.game_state() == MazeGameState.PLAYING:
            self.current_location = self.maze.current_location()
            self.maze_size = self.maze.size()
            maze_size_x, maze_size_y = self.maze_size
            self.maze_tracker = [[MazeMaterials.FOG for x in range(maze_size_x)] for y in range(maze_size_y)] 
            while True:
                maze_move = self.maze.update(init_dir)
                if maze_move != MazeResult.SUCCESS:
                    if maze_move == MazeResult.END:
                        print("<<< found the end! >>>")
                        # reset maze runner
                    elif maze_move == MazeResult.WALL:
                        update_loc = self.current_location.peek(init_dir)
                        self._update_maze_tracker(update_loc, MazeMaterials.WALL)
                    break
                self.current_location.move(init_dir)
                self._update_maze_tracker(self.current_location, MazeMaterials.PATH)
            if self._pledge_algo(init_dir):
                print("<<< found the end! >>>")
                self.report_game_status()


if __name__ == '__main__':
    print("Welcome to maze runner.")
    print("Input your UID to continue.")
    uid = input()
    mazerunner = MazeRunner(uid)
    mazerunner.run_pure_pledge()
