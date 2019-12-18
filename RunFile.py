from MazeSolving import Maze
import turtle

maze_samples = ['MazeSample1.txt','MazeSample2.txt']

for maze in maze_samples:
	while True:
		myMaze = Maze(maze)
		myMaze.MazePlot()
		myMaze.Pos_Update(myMaze.entrance[0],myMaze.entrance[1])
	# # Algo One -- simple random recursive one
		myMaze. solver_recursive( myMaze.entrance[0], myMaze.entrance[1])
		turtle.Screen().clear()
		break
	# turtle.Screen().bye()



for maze in maze_samples:
	while True:
		myMaze = Maze(maze)
		myMaze.MazePlot()
		myMaze.Pos_Update(myMaze.entrance[0],myMaze.entrance[1])
		# Algo Two -- A* algorithm
		print("Path to the exit: ", myMaze.solver_astar())
		myMaze.astar_path_show()
		turtle.Screen().clear()
		break


