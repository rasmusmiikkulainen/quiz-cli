import os
import time
import readchar
allowed_commands = ("create", "play", "quit")


def askCommand():
    commandText = "create, play or quit: "
    command = ""
    clearTerminal()
    print("Welcome to cli-quiz!")
    while command != "quit":
        print("Select command.")
        command = input(commandText)
        while command not in allowed_commands:
            print("command not found")
            command = input(commandText)
        clearTerminal()
        if command == "create":
            flashcardCreate()
        elif command == "play":
            flashcardChoose()
        clearTerminal()
    clearTerminal()


def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")


def flashcardCreate():
    cardNum = 1
    fronts = []
    backs = []
    print("Welcome to the flashcard creator!")
    print("When you are ready, enter \"/done\" when the program asks for the next flashcard.")
    print()
    front = input(f"card {cardNum} front: ")
    while front != "/done":
        fronts.append(front)
        back = input(f"card {cardNum} back: ")
        backs.append(back)
        cardNum += 1
        print()
        front = input(f"card {cardNum} front: ")
    if len(fronts) != 0:
        setName = input("Enter a name for your flashcard set: ")
        originPath = os.path.abspath("./")
        getFolders("./")
        if "flashcards" not in folders:
            os.mkdir("./flashcards")
            print("flashcards folder not found, folder created")
        os.chdir("./flashcards")
        getFiles("./")
        while f"{setName}.cards" in files or setName.isnumeric():
            if f"{setName}.cards" in files:
                print(f"You already have a set named {setName}.")
            elif setName.isnumeric():
                print("Your set name can't be an integer.")
            setName = input("Enter another name: ")
        with open(f"{setName}.cards", "a") as file:
            for i in range(len(fronts)):
                file.write(f"{fronts[i]} / {backs[i]}\n")
            file.close()
        clearTerminal()
        print("Here is a list of your flashcards:")
        for i in range(len(fronts)):
            print()
            print(f"Flashcard {i+1}:")
            print(f"Front: {fronts[i]}")
            print(f"Back: {backs[i]}")
        os.chdir(originPath)


def getFolders(dir):
    global folders
    folders = [f for f in os.listdir(dir) if os.path.isdir("/".join((dir, f)))]


def getFiles(dir):
    global files
    files = [f for f in os.listdir(dir) if os.path.isfile("/".join((dir, f)))]


def flashcardChoose():
    global originPath
    originPath = os.path.abspath("./")
    getFolders("./")
    if "flashcards" not in folders:
        print("flashcards folder not found.")
        os.mkdir("./flashcards")
        print("Folder created.")
    os.chdir("./flashcards")
    getFiles("./")
    global cards
    cards = [f for f in files if f[-6:] == ".cards" and os.path.isfile("/".join(("./", f))) and f[:-6].isnumeric() == False]
    if len(cards) == 0:
        print("You have not created any flashcards. You need to create a set first before you can play.")
        print("Returning to menu in 3 seconds.")
        time.sleep(3)
    else:
        askForCards()
        valids = [i for i in cards if i[:-6] == choose]
        while True:
            if choose.isnumeric():
                if int(choose) in range(1, len(cards) + 1):
                    play = int(choose) - 1
                    break
            elif len(valids) > 0:
                for i in range(len(cards)):
                    if f"{choose}.cards" == cards[i]:
                        play = i
                        break
                break
            print("Flashcard set not found.")
            askForCards()
        flashcardPlay(play)


def askForCards():
    for i in range(len(cards)):
        print(f"{i + 1}) {cards[i][:-6]}")
    print()
    global choose
    choose = input(
        "Enter the name or number of the flashcard set you want to play: ")


def flashcardPlay(set):
    fronts = []
    with open(f"./{cards[set]}") as save:
        for line in save:
            fronts.append(tuple(line.strip().split(" / ")))
        save.close()
    clearTerminal()
    print("Control the game with your arrow keys.")
    print("To flip a card, use the up and down keys.")
    print("To mark the card as known, press the right arrow. To mark it as still learning, press the left arrow.")
    print()
    input("Press enter when you are ready to play: ")
    known = 0
    stillLearning = 0
    for i in range(len(fronts)):
        clearTerminal()
        print(f"{i+1} / {len(fronts)}")
        print(fronts[i][0])
        print()
        flipped = False
        while True:
            event = readchar.readkey()
            clearTerminal()
            print(f"{i+1} / {len(fronts)}")
            if event in (readchar.key.UP, readchar.key.DOWN):
                if flipped:
                    print(fronts[i][1])
                    flipped = False
                else:
                    print(fronts[i][0])
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
        if isknown:
            print("Known")
        else:
            print("Still learning")
        print()
        print(f"Known: {known} Still learning: {stillLearning}")
        print(f"{known} / {i+1} known.")
        time.sleep(2)
    os.chdir(originPath)
    clearTerminal()
    print("Game finished.")
    print(f"Known: {known}")
    print(f"Still learning: {stillLearning}")
    print(f"You know {round(known/len(fronts)*100, 2)}% of the flashcards.")
    input("Press enter to continue: ")


askCommand()
