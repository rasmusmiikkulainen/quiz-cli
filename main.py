import os
import time
# The library readchar is used to register live key inputs from the user.
import readchar
# os.path.abspath() returns the full file path
# Here it is saved to a variable to later return to the main program directory after working in ./flashcards (explained later).
originPath = os.path.abspath("./")


def askCommand():
    """
    Display the main menu and process user commands until "quit" is selected.
    Allows the user to create flashcard sets, play existing ones or quit the program.
    """
    allowed_commands = ("create", "play", "quit")
    commandText = "create, play or quit: "
    command = ""
    clearTerminal()
    print("Welcome to quiz-cli!")
    while command != "quit":
        print("Select command.")
        command = input(commandText)
        while command not in allowed_commands:
            print("Command not found.")
            command = input(commandText)
        clearTerminal()
        if command == "create":
            flashcardCreate()
        elif command == "play":
            flashcardChoose()
        clearTerminal()
    clearTerminal()


def clearTerminal():
    """
    Clear the terminal screen.
    Uses the 'cls' command on Windows and 'clear' on other operating systems.
    """
    # os.system() allows to execute commands in the system terminal.
    # os.name returns the name of the operating system type: "nt" for Windows and "posix" for Linux/MacOS.
    # Different operating systems use different commands to clear the terminal.
    # Windows uses "cls", while Linux and MacOS use "clear".
    os.system("cls" if os.name == "nt" else "clear")


def flashcardCreate():
    """
    Create a new flashcard set interactively.
    Prompts the user for front and back of each card, checks that they are not empty,
    validates the set name, and saves the file in the flashcards folder.
    """
    cardNum = 1
    fronts = []
    backs = []
    print("Welcome to the flashcard creator!")
    print("When you are ready, enter \"/done\" when the program asks for the next flashcard.")
    print()
    front = input(f"card {cardNum} front: ")
    # .strip() can be used to remove unwanted characters.
    # By default it returns the string before the dot with no whitespace.
    # Here it is used to check if the flashcard is empty or full of spaces.
    # This is possible because an empty string returns False in a conditional.
    while not front.strip():
        print("The flashcard cannot be empty.")
        front = input(f"card {cardNum} front: ")
    while front != "/done":
        fronts.append(front)
        back = input(f"card {cardNum} back: ")
        while not back.strip():
            print("The flashcard cannot be empty.")
            back = input(f"card {cardNum} back: ")
        backs.append(back)
        cardNum += 1
        print()
        front = input(f"card {cardNum} front: ")
        while not front.strip():
            print("The flashcard cannot be empty.")
            front = input(f"card {cardNum} front: ")
    if len(fronts) != 0:
        setName = input("Enter a name for your flashcard set: ")
        folders = getFolders("./")      # ./ means the current active directory
        if "flashcards" not in folders:
            # os.mkdir() can be used to create folders.
            # The following creates the folder 'flashcards':
            os.mkdir("flashcards")
        # os.chdir() changes the active directory.
        # This changes the active directory to 'flashcards':
        os.chdir("flashcards")
        files = getFiles("./")
        # .isnumeric() returns True if all the characters in the string are integers.
        # For example, "256".isnumeric() returns True, but "1.32".isnumeric() returns False, because it also contains a dot.
        while f"{setName}.cards" in files or setName.isnumeric() or not setName.strip() or len(setName) >= 50:
            if f"{setName}.cards" in files:
                print(f"You already have a set named {setName}.")
            elif setName.isnumeric():
                print("Your set name can't be an integer.")
            elif not setName.strip():
                print("Your set name can't be empty.")
            elif len(setName) >= 50:
                print("Your set name is too long. The maximum is 50 characters.")
            setName = input("Enter another name: ")
        # The open() function has different modes that are specified after the file location
        # Here "a", or append mode is used. This mode can be used to write new data to a file.
        # If the file exists, "a" adds the new content at the end of that file.
        # If not, it creates the file automatically and adds the new content there.
        with open(f"{setName}.cards", "a") as file:
            for i in range(len(fronts)):
                file.write(f"{i+1}.\n")
                file.write(f"front: {fronts[i]}\n")
                file.write(f"back: {backs[i]}\n")
        clearTerminal()
        print("Here is a list of your flashcards:")
        for i in range(len(fronts)):
            print()
            print(f"Flashcard {i+1}:")
            print(f"Front: {fronts[i]}")
            print(f"Back: {backs[i]}")
        os.chdir(originPath)
        print()
        input("Press enter to continue: ")


def getFolders(dir):
    """
    Get a list of folders in a given directory.
    Args:
        dir: path to directory
    Returns:
        list of the folder names as strings
    """
    # os.listdir() lists all contents of a specified directory
    # os.path.isdir() returns True if the specified file path in the argument is a directory (folder)
    # os.path.join() is essentially the same as "/".join((dir, f))
    return [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]


def getFiles(dir):
    """
    Get a list of files in a given directory.
    Args:
        dir: path to directory
    Returns:
        list of file names as strings
    """
    # os.path.isfile() returns True if the specified file path in the argument is a file
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


