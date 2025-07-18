import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os
import csv

# Global score trackers
wins = 0
losses = 0
ties = 0
history = []
player_move_counts = {"R": 0, "P": 0, "S": 0}
player_name = ""
LEADERBOARD_FILE = "leaderboard.json"


# Load existing leaderboard
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return {}


# Save current player's score to leaderboard
def save_leaderboard():
    leaderboard = load_leaderboard()
    leaderboard[player_name] = {"wins": wins, "losses": losses, "ties": ties}
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=2)


# Show full leaderboard in a messagebox
def show_leaderboard():
    leaderboard = load_leaderboard()
    if not leaderboard:
        messagebox.showinfo("Leaderboard", "No scores yet.")
        return

    leaderboard_text = "\n".join(
        f"{name}: {data['wins']}W - {data['losses']}L - {data['ties']}T"
        for name, data in leaderboard.items()
    )
    messagebox.showinfo("Leaderboard", leaderboard_text)


# Adaptive AI to counter player’s frequent move
def adaptive_ai():
    total = sum(player_move_counts.values())
    if total == 0:
        return random.choice(["R", "P", "S"])
    most_common = max(player_move_counts, key=player_move_counts.get)
    counter = {"R": "P", "P": "S", "S": "R"}
    return counter[most_common]


# Handle player move and game outcome
def update_status(player_move):
    global wins, losses, ties

    player_move_counts[player_move] += 1
    comp_move = adaptive_ai()

    result = ""
    if player_move == comp_move:
        result = "Tie!"
        ties += 1
    elif (player_move == "R" and comp_move == "S") or \
         (player_move == "P" and comp_move == "R") or \
         (player_move == "S" and comp_move == "P"):
        result = "You Win!"
        wins += 1
    else:
        result = "You Lose!"
        losses += 1

    move_map = {"R": "Rock", "P": "Paper", "S": "Scissors"}
    history.append(f"You: {move_map[player_move]} | Computer: {move_map[comp_move]} => {result}")
    if len(history) > 10:
        history.pop(0)

    save_leaderboard()
    update_ui(result)


# Update the GUI display
def update_ui(result):
    status_var.set(result)
    score_var.set(f"{player_name} → Wins: {wins}, Losses: {losses}, Ties: {ties}")
    history_var.set("\n".join(history))


# Export history to CSV file
def export_history():
    if not history:
        messagebox.showinfo("Export", "No history to export.")
        return

    filename = f"{player_name}_history.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Your Move", "Computer Move", "Result"])
        for h in history:
            parts = h.split("=>")
            moves, result = parts[0].strip(), parts[1].strip()
            you, comp = moves.split("|")
            writer.writerow([you.split(":")[1].strip(), comp.split(":")[1].strip(), result])
    
    messagebox.showinfo("Export", f"Game history exported to {filename}")


# Prompt for player's name
def ask_player_name():
    global player_name
    name = simpledialog.askstring("Welcome", "Enter your name:")
    if not name:
        name = "Anonymous"
    player_name = name


# Handle move selection
def on_choice(choice):
    update_status(choice)


# Tkinter setup
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("400x500")

# Ask player name before starting
ask_player_name()

# Variables
status_var = tk.StringVar()
score_var = tk.StringVar()
history_var = tk.StringVar()

# UI Components
tk.Label(root, text="Rock Paper Scissors", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="Rock", width=20, command=lambda: on_choice("R")).pack(pady=5)
tk.Button(root, text="Paper", width=20, command=lambda: on_choice("P")).pack(pady=5)
tk.Button(root, text="Scissors", width=20, command=lambda: on_choice("S")).pack(pady=5)

tk.Label(root, textvariable=status_var, font=("Arial", 12), fg="blue").pack(pady=10)
tk.Label(root, textvariable=score_var, font=("Arial", 11)).pack(pady=5)

tk.Label(root, text="Recent Games:", font=("Arial", 10, "bold")).pack()
tk.Label(root, textvariable=history_var, justify="left", font=("Courier", 10)).pack(pady=5)

tk.Button(root, text="Show Leaderboard", command=show_leaderboard).pack(pady=10)
tk.Button(root, text="Export History", command=export_history).pack(pady=5)

update_ui("Make your move!")
root.mainloop()
