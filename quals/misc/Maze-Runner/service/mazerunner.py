#!/usr/local/bin/python

import random

"""
Materials from the NUS School of Computing CS2040S (Data Structures and Algorithms) course were utilized in the creation of this maze-solving challenge
"""


class Room:
    def __init__(self, north, south, east, west):
        self.north_wall = north
        self.south_wall = south
        self.east_wall = east
        self.west_wall = west
        self.on_path = False

    def has_west_wall(self):
        return self.west_wall

    def has_east_wall(self):
        return self.east_wall

    def has_north_wall(self):
        return self.north_wall

    def has_south_wall(self):
        return self.south_wall


class Maze:
    WALL = "#"

    def __init__(self, rooms):
        assert len(rooms) > 0
        self.rooms = rooms
        self.rows = len(rooms) * 2 + 1
        self.columns = len(rooms[0]) * 2 + 1

    def get_room(self, row, column):
        if (
            row >= self.get_rows()
            or column >= self.get_columns()
            or row < 0
            or column < 0
        ):
            raise ValueError()
        return self.rooms[row][column]

    def get_rows(self):
        return self.rows // 2

    def get_columns(self):
        return self.columns // 2


class MazeSolverWithPower:
    NORTH, SOUTH, EAST, WEST = range(4)
    DELTAS = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # North  # South  # East  # West

    class Pair:
        def __init__(self, coord, dist):
            self.coord = coord
            self.dist = dist

    class Coord:
        def __init__(self, row, col, superpower_left):
            self.row = row
            self.col = col
            self.superpower_left = superpower_left

    def __init__(self):
        pass

    def initialize(self, maze):
        self.maze = maze

    def move(self, frontier, visited, parent, curr, direction, dist, use_superpower):
        next_row = curr.row + self.DELTAS[direction][0]
        next_col = curr.col + self.DELTAS[direction][1]
        next_superpower_left = curr.superpower_left - (1 if use_superpower else 0)

        if (
            next_row < 0
            or next_row > self.maze.get_rows() - 1
            or next_col < 0
            or next_col > self.maze.get_columns() - 1
        ):
            return
        if (
            next_superpower_left < 0
            or visited[next_row][next_col][next_superpower_left]
        ):
            return

        visited[next_row][next_col][next_superpower_left] = True
        parent[next_row][next_col][next_superpower_left] = curr

        frontier.append(
            self.Pair(self.Coord(next_row, next_col, next_superpower_left), dist + 1)
        )

        for i in range(self.max_superpower + 1):
            if i != next_superpower_left and visited[next_row][next_col][i]:
                return

    def path_search(self, start_row, start_col, end_row, end_col, superpowers):
        self.max_superpower = superpowers

        frontier = []
        visited = [
            [[False] * (superpowers + 1) for _ in range(self.maze.get_columns())]
            for _ in range(self.maze.get_rows())
        ]
        parent = [
            [[None] * (superpowers + 1) for _ in range(self.maze.get_columns())]
            for _ in range(self.maze.get_rows())
        ]

        visited[start_row][start_col][superpowers] = True
        frontier.append(self.Pair(self.Coord(start_row, start_col, superpowers), 0))

        while frontier:
            curr_pair = frontier.pop(0)
            curr_dist = curr_pair.dist
            curr_coord = curr_pair.coord

            if curr_coord.row == end_row and curr_coord.col == end_col:
                par_coord = curr_coord
                while (
                    parent[par_coord.row][par_coord.col][par_coord.superpower_left]
                    is not None
                ):
                    self.maze.get_room(par_coord.row, par_coord.col).on_path = True
                    par_coord = parent[par_coord.row][par_coord.col][
                        par_coord.superpower_left
                    ]
                self.maze.get_room(par_coord.row, par_coord.col).on_path = True
                return curr_dist

            room = self.maze.get_room(curr_coord.row, curr_coord.col)

            self.move(
                frontier,
                visited,
                parent,
                curr_coord,
                self.NORTH,
                curr_dist,
                room.has_north_wall(),
            )
            self.move(
                frontier,
                visited,
                parent,
                curr_coord,
                self.SOUTH,
                curr_dist,
                room.has_south_wall(),
            )
            self.move(
                frontier,
                visited,
                parent,
                curr_coord,
                self.EAST,
                curr_dist,
                room.has_east_wall(),
            )
            self.move(
                frontier,
                visited,
                parent,
                curr_coord,
                self.WEST,
                curr_dist,
                room.has_west_wall(),
            )


