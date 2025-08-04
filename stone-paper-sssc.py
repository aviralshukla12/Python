import random, sys

print("Let's Play ROCK PAPER SCISSORS GAME!")
# Integrating round of 5 game
wins = 0
losses = 0
ties = 0
computer_wins = 0
player_wins = 0
max_rounds = 5
current_round = 0



while current_round<max_rounds and computer_wins <3 and player_wins < 3:
    current_round += 1
    print("\nRound %s of %s" % (current_round, max_rounds))
    print("Current streak: %s Wins, %s Losses, %s Ties" % (wins, losses, ties))
    
    print("Type 'Q' to quit \n'R' for ROCK, 'P' for PAPER, 'S' for SCISSORS")
    playermove = input().upper()
    if playermove == "Q":
        sys.exit()

    if playermove == "R":
        print("ROCK versus...")
    if playermove == "P":
        print("PAPER versus...")
    if playermove == "S":
        print("SCISSORS versus...")

    randomNum = random.randint(1, 3)
    if randomNum == 1:
        compMove = "R"
        print("ROCK")
    if randomNum == 2:
        compMove = "P"
        print("PAPER")
    if randomNum == 3:
        compMove = "S"
        print("SCISSORS")

    if playermove == compMove:
        print("It's a tie!")
        ties += 1
    elif (playermove == "R" and compMove == "S") or (playermove == "P" and compMove == "R") or (playermove == "S" and compMove == "P"):
        print("It's a win!")
        wins += 1
        player_wins += 1
    else:
        print("It's a loss!")
        losses += 1
        computer_wins += 1
    print(f"{current_round} Round Score - You: {player_wins}, Computer: {computer_wins}")

# Declaring the final winner
if player_wins > computer_wins:
    print("\nYou won the Best of 5 matches! 🏆")
elif computer_wins > player_wins:
    print("\nComputer won the Best of 5 matches! 😔")
else:
    print("\nThe match ended in a tie! 🤝")

print(f"Final Game Stats: {wins} Wins, {losses} Losses, {ties} Ties")
