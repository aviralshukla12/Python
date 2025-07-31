import random
import sys

print("🎮 Let's Play ROCK PAPER SCISSORS GAME! 🎮\n")

wins = 0
losses = 0
ties = 0
move_names = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}

while True:
    print("Current streak: %s Wins, %s Losses, %s Ties" % (wins, losses, ties))
    while True:
        print("\nType 'Q' to quit")
        print("'R' for ROCK, 'P' for PAPER, 'S' for SCISSORS")
        playermove = input("Your move: ").upper()
        if playermove == "Q":
            print("Thanks for playing! Final score: %s Wins, %s Losses, %s Ties" % (wins, losses, ties))
            sys.exit()
        if playermove in ['R', 'P', 'S']:
            break
        print("Invalid input! Please enter 'R', 'P', 'S' or 'Q'.")

    compMove = random.choice(['R', 'P', 'S'])
    print("You chose:", move_names[playermove])
    print("Computer chose:", move_names[compMove])

    if playermove == compMove:# i have shorten the overall logic 
        print("It's a tie!")
        ties += 1
    elif (playermove == 'R' and compMove == 'S') or \
         (playermove == 'P' and compMove == 'R') or \
         (playermove == 'S' and compMove == 'P'):
        print("You win!")
        wins += 1
    else:
        print("You lose!")
        losses += 1