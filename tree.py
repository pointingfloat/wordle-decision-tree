from comp_word import *
from words import *
import re
import argparse

# Print wordle decision tree
#   Start with user-specified guess
#   Subsequent guesses based on greedy 1-step maximum expected entropy reduction 
#   Subsequent guesses chosen from either
#   legal guesses, wordle set, or remaining possibles (hard mode)

# Log count of leaf nodes at each level
N_level = {}

def log_level(n):
  if n not in N_level:
    N_level[n] = 0
  N_level[n] = N_level[n]+1
  

def max_ent_guess(guesses, possibles):
  # find max one-guess entropy reduction
  # return (guess, patt_d) of best guess against given possibles
  #print("One-guess max entropy reduction")
  #print(f"Testing {len(guesses)} guesses against {len(possibles)} possible wordles")

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
      #print(f"   new best: {g_max_e} {e_max:.3f}")
  return g_max_e


# possible selection functions
def l1g(possibles):
  # consider all legal words
  return max_ent_guess(LEGAL_GUESSES, possibles)

def w1g(possibles):
  # consider all potential wordles
  return max_ent_guess(POSSIBLE_WORDLES, possibles)

def p1g(possibles):
  # consider only remaining possibles (hard mode)
  return max_ent_guess(possibles, possibles)

buff_text = ''
buff_level = 1

def buff_node(level, text):
  global buff_level
  global buff_text
  # consider only levels up to print_level (if cmd-line arg is set)
  if args.print_level == None or args.print_level >= level:
    # if level does not increase, flush and replace with new indent
    if level <= buff_level:
      print(buff_text)
      buff_text = (18*(level-1))*' '
    # assume that level goes up by at most 1
    # append text to buffer
    buff_text = buff_text + f"{text:18s}"
    buff_level = level

def flush_buff():
  global buff_level
  global buff_text
  print(buff_text)
  buff_text = ''
  buff_level = 1


def DFS_step(level, possibles, guess, select_f):
  # level used for printing and logging
  # possibles are before guess
  # level applies to guess
  # DFS_step figures out possible (level)th responses
  # For each, either records a leaf node or computes guess level+1
  # then prints and, if needed, recurses
  
  patt_d = categorize_possibles(guess, possibles)
  for p in sorted(patt_d.keys()):
    if p == ALL_GOOD:
      buff_node(level,p)
      log_level(level)
      continue
    poss_new = patt_d[p]
    guess_new = select_f(poss_new)
    buff_node(level, f"{p} {len(poss_new):4d} {guess_new}")
    DFS_step(level+1, poss_new, guess_new, select_f)
  return

def DFS_tree(possibles, guess, select_f):
  DFS_step(1, possibles, guess1, select_f)
  flush_buff()



#dictionary of select functions
select_f_d = {'any':l1g, 'wordle':w1g, 'hard':p1g}
            
parser = argparse.ArgumentParser(description='Produce wordle decision tree for a starting guess')
parser.add_argument('select_mode', choices=select_f_d.keys(),
                    help='choose guess from any legal word, a possible wordle, or (hard mode) satisfying given clues')
parser.add_argument('--guess1', help='force specific first guess')
parser.add_argument('--print_level', default=None, type=int)
args = parser.parse_args()

select_f = select_f_d[args.select_mode]
print(f"Guesses are selected by (greedy) maximizing expected entropy reduction")
print(f"Selection mode is {args.select_mode}")
possibles = POSSIBLE_WORDLES
if args.guess1:
  guess1 = args.guess1
  print(f"First guess is {guess1} set by command line argument")
else:
  guess1 = select_f(possibles)
  print(f"First guess is {guess1} selected by mode {args.select_mode}")

if args.print_level:
  print(f"Wordle decision tree to level {args.print_level}:")
else:
  print("Wordle decision tree:")
  
DFS_step(1, possibles, guess1, select_f)

print()
# report level histogram
print(f"N   # wordles identified on guess N")
s_lev_n = 0
for n in sorted(N_level.keys()):
  print(f"{n}   {N_level[n]}")
  s_lev_n = s_lev_n + n * N_level[n]
print(f"{s_lev_n/sum(N_level.values()):.3f} expected levels")

  
