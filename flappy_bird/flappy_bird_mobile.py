# flappy_bird_kivy_fixed.py
import kivy
kivy.require("2.3.0")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import random, json, os, time

WIDTH, HEIGHT = 420, 640
FPS = 1 / 60
BIRD_SIZE = 34
BIRD_X = 110
GRAVITY = -900.0        # Negative because up is positive in Kivy
FLAP_V = 340.0
PIPE_WIDTH = 72
PIPE_GAP = 170
PIPE_SPEED = 180.0
SPAWN_INTERVAL = 1.6
SAVE_FILE = "flappy_highscore.json"
BG_COLOR = "#70c5ce"
GROUND_HEIGHT = 80

def load_highscore():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return int(json.load(f).get("high_score", 0))
        except:
            return 0
    return 0

def save_highscore(score):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump({"high_score": int(score)}, f)
    except:
        pass

def rects_intersect(a, b):
    return not (a[2] <= b[0] or a[0] >= b[2] or a[3] <= b[1] or a[1] >= b[3])

class FlappyGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (WIDTH, HEIGHT)
        Window.clearcolor = get_color_from_hex(BG_COLOR)

        self.state = "menu"
        self.bird_y = HEIGHT // 2
        self.bird_v = 0
        self.pipes = []
        self.spawn_timer = 0
        self.score = 0
        self.high_score = load_highscore()
        self.last_time = time.time()

        self.score_label = Label(text="", font_size=28, color=(1, 1, 1, 1),
                                 pos=(WIDTH - 60, HEIGHT - 40))
        self.add_widget(self.score_label)
        self.overlay_label = Label(text="", font_size=22, color=(1, 1, 0, 1),
                                   halign="center", valign="middle",
                                   size=(WIDTH, HEIGHT), pos=(0, 0))
        self.add_widget(self.overlay_label)

        self.show_menu()

        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_mouse_down=self._on_mouse_down)

    def show_menu(self):
        self.state = "menu"
        self.overlay_label.text = (
            f"[b]Flappy Bird[/b]\n\nPress SPACE / Click to Start\n"
            f"P = Pause    R = Restart\nHigh Score: {self.high_score}"
        )
        self.overlay_label.markup = True

    def start_game(self):
        self.state = "playing"
        self.bird_y = HEIGHT // 2
        self.bird_v = 0
        self.pipes.clear()
        self.score = 0
        self.spawn_timer = 0.4
        self.overlay_label.text = ""
        self.last_time = time.time()
        Clock.schedule_interval(self.update, FPS)

    def spawn_pipe(self):
        gap_y = random.randint(110, HEIGHT - GROUND_HEIGHT - 110 - PIPE_GAP)
        self.pipes.append({"x": WIDTH, "gap_y": gap_y, "scored": False})

    def update(self, _):
        if self.state != "playing":
            return

        now = time.time()
        dt = now - self.last_time
        if dt > 0.05:
            dt = 0.05
        self.last_time = now

        # Bird physics
        self.bird_v += GRAVITY * dt
        self.bird_y += self.bird_v * dt

        # Ground / ceiling
        if self.bird_y <= GROUND_HEIGHT:
            self.bird_y = GROUND_HEIGHT
            self.end_game()
        if self.bird_y + BIRD_SIZE >= HEIGHT:
            self.bird_y = HEIGHT - BIRD_SIZE
            self.bird_v = 0

        # Pipes
        for p in self.pipes:
            p["x"] -= PIPE_SPEED * dt
        self.pipes = [p for p in self.pipes if p["x"] + PIPE_WIDTH > 0]

        # Spawn
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_pipe()
            self.spawn_timer = SPAWN_INTERVAL

        # Collision & scoring
        bird_rect = (BIRD_X, self.bird_y,
                     BIRD_X + BIRD_SIZE, self.bird_y + BIRD_SIZE)
        for p in self.pipes:
            if not p["scored"] and p["x"] + PIPE_WIDTH < BIRD_X:
                p["scored"] = True
                self.score += 1
            top_rect = (p["x"], p["gap_y"] + PIPE_GAP,
                        p["x"] + PIPE_WIDTH, HEIGHT)
            bottom_rect = (p["x"], 0,
                           p["x"] + PIPE_WIDTH, p["gap_y"])
            if rects_intersect(bird_rect, top_rect) or rects_intersect(bird_rect, bottom_rect):
                self.end_game()

        self.draw()

    def draw(self):
        self.canvas.clear()

        # Background
        with self.canvas:
            Color(*get_color_from_hex(BG_COLOR))
            Rectangle(pos=(0, 0), size=(WIDTH, HEIGHT))

        # Pipes
        with self.canvas:
            Color(*get_color_from_hex("#2e8b57"))
            for p in self.pipes:
                Rectangle(pos=(p["x"], 0), size=(PIPE_WIDTH, p["gap_y"]))
                Rectangle(pos=(p["x"], p["gap_y"] + PIPE_GAP),
                          size=(PIPE_WIDTH, HEIGHT - (p["gap_y"] + PIPE_GAP)))

        # Ground
        with self.canvas:
            Color(*get_color_from_hex("#de9b5c"))
            Rectangle(pos=(0, 0), size=(WIDTH, GROUND_HEIGHT))
            Color(*get_color_from_hex("#c17e45"))
            Rectangle(pos=(0, GROUND_HEIGHT), size=(WIDTH, 6))

        # Bird
        with self.canvas:
            Color(1, 0.92, 0.23)
            Ellipse(pos=(BIRD_X, self.bird_y), size=(BIRD_SIZE, BIRD_SIZE))

        self.score_label.text = str(self.score)

    def end_game(self):
        self.state = "gameover"
        Clock.unschedule(self.update)
        if self.score > self.high_score:
            self.high_score = self.score
            save_highscore(self.high_score)
        self.overlay_label.text = (
            f"[b]GAME OVER[/b]\nScore: {self.score}  High: {self.high_score}\n"
            "Press SPACE / Click / R to Restart"
        )
        self.overlay_label.markup = True

    def flap(self):
        if self.state == "menu":
            self.start_game()
        elif self.state == "playing":
            self.bird_v = FLAP_V
        elif self.state == "paused":
            self.state = "playing"
            self.overlay_label.text = ""
            self.last_time = time.time()
            Clock.schedule_interval(self.update, FPS)
        elif self.state == "gameover":
            self.start_game()

    def toggle_pause(self):
        if self.state == "playing":
            self.state = "paused"
            Clock.unschedule(self.update)
            self.overlay_label.text = "[b]PAUSED[/b]"
            self.overlay_label.markup = True
        elif self.state == "paused":
            self.state = "playing"
            self.overlay_label.text = ""
            self.last_time = time.time()
            Clock.schedule_interval(self.update, FPS)

    def restart(self):
        self.start_game()

    def _on_key_down(self, window, key, *_):
        if key in (32, 273):  # Space / Up
            self.flap()
        elif key in (112, 80):  # P
            self.toggle_pause()
        elif key in (114, 82):  # R
            self.restart()

    def _on_mouse_down(self, window, x, y, button, *_):
        if button == "left":
            self.flap()

class FlappyApp(App):
    def build(self):
        return FlappyGame()

if __name__ == "__main__":
    FlappyApp().run()
