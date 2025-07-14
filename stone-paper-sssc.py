import random
import sys
import time
from datetime import datetime
import json
import os

MOVES = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}
WIN_CONDITIONS = {
    'R': {'S': 'crushes', 'P': 'is covered by'},
    'P': {'R': 'covers', 'S': 'is cut by'},
    'S': {'P': 'cuts', 'R': 'are crushed by'}
}

class RockPaperScissors:
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.streak = 0
        self.history = []
        self.load_game()
        
    def load_game(self):
        if os.path.exists('rps_save.json'):
            try:
                with open('rps_save.json', 'r') as f:
                    data = json.load(f)
                    self.wins = data.get('wins', 0)
                    self.losses = data.get('losses', 0)
                    self.ties = data.get('ties', 0)
                    self.streak = data.get('streak', 0)
                    self.history = data.get('history', [])
            except:
                pass
    
    def save_game(self):
        data = {
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'streak': self.streak,
            'history': self.history
        }
        with open('rps_save.json', 'w') as f:
            json.dump(data, f)
    
    def display_stats(self):
        total = self.wins + self.losses + self.ties
        win_rate = (self.wins / total * 100) if total > 0 else 0
        print("\n"+"="*40)
        print(f"Current Stats: {self.wins} Wins, {self.losses} Losses, {self.ties} Ties")
        print(f"Win Rate: {win_rate:.1f}% | Current Streak: {self.streak}")
        print("="*40 + "\n")
        
    def get_computer_move(self):
        #this. can adapt to the player patterns
        if len(self.history) < 3:
            return random.choice(list(MOVES.keys()))
        
        #this analyzes the last moves
        last_moves = [h['player'] for h in self.history[-3:]]
        most_common = max(set(last_moves), key=last_moves.count)
        
        #mathc the most commin moove
        if most_common == 'R':
            return 'P'
        elif most_common == 'P':
            return 'S'
        else:
            return 'R'
    
    def get_player_move(self):
        while True:
            print("\nChoose your move:")
            print("[R]ock  [P]aper  [S]cissors")
            print("[L]eaderboard  [H]istory  [Q]uit")
            choice = input("> ").upper()
            
            if choice in MOVES:
                return choice
            elif choice == 'Q':
                self.save_game()
                print("\nThanks for playing! Final stats:")
                self.display_stats()
                sys.exit()
            elif choice == 'H':
                self.show_history()
            elif choice == 'L':
                self.show_leaderboard()
            else:
                print("Invalid input. Please enter R, P, S, L, H, or Q.")
    
    def show_history(self):
        print("\n" + "="*40)
        print("GAME HISTORY (Last 10 matches)")
        print("="*40)
        for game in self.history[-10:]:
            result = "Win" if game['result'] == 'win' else "Loss" if game['result'] == 'loss' else "Tie"
            print(f"{game['time']}: You chose {MOVES[game['player']]}, Computer chose {MOVES[game['computer']]} - {result}")
        print("="*40 + "\n")
    
    def show_leaderboard(self):
        if not self.history:
            print("\nNo games played yet!\n")
            return
            
        streaks = []
        current_streak = 0
        max_streak = 0
        
        for game in self.history:
            if game['result'] == 'win':
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
                
        print("\n" + "="*40)
        print("LEADERBOARD")
        print("="*40)
        print(f"Longest Win Streak: {max_streak}")
        print(f"Current Win Streak: {self.streak}")
        print("="*40 + "\n")
    
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
    
    def play_round(self):
        player_move = self.get_player_move()
        computer_move = self.get_computer_move()
        
        print(f"\nYou chose: {MOVES[player_move]}")
        time.sleep(0.5)
        print(f"Computer chose: {MOVES[computer_move]}")
        time.sleep(0.5)
        
        if player_move == computer_move:
            print("\nIt's a tie!")
        else:
            verb = WIN_CONDITIONS[player_move].get(computer_move, 'vs')
            print(f"\n{MOVES[player_move]} {verb} {MOVES[computer_move]}!")
        
        result = self.determine_winner(player_move, computer_move)
        
        #this can be used to record the game hitory ok
        self.history.append({
            'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'player': player_move,
            'computer': computer_move,
            'result': result
        })
        
        time.sleep(1)
        self.display_stats()
        time.sleep(1)

def main():
    print("\n" + "="*40)
    print("ROCK PAPER SCISSORS ULTIMATE".center(40))
    print("="*40)
    print("Welcome to the Rock Paper Scissors experience!")
    print("="*40 + "\n")
    
    game = RockPaperScissors()
    
    while True:
        game.play_round()

if __name__ == "__main__":
    main()