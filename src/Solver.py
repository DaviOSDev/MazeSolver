class Node():
    def __init__(self, state, parent, action, distance, steps = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.distance = distance
        self.steps = steps

    def __str__(self) -> str:
        return f"Node: {self.state}"
    
class Frontier():

    def __init__(self) -> None:
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def isEmpty(self):
        return len(self.frontier) == 0
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

class QueueFrontier(Frontier):

    def pop(self):
        if self.isEmpty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
    
class StackFrontier(Frontier):

    def pop(self):
        if self.isEmpty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        
class Maze():
    def __init__(self, filename) -> None:

        with open (filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")
        
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        self.distanceToGoal = []
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        row.append(1)
                        self.start = (i, j)

                    elif contents[i][j] == "B":
                        row.append(2)
                        self.goal = (i, j)

                    elif contents[i][j] == "." or contents[i][j] == " ":
                        row.append(0)

                    else:
                        row.append(3)

                except IndexError:
                    row.append(-1)

            self.walls.append(row)
            self.distanceToGoal.append([0] * self.width)
        
        self.calculateDistance()
        self.solution = None
    
    def calculateDistance(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.walls[x][y] == 0 or self.walls[x][y] == 1:
                    self.distanceToGoal[x][y] = abs(self.goal[0] - x) + abs(self.goal[1] - y)   

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col == 3:
                    print("█", end="")

                elif (i, j) == self.start:
                    print("A", end="")

                elif (i, j) == self.goal:
                    print("B", end="")

                elif solution is not None and (i, j) in solution:
                    print("*", end="")

                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        
        candidates = [
            ("↑", (row -1, col)),
            ("↓", (row + 1, col)),
            ("←", (row, col -1)),
            ("→", (row, col +1))
        ]

        neighbors = []
        for action, (x, y) in candidates:
            if 0 <= x < self.height and 0 <= y < self.width and self.walls[x][y] != 3:
                neighbors.append((action, (x, y)))
        
        return neighbors
    
    def getMinDistance(self, frontier):
        node = frontier[0]
        for child in frontier:
            if (child.distance + (child.steps)) < (node.distance + (node.steps)):
                node = child
        frontier.pop(frontier.index(node))
        return node
    
    def solve(self):

        start = Node(state=self.start, parent=None, action=None, distance=self.distanceToGoal[self.start[0]][self.start[1]])
        frontier = StackFrontier()
        frontier.add(start)

        self.numExplored = 0
        self.explored = set()

        while True:

            if frontier.isEmpty():
                print("no solution")
                return
            
            #A* search
            node = self.getMinDistance(frontier.frontier)
            
            # DFS
            #node = frontier.pop()
            self.presentSteps = node.steps
            self.presentSteps += 1
            self.numExplored += 1
            

            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action, distance=self.distanceToGoal[state[0]][state[1]], steps=self.presentSteps)
                    frontier.add(child)


    def DrawImage(self, filename, showSolution = True, showExplored=False):
        from PIL import Image, ImageDraw

        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )

        draw = ImageDraw.Draw(img)
        if self.solution is not None:
            solution = self.solution[1]
        else:
            solution = None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                
                # Walls
                if col == 3:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and showSolution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and showExplored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
                draw.text([j * cell_size + cell_border, i * cell_size + cell_border],f"{self.distanceToGoal[i][j]}", fill=(0, 0, 0))

        img.save(filename)

import sys

if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

filename = sys.argv[1]
maze = Maze(filename)
print("Maze:")
maze.print()
print("Solving...")
maze.solve()
print("Solution:")
maze.print()
maze.DrawImage("maze.png", True, True)
print(f"Number of steps: {len(maze.solution[0])}")
print(f"Number of explored cells: {maze.numExplored}")
print(f"Steps: {maze.solution[0]}")