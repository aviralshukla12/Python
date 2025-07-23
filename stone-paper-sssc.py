import random, sys

print("_________________Let's Play ROCK PAPER SCISSORS GAME!____________________")

wins = 0
losses = 0
ties = 0

# Mapping for moves
moves = {"R": "ROCK", "P": "PAPER", "S": "SCISSORS"}
outcomes = {
    ("R", "S"): "win",
    ("R", "P"): "loss",
    ("P", "R"): "win",
    ("P", "S"): "loss",
    ("S", "P"): "win",
    ("S", "R"): "loss"
}

while True:
    print(f"Current streak: {wins} Wins, {losses} Losses, {ties} Ties")
    while True:
        playermove = input("Type 'Q' to quit\n'R' for ROCK, 'P' for PAPER, 'S' for SCISSORS: ").upper()
        if playermove == "Q":
            sys.exit()
        if playermove in moves:
            break

    print(f"{moves[playermove]} \nversus...")

    compMove = random.choice(list(moves.keys()))
    print(moves[compMove])

    if playermove == compMove:
        print("It's a tie!")
        ties += 1
    else:
        result = outcomes.get((playermove, compMove))
        if result == "win":
            print("It's a win!")
            wins += 1
        else:
            print("It's a loss!")
            losses += 1
