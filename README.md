# quiz-cli
This is a small command line game for creating and reviewing flashcard sets as well as tracking learning progress.
## Target assessment level
The target assessment level of this work is 3.
## Specification
### What does this program do?
This program allows the user to:
- create flashcard sets with a front (question) and back (answer) side for each card and save them to files.
- play through flashcards by flipping them using their arrow keys.
- mark cards as "known" or "still learning" as they are playing.
- view a progress report at the end of their playing session.
### Data format
The created flashcard set is saved to a data text file and is named (user selected name).cards. The file consists of lines, each line containing `front / back`. `front` being the question and `back` being the answer. Both sides of the card are always supplied when creating the flashcard set.
## Correctness
### Typical test case
Previously created file [french.cards](https://github.com/rasmusmiikkulainen/tree/main/flashcards/frenc.cards) contains 6 flashcards. When the program (file [main.py](https://github.com/rasmusmiikkulainen/blob/main/main.py)) is run, the user selects `play` from the main menu and then inputs `french` when the program asks to pick a flashcard set to play.

The program then goes through all the flashcards in the set by first showing the question side of the flashcard. The user can then flip the card by pressing either their up or down arrow key to reveal the answer. When they are done with the flashcard, they can press the right arrow key to mark it as "known" or the left arrow key to mark it as "still learning". The flashcard does not need to be flipped before this.

When the user has gone through all the flashcards, the program then displays a summary of their progress, including the number of cards marked as "known" and "still learning", as well as the percentage of cards known.
```
Game finished.
Known: 3
Still learning: 3
You know 50.0% of the flashcards.
Press enter to continue: 
```
### Resource management
The input data file is opened using a `with`-statement, will therefore be closed automatically when it's no longer used.
## Additional notes
I assumed that the "no unnecessary whitespace"-criteria for level 1 only applied to java code, as the provided example contained it.