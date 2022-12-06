import random, sys

print("Let's Play ROCK PAPER SCISSORS GAME!")

wins = 0
losses = 0
ties = 0

while True:
    print("Current streak: %s Wins, %s Losses, %s Ties" % (wins, losses, ties))
    while True:
        print("Type 'Q' to quit \n'R' for ROCK, 'P' for PAPER, 'S' for SCISSORS")
        playermove = input().upper()
        if playermove == "Q":
            sys.exit()
        if playermove == "R" or playermove == "P" or playermove == "S":
            break

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
    elif playermove == "R" and compMove == "P":
        print("It's a loss!")
        losses += 1
    elif playermove == "R" and compMove == "S":
        print("It's a win!")
        wins += 1
    elif playermove == "P" and compMove == "S":
        print("It's a loss!")
        losses += 1
    elif playermove == "P" and compMove == "R":
        print("It's a win!")
        wins += 1
    elif playermove == "S" and compMove == "R":
        print("It's a loss!")
        losses += 1
    elif playermove == "S" and compMove == "P":
        print("It's a win!")
        wins += 1
    else:
        print("Thanks for trying my game")
