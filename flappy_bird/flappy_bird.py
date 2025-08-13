"""
Flappy Bird - Polished Tkinter Version
Controls:
 - Space / Up arrow / Left mouse click  -> flap / start / restart
 - P -> pause / resume
 - R -> restart after game over
"""
import tkinter as tk
import random
import time
import json
import os

# ----------------- Config -----------------
WIDTH = 420
HEIGHT = 640
FPS_MS = 16                 # ~60 FPS
BIRD_SIZE = 34
BIRD_X = 110                # fixed horizontal position for bird
GRAVITY = 900.0             # pixels / s^2
FLAP_V = -340.0             # instant velocity on flap (px / s)
PIPE_WIDTH = 72
PIPE_GAP = 170
PIPE_SPEED = 180.0          # pixels / second
SPAWN_INTERVAL = 1.6        # seconds between pipes
SAVE_FILE = "flappy_highscore.json"
BG_COLOR = "#70c5ce"
GROUND_HEIGHT = 80
TEXT_FONT = ("Arial", 18, "bold")
SCORE_FONT = ("Arial", 28, "bold")

# ----------------- Helpers -----------------
def load_highscore():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                return int(data.get("high_score", 0))
        except Exception:
            return 0
    return 0

def save_highscore(score):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump({"high_score": int(score)}, f)
    except Exception:
        pass

def rects_intersect(a, b):
    # a and b are (x1,y1,x2,y2)
    return not (a[2] <= b[0] or a[0] >= b[2] or a[3] <= b[1] or a[1] >= b[3])

