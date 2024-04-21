from pwn import *


"""
Materials from the NUS School of Computing CS2040S (Data Structures and Algorithms) course were utilized in the creation of this maze-solving challenge
"""

r = remote("127.0.0.1", 31112)


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


solver = MazeSolverWithPower()

for _ in range(50):
    r.recvuntil(b"LEVEL")
    r.recvuntil(b":")

    t1 = "You have been given"
    maze_str = r.recvuntil(t1).decode()[: -len(t1)]
    maze_rows = maze_str.split("\n")[1:-2]
    rows = len(maze_rows) // 2
    columns = rows

    t2 = "wall-phases"
    num_phase = int(r.recvuntil(t2).decode()[: -len(t2)])

    wall = [[[True, True, True, True] for _ in range(columns)] for _ in range(rows)]

    for i in range(rows):
        verts = list(maze_rows[i * 2 + 1])
        for j in range(columns - 1):
            has_wall = verts[5 + 4 * j] != " "
            wall[i][j][MazeSolverWithPower.EAST] = has_wall
            wall[i][j + 1][MazeSolverWithPower.WEST] = has_wall
        horiz = list(maze_rows[i * 2 + 2])
        if i < rows - 1:
            for j in range(columns):
                has_wall = horiz[3 + 4 * j] != " "
                wall[i][j][MazeSolverWithPower.SOUTH] = has_wall
                wall[i + 1][j][MazeSolverWithPower.NORTH] = has_wall
    rooms = [
        [
            Room(
                wall[i][j][MazeSolverWithPower.NORTH],
                wall[i][j][MazeSolverWithPower.SOUTH],
                wall[i][j][MazeSolverWithPower.EAST],
                wall[i][j][MazeSolverWithPower.WEST],
            )
            for j in range(columns)
        ]
        for i in range(rows)
    ]
    maze = Maze(rooms)

    solver.initialize(maze)
    ans = solver.path_search(0, 0, rows - 1, columns - 1, num_phase)
    print(ans)

    r.recvuntil(b"?")
    r.sendline(str(ans))
r.interactive()
