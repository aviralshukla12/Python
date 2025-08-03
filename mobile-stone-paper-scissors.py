from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from datetime import datetime
import random
import json
import os


class ImageButton(ButtonBehavior, Image):
    pass


MOVES = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}


class HomeScreen(Screen):
    pass


class GameScreen(Screen):
    result_text = StringProperty("")
    result_bg_color = ListProperty([1, 1, 1, 1])

    wins = NumericProperty(0)
    losses = NumericProperty(0)
    ties = NumericProperty(0)
    streak = NumericProperty(0)

    def on_pre_enter(self):
        self.load_data()
        self.update_stats()

    def adaptive_ai(self):
        if len(self.manager.history) < 3:
            return random.choice(['R', 'P', 'S'])
        last_moves = [h['player'] for h in self.manager.history[-3:]]
        most_common = max(set(last_moves), key=last_moves.count)
        counter = {'R': 'P', 'P': 'S', 'S': 'R'}
        return counter[most_common]

    def play(self, user_move):
        computer_move = self.adaptive_ai()
        result = self.determine_winner(user_move, computer_move)
        self.manager.history.append({
            'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'player': user_move,
            'computer': computer_move,
            'result': result
        })

        feedback = {
            'win': ("You Win!", [0.36, 0.85, 0.35, 1]),
            'loss': ("Computer Wins!", [0.95, 0.42, 0.42, 1]),
            'tie': ("It's a Draw!", [0.99, 0.85, 0.24, 1])
        }
        text, color = feedback[result]
        self.result_text = f"{MOVES[user_move]} vs {MOVES[computer_move]} — {text}"
        self.result_bg_color = color
        self.update_stats()
        self.save_data()

    def determine_winner(self, player, computer):
        if player == computer:
            self.ties += 1
            self.streak = 0
            return 'tie'
        elif (player == 'R' and computer == 'S') or \
             (player == 'P' and computer == 'R') or \
             (player == 'S' and computer == 'P'):
            self.wins += 1
            self.streak += 1
            return 'win'
        else:
            self.losses += 1
            self.streak = 0
            return 'loss'

    def update_stats(self):
        total = self.wins + self.losses + self.ties
        win_rate = (self.wins / total * 100) if total > 0 else 0
        self.ids.stats_label.text = f"Wins: {self.wins}  Losses: {self.losses}  Ties: {self.ties}\nStreak: {self.streak}  Win Rate: {win_rate:.1f}%"

    def load_data(self):
        if os.path.exists('rps_kivy_save.json'):
            try:
                with open('rps_kivy_save.json', 'r') as f:
                    data = json.load(f)
                    self.wins = data.get('wins', 0)
                    self.losses = data.get('losses', 0)
                    self.ties = data.get('ties', 0)
                    self.streak = data.get('streak', 0)
                    self.manager.history = data.get('history', [])
            except:
                pass

    def save_data(self):
        data = {
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'streak': self.streak,
            'history': self.manager.history
        }
        with open('rps_kivy_save.json', 'w') as f:
            json.dump(data, f)

    def reset_game(self):
        self.wins = self.losses = self.ties = self.streak = 0
        self.manager.history = []
        self.update_stats()
        self.result_text = ""
        self.result_bg_color = [1, 1, 1, 1]
        self.save_data()


class HistoryScreen(Screen):
    def on_pre_enter(self):
        self.ids.history_text.text = "\n".join([
            f"{h['time']} | {MOVES[h['player']]} vs {MOVES[h['computer']]} : {h['result'].capitalize()}"
            for h in self.manager.history[-10:]
        ]) or "No history yet."


class LeaderboardScreen(Screen):
    def on_pre_enter(self):
        gs = self.manager.get_screen('game')
        max_streak = 0
        current_streak = 0
        for h in self.manager.history:
            if h['result'] == 'win':
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        total = len(self.manager.history)
        win_rate = (gs.wins / total * 100) if total > 0 else 0

        self.ids.leaderboard_label.text = f"""
Total Games: {total}
Wins: {gs.wins}
Losses: {gs.losses}
Ties: {gs.ties}
Longest Win Streak: {max_streak}
Current Streak: {gs.streak}
Win Rate: {win_rate:.1f}%
        """


class RPSApp(App):
    def build(self):
        Builder.load_file('rps.kv')
        sm = ScreenManager()
        sm.history = []
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(LeaderboardScreen(name='leaderboard'))
        return sm


if __name__ == '__main__':
    RPSApp().run()
