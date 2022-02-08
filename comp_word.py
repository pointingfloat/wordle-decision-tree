"""wordle comparison
   2022 1 27  B Fleischer
     At least for now, no classes, just a utility function
     To do:
       Throw errors instead of failing
   2022 2 8   B Fleischer
     entropy_dict: add bonus if ALL_GOOD is one of the keys
       Looking at entropy alone doesn't distinguish between a correct guess
       and a wrong guess which reduces the set of possibles to 1.
       If the possible set has only one wordle, the entropy change
       is 0 for any guess, so not distinguishing the right answer likely
       results in an infinite loop.
       You could say entropy is not the whole story here. Entropy is about
       what you know. In the game you have to not only know the word,
       but also confirm it by guessing. 
"""

from math import log2

CORRECT_C = '*'
PRESENT_C = '+'
WRONG_C = '.'


def comp_word(guess, target):
  # compare one guessed word to a target word
  # return pattern, each char indicates status of corresponding char in guess
  if len(guess) != len(target):
    print(f"comp_word: guess {guess} and target {target} are not the same length")
    quit()
    return None
  
  pl = list(guess) # initialize pattern (list) with letters of guess
  tl = list(target)
  
  # Replace CORRECT matches in pattern with CORRECT_C
  for i in range(len(pl)):
    if pl[i] == tl[i]:
      pl[i] = CORRECT_C
      tl[i] = CORRECT_C
    
  # Replace PRESENT letters and mismatches in pattern
  for i in range(len(pl)):
    if pl[i] == CORRECT_C:
      continue
    if pl[i] in tl:
      tl[tl.index(pl[i])] = PRESENT_C
      pl[i] = PRESENT_C
    else:
      pl[i] = WRONG_C

  # return pattern as string
  return ''.join(pl)
  

def categorize_possibles(guess, possibles):
  # For one guessed word, create a dict of possible results
  # Keys are compare patterns, values are lists of targets
  poss_d = {}
  for target in possibles:
    pattern = comp_word(guess, target)
    if pattern not in poss_d:
      poss_d[pattern] = []
    poss_d[pattern].append(target)

  return poss_d


def partition_dict(d):
  # d is a dict with lists as values
  # return list of value lengths
  return [len(d[k]) for k in d]

def has_all_good(d):
  # see if any key in dict d is all_good (no '+', no '.')
  for k in d.keys():
    if '+' not in k and '.' not in k:
      return True
  return False

def entropy_dict(d):
  # d is a dict with lists as values
  # compute entropy of partition
  part = partition_dict(d)
  N = sum(part)
  # if d includes ALL_GOOD, give bonus credit of 1/N
  if has_all_good(d):
    bonus = 1/N
  else:
    bonus = 0
  frac = [i/N for i in part]
  return sum( [-f * log2(f) for f in frac] ) + bonus
    
