from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
import random
import json
import os

CELL_SIZE = 20
GRID_WIDTH = 25
GRID_HEIGHT = 25
UPDATE_DELAY = 0.1
SAVE_FILE = "snake_game_save.json"


class SnakeGame(Widget):
    def __init__(self, score_label, high_score_label, **kwargs):
        super().__init__(**kwargs)
        self.score_label = score_label
        self.high_score_label = high_score_label

        self.snake = [(5, 5)]
        self.direction = (1, 0)
        self.food = None
        self.score = 0
        self.high_score = 0
        self.game_running = True

        self.load_data()
        self.spawn_food()
        self.update_canvas()

        Clock.schedule_interval(self.update, UPDATE_DELAY)
        Window.bind(on_key_down=self.on_key_down)

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
        self.update_canvas()
        self.score_label.text = f"Score: {self.score}"
        self.high_score_label.text = f"High Score: {self.high_score}"

    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def on_key_down(self, window, key, *args):
        key_map = {
            273: (0, 1),   # Up
            274: (0, -1),  # Down
            276: (-1, 0),  # Left
            275: (1, 0)    # Right
        }
        if key in key_map:
            new_dir = key_map[key]
            opposite = (-self.direction[0], -self.direction[1])
            if new_dir != opposite:
                self.direction = new_dir

    def update(self, dt):
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

        self.update_canvas()
        self.score_label.text = f"Score: {self.score}"

    def update_canvas(self):
        self.canvas.clear()
        with self.canvas:
            # Snake body
            for segment in self.snake[:-1]:
                Color(0.6, 0.8, 0.5)
                Rectangle(pos=(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE),
                          size=(CELL_SIZE, CELL_SIZE))

            # Snake head
            head = self.snake[-1]
            Color(1, 0.4, 0.4)
            Rectangle(pos=(head[0] * CELL_SIZE, head[1] * CELL_SIZE),
                      size=(CELL_SIZE, CELL_SIZE))

            # Food
            Color(0.8, 0.6, 0.3)
            Ellipse(pos=(self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE),
                    size=(CELL_SIZE, CELL_SIZE))

    def end_game(self):
        self.game_running = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_data()

        self.high_score_label.text = f"High Score: {self.high_score}"
        self.score_label.text = f"Game Over! Final Score: {self.score}"
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1)
            Rectangle(pos=(0, (GRID_HEIGHT * CELL_SIZE) // 2 - 20),
                      size=(GRID_WIDTH * CELL_SIZE, 40))


class SnakeApp(App):
    def build(self):
        Window.size = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE + 40)
        main_layout = BoxLayout(orientation="vertical", padding=0, spacing=0)

        # Score bar
        top_bar = BoxLayout(size_hint_y=None, height=40, padding=10, spacing=10)
        self.score_label = Label(text="Score: 0", color=(1, 1, 1, 1),
                                 bold=True, font_size=16)
        self.high_score_label = Label(text="High Score: 0", color=(1, 1, 1, 1),
                                      bold=True, font_size=16)

        restart_btn = Button(text="🔁 Restart", background_color=(0.2, 0.6, 1, 1),
                             color=(1, 1, 1, 1), bold=True)
        restart_btn.bind(on_press=self.restart_game)

        top_bar.add_widget(self.score_label)
        top_bar.add_widget(self.high_score_label)
        top_bar.add_widget(restart_btn)

        # Game
        self.game = SnakeGame(score_label=self.score_label, high_score_label=self.high_score_label)

        main_layout.add_widget(top_bar)
        main_layout.add_widget(self.game)
        return main_layout

    def restart_game(self, instance):
        self.game.reset_game()


if __name__ == '__main__':
    SnakeApp().run()
