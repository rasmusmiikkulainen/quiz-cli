import os
import time
# The library readchar is used to register live key inputs from the user.
import readchar
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
    # os.system allows to execute commands in the system terminal.
    # os.name returns the name of the operating system dependant module that the os library needs to function properly.
    # This library essentially decides what kind of commands in the terminal to use when, for example, using the listdir()-function.
    # In Windows, this command is "dir", but in Linux it's "ls", and python needs to know which one to use.
    # The most common os.name values are "nt", which is the Windows module, and "posix", which is used in Linux and MacOS.
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
        folders = getFolders("./")
        if "flashcards" not in folders:
            os.mkdir("./flashcards")
        os.chdir("./flashcards")
        files = getFiles("./")
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
    folders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
    return folders


def getFiles(dir):
    """
    Get a list of files in a given directory.
    Args:
        dir: path to directory
    Returns:
        list of file names as strings
    """
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return files


def flashcardChoose():
    """
    Display numbered list of available flashcards and prompt user to select one.
    Checks that the selected flashcard set exists and if so, starts the game.
    """
    if "flashcards" not in getFolders("./"):
        os.mkdir("./flashcards")    # This command creates the folder "flashcards".
    os.chdir("./flashcards")        # The following command then changes the active folder to ./flashcards.
    global cards                    # The keyword global here is used to make the cards variable accessible globally, not just inside this function.
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
                break
            elif f"{choose}.cards" in cards:
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
    choose = input("Enter the name or number of the flashcard set you want to play: ")
    return choose


def flashcardPlay(cardset):
    """
    Play the flashcards of the previously selected set.
    User can flip the cards, mark them as known/still learning, and replay the set.
    Args:
        cardset: index of the selected flashcard set in global cards list
    """
    fronts = []
    backs = []
    replay = "restart"
    with open(f"./{cards[cardset]}") as save:
        for line in save:
            if line.startswith("front: "):      # .startswith() can be used to check whether a string starts with the string inputted inside the parentheses.
                fronts.append(line[7:-2])
            elif line.startswith("back: "):
                backs.append(line[6:-2])
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
                event = readchar.readkey()      # readchar.readkey returns the name of the keyboard key pressed
                clearTerminal()
                print(f"Card {i+1} / {len(fronts)}")
                if event in (readchar.key.UP, readchar.key.DOWN):
                    if flipped:
                        print(fronts[i])
                        flipped = False
                    else:
                        print(backs[i])
                        flipped = True
                    print()
                elif event == readchar.key.LEFT:
                    stillLearning += 1
                    isknown = False
                    break
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
            print(f"Known: {known} Still learning: {stillLearning}")
            print(f"{known} / {i+1} known.")
            time.sleep(2)   # time.sleep() is used to pause the program for a specified amount of seconds, in this case 2.
        clearTerminal()
        print("Game finished.")
        print(f"Known: {known}")
        print(f"Still learning: {stillLearning}")
        print(f"You knew {round(known/len(fronts)*100, 2)}% of the flashcards.")
        print()
        replay = input("If you want to replay the flashcards, enter \"restart\". Otherwise, press enter to continue: ")
        while replay not in ["restart", ""]:
            print("Command not found.")
            replay = input("If you want to replay the flashcards, enter \"restart\". Otherwise, press enter to continue: ")
    os.chdir(originPath)


askCommand()