class MazeGenerator:
    NORTH, SOUTH, EAST, WEST = range(4)
    DELTAS = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # North  # South  # East  # West

    class Pair:
        def __init__(self, row, col):
            self.row = row
            self.col = col

    @staticmethod
    def generate_maze(rows, columns):
        wall = [[[True, True, True, True] for _ in range(columns)] for _ in range(rows)]
        visited = [[False for _ in range(columns)] for _ in range(rows)]

        stack = [MazeGenerator.Pair(0, 0)]
        visited[0][0] = True  # Marking the start cell as visited
        while stack:
            current = stack[-1]
            row, col = current.row, current.col
            unvisited_neighbors = []

            for index, delta in enumerate(MazeGenerator.DELTAS):
                new_row = row + delta[0]
                new_col = col + delta[1]

                if (
                    0 <= new_row < rows
                    and 0 <= new_col < columns
                    and not visited[new_row][new_col]
                ):
                    unvisited_neighbors.append((index, new_row, new_col))

            if unvisited_neighbors:
                index, new_row, new_col = random.choice(unvisited_neighbors)
                wall[row][col][index] = False
                index_opposite = (
                    1 if index == 0 else 0 if index == 1 else 3 if index == 2 else 2
                )  # Finding the opposite direction
                wall[new_row][new_col][index_opposite] = False
                stack.append(MazeGenerator.Pair(new_row, new_col))
                visited[new_row][new_col] = True  # Marking the new cell as visited
            else:
                stack.pop()  # Backtrack when there are no unvisited neighbors

        rooms = [
            [
                Room(
                    wall[i][j][MazeGenerator.NORTH],
                    wall[i][j][MazeGenerator.SOUTH],
                    wall[i][j][MazeGenerator.EAST],
                    wall[i][j][MazeGenerator.WEST],
                )
                for j in range(columns)
            ]
            for i in range(rows)
        ]
        return Maze(rooms)


class MazePrinter:
    class PrinterBlocks:
        WALL = "##"
        PATH = "XX"
        AIR = "  "

        WALL_VERTICAL = " ┃"
        WALL_HORIZONTAL = "━━"
        WALL_TOPLEFT = " ┏"
        WALL_TOPRIGHT = "━┓"
        WALL_BOTTOMLEFT = " ┗"
        WALL_BOTTOMRIGHT = "━┛"
        WALL_LEFT = "━┫"
        WALL_RIGHT = " ┣"
        WALL_UP = "━┻"
        WALL_DOWN = "━┳"
        WALL_CORNER = "━╋"

        WALL_LEFTHALF = "━ "
        WALL_RIGHTHALF = " ━"
        WALL_TOPHALF = " ╹"
        WALL_BOTTOMHALF = " ╻"

    CORNER = [
        PrinterBlocks.AIR,
        PrinterBlocks.WALL_LEFTHALF,
        PrinterBlocks.WALL_RIGHTHALF,
        PrinterBlocks.WALL_HORIZONTAL,
        PrinterBlocks.WALL_BOTTOMHALF,
        PrinterBlocks.WALL_TOPRIGHT,
        PrinterBlocks.WALL_TOPLEFT,
        PrinterBlocks.WALL_DOWN,
        PrinterBlocks.WALL_TOPHALF,
        PrinterBlocks.WALL_BOTTOMRIGHT,
        PrinterBlocks.WALL_BOTTOMLEFT,
        PrinterBlocks.WALL_UP,
        PrinterBlocks.WALL_VERTICAL,
        PrinterBlocks.WALL_LEFT,
        PrinterBlocks.WALL_RIGHT,
        PrinterBlocks.WALL_CORNER,
    ]

    def print_maze(self, maze):
        for i in range(maze.get_rows()):
            print(
                (
                    self.PrinterBlocks.WALL_TOPLEFT
                    if i == 0
                    else (
                        self.PrinterBlocks.WALL_RIGHT
                        if maze.get_room(i, 0).has_north_wall()
                        else self.PrinterBlocks.WALL_VERTICAL
                    )
                ),
                end="",
            )
            for j in range(maze.get_columns()):
                room = maze.get_room(i, j)
                if room.has_north_wall():
                    print(self.PrinterBlocks.WALL_HORIZONTAL, end="")
                else:
                    if i > 0 and maze.get_room(i - 1, j).on_path and room.on_path:
                        print(self.PrinterBlocks.PATH, end="")
                    else:
                        print(self.PrinterBlocks.AIR, end="")

                if i == 0:
                    print(
                        (
                            self.PrinterBlocks.WALL_TOPRIGHT
                            if j == maze.get_columns() - 1
                            else (
                                self.PrinterBlocks.WALL_DOWN
                                if room.has_east_wall()
                                else self.PrinterBlocks.WALL_HORIZONTAL
                            )
                        ),
                        end="",
                    )
                elif j == maze.get_columns() - 1:
                    print(
                        (
                            self.PrinterBlocks.WALL_LEFT
                            if room.has_north_wall()
                            else self.PrinterBlocks.WALL_VERTICAL
                        ),
                        end="",
                    )
                else:
                    north = maze.get_room(i - 1, j).has_east_wall()
                    south = room.has_east_wall()
                    west = room.has_north_wall()
                    east = maze.get_room(i, j + 1).has_north_wall()

                    corner = (
                        (1 if north else 0) * 8
                        + (1 if south else 0) * 4
                        + (1 if east else 0) * 2
                        + (1 if west else 0)
                    )
                    print(self.CORNER[corner], end="")
            print()

            for j in range(maze.get_columns()):
                room = maze.get_room(i, j)
                if room.has_west_wall():
                    print(self.PrinterBlocks.WALL_VERTICAL, end="")
                else:
                    if j > 0 and maze.get_room(i, j - 1).on_path and room.on_path:
                        print(self.PrinterBlocks.PATH, end="")
                    else:
                        print(self.PrinterBlocks.AIR, end="")

                if room.on_path:
                    print(self.PrinterBlocks.PATH, end="")
                else:
                    print(self.PrinterBlocks.AIR, end="")
            print(self.PrinterBlocks.WALL_VERTICAL)

        print(self.PrinterBlocks.WALL_BOTTOMLEFT, end="")
        print(self.PrinterBlocks.WALL_HORIZONTAL, end="")
        for j in range(maze.get_columns() - 1):
            print(
                (
                    self.PrinterBlocks.WALL_UP
                    if maze.get_room(maze.get_rows() - 1, j).has_east_wall()
                    else self.PrinterBlocks.WALL_HORIZONTAL
                ),
                end="",
            )
            print(self.PrinterBlocks.WALL_HORIZONTAL, end="")
        print(self.PrinterBlocks.WALL_BOTTOMRIGHT, end="")
        print()