def flashcardChoose():
    """
    Display numbered list of available flashcards and prompt user to select one.
    Checks that the selected flashcard set exists and if so, starts the game.
    """
    if "flashcards" not in getFolders("./"):
        os.mkdir("./flashcards")
    os.chdir("./flashcards")
    # By default variables inside a function are not accessible outside it.
    # The keyword global here is used to make the 'cards'-variable accessible globally.
    # This means that the cards-variable can be accessed from outside this function as well.
    global cards
    cards = [f for f in getFiles("./") if f[-6:] == ".cards" and f[:-6].isnumeric() == False]
    if len(cards) == 0:
        os.chdir(originPath)
        print("You have not created any flashcards. You need to create a set first before you can play.")
        input("Press enter to continue: ")
    else:
        choose = askForCards()
        while True:
            if choose.isnumeric() and 1 <= int(choose) <= len(cards):
                play = int(choose) - 1
                # break exits the loop
                break
            elif f"{choose}.cards" in cards:
                # .index returns the position (index) of the first matching item in a list
                # For example ["french", "english"].index("english") returns 1.
                play = cards.index(f"{choose}.cards")
                break
            print("Flashcard set not found.")
            choose = askForCards()
        flashcardPlay(play)


def askForCards():
    """
    Display available flashcard sets and prompt the user for selection.
    Returns:
        user's choice as string (either the set name or the corresponding number)
    """
    for i in range(len(cards)):
        print(f"{i + 1}) {cards[i][:-6]}")
    print()
    return input("Enter the name or number of the flashcard set you want to play: ")


def flashcardPlay(cardset):
    """
    Play the flashcards of the previously selected set.
    User can choose to play the flashcards in reverse or normal mode, 
    flip the cards, mark them as known/still learning, and replay the set.
    Args:
        cardset: index of the selected flashcard set in global cards list
    """
    fronts = []
    backs = []
    replay = "restart"
    with open(f"./{cards[cardset]}") as save:
        for line in save:
            # .startswith() returns True if the string before the dot starts with the string specified in the argument.
            # for example, "apple is a fruit".startswith("apple") returns True
            if line.startswith("front: "):
                # .rstrip() returns the string before the dot without trailing whitespace.
                # for example, "apple\n".rstrip() and "apple  ".rstrip() both return "apple"
                fronts.append(line[7:].rstrip())
            elif line.startswith("back: "):
                backs.append(line[6:].rstrip())
    playText = "If you want to have the answer side of the card shown first, enter \"reverse\"."
    while replay == "restart":
        clearTerminal()
        print("Control the flashcards with your arrow keys.")
        print("To flip a card, use the up and down keys.")
        print("To mark the card as known, press the right arrow. To mark it as still learning, press the left arrow.")
        print()
        print(playText)
        play = input("Otherwise, press enter to play: ")
        while play not in ("reverse", ""):
            print("Command not found.")
            print(playText)
            play = input("Otherwise, press enter to play: ")
        if play == "reverse":
            reverse = True
        else:
            reverse = False
        known = 0
        stillLearning = 0
        for i in range(len(fronts)):
            clearTerminal()
            print(f"Card {i+1} / {len(fronts)}")
            if reverse:
                flipped = True
                print(backs[i])
            else:
                flipped = False
                print(fronts[i])
            print()
            while True:
                # readchar.readkey() returns the name of the keyboard key pressed
                event = readchar.readkey()
                clearTerminal()
                print(f"Card {i+1} / {len(fronts)}")
                # readchar.key.UP means the up arrow key, readchar.key.DOWN means the down arrow
                if event in (readchar.key.UP, readchar.key.DOWN):
                    if flipped:
                        print(fronts[i])
                        flipped = False
                    else:
                        print(backs[i])
                        flipped = True
                    print()
                # readchar.key.LEFT means the left arrow key
                elif event == readchar.key.LEFT:
                    stillLearning += 1
                    isknown = False
                    break
                # readchar.key.RIGHT means the right arrow key
                elif event == readchar.key.RIGHT:
                    known += 1
                    isknown = True
                    break
            clearTerminal()
            print(f"{round((i+1)/len(fronts)*100, 2)}% done.")
            if isknown:
                print("Known")
            else:
                print("Still learning")
            print()
            print(f"{known} / {i+1} known.")
            # time.sleep() is used to pause the program for a specified amount of seconds, in this case 1.5.
            time.sleep(1.5)
        clearTerminal()
        print("Game finished.")
        print(f"Known: {known}")
        print(f"Still learning: {stillLearning}")
        print(f"You knew {round(known/len(fronts)*100, 2)}% of the flashcards.")
        print()
        replay = input("If you want to replay the flashcards, enter \"restart\". Otherwise, press enter to continue: ")
        while replay not in ("restart", ""):
            print("Command not found.")
            replay = input("If you want to replay the flashcards, enter \"restart\". Otherwise, press enter to continue: ")
    os.chdir(originPath)


askCommand()
