with open("inputs/day_4_pbr.txt") as file:
  lines = [line.rstrip() for line in file]

part1 = 0
out = sum([int(pow(2,len(set(prizes[0].split()).intersection(set(prizes[1].split()))) - 1)) for prizes in [line.split(": ")[1].split("| ") for line in lines]])
print(out)

part2 = 0
cards = [1]*len(lines)
for x in range(len(lines)):
  prizes = lines[x].split(": ")[1].split("| ")
  wins = len(set(prizes[0].split()).intersection(set(prizes[1].split())))
  for y in range(wins):
    cards[x + y + 1] += cards[x]
part2 = sum(cards)
print(part2)