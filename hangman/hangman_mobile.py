from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
import random
import json
import os
from datetime import datetime

SAVE_FILE = "hangman_save.json"
WORDS_FILE = "words.txt"

FALLBACK_WORDS = [
    "python","kotlin","variable","function","class","inheritance","encapsulation","polymorphism",
    "recursion","iterator","generator","algorithm","database","network","protocol","compiler",
    "interpreter","abstraction","optimization","synchronization","asynchronous","pipeline","container",
]

DIFFICULTY_RULES = {
    "Easy": {"min_len": 4, "max_len": 7, "max_attempts": 8},
    "Normal": {"min_len": 6, "max_len": 12, "max_attempts": 7},
    "Hard": {"min_len": 8, "max_len": 20, "max_attempts": 6},
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
        self.secret_word = random.choice(candidates)
        self.display = ["_" if c.isalpha() else c for c in self.secret_word]
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
        hidden = [i for i, c in enumerate(self.display) if c == "_"]
        if not hidden:
            return False, None
        idx = random.choice(hidden)
        letter = self.secret_word[idx]
        self.hints_left -= 1
        self.wrong_letters.add("\u273f")  # hint as 'miss'
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


class HangmanCanvas(Widget):
    attempts = NumericProperty(0)

    def on_attempts(self, instance, value):
        self.canvas.clear()
        w, h = self.width, self.height
        with self.canvas:
            Color(0.6, 0.7, 1)
            # Gallows
            Line(points=[60, 20, 60, h-40], width=6)
            Line(points=[60, h-40, w-60, h-40], width=6)
            Line(points=[w-60, h-40, w-60, h-100], width=4)
            # Hangman parts
            if value >= 1:
                Ellipse(pos=(w-80, h-140, 60, 60))
            if value >= 2:
                Line(points=[w-50, h-140, w-50, h-240], width=3)
            if value >= 3:
                Line(points=[w-50, h-180, w-80, h-220], width=3)
            if value >= 4:
                Line(points=[w-50, h-180, w-20, h-220], width=3)
            if value >= 5:
                Line(points=[w-50, h-240, w-80, h-290], width=3)
            if value >= 6:
                Line(points=[w-50, h-240, w-20, h-290], width=3)
            if value >= 7:
                Line(points=[w-75, h-125, w-65, h-115], width=2)
                Line(points=[w-75, h-115, w-65, h-125], width=2)

class HangmanAppUI(BoxLayout):
    word_text = StringProperty("")
    info_text = StringProperty("")
    wrong_text = StringProperty("")
    status_text = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=10, **kwargs)
        self.stats = {"games":0, "wins":0, "streak":0, "best":0, "difficulty":"Normal", "last_played":None}
        self._load_stats()
        self.words = self._load_words()
        self.game = HangmanGame(self.words)
        self._game_active = True

        # Top: Status & controls
        top = BoxLayout(size_hint_y=None, height=40, spacing=5)
        self.status_lbl = Label(text=self.status_text)
        self.diff_btn = Button(text="New Game", size_hint_x=None, width=100, on_press=lambda x: self.new_game())
        top.add_widget(self.status_lbl)
        top.add_widget(self.diff_btn)
        self.add_widget(top)

        # Middle: Hangman + word
        middle = BoxLayout()
        self.hangman_canvas = HangmanCanvas(size_hint=(0.4,1))
        middle.add_widget(self.hangman_canvas)
        self.word_lbl = Label(text=self.word_text, font_size=40)
        middle.add_widget(self.word_lbl)
        self.add_widget(middle)

        # Keyboard
        kb = GridLayout(cols=10, size_hint_y=None, height=200, spacing=2)
        self.kb_buttons = {}
        for ch in "QWERTYUIOPASDFGHJKLZXCVBNM":
            btn = Button(text=ch, on_press=lambda b, x=ch: self.press(x))
            kb.add_widget(btn)
            self.kb_buttons[ch.lower()] = btn
        self.add_widget(kb)

        self.new_game()

    def _load_stats(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    self.stats.update(json.load(f))
            except: pass

    def _save_stats(self):
        self.stats["last_played"] = datetime.now().isoformat(timespec="seconds")
        with open(SAVE_FILE, "w") as f:
            json.dump(self.stats, f, indent=2)

    def _load_words(self):
        if os.path.exists(WORDS_FILE):
            try:
                with open(WORDS_FILE,"r") as f:
                    words = [w.strip() for w in f if w.strip().isalpha()]
                    if len(words)>=50: return words
            except: pass
        return FALLBACK_WORDS

    def press(self, ch):
        if not self._game_active: return
        outcome = self.game.guess(ch)
        self.update_ui()
        self.kb_buttons[ch.lower()].disabled = True
        if self.game.is_won():
            self.end_game(True)
        elif self.game.is_lost():
            self.end_game(False)

    def new_game(self):
        self._game_active = True
        self.game.start_new("Normal")
        for b in self.kb_buttons.values(): b.disabled=False
        self.update_ui()

    def update_ui(self):
        self.word_text = " ".join(self.game.display).upper()
        self.word_lbl.text = self.word_text
        self.hangman_canvas.attempts = self.game.attempts_used()

    def end_game(self, won):
        self._game_active = False
        self.stats["games"] +=1
        if won: 
            self.stats["wins"] +=1
            self.stats["streak"] +=1
        else:
            self.stats["streak"]=0
        self._save_stats()


class HangmanApp(App):
    def build(self):
        return HangmanAppUI()

if __name__=="__main__":
    HangmanApp().run()
