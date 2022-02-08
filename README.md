# wordle-decision-tree

Some aids for playing Matt Wardle's wordle game. 
The guide script advises you guess by guess. The tree script writes a complete text-formatted decision tree. 
Choices for each guess are based on maximizing entropy reduction, greedily looking at only the next guess. 
Both scripts allow you to choose a guess universe of either all allowed guesses (12K+), potential wordles (~2300) or words that satisfy the current clues ('hard mode').
