"""
Tournament Winner
There's an algorithms tournament where programmer teams race to solve
problems. The format is round-robin: each team plays every other team once,
and every matchup picks a home team and an away team. Each contest produces a
single winner—no ties. Winners earn three points; losers earn none. The
overall champion is the team with the highest point total.

You're given two arrays. `competitions` lists each matchup as
`[homeTeam, awayTeam]`, while `results[i]` is `1` when the home team won
`competitions[i]`, and `0` otherwise. Each team name is a string up to
30 characters.

Exactly one team wins the tournament, and every team appears in at least two
matches because the tournament always features at least two teams.

Sample Input
competitions = [
  ["HTML", "C#"],
  ["C#", "Python"],
  ["Python", "HTML"],
]
results = [0, 0, 1]

Sample Output
"Python" (C# beats HTML, Python Beats C#, and Python Beats HTML.)
HTML - 0 points
C# - 3 points
Python - 6 points
"""

from collections import defaultdict
from operator import itemgetter

competitions = [
  ["HTML", "C#"],
  ["C#", "Python"],
  ["Python", "HTML"],
]
results = [0, 0, 1]

team_scores = defaultdict(int)

for game_index, ((home_team, away_team), result) in enumerate(zip(competitions, results)):
    for team in (home_team, away_team):
        team_scores[team] += 0

    winner = home_team if result == 1 else away_team
    team_scores[winner] += 3

    print(f'Game: {game_index}')
    print(dict(team_scores))

for team, score in sorted(team_scores.items(), key=itemgetter(1), reverse=True):
    print(f'{team}: {score}')
