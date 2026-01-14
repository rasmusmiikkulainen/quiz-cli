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
The created flashcard set is saved to a data text file and is named (user selected name).cards. The file consists of lines, and each flashcard has three of them. The first line contains the flashcard number for ease of editing, the second line contains the front side, and the third line contains the back side of the card, like so:
```
1.
front: Bonjour
back: Hello
2.
front: Bonsoir
back: Good evening
```
Both the question and the answer are supplied by user input when creating the flashcard set.
## Correctness
### Typical test case
The user runs the program (file [main.py](https://github.com/rasmusmiikkulainen/quiz-cli/blob/main/main.py)) and inputs "create". The user is then shown the interactive flashcard creator:
```
Welcome to the flashcard creator!
When you are ready, enter "/done" when the program asks for the next flashcard.

card 1 front: 
```
The user then creates however many flashcards they want by first inputting a front, then a back side for the flashcard. When they are done, they then input `/done`, when the program asks for the front side of the next flashcard.
```
...

card X front: /done
```
The program then asks the user to input a name for their newly created flashcard set. When the user inputs a valid name, the flashcard set is saved in `./flashcards`. The program creates this folder if it doesn't already exist. The flashcard set is saved as `(chosen name).cards`.

After returning to the main menu, the user inputs "play". The user is then shown a numbered list of all the `.cards`-files in `./flashcards` (in the same directory as [main.py](https://github.com/rasmusmiikkulainen/quiz-cli/blob/main/main.py)). The user can then input either the name or the corresponding number of the flashcard set to select it. After selecting a valid flashcard set, the user is shown instructions on how to play the game. In the input field below the instructions the user can choose to input "reverse" to play the flashcards so that the back side is shown first, or leave it empty to play normally.

The program then goes through all the flashcards in the set by first showing the earlier specified side of the flashcard. The user can then flip the card by pressing either their up or down arrow key to reveal the other side. When they are done with the flashcard, they can press the right arrow key to mark it as "known" or the left arrow key to mark it as "still learning". Between each flashcard the program shows a quick report for 1.5 seconds, which shows the user's progress through the flashcard set in percentages, whether the last card was marked as "known" or "still learning" and the amount of flashcards marked as known out of the amount of flashcards played.

When the user has gone through all the flashcards, the program then displays a complete summary of their progress, including the number of cards marked as "known" and "still learning", as well as the percentage of cards known.
```
Game finished.
Known: 3
Still learning: 3
You knew 50.0% of the flashcards.
Press enter to continue: 
```
### Resource management
All data files are opened using a `with`-statement, and will therefore be closed automatically when they are no longer used.