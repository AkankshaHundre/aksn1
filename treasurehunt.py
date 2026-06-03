import time

print("=================================")
print("      AI TREASURE HUNT MAZE")
print("=================================")

# ---------------- LEVELS ----------------

print("\nSelect Level")
print("1. Easy")
print("2. Medium")

level = input("Enter choice: ")

if level == "1":
    maze = [
        ['S', '.', '.', '#', '.'],
        ['#', '#', '.', '#', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '.'],
        ['.', '.', '.', 'T', '.']
    ]

elif level == "2":
    maze = [
        ['S', '#', '.', '.', '.'],
        ['.', '#', '.', '#', '.'],
        ['.', '.', '.', '#', '.'],
        ['#', '#', '.', '.', '.'],
        ['.', '.', '#', 'T', '.']
    ]

else:
    print("Invalid Choice")
    exit()

# ---------------- DISPLAY ----------------

symbols = {
    'S': '🟩',
    'T': '💰',
    '#': '⬛',
    '.': '⬜',
    '*': '🟨',
    'P': '🧙'
}

def show_maze(board):
    for row in board:
        for cell in row:
            print(symbols[cell], end=" ")
        print()
    print()

show_maze(maze)

# ---------------- FIND START ----------------

def find_start():
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                return (i, j)

start = find_start()

# ---------------- DFS ----------------

visited = set()
path = []

def dfs(x, y):

    if maze[x][y] == 'T':
        path.append((x, y))
        return True

    visited.add((x, y))
    path.append((x, y))

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dx, dy in directions:

        nx = x + dx
        ny = y + dy

        if (0 <= nx < len(maze) and
            0 <= ny < len(maze[0]) and
            maze[nx][ny] != '#' and
            (nx, ny) not in visited):

            if dfs(nx, ny):
                return True

    path.pop()
    return False

# ---------------- PLAYER MODE ----------------

def play_game():

    x, y = start
    steps = 0

    while maze[x][y] != 'T':

        board = [row[:] for row in maze]
        board[x][y] = 'P'

        show_maze(board)

        move = input("Move (W/A/S/D): ").upper()

        nx, ny = x, y

        if move == 'W':
            nx -= 1

        elif move == 'S':
            nx += 1

        elif move == 'A':
            ny -= 1

        elif move == 'D':
            ny += 1

        else:
            print("Invalid Move")
            continue

        if (0 <= nx < len(maze) and
            0 <= ny < len(maze[0]) and
            maze[nx][ny] != '#'):

            x = nx
            y = ny
            steps += 1

        else:
            print("Wall Hit!")

    print("\n🎉 TREASURE FOUND!")
    print("Your Steps:", steps)

    return steps

# ---------------- AI SOLVER ----------------

def ai_solve():

    visited.clear()
    path.clear()

    dfs(start[0], start[1])

    print("\nAI Exploring...\n")

    for step in path:

        board = [row[:] for row in maze]

        for px, py in path:
            if board[px][py] not in ['S', 'T']:
                board[px][py] = '*'

        x, y = step

        if board[x][y] not in ['S', 'T']:
            board[x][y] = 'P'

        show_maze(board)

        time.sleep(0.4)

    print("💰 Treasure Found!")
    print("Path Length:", len(path))
    print("Visited Cells:", len(visited))
    print("Score:", 100 - len(path))

# ---------------- MENU ----------------

print("=================================")
print("1. Play Yourself")
print("2. Watch AI Solve")
print("3. Race Against AI")
print("=================================")

choice = input("Choose Mode: ")

# ---------- PLAY ----------

if choice == "1":

    play_game()

# ---------- AI ----------

elif choice == "2":

    ai_solve()

# ---------- RACE ----------

elif choice == "3":

    print("\nYOUR TURN\n")

    player_steps = play_game()

    visited.clear()
    path.clear()

    dfs(start[0], start[1])

    ai_steps = len(path)

    print("\n=========== RESULT ===========")
    print("Your Steps :", player_steps)
    print("AI Steps   :", ai_steps)

    if player_steps < ai_steps:
        print("🏆 You Beat The AI!")

    elif player_steps > ai_steps:
        print("🤖 AI Wins!")

    else:
        print("🤝 Draw!")

else:
    print("Invalid Choice")
