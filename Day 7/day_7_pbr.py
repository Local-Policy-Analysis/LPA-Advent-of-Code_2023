with open("inputs/day_7_pbr.txt") as file:
  lines = [line.rstrip().split() for line in file]


cardstopoints = "23456789TJQKA"

# I feel like there is a better way to do this
def type_score(cards):
  counts = []
  st = set(cards)
  if len(st) == 5: # High card
    return(0)
  if len(st) == 1: # Five of a kind
    return(6e7)
  for card in st:
    counts.append(cards.count(card))
  if max(counts) == 4: # Four of a kind
    return(5e7)
  elif (3 in counts) and (2 in counts): # Full House
    return(4e7)
  elif (3 in counts): # Three of a kind
    return(3e7)
  elif counts.count(2) == 2: #two pair
    return(2e7)
  else:
    return(1e7)


def score(info, cardscores):
  cards = info[0]
  raw_score = int("0x" + "".join([hex((cardscores.index(x) + 1))[-1] for x in cards]), 0)
  return(raw_score + type_score(cards))


winnings = [(x+1) * int(state[1]) for x, state in enumerate(sorted(lines, key=lambda x: score(x, cardstopoints)))]
print("Part 1: {}".format(sum(winnings)))

cardstopoints2 = "J23456789TQKA"

def replaceJ(hand):
  if hand == "JJJJJ":
    return(hand)
  no_jacks = hand.replace("J", "")
  most_common = sorted(no_jacks, key=lambda x: no_jacks.count(x))[-1]
  return(hand.replace("J", most_common))

def score2(info, cardscores):
  cards = info[0]
  raw_score = int("0x" + "".join([hex((cardscores.index(x) + 1))[-1] for x in cards]), 0)
  return(raw_score + type_score(replaceJ(cards)))

winnings = [(x+1) * int(state[1]) for x, state in enumerate(sorted(lines, key=lambda x: score2(x, cardstopoints2)))]
print("Part 2: {}".format(sum(winnings)))