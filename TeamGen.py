"""
TeamGen.py

Interactively split a list of people into random teams of a given size.
Duplicate names are removed automatically.

Usage:
    python TeamGen.py
    # enter team size, then enter names one per line
    # press 'q' when done entering names

Dependencies:
    None (stdlib only)
"""

import random


def main():
    team_size = int(input("How many people per team: "))
    names = []

    while True:
        name = input("Enter a team member name (q to quit): ")
        if name.lower() == "q":
            break
        names.append(name)

    names = list(set(names))
    random.shuffle(names)

    teams = []
    while names:
        teams.append([names.pop(0) for _ in range(team_size) if names])

    for i, team in enumerate(teams, 1):
        print(f"Team {i}: {', '.join(team)}")

    print(f"\nSplit {sum(len(t) for t in teams)} people into {len(teams)} teams")


if __name__ == "__main__":
    main()