# ----------------- Game Class -----------------
class FlappyBird:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird — Polished Tkinter")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        # state
        self.state = "menu"   # menu | playing | paused | gameover
        self.last_time = None
        self._job = None

        # game objects
        self.bird_id = None
        self.bird_v = 0.0
        self.pipes = []       # list of dicts {x, gap_y, top_id, bottom_id, scored}
        self.spawn_timer = 0.0
        self.score = 0
        self.high_score = load_highscore()

        # ui
        self.score_text_id = None
        self.overlay_ids = []
        self.pause_text_id = None

        # input bindings
        root.bind("<space>", self.on_flap)
        root.bind("<Up>", self.on_flap)
        root.bind("<Button-1>", self.on_flap)   # mouse left click
        root.bind("p", self.toggle_pause)
        root.bind("P", self.toggle_pause)
        root.bind("r", self.force_restart)
        root.protocol("WM_DELETE_WINDOW", self._on_close)

        # draw static ground
        self.draw_background()
        self.show_menu()

    # ---------- drawing ----------
    def draw_background(self):
        self.canvas.delete("background")
        # sky already BG_COLOR; draw ground strip
        self.canvas.create_rectangle(0, HEIGHT - GROUND_HEIGHT, WIDTH, HEIGHT, fill="#de9b5c", width=0, tags="background")
        # ground detail
        self.canvas.create_rectangle(0, HEIGHT - GROUND_HEIGHT - 6, WIDTH, HEIGHT - GROUND_HEIGHT, fill="#c17e45", width=0, tags="background")

    def create_bird(self):
        cy = HEIGHT//2
        x1 = BIRD_X - BIRD_SIZE//2
        y1 = cy - BIRD_SIZE//2
        x2 = BIRD_X + BIRD_SIZE//2
        y2 = cy + BIRD_SIZE//2
        self.bird_id = self.canvas.create_oval(x1, y1, x2, y2, fill="#ffeb3b", outline="#d8b41b", width=2)
        # simple eye
        self.canvas.create_oval(BIRD_X+6, cy-6, BIRD_X+11, cy-1, fill="#222", tags=("bird_eye",))
        # wing (animated by moving it slightly)
        self.wing_id = self.canvas.create_polygon(BIRD_X-4, cy, BIRD_X+2, cy-4, BIRD_X+6, cy, fill="#f0c419", outline="")

    def clear_game_objects(self):
        if self.bird_id:
            self.canvas.delete(self.bird_id)
        self.canvas.delete("pipe")
        self.canvas.delete("score")
        self.canvas.delete("overlay")
        self.canvas.delete("bird_eye")
        try:
            del self.wing_id
        except Exception:
            pass
        self.pipes.clear()

    # ---------- state screens ----------
    def show_menu(self):
        self.canvas.delete("all")
        self.draw_background()
        self.overlay_ids = []
        title = self.canvas.create_text(WIDTH//2, HEIGHT//2 - 70, text="Flappy Bird", font=("Helvetica", 40, "bold"), fill="white", tags="overlay")
        hint = self.canvas.create_text(WIDTH//2, HEIGHT//2 - 20, text="Press SPACE / Click to Start", font=TEXT_FONT, fill="#ffc107", tags="overlay")
        sub = self.canvas.create_text(WIDTH//2, HEIGHT//2 + 20, text="Space/Up/Click = Flap    P = Pause    R = Restart", font=("Helvetica", 12), fill="white", tags="overlay")
        hs = self.canvas.create_text(WIDTH//2, HEIGHT//2 + 70, text=f"High Score: {self.high_score}", font=("Helvetica", 16), fill="white", tags="overlay")
        self.overlay_ids = [title, hint, sub, hs]
        self.state = "menu"
        # set up a light demo bird to bob up/down
        self.demo_bob = 0.0
        self._demo_bob_job()

    def _demo_bob_job(self):
        # small bob animation while on menu
        if self.state != "menu":
            return
        self.canvas.delete("demo_bird")
        bob_y = HEIGHT//2 + int(8 * (1 + random.random()) * (0.5 - 0.5))
        # draw a simple bird sample
        bx1 = BIRD_X - 20
        by1 = HEIGHT//2 - 20
        bx2 = BIRD_X + 20
        by2 = HEIGHT//2 + 20
        self.canvas.create_oval(bx1, by1, bx2, by2, fill="#ffeb3b", outline="#d8b41b", width=2, tags="demo_bird")
        # loop slow
        self.root.after(700, self._demo_bob_job)

    def show_gameover(self):
        self.state = "gameover"
        # overlay
        self.overlay_ids = []
        panel = self.canvas.create_rectangle(WIDTH//2 - 180, HEIGHT//2 - 90, WIDTH//2 + 180, HEIGHT//2 + 90, fill="#000000cc", outline="", tags="overlay")
        t1 = self.canvas.create_text(WIDTH//2, HEIGHT//2 - 30, text="GAME OVER", font=("Helvetica", 32, "bold"), fill="#ff5252", tags="overlay")
        t2 = self.canvas.create_text(WIDTH//2, HEIGHT//2 + 10, text=f"Score: {self.score}   High: {self.high_score}", font=TEXT_FONT, fill="white", tags="overlay")
        t3 = self.canvas.create_text(WIDTH//2, HEIGHT//2 + 50, text="Press SPACE / Click / R to Replay", font=("Helvetica", 14), fill="#ffc107", tags="overlay")
        self.overlay_ids = [panel, t1, t2, t3]

    # ---------- input handlers ----------
    def on_flap(self, event=None):
        # universal handler: acts depending on state
        if self.state == "menu":
            # start playing
            self.start_game()
            return
        if self.state == "playing":
            # flap
            self.bird_v = FLAP_V
            # small wing animation
            try:
                self.canvas.coords(self.wing_id, BIRD_X-4, (self.canvas.coords(self.bird_id)[1]+self.canvas.coords(self.bird_id)[3])/2,
                                   BIRD_X+2, self.canvas.coords(self.bird_id)[1]+6, BIRD_X+6, (self.canvas.coords(self.bird_id)[1]+self.canvas.coords(self.bird_id)[3])/2)
            except Exception:
                pass
            return
        if self.state == "gameover":
            # restart on flap/click
            self.restart()
            return
        if self.state == "paused":
            # unpause + flap
            self.toggle_pause()
            self.bird_v = FLAP_V
            return

    def toggle_pause(self, event=None):
        if self.state == "playing":
            self.state = "paused"
            if self.pause_text_id is None:
                self.pause_text_id = self.canvas.create_text(WIDTH//2, HEIGHT//2, text="PAUSED", font=("Helvetica", 36, "bold"), fill="white", tags="overlay")
        elif self.state == "paused":
            self.canvas.delete(self.pause_text_id)
            self.pause_text_id = None
            self.last_time = time.time()
            self.state = "playing"
            self._schedule_next_frame()

    def force_restart(self, event=None):
        # user pressed R
        if self.state in ("playing", "paused", "gameover"):
            self.restart()

    # ---------- game lifecycle ----------
    def start_game(self):
        # clear overlays + demo
        self.canvas.delete("demo_bird")
        for item in self.overlay_ids:
            try: self.canvas.delete(item)
            except: pass
        self.overlay_ids.clear()

        # reset
        self.clear_game_objects()
        self.create_bird()
        self.score = 0
        self.pipes = []
        self.spawn_timer = 0.4  # spawn first pipe quickly
        self.last_time = time.time()
        self.bird_v = 0.0
        self.state = "playing"

        # score label
        if self.score_text_id:
            self.canvas.delete(self.score_text_id)
        self.score_text_id = self.canvas.create_text(WIDTH - 16, 12, anchor="ne", text=f"{self.score}", font=SCORE_FONT, fill="white", tags="score")

        # start main loop
        self._schedule_next_frame()

    def restart(self):
        # cleanup any scheduled callback to avoid dupes
        if self._job:
            try:
                self.root.after_cancel(self._job)
            except Exception:
                pass
            self._job = None
        # save high score
        if self.score > self.high_score:
            self.high_score = self.score
            save_highscore(self.high_score)
        # tiny flash or sound could go here
        self.clear_game_objects()
        self.start_game()

    def end_game(self):
        self.state = "gameover"
        # save high score
        if self.score > self.high_score:
            self.high_score = self.score
            save_highscore(self.high_score)
        self.show_gameover()
        # stop loop (no scheduling next)
        if self._job:
            try:
                self.root.after_cancel(self._job)
            except Exception:
                pass
            self._job = None

    def _on_close(self):
        # cancel scheduled job before closing
        if self._job:
            try:
                self.root.after_cancel(self._job)
            except Exception:
                pass
        self.root.destroy()

    # ---------- pipes ----------
    def spawn_pipe(self):
        gap_y = random.randint(110, HEIGHT - GROUND_HEIGHT - 110 - PIPE_GAP)
        x = WIDTH + 4
        top_id = self.canvas.create_rectangle(x, 0, x + PIPE_WIDTH, gap_y, fill="#2e8b57", width=0, tags="pipe")
        bottom_id = self.canvas.create_rectangle(x, gap_y + PIPE_GAP, x + PIPE_WIDTH, HEIGHT - GROUND_HEIGHT, fill="#2e8b57", width=0, tags="pipe")
        pipe = {"x": float(x), "gap_y": gap_y, "top": top_id, "bottom": bottom_id, "scored": False}
        self.pipes.append(pipe)

    # ---------- main loop ----------
    def _schedule_next_frame(self):
        # schedule next frame if playing
        if self.state == "playing":
            self._job = self.root.after(FPS_MS, self._frame)

    def _frame(self):
        now = time.time()
        dt = now - (self.last_time or now)
        # clamp dt to avoid huge jumps
        if dt > 0.05:
            dt = 0.05
        self.last_time = now

        # update physics
        self.bird_v += GRAVITY * dt
        # convert bird velocity to movement in pixels this frame
        dy = self.bird_v * dt
        self.canvas.move(self.bird_id, 0, dy)
        # move wing to follow
        try:
            bx1, by1, bx2, by2 = self.canvas.coords(self.bird_id)
            mid_y = (by1 + by2)/2
            # basic wing follow
            self.canvas.coords(self.wing_id, BIRD_X-4, mid_y, BIRD_X+2, mid_y-8, BIRD_X+6, mid_y)
            self.canvas.coords("bird_eye", BIRD_X+6, mid_y-6, BIRD_X+11, mid_y-1)
        except Exception:
            pass

        # bird bounds check top/bottom (collide with ground)
        bx1, by1, bx2, by2 = self.canvas.coords(self.bird_id)
        if by1 <= 4:
            # hit ceiling -> clamp and bounce a little
            self.canvas.coords(self.bird_id, bx1, 4, bx2, 4 + (by2-by1))
            self.bird_v = 0.0
            by1 = 4
        if by2 >= HEIGHT - GROUND_HEIGHT:
            # hit ground -> game over
            self.end_game()
            return

        # update pipes
        remove_list = []
        for p in list(self.pipes):
            p["x"] -= PIPE_SPEED * dt
            x = p["x"]
            # update rectangle coords
            self.canvas.coords(p["top"], x, 0, x + PIPE_WIDTH, p["gap_y"])
            self.canvas.coords(p["bottom"], x, p["gap_y"] + PIPE_GAP, x + PIPE_WIDTH, HEIGHT - GROUND_HEIGHT)

            # scoring: when pipe right edge crosses bird_x and not yet scored
            if (not p["scored"]) and (x + PIPE_WIDTH < BIRD_X):
                p["scored"] = True
                self.score += 1
                self.canvas.itemconfigure(self.score_text_id, text=str(self.score))

            # remove off-screen pipes
            if x + PIPE_WIDTH < -10:
                remove_list.append(p)

        for p in remove_list:
            try:
                self.canvas.delete(p["top"])
                self.canvas.delete(p["bottom"])
            except Exception:
                pass
            if p in self.pipes:
                self.pipes.remove(p)

        # spawn logic
        self.spawn_timer -= dt
        if self.spawn_timer <= 0.0:
            self.spawn_pipe()
            self.spawn_timer = SPAWN_INTERVAL

        # collision detection with pipes
        bird_bbox = self.canvas.coords(self.bird_id)
        for p in self.pipes:
            top_bbox = self.canvas.coords(p["top"])
            bot_bbox = self.canvas.coords(p["bottom"])
            if rects_intersect(bird_bbox, top_bbox) or rects_intersect(bird_bbox, bot_bbox):
                self.end_game()
                return

        # schedule next
        self._schedule_next_frame()

    # ---------- run ----------
    def run(self):
        self.root.mainloop()

# ----------------- run the game -----------------
if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBird(root)
    game.run()
