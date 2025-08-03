import tkinter as tk
import random
import json
import os

CELL_SIZE = 20
GRID_WIDTH = 25
GRID_HEIGHT = 25
UPDATE_DELAY = 100  # ms

SAVE_FILE = 'snake_game_save.json'

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake Game Deluxe 🐍")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=CELL_SIZE * GRID_WIDTH,
                                height=CELL_SIZE * GRID_HEIGHT, bg="#1e1e1e", bd=0, highlightthickness=0)
        self.canvas.pack()

        self.score = 0
        self.high_score = 0
        self.snake = [(5, 5)]
        self.direction = (1, 0)
        self.food = None
        self.game_running = False

        self.load_data()
        self.draw_ui()
        self.reset_game()

        self.root.bind("<Key>", self.change_direction)

    def draw_ui(self):
        self.top_frame = tk.Frame(self.root, bg="#282c34")
        self.top_frame.pack(fill="x")

        self.score_label = tk.Label(self.top_frame, text="Score: 0", fg="white", bg="#282c34",
                                    font=("Consolas", 14, "bold"))
        self.score_label.pack(side="left", padx=10)

        self.high_score_label = tk.Label(self.top_frame, text=f"High Score: {self.high_score}", fg="white",
                                         bg="#282c34", font=("Consolas", 14, "bold"))
        self.high_score_label.pack(side="right", padx=10)

        self.reset_button = tk.Button(self.top_frame, text="🔁 Restart", command=self.reset_game,
                                      bg="#61afef", fg="white", font=("Consolas", 12, "bold"), bd=0, relief="flat")
        self.reset_button.pack(side="left", padx=10)

    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
            except:
                self.high_score = 0

    def save_data(self):
        with open(SAVE_FILE, 'w') as f:
            json.dump({"high_score": self.high_score}, f)

    def reset_game(self):
        self.snake = [(5, 5)]
        self.direction = (1, 0)
        self.score = 0
        self.game_running = True
        self.spawn_food()
        self.update_ui()
        self.game_loop()

    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def change_direction(self, event):
        key = event.keysym
        new_dir = {
            'Up': (0, -1),
            'Down': (0, 1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }.get(key)

        if new_dir:
            opposite = (-self.direction[0], -self.direction[1])
            if new_dir != opposite:  # Prevent reversing
                self.direction = new_dir

    def game_loop(self):
        if not self.game_running:
            return

        head_x, head_y = self.snake[-1]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.end_game()
            return

        self.snake.append(new_head)

        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop(0)

        self.update_ui()
        self.root.after(UPDATE_DELAY, self.game_loop)

    def update_ui(self):
        self.canvas.delete("all")

        # Draw snake
        for segment in self.snake:
            x1 = segment[0] * CELL_SIZE
            y1 = segment[1] * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#98c379", outline="#1e1e1e")

        # Draw head with highlight
        hx, hy = self.snake[-1]
        self.canvas.create_rectangle(hx * CELL_SIZE, hy * CELL_SIZE,
                                     hx * CELL_SIZE + CELL_SIZE, hy * CELL_SIZE + CELL_SIZE,
                                     fill="#e06c75", outline="#1e1e1e")

        # Draw food
        fx, fy = self.food
        self.canvas.create_oval(fx * CELL_SIZE, fy * CELL_SIZE,
                                fx * CELL_SIZE + CELL_SIZE, fy * CELL_SIZE + CELL_SIZE,
                                fill="#d19a66", outline="#1e1e1e")

        self.score_label.config(text=f"Score: {self.score}")

    def end_game(self):
        self.game_running = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_data()
        self.high_score_label.config(text=f"High Score: {self.high_score}")
        self.canvas.create_text(CELL_SIZE * GRID_WIDTH // 2,
                                CELL_SIZE * GRID_HEIGHT // 2,
                                text="Game Over", fill="white",
                                font=("Consolas", 24, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SnakeGame(root)
    root.mainloop()
