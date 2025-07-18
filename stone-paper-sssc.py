import random

print("Let's Play ROCK PAPER SCISSORS GAME!")

wins = 0
losses = 0
ties = 0


while True:
    try:
        total_rounds = int(input("How many rounds would you like to play? (e.g., 3, 5): "))
        if total_rounds > 0:
            break
        else:
            print("Please enter a positive number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

round_num = 1

while round_num <= total_rounds:
    print(f"\nRound {round_num} of {total_rounds}")
    print(f"Current score: {wins} Wins, {losses} Losses, {ties} Ties")


    while True:
        print("Type 'R' for ROCK, 'P' for PAPER, 'S' for SCISSORS")
        playermove = input("Your move: ").upper()
        if playermove in ["R", "P", "S"]:
            break
        else:
            print("Invalid input. Try again.")


    moves = {"R": "ROCK", "P": "PAPER", "S": "SCISSORS"}
    print(f"{moves[playermove]} versus...")


    compMove = random.choice(["R", "P", "S"])
    print(moves[compMove])


    if playermove == compMove:
        print("It's a tie!")
        ties += 1
    elif (playermove == "R" and compMove == "S") or \
         (playermove == "P" and compMove == "R") or \
         (playermove == "S" and compMove == "P"):
        print("You win this round!")
        wins += 1
    else:
        print("You lose this round!")
        losses += 1

    round_num += 1


print("\n--- GAME OVER ---")
print(f"Final score: {wins} Wins, {losses} Losses, {ties} Ties")

if wins > losses:
    print("🎉 You are the overall winner!")
elif losses > wins:
    print("😢 You lost the game. Better luck next time!")
else:
    print("😐 It's a tie overall!")

