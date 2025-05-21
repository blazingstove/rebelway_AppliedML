"""
a_star.py 

Implements an A* pathfinding class to solve a path through a grid maze

"""

import heapq

class AStarPathFinding:
    """ Class for solving path through a maze """

    def __init__(self, maze, start_pos, target_pos):

        self.maze = maze
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.open_list = []
        self.closed_set = set()
        self.came_from = {}

    def heuristic(self, a, b):
        """ Return distance between a and b using 
        Manhattan (aka Taxicab) distance ( movement along a grid ) """

        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def is_valid(self, pos):
        """ Return True if the input pos is within the bounds of the maze, False othehrwise """

        row, col = pos
        return 0 <= row < len(self.maze) and 0 <= col < len(self.maze[0]) and self.maze[row][col] == 1
    
    def get_neighbors(self, pos):
        """ Return a list of adjacent (valid) neigbors in the maze """

        neighbors = []
        directions = [(0,1), (1,0), (0,-1), (-1,0) ]

        for d in directions:
            neighbor = (pos[0] + d[0] , pos[1] + d[1])
            if self.is_valid(neighbor):
                neighbors.append(neighbor)
        return neighbors

    def reconstruct_path(self, current):
        """ Return the reversed list of path steps back to the original 
        starting point"""

        path = [current]
        
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)
        path.reverse()
        return path

    def find_path(self)->list:
        """ Calculate the optimal path through the maze from the starting pos to the target pos 
        and return a list of the path steps if successful, False otherwise """

        heapq.heappush(self.open_list, (0, self.start_pos))

        g_score = {self.start_pos: 0}
        f_score = {self.start_pos: self.heuristic(self.start_pos, self.target_pos)}

        while self.open_list:
            _, current = heapq.heappop(self.open_list)
            
            if current == self.target_pos:
                return self.reconstruct_path(current)
            
            self.closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in self.closed_set:
                    continue
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    self.came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, self.target_pos)

                    heapq.heappush(self.open_list, (f_score[neighbor], neighbor) )

        return None

if __name__ == "__main__":

    maze = [

            [1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 1],
            [0, 1, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1]]

    start_pos = (0,1)
    target_pos = (7,7)

    path_finder = AStarPathFinding(maze, start_pos, target_pos)
    path = path_finder.find_path()

    if path:
        print("Path found :", path)
    else:
        print("No path found")