def generate_problem(lvl, sz, superpowers):
    print(f"LEVEL {lvl}:")
    maze = MazeGenerator.generate_maze(sz, sz)
    solver = MazeSolverWithPower()
    MazePrinter().print_maze(maze)

    solver.initialize(maze)
    sol = solver.path_search(0, 0, sz - 1, sz - 1, superpowers)

    print(f"\nYou have been given {superpowers} wall-phases\n")
    print("Hurry! How many steps does it take to escape? ")

    ans = input("")
    try:
        if int(ans) == sol:
            return True
    except:
        pass

    print(
        f"I think you can run faster! You could've followed this map instead and got {sol} steps!"
    )
    MazePrinter().print_maze(maze)
    exit(0)


BREAK_LINE = 50 * "-"
WELCOME = (
    """Welcome fellow Maze Runners!

Prepare yourselves to embark on a quest like no other. Your mission is simple: conquer a series of perplexing mazes by finding the shortest path from one corner to another. Here's a map of the route taken by one of your teammates.

┏━━━┳━━━━━━━━━━━┳━━━┓
┃XX ┃           ┃   ┃
┃XX ┃   ━━━━┓   ╹   ┃
┃XX ┃       ┃       ┃
┃XX ┃   ╻   ┗━━━━━━ ┃
┃XX ┃   ┃           ┃
┃XX ┗━━━╋━━━━━━━    ┃
┃XXXXXX ┃XXXXXXXXXX ┃
┣━━━ XX ╹XX ┏━━━ XX ┃
┃    XXXXXX ┃    XX ┃
┗━━━━━━━━━━━┻━━━━━━━┛

But beware! The path to victory is fraught with obstacles and dead ends. Fear not, however, for you possess a remarkable ability to transcend the barriers of conventional navigation. With a limited number of opportunities to phase through walls, your choices will shape your journey's outcome.

Do you have what it takes to unravel the mysteries of these labyrinthine puzzles and emerge victorious? The fate of your team rests in your hands. May your steps be swift as you navigate through the maze of challenges that await!

"""
    + BREAK_LINE
)
MIN_LEVEL = 5
MAX_LEVEL = 54
SUPERPOWER_SCALE_MIN = 0
SUPERPOWER_SCALE_MAX = 0.4


if __name__ == "__main__":
    print(WELCOME)
    level = 1
    for N in range(MIN_LEVEL, MAX_LEVEL + 1):
        superpower = int(
            (
                SUPERPOWER_SCALE_MIN
                + (SUPERPOWER_SCALE_MAX - SUPERPOWER_SCALE_MIN) * random.random()
            )
            * N
        )
        correct = generate_problem(level, N, superpower)
        level += 1
        print("\n" + BREAK_LINE)

    print(
        """Congratulations! You've made it out of the maze! Your determination, courage, and problem-solving skills have led you to freedom. Now, embrace the next chapter of your journey with the same resilience and bravery. The maze may be behind you, but the adventure continues!\n"""
    )

    with open("flag.txt") as f:
        print(f.readline())
