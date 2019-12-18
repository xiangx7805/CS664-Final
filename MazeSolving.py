import numpy as np
import pandas as pd
import pickle
import turtle

## Dec 13
# this code allow the player to read a txt file
# with special characters for different scenarios
# for instance: + for walls, 'S' for start position/Entrance
# white space allow the move
# we will show two samples
# MazeSample1.text & MazeSample2.txt
record_path = 'O'
tried = '.'
wall = '+'
dead_end = '-'

class Maze:

    # initialize the maze
    def __init__(self,MazeSample):
        maze_row = 0
        maze_col = 0
        self.maze_list = []
        maze_sample = open(MazeSample,'r')

        # find the start position / Entrance
		# and record as self.entrance
        for line in maze_sample:
            row_List = []
            col_in_row = 0
            for ch in line[:-1]:
                row_List.append(ch)
                # entrance
                if ch == 'S':
                    self.entrance_row = maze_row
                    self.entrance_col = col_in_row
                    self.entrance = (self.entrance_row,self.entrance_col)
                    print("start position is " + str(self.entrance))

                # exit
                if ch == 'E':
                    self.exit_row = maze_row
                    self.exit_col = col_in_row
                    self.exit = (self.exit_row,self.exit_col)
                    print("Exit position is " + str(self.exit))


                col_in_row = col_in_row + 1
            maze_row = maze_row + 1
            self.maze_list.append(row_List)
            maze_col = len(row_List)
            # print(maze_col,maze_row)
            # now,  maze_col , maze_row == 30,30

        self.nrows = maze_row # 30
        self.ncols = maze_col # 30
        self.xTranslate = -maze_col/2 # -15
        self.yTranslate = maze_row/2 #  15

        # set player
		# here we use turtle to display the user interface
        self.player = turtle.Turtle()
        self.player.shape('square')
        self.player.color('blue')
        self.player.speed(0)
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(-15,-15,15,15)
        # for we have a 30*30 maze, and the centre is (0,0)
		# the corners' coordinates of the maze interface are:
        self.wn.title('Maze Solving, Xiang Xu')
		# self.wn.bgcolor('black')

        # test maze read right
        # maze_list = self.maze_list
        # with open('outfile.txt', 'w') as file_handler:
        #     for item in maze_list:
        #         file_handler.write("{}\n".format(item))
        # print("Writing OK")

    # Plot the maze in a window
    def MazePlot(self):
        self.player.speed(0)
        self.wn.tracer(0)
        for y in range(self.nrows): #30
            for x in range(self.ncols): #30
                if self.maze_list[y][x] == wall:
                    self.MazeCanvas(x+-15,-y+15,'orange')
        self.player.color('black')
        self.player.fillcolor('blue')
        self.wn.update()
        self.wn.tracer(1)

    def MazeCanvas(self,x,y,color):
        self.player.up() # no draw when moving
        self.player.goto(x-.5,y-.5)
        self.player.color(color)
        self.player.fillcolor(color)
        self.player.setheading(90)
        self.player.down()
        self.player.begin_fill()
        for i in range(4):
            self.player.forward(1)
            self.player.right(90)
        self.player.end_fill()

    # def maze_reset(self):
    #     self.wn = turtle.Screen().clear()

    # draw the move
    def Player_move(self,x,y):
        self.player.up()
        self.player.goto(x-15,-y+15)

    def Path_show(self,color):
        self.player.dot(10,color)

    def Pos_Update(self,row,col,val=None):
        if val:
            self.maze_list[row][col] = val
        self.Player_move(col,row)

        if val == record_path:
            color = 'green'
        elif val == wall:
            color = 'red'
        elif val == tried:
            color = 'black'
        elif val == dead_end:
            color = 'red'
        else:
            color = None

        if color:
            self.Path_show(color)

    # identify if at the exit -- WIN
    def Exit_Find(self,row,col):
        self.curr =(row,col)
        # exit is always on the outside wall, aka row or col is 0 or 30
		# but the special case, not the entrance, aka the start position
        IDexit = (
                    (row == 0 or
                    row == self.nrows-1 or
                    col == 0 or
                    col == self.ncols-1 ) and
                    self.curr != self.entrance
                )
        while IDexit:
            self.exit = (row,col)
            print('the function Id exit owrks at ',self.exit)
            break
        return (IDexit)

    # Allow 'Maze' object to support indexing
    def __getitem__(self,idx):
        return self.maze_list[idx]

    # Method One simple random walk -- recursive function
    def  solver_recursive(self, row, col):
        # try each of four directions from this point until we find a way out.
        # base Case return values:
        #  1. We have run into an wall, return false
        self.curr= (row,col)
        print('Now we at', self.curr)
        self.Pos_Update(row, col)
        if self[row][col] == wall :
            return False
        #  2. We have found a square that has already been explored
        if self[row][col] == tried or self[row][col] == dead_end:
            return False
        # 3. We have found an outside edge not occupied by an wall
        if self.Exit_Find(row,col):
            self.Pos_Update(row, col, record_path)
            print('Exit!!! Yeah! ')
            return True
        self.Pos_Update(row, col, tried)
        # Otherwise, use logical short circuiting to try each direction
        # in turn (if needed)
        found = self. solver_recursive(row-1, col) or \
                self. solver_recursive( row+1, col) or \
                self. solver_recursive( row, col-1) or \
                self. solver_recursive( row, col+1)
        if found:
            self.Pos_Update(row, col, record_path)
        else:
            self.Pos_Update(row, col, dead_end)
        print('Found: ',found,' ',self.curr )

        return found

    ## Method Two: A* algorithm
    # A* is based on the cost of the path and
    # an estimate of the cost required to extend the path all the way to the goal.
    def solver_astar(self):
        maze_list = self.maze_list
        tried_path, closed = [[self.entrance]], [self.entrance]
        # print(tried_path,closed)
        exit = self.exit

        # tried_path is a list of paths, each of which begins at the self.entrance
        # closed is a list of the cells we have found a shortest path to
        while len(tried_path) > 0:
            path = tried_path[0]
            pos_curr = path[len(path) - 1]
            # print("Current position in neighbour loop: ", pos_curr)

            if maze_list[pos_curr[0]][pos_curr[1]] == 'E':
                print('Exit!!! Yeah! ')
                print('Path', path)
                return path  # Found the exit
            self.Pos_Update(pos_curr[0], pos_curr[1], tried)

            # throw away the path we just tested.
            tried_path = tried_path[1:]
            # insert children of path into tried_path list. Each child is a path.
            for cell in self.neighbours(pos_curr, maze_list):
                self.Path_show('black')
                if cell not in closed:
                    tried_path = self.insert(path + [cell], tried_path, exit)
            closed = closed + [pos_curr]
            # and add its last cell to closed list
            # will not go there again
            # print("Been there: ", tried_path)
            self.astar_path = path
            self.astar_tried = tried_path
        return None

    # neighbours: cell*maze -> list<cell>
    # If c is a cell and M is a maze,
    # neighbours(C,M) is a list of the neighbours of C in M.
    def neighbours(self,curr, maze_list):

        neighbours = []
        i, j = curr
        # print("curr in neighbour loop: ", curr, ' ', maze_list[i][j])
        # print('Neighbours are ', maze_list[i][j + 1])

        if(i > 0):
            if maze_list[i - 1][j] != '+':
                neighbours += [(i - 1, j)]
        if(j > 0):
            if maze_list[i][j - 1] != '+':
                neighbours += [(i, j - 1)]
        if(i < len(maze_list) - 1):
            if maze_list[i + 1][j] != '+':
                neighbours += [(i + 1, j)]
        if(j < len(maze_list) - 1):
            if maze_list[i][j + 1] != '+':
                neighbours += [(i, j + 1)]

        # print("Neighbours: ", neighbours, 'with ch in maze',"'"+str(maze_list[neighbours[0][0]][neighbours[0][1]])+"'")
        return neighbours


    # insert: path * list<path>  * cell -> list<path>
    def insert(self,path, tried_path, exit):

        # The estimated total cost of a path is its length plus the manhattanD.
        # A* to minimize f(n) = g(n) + h(n)
        # where f(n) -- cost
        #       g(n) -- length
        #       h(n) -- manhattanD(?, exitPosition)
        # cost = length + manhattanD(?, exitPosition)
        for i in range(0, len(tried_path)):
            if len(path) + self.manhattanD(path[len(path) - 1], exit) <= \
                    len(tried_path) + self.manhattanD(tried_path[0][i], exit):
                # we always select  one with the the shorter distance, but move further
                return tried_path[0:i] + [path] + tried_path[i:len(tried_path)]
        return tried_path + [path]


    # ManhattanD: cell*cell -> int
    # manhattanD(c1,c2) is the Manhattan distance between c1 and c2
    def manhattanD(self,c1, c2):
        i1, j1 = c1
        # print(' i1, j1 = c1', c1)
        i2, j2 = c2
        # print('i2, j2 = c2',c2,' ', i2)
        return abs(i1 - i2) + abs(j1 - j2)

    # finally we show our shortest path with green dot
    def astar_path_show(self):
        for item in self.astar_path:
            self.Pos_Update(item[0], item[1], record_path)
