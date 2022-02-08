from comp_word import *
from words import *
import re

# wordle guide, providing
#   tracking of  wordle game in progress
#   reporting of remaining possible wordles 
#   suggested legal guess with best entropy reduction
#   suggested guess from current possibles

def help_msg():
  print("  q to quit")
  print("  w to list remaining possible wordles")
  print("  p to list pattern frequencies for current guess")
  print("  l1g  for the legal word with the best expected 1-guess entropy reduction")
  print("  p1g  for the potential wordle with the best expected 1-guess entropy reduction")
  print("  h1g  (hard mode) for the remaining possible word with best entropy reduction")
  print("  a potential guess to analyze")
  print("  a pattern returned by wordle for the last guess")
  print()


def max_ent_guess(guesses, possibles):
  # find max one-guess entropy reduction
  # return (guess, poss_d) of best guess against given possibles
  print("One-guess max entropy reduction")
  print(f"Testing {len(guesses)} guesses against {len(possibles)} possible wordles")

  e_max = None
  g_max_e = None
  p_max_e = None
  for g in guesses:
    patt_d = categorize_possibles(g, possibles)
    e = entropy_dict(patt_d)
    if e_max == None or e > e_max:
      g_max_e = g
      p_max_e = patt_d
      e_max = e
      print(f"   new best: {g_max_e} {e_max:.3f}")
  return g_max_e, p_max_e, e_max

  
pattern_re = re.compile('['+CORRECT_C+PRESENT_C+WRONG_C+']*$')
possibles = POSSIBLE_WORDLES
guess = None
patt_d = None
done = False

print("Welcome to wordle guide. At the W> prompt, you may enter:")
help_msg()


while True:
  if len(possibles) > 1:
    print(f"There are now {len(possibles)} possible wordles")
  else:
    print(f"The wordle must be {possibles[0]}")
  cmd = input("W> ").lower()
  

  if cmd == 'q':
    break
    
  if cmd == 'w':
    print(f"possible words: {possibles}")
    continue

  if cmd == 'p':
    print(f"frequencies of {len(patt_d)} patterns, with guess {guess}: ")
    for p in patt_d:
      print(f"  {p} {len(patt_d[p])}")
    print
    continue

  if cmd == 'l1g':
    guess, patt_d, ent = max_ent_guess(LEGAL_GUESSES, possibles)
    print(f"The guess {guess} has expected entropy reduction of {ent:.3f}")
    continue

  if cmd == "p1g":
    guess, patt_d, ent = max_ent_guess(POSSIBLE_WORDLES, possibles)
    print(f"The guess {guess} has expected entropy reduction of {ent:.3f}")
    continue

  if cmd == "h1g":
    guess, patt_d, ent = max_ent_guess(possibles, possibles)
    print(f"The guess {guess} has expected entropy reduction of {ent:.3f}")
    continue

  if len(cmd) == LEN and cmd.isalpha():
    guess = cmd
    patt_d = categorize_possibles(guess, possibles)
    ent = entropy_dict(patt_d)
    print(f"The guess {guess} has expected entropy reduction of {ent:.3f} based on pattern counts")
    print(partition_dict(patt_d))
    continue

  if len(cmd) == LEN and pattern_re.match(cmd):
    if patt_d == None:
      print("No guess has been analyzed! Request a suggested guess or enter the one you're playing")
      continue
    if cmd not in patt_d:
      print("Unexpected pattern! Analysis predicts one of the following:")
      print(patt_d.keys())
      continue
    possibles = patt_d[cmd]
    continue

  print(f"Command {cmd} not recognized")
  help_msg()
  continue

print('done')

