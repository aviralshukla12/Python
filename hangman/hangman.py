import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

SAVE_FILE = "hangman_save.json"
WORDS_FILE = "words.txt"

# Built-in fallback word list (English, mixed lengths)
FALLBACK_WORDS = [
    "python","kotlin","variable","function","class","inheritance","encapsulation","polymorphism",
    "recursion","iterator","generator","algorithm","database","network","protocol","compiler",
    "interpreter","abstraction","optimization","synchronization","asynchronous","pipeline","container",
    "framework","library","package","virtualenv","repository","encryption","decryption","signature",
    "blockchain","consensus","throughput","latency","bandwidth","parallel","concurrency","scalability",
    "interface","component","architecture","microservice","refactor","testing","coverage","mocking",
    "decorator","singleton","observer","strategy","factory","builder","prototype","adapter","bridge",
    "facade","mediator","proxy","command","state","visitor","iterator","memento","flyweight",
    "gradient","backpropagation","neuron","activation","regularization","dropout","optimizer","dataset",
    "feature","label","cluster","regression","classification","pipeline","tokenizer","embedding",
    "attention","transformer","sequence","temporal","spatial","graph","topology","metadata","index",
    "cursor","trigger","materialized","transaction","isolation","consistency","durability","availability",
    "idempotent","deterministic","stochastic","heuristic","approximation","quantization","sampling"
]

DIFFICULTY_RULES = {
    "Easy": {"min_len": 4,  "max_len": 7,  "max_attempts": 8},
    "Normal": {"min_len": 6,  "max_len": 12, "max_attempts": 7},
    "Hard": {"min_len": 8,  "max_len": 20, "max_attempts": 6},
}

class HangmanGame:
    def __init__(self, words):
        self.words = words
        self.secret_word = ""
        self.display = []
        self.wrong_letters = set()
        self.correct_letters = set()
        self.max_attempts = 7
        self.hints_left = 1

    def start_new(self, difficulty: str):
        rules = DIFFICULTY_RULES.get(difficulty, DIFFICULTY_RULES["Normal"])
        self.max_attempts = rules["max_attempts"]
        candidates = [w.lower() for w in self.words if rules["min_len"] <= len(w) <= rules["max_len"] and w.isalpha()]
        if not candidates:
            candidates = FALLBACK_WORDS
        self.secret_word = random.choice(candidates).lower()
        self.display = ["_" if ch.isalpha() else ch for ch in self.secret_word]
        self.wrong_letters = set()
        self.correct_letters = set()
        self.hints_left = 1

    def guess(self, ch: str):
        ch = ch.lower()
        if not ch.isalpha() or len(ch) != 1:
            return "invalid"
        if ch in self.correct_letters or ch in self.wrong_letters:
            return "repeat"
        if ch in self.secret_word:
            self.correct_letters.add(ch)
            for i, c in enumerate(self.secret_word):
                if c == ch:
                    self.display[i] = ch
            return "hit"
        else:
            self.wrong_letters.add(ch)
            return "miss"

    def use_hint(self):
        if self.hints_left <= 0:
            return False, None
        hidden_indices = [i for i, c in enumerate(self.display) if c == "_"]
        if not hidden_indices:
            return False, None
        idx = random.choice(hidden_indices)
        letter = self.secret_word[idx]
        self.hints_left -= 1
        # Hint costs half a miss (rounded up) by consuming one attempt directly
        # More punishing on Hard
        self.wrong_letters.add("\u273f")  # decorative marker for hint-usage as a 'miss'
        for i, c in enumerate(self.secret_word):
            if c == letter:
                self.display[i] = letter
                self.correct_letters.add(letter)
        return True, letter

    def is_won(self):
        return "_" not in self.display

    def is_lost(self):
        return len([w for w in self.wrong_letters if w]) >= self.max_attempts

    def attempts_used(self):
        return len([w for w in self.wrong_letters if w])

    def attempts_left(self):
        return max(0, self.max_attempts - self.attempts_used())


class HangmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman — Deluxe Tkinter")
        self.geometry("900x600")
        self.minsize(820, 560)
        self.configure(bg="#0b1021")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.stats = {
            "games": 0,
            "wins": 0,
            "streak": 0,
            "best": 0,
            "difficulty": "Normal",
            "last_played": None,
        }

        self._load_stats()
        self.words = self._load_words()
        self.game = HangmanGame(self.words)

        self.style = ttk.Style(self)
        self._setup_style()
        self._build_ui()
        self.new_game()

        self.bind("<Key>", self._on_keypress)

    # ------------------ Persistence ------------------
    def _load_stats(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    self.stats = json.load(f)
            except Exception:
                pass

    def _save_stats(self):
        self.stats["last_played"] = datetime.now().isoformat(timespec="seconds")
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, indent=2)
        except Exception:
            pass

    def _load_words(self):
        if os.path.exists(WORDS_FILE):
            try:
                with open(WORDS_FILE, "r", encoding="utf-8") as f:
                    words = [w.strip() for w in f if w.strip() and w.strip().isalpha()]
                    if len(words) >= 50:
                        return words
            except Exception:
                pass
        return FALLBACK_WORDS

    # ------------------ UI Setup ------------------
    def _setup_style(self):
        # Dark theme styling
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#0b1021")
        self.style.configure("Header.TLabel", background="#0b1021", foreground="#e2e8f0", font=("Segoe UI", 18, "bold"))
        self.style.configure("Sub.TLabel", background="#0b1021", foreground="#a8b0c2", font=("Segoe UI", 11))
        self.style.configure("Word.TLabel", background="#0b1021", foreground="#f8fafc", font=("JetBrains Mono", 28, "bold"))
        self.style.configure("Info.TLabel", background="#0b1021", foreground="#9fb3ff", font=("Segoe UI", 11, "bold"))
        self.style.configure("Stat.TLabel", background="#0b1021", foreground="#cbd5e1", font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        self.style.map("TButton", foreground=[('disabled', '#777')])

    def _build_ui(self):
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        # Header
        header = ttk.Frame(container)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header.columnconfigure(1, weight=1)
        ttk.Label(header, text="Hangman", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        self.status_label = ttk.Label(header, text="", style="Sub.TLabel")
        self.status_label.grid(row=1, column=0, sticky="w")

        # Controls on the right
        ctrl = ttk.Frame(header)
        ctrl.grid(row=0, column=2, rowspan=2, sticky="e")
        self.diff_var = tk.StringVar(value=self.stats.get("difficulty", "Normal"))
        ttk.Label(ctrl, text="Difficulty", style="Sub.TLabel").grid(row=0, column=0, padx=(0,6))
        self.diff_cb = ttk.Combobox(ctrl, values=list(DIFFICULTY_RULES.keys()), textvariable=self.diff_var, state="readonly", width=8)
        self.diff_cb.grid(row=0, column=1)
        self.diff_cb.bind("<<ComboboxSelected>>", lambda e: self._on_change_difficulty())
        ttk.Button(ctrl, text="New Game", command=self.new_game).grid(row=0, column=2, padx=(10,0))
        self.hint_btn = ttk.Button(ctrl, text="Hint", command=self._hint)
        self.hint_btn.grid(row=0, column=3, padx=(8,0))
        ttk.Button(ctrl, text="Reset Stats", command=self._reset_stats).grid(row=0, column=4, padx=(8,0))

        # Main area: left canvas (gallows), right word + keyboard + stats
        main = ttk.Frame(container)
        main.grid(row=1, column=0, sticky="nsew")
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        # Gallows canvas
        self.canvas = tk.Canvas(main, width=320, height=360, bg="#0f1531", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=3, sticky="nsw", padx=(0, 16))

        # Word display
        word_frame = ttk.Frame(main)
        word_frame.grid(row=0, column=1, sticky="ew")
        self.word_var = tk.StringVar(value="")
        self.word_label = ttk.Label(word_frame, textvariable=self.word_var, style="Word.TLabel")
        self.word_label.grid(row=0, column=0, sticky="w")

        # Info + wrong letters
        info_frame = ttk.Frame(main)
        info_frame.grid(row=1, column=1, sticky="ew", pady=(6, 6))
        self.attempts_var = tk.StringVar()
        self.wrongs_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.attempts_var, style="Info.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(info_frame, textvariable=self.wrongs_var, style="Info.TLabel").grid(row=0, column=1, sticky="w", padx=(16,0))

        # On-screen keyboard
        kb = ttk.Frame(main)
        kb.grid(row=2, column=1, sticky="nsew")
        kb.columnconfigure(tuple(range(10)), weight=1)
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.kb_buttons = {}
        for r, letters in enumerate(rows):
            row_frame = ttk.Frame(kb)
            row_frame.grid(row=r, column=0, sticky="ew", pady=3)
            # left padding for staggered look
            pad = 0 if r == 0 else (20 if r == 1 else 42)
            row_frame.grid_columnconfigure(0, minsize=pad)
            for c, ch in enumerate(letters, start=1):
                btn = ttk.Button(row_frame, text=ch, width=3, command=lambda x=ch: self._press(x))
                btn.grid(row=0, column=c, padx=3, pady=3)
                self.kb_buttons[ch.lower()] = btn

        # Stats bar
        stats = ttk.Frame(container)
        stats.grid(row=2, column=0, sticky="ew", pady=(12,0))
        self.stats_var = tk.StringVar(value=self._format_stats())
        ttk.Label(stats, textvariable=self.stats_var, style="Stat.TLabel").grid(row=0, column=0, sticky="w")

    # ------------------ Interactions ------------------
    def _press(self, ch: str):
        if not self._game_active:
            return
        outcome = self.game.guess(ch)
        if outcome == "invalid" or outcome == "repeat":
            self._pulse(self.status_label, text="Already used" if outcome=="repeat" else "Type A–Z only")
            return
        self._update_ui_after_guess(ch)

    def _on_keypress(self, event):
        ch = event.char
        if ch:
            self._press(ch.upper())

    def _update_ui_after_guess(self, ch: str):
        # Disable keyboard button
        btn = self.kb_buttons.get(ch.lower())
        if btn:
            btn.state(["disabled"])  # disable button
        # Update labels
        self.word_var.set(self._spaced_word())
        self._update_info()
        self._draw_hangman()
        # Flash letter in word if hit
        if ch.lower() in self.game.secret_word:
            self._flash(self.word_label)
        else:
            self._shake(self.canvas)
        # Check end state
        if self.game.is_won():
            self._end_game(won=True)
        elif self.game.is_lost():
            self._end_game(won=False)

    def _hint(self):
        if not self._game_active:
            return
        ok, letter = self.game.use_hint()
        if not ok:
            self._pulse(self.status_label, text="No hints left")
            return
        # Disable the revealed letter's key, too
        btn = self.kb_buttons.get(letter)
        if btn:
            btn.state(["disabled"]) 
        self.word_var.set(self._spaced_word())
        self._update_info()
        self._draw_hangman()
        self._flash(self.word_label)
        if self.game.is_won():
            self._end_game(won=True)

    def _on_change_difficulty(self):
        self.stats["difficulty"] = self.diff_var.get()
        self._save_stats()
        self.new_game()

    def _reset_stats(self):
        if messagebox.askyesno("Reset Stats", "Reset all stats (games, wins, streaks)?"):
            self.stats = {
                "games": 0, "wins": 0, "streak": 0, "best": 0,
                "difficulty": self.diff_var.get(), "last_played": None,
            }
            self._save_stats()
            self.stats_var.set(self._format_stats())
            self._pulse(self.status_label, text="Stats reset")

    # ------------------ Game Flow ------------------
    def new_game(self):
        self._game_active = True
        self.canvas.delete("all")
        self.status_label.configure(text=f"Good luck! Difficulty: {self.diff_var.get()}")
        self.game.start_new(self.diff_var.get())
        self.word_var.set(self._spaced_word())
        self._update_info()
        for b in self.kb_buttons.values():
            b.state(["!disabled"])
        self.hint_btn.state(["!disabled"]) if self.game.hints_left > 0 else self.hint_btn.state(["disabled"]) 
        self._draw_gallows()

    def _end_game(self, won: bool):
        self._game_active = False
        self.stats["games"] += 1
        if won:
            self.stats["wins"] += 1
            self.stats["streak"] += 1
            self.stats["best"] = max(self.stats["best"], self.stats["streak"])
            self.status_label.configure(text="You win! \U0001F389")
            self._celebrate()
        else:
            self.stats["streak"] = 0
            self.status_label.configure(text=f"You lost. Word was: {self.game.secret_word.upper()}")
            self._shake(self.word_label)
        self._save_stats()
        self.stats_var.set(self._format_stats())
        for b in self.kb_buttons.values():
            b.state(["disabled"]) 
        self.hint_btn.state(["disabled"]) 

    # ------------------ UI Helpers ------------------
    def _format_stats(self):
        g = self.stats.get("games", 0)
        w = self.stats.get("wins", 0)
        rate = (w / g * 100) if g else 0.0
        return (
            f"Games: {g}   Wins: {w}   Win%: {rate:.1f}%   "
            f"Streak: {self.stats.get('streak',0)}   Best: {self.stats.get('best',0)}   "
            f"Difficulty: {self.stats.get('difficulty','Normal')}"
        )

    def _spaced_word(self):
        return " ".join(ch.upper() for ch in self.game.display)

    def _update_info(self):
        self.attempts_var.set(f"Attempts: {self.game.attempts_used()}/{self.game.max_attempts}  (left: {self.game.attempts_left()})")
        wrongs = [w for w in self.game.wrong_letters if w and w != "\u273f"]
        extra = " | hint used" if "\u273f" in self.game.wrong_letters else ""
        self.wrongs_var.set(f"Wrong: {' '.join(sorted(w.upper() for w in wrongs))}{extra}")

    # ------------------ Drawing ------------------
    def _draw_gallows(self):
        c = self.canvas
        w, h = int(c["width"]), int(c["height"])
        c.create_rectangle(20, h-20, w-20, h-10, fill="#182046", outline="")  # ground
        c.create_line(60, h-20, 60, 40, width=6, fill="#9fb3ff")
        c.create_line(60, 40, 200, 40, width=6, fill="#9fb3ff")
        c.create_line(200, 40, 200, 80, width=4, fill="#9fb3ff")

    def _draw_hangman(self):
        # Draw parts based on attempts used
        c = self.canvas
        c.delete("hang")
        a = self.game.attempts_used()
        # 1: head
        if a >= 1:
            c.create_oval(170, 80, 230, 140, outline="#e2e8f0", width=3, tags="hang")
        # 2: body
        if a >= 2:
            c.create_line(200, 140, 200, 220, fill="#e2e8f0", width=3, tags="hang")
        # 3: left arm
        if a >= 3:
            c.create_line(200, 160, 165, 190, fill="#e2e8f0", width=3, tags="hang")
        # 4: right arm
        if a >= 4:
            c.create_line(200, 160, 235, 190, fill="#e2e8f0", width=3, tags="hang")
        # 5: left leg
        if a >= 5:
            c.create_line(200, 220, 175, 270, fill="#e2e8f0", width=3, tags="hang")
        # 6: right leg
        if a >= 6:
            c.create_line(200, 220, 225, 270, fill="#e2e8f0", width=3, tags="hang")
        # 7: face X
        if a >= 7:
            c.create_line(185, 100, 195, 110, fill="#e2e8f0", width=2, tags="hang")
            c.create_line(185, 110, 195, 100, fill="#e2e8f0", width=2, tags="hang")
            c.create_line(205, 100, 215, 110, fill="#e2e8f0", width=2, tags="hang")
            c.create_line(205, 110, 215, 100, fill="#e2e8f0", width=2, tags="hang")
            c.create_line(188, 125, 212, 125, fill="#e2e8f0", width=2, tags="hang")

    # ------------------ Micro-animations ------------------
    def _flash(self, widget, times: int = 2, interval: int = 120):
        orig = widget.cget("foreground") if isinstance(widget, ttk.Label) else None
        def step(i):
            if i <= 0:
                if orig is not None:
                    widget.configure(foreground="#f8fafc")
                return
            if orig is not None:
                widget.configure(foreground="#91ffb1")
            self.after(interval, lambda: (orig is not None) and widget.configure(foreground="#f8fafc") or None)
            self.after(interval*2, lambda: step(i-1))
        step(times)

    def _pulse(self, widget, text=None, times: int = 2, interval: int = 120):
        if text is not None:
            widget.configure(text=text)
        def step(i):
            if i <= 0:
                return
            widget.configure(foreground="#ffffff")
            self.after(interval, lambda: widget.configure(foreground="#a8b0c2"))
            self.after(interval*2, lambda: step(i-1))
        step(times)

    def _shake(self, widget, distance: int = 8, shakes: int = 6, interval: int = 20):
        # Applies to canvas or label by moving with place or canvas move
        if isinstance(widget, tk.Canvas):
            target = widget
            def step(i, dir):
                if i <= 0:
                    return
                target.move("all", dir*distance, 0)
                self.after(interval, lambda: (target.move("all", -dir*distance, 0), step(i-1, -dir)))
            step(shakes, 1)
        else:
            # For labels: use place inside a frame? Simpler: flash instead
            self._flash(widget)

    def _celebrate(self):
        # Simple confetti dots on canvas
        c = self.canvas
        for i in range(60):
            x = random.randint(40, 300)
            y = random.randint(40, 300)
            r = random.randint(2, 5)
            c.create_oval(x-r, y-r, x+r, y+r, fill="#91ffb1", outline="", tags="celebrate")
        self.after(900, lambda: c.delete("celebrate"))


if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()
