import tkinter as tk
from tkinter import messagebox

# Configuration
CELL_SIZE = 70
MAZE = [
    ['S', '.', 'D', '.', '.'],
    ['#', '.', '#', '.', 'D'],
    ['D', '.', '.', '#', '.'],
    ['.', '#', 'D', '.', '.'],
    ['D', '.', '.', '.', 'E']
]

class DiamondRace:
    def __init__(self, root):
        self.root = root
        self.root.title("Diamond Collector: Score Battle")
        
        self.rows = len(MAZE)
        self.cols = len(MAZE[0])
        
        # Positions and Scores
        self.human_pos = self.find_start()
        self.ai_pos = self.find_start()
        self.human_score = 0
        self.ai_score = 0
        self.game_over = False

        # AI Pathfinding
        self.ai_path = []
        self.get_ai_strategy()

        # Canvas Setup
        self.canvas = tk.Canvas(root, width=self.cols*CELL_SIZE, height=self.rows*CELL_SIZE, bg="#f0f0f0")
        self.canvas.pack(pady=10)
        
        self.score_label = tk.Label(root, text="YOU: 0 | BOT: 0", font=("Courier", 18, "bold"), fg="#2c3e50")
        self.score_label.pack()

        # Controls
        self.root.bind("<KeyPress>", self.move_human)
        
        self.draw_grid()
        self.move_ai_loop()

    def find_start(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if MAZE[r][c] == 'S': return (r, c)
        return (0, 0)

    def get_ai_strategy(self):
        """Uses DFS to find a path that hits as many diamonds as possible"""
        path_found = []
        visited = set()

        def dfs(r, c, current_path):
            if (r, c) == (self.rows-1, self.cols-1):
                path_found.append(list(current_path))
                return
            
            visited.add((r, c))
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < self.rows and 0 <= nc < self.cols and 
                    MAZE[nr][nc] != '#' and (nr, nc) not in visited):
                    current_path.append((nr, nc))
                    dfs(nr, nc, current_path)
                    current_path.pop()
            visited.remove((r, c))

        dfs(self.ai_pos[0], self.ai_pos[1], [self.ai_pos])
        # Pick the path that has the most diamonds ('D') in it
        self.ai_path = max(path_found, key=lambda p: sum(1 for r, c in p if MAZE[r][c] == 'D'))

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1, x2, y2 = c*CELL_SIZE, r*CELL_SIZE, (c+1)*CELL_SIZE, (r+1)*CELL_SIZE
                
                # Draw environment
                color = "white"
                content = ""
                if MAZE[r][c] == '#': color = "#34495e"
                elif MAZE[r][c] == 'D': content = "💎"
                elif MAZE[r][c] == 'E': color = "#2ecc71"
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#bdc3c7")
                if content: self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=content, font=("Arial", 24))

        # Draw Players
        self.draw_player(self.ai_pos, "#e74c3c", "🤖")
        self.draw_player(self.human_pos, "#3498db", "👤")

    def draw_player(self, pos, color, icon):
        r, c = pos
        x, y = c*CELL_SIZE + CELL_SIZE//2, r*CELL_SIZE + CELL_SIZE//2
        self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
        self.canvas.create_text(x, y, text=icon, font=("Arial", 16))

    def move_human(self, event):
        if self.game_over: return
        r, c = self.human_pos
        if event.keysym == 'Up': r -= 1
        elif event.keysym == 'Down': r += 1
        elif event.keysym == 'Left': c -= 1
        elif event.keysym == 'Right': c += 1

        if 0 <= r < self.rows and 0 <= c < self.cols and MAZE[r][c] != '#':
            self.human_pos = (r, c)
            self.check_collect(r, c, "human")
            self.draw_grid()
            if MAZE[r][c] == 'E': self.end_game()

    def move_ai_loop(self):
        if self.game_over: return
        if self.ai_path:
            self.ai_pos = self.ai_path.pop(0)
            self.check_collect(self.ai_pos[0], self.ai_pos[1], "ai")
            self.draw_grid()
            if MAZE[self.ai_pos[0]][self.ai_pos[1]] == 'E':
                self.end_game()
                return
        self.root.after(700, self.move_ai_loop)

    def check_collect(self, r, c, player):
        if MAZE[r][c] == 'D':
            MAZE[r][c] = '.'
            if player == "human": self.human_score += 1
            else: self.ai_score += 1
            self.score_label.config(text=f"YOU: {self.human_score} | BOT: {self.ai_score}")

    def end_game(self):
        self.game_over = True
        result = "It's a Tie!"
        if self.human_score > self.ai_score: result = "You Win! 🏆"
        elif self.ai_score > self.human_score: result = "AI Wins! 🤖"
        
        messagebox.showinfo("Match Ended", f"{result}\n\nFinal Score:\nYou: {self.human_score}\nAI: {self.ai_score}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = DiamondRace(root)
    root.mainloop()