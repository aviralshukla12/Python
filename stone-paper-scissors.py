import tkinter as tk
import random
import json
import os
from datetime import datetime

MOVES = {'R': 'Rock 🪨', 'P': 'Paper 📄', 'S': 'Scissors ✂️'}

class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 Rock Paper Scissors Ultimate 🎉")
        self.root.geometry("500x600")
        self.root.configure(bg="#FFFAE3")

        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.streak = 0
        self.history = []
        self.load_data()

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="ROCK PAPER SCISSORS!", font=("Comic Sans MS", 28, "bold"),
                 bg="#FFFAE3", fg="#FF6B6B").pack(pady=20)

        self.stats_label = tk.Label(self.root, font=("Comic Sans MS", 14),
                                    bg="#FFFAE3", fg="#444")
        self.stats_label.pack(pady=10)

        self.result_label = tk.Label(self.root, font=("Comic Sans MS", 20, "bold"),
                                     width=30, height=2, bg="#FFFAE3")
        self.result_label.pack(pady=20)

        btn_frame = tk.Frame(self.root, bg="#FFFAE3")
        btn_frame.pack(pady=20)

        rock_btn = tk.Button(btn_frame, text="🪨 Rock", command=lambda: self.play('R'))
        paper_btn = tk.Button(btn_frame, text="📄 Paper", command=lambda: self.play('P'))
        scissors_btn = tk.Button(btn_frame, text="✂️ Scissors", command=lambda: self.play('S'))

        for btn in (rock_btn, paper_btn, scissors_btn):
            btn.config(font=("Comic Sans MS", 14, "bold"),
                       bg="#FFD93D", fg="#444",
                       activebackground="#FF6B6B", activeforeground="#fff",
                       width=10, height=2, bd=4, relief="groove", cursor="hand2")
            btn.pack(side="left", padx=15)

        tk.Button(self.root, text="📋 View History", command=self.show_history,
                  font=("Comic Sans MS", 12), bg="#5CD859", fg="white",
                  width=20, height=2).pack(pady=10)

        tk.Button(self.root, text="🏆 View Leaderboard", command=self.show_leaderboard,
                  font=("Comic Sans MS", 12), bg="#FF6B6B", fg="white",
                  width=20, height=2).pack(pady=10)

        tk.Button(self.root, text="🔄 Reset Stats", command=self.reset_game,
                  font=("Comic Sans MS", 12), bg="#FFD93D", fg="#444",
                  width=20, height=2).pack(pady=10)

        tk.Button(self.root, text="🚪 Quit", command=self.quit_game,
                  font=("Comic Sans MS", 12), bg="#FF6B6B", fg="white",
                  width=20, height=2).pack(pady=10)

        self.update_stats()

    def load_data(self):
        if os.path.exists('rps_gui_save.json'):
            try:
                with open('rps_gui_save.json', 'r') as f:
                    data = json.load(f)
                    self.wins = data.get('wins', 0)
                    self.losses = data.get('losses', 0)
                    self.ties = data.get('ties', 0)
                    self.streak = data.get('streak', 0)
                    self.history = data.get('history', [])
            except:
                pass

    def save_data(self):
        data = {
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'streak': self.streak,
            'history': self.history
        }
        with open('rps_gui_save.json', 'w') as f:
            json.dump(data, f)

    def adaptive_ai(self):
        if len(self.history) < 3:
            return random.choice(['R', 'P', 'S'])
        last_moves = [h['player'] for h in self.history[-3:]]
        most_common = max(set(last_moves), key=last_moves.count)
        counter = {'R': 'P', 'P': 'S', 'S': 'R'}
        return counter[most_common]

    def play(self, user_move):
        computer_move = self.adaptive_ai()
        result = self.determine_winner(user_move, computer_move)

        self.history.append({
            'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'player': user_move,
            'computer': computer_move,
            'result': result
        })

        feedback = {
            'win': ("You Win! 🥳", "#5CD859"),
            'loss': ("Computer Wins! 😝", "#FF6B6B"),
            'tie': ("It's a Draw! 🤝", "#FFD93D")
        }

        text, color = feedback[result]
        self.result_label.config(text=f"{MOVES[user_move]} vs {MOVES[computer_move]} — {text}", bg=color)
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
        self.stats_label.config(
            text=f"Wins: {self.wins}  Losses: {self.losses}  Ties: {self.ties}\n"
                 f"Streak: {self.streak}  Win Rate: {win_rate:.1f}%"
        )

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("📋 Game History")
        history_window.configure(bg="#FFFAE3")

        tk.Label(history_window, text="Last 10 Matches", font=("Comic Sans MS", 16, "bold"),
                 bg="#FFFAE3").pack(pady=10)

        text = tk.Text(history_window, width=50, height=15, bg="#fff", font=("Comic Sans MS", 12))
        text.pack(padx=10, pady=10)

        for h in self.history[-10:]:
            result = "Win" if h['result'] == 'win' else "Loss" if h['result'] == 'loss' else "Tie"
            text.insert(tk.END, f"{h['time']}: You chose {MOVES[h['player']]}, Computer chose {MOVES[h['computer']]} — {result}\n")

        text.config(state='disabled')

    def show_leaderboard(self):
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("🏆 Leaderboard")
        leaderboard_window.configure(bg="#FFFAE3")

        max_streak = 0
        current_streak = 0
        for h in self.history:
            if h['result'] == 'win':
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        total_games = len(self.history)
        win_rate = (self.wins / total_games * 100) if total_games > 0 else 0

        tk.Label(leaderboard_window, text="Your Leaderboard", font=("Comic Sans MS", 16, "bold"),
                 bg="#FFFAE3").pack(pady=10)

        stats = f"""
        Total Games: {total_games}
        Wins: {self.wins}
        Losses: {self.losses}
        Ties: {self.ties}
        Longest Win Streak: {max_streak}
        Current Win Streak: {self.streak}
        Win Rate: {win_rate:.1f}%
        """
        tk.Label(leaderboard_window, text=stats.strip(), justify='left',
                 bg="#FFFAE3", font=("Comic Sans MS", 12)).pack(pady=20)

    def reset_game(self):
        self.wins = self.losses = self.ties = self.streak = 0
        self.history = []
        self.update_stats()
        self.result_label.config(text="", bg="#FFFAE3")
        self.save_data()

    def quit_game(self):
        self.save_data()
        self.root.quit()


root = tk.Tk()
app = RPSGame(root)
root.mainloop()
