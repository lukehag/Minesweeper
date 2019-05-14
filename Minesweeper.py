# Minesweeper

import random, sys, csv, ast

# Display board
def display(x, y, tiles):
    xPos = []
    yPos = []
    print(end="    ")
    
    for i in range(1, x+1):
        if i < 27:
            letter = chr(i + 64)
            xPos.append(letter)
        else:
            letter = chr(i + 70)
            xPos.append(letter)
    print(*xPos, sep="   ")
    print("  ", end="")
    print('-' * (x*4+1))
    
    for i in range(1, y+1):
        if i > 9:
            print(i, end="")
        else:
            print(i, end=" ")
        for j in range(1, x+1):
            print("|", end=" ")
            print(tiles[i-1][j-1], end=" ")
            if j == x:
                print("|")
                print("  ", end="")
                print('-' * (x*4+1))        

# Create a new board
def newBoard():
    # Determine X values
    while True:
        try:
            print("Must be between 10 and 45 tiles")
            inputX = input("X axis >> ")
            sizeX = int(inputX)

            if sizeX >= 10 and sizeX <= 45:
                print(end='\n')
                break

            print("Error: Invalid size")
            print(end='\n')
            
        except(ValueError):
            print("Error: Invalid input")
            print(end='\n')

    # Determine Y values
    while True:
        try:
            print("Must be between 10 and 45 tiles")
            inputY = input("Y axis >> ")
            sizeY = int(inputY)

            if sizeY >= 10 and sizeY <= 45:
                print(end='\n')
                break

            print("Error: Invalid size")
            print(end='\n')
            
        except(ValueError):
            print("Error: Invalid input", end='\n\n')

    # Determine difficulty
    while True:
        print("A: Easy")
        print("B: Medium")
        print("C: Hard")

        diff = input("Difficulty >> ")

        if diff == 'a' or diff == 'A' or diff == 'b' or diff == 'B' or diff == 'c' or diff == 'C':
            if diff == 'a' or diff == 'A':
                diff = 1
            elif diff == 'b' or diff == 'B':
                diff = 2
            elif diff == 'c' or diff == 'C':
                diff = 3
            break

        print("Error: Invalid input", end='\n\n')

    # Set up tiles
    tiles = []
    mines = []
    values = []
    for i in range(sizeY):
        newT = []
        newM = []
        newV = []
        for j in range(sizeX):
            newT.append('-')
            newM.append(False)
            newV.append(0)
        tiles.append(newT)
        mines.append(newM)
        values.append(newV)
        
    # Set up mines
    random.seed()
    for i in range(sizeY):
        for j in range(sizeX):
            if diff == 1:
                randValue = random.randint(1,9)
                if randValue == 1:
                    mines[i][j] = True
                    
            elif diff == 2:
                randValue = random.randint(1,6)
                if randValue == 1:
                    mines[i][j] = True
                    
            elif diff == 3:
                randValue = random.randint(1,3)
                if randValue == 1:
                    mines[i][j] = True
                    
    # Set up tile values
    for i in range(sizeY):
        for j in range(sizeX):
            if mines[i][j]:
                values[i][j] = 9

                if j > 0: # West
                    values[i][j-1] += 1
                if j < len(mines[i]) - 1: # East
                    values[i][j+1] += 1
                if i < len(mines) - 1: # South
                    values[i+1][j] += 1
                if i > 0: # North
                    values[i-1][j] += 1
                if j > 0 and i < len(mines)-1: # South-West
                    values[i+1][j-1] += 1
                if j > 0 and i > 0: # North-West
                    values[i-1][j-1] += 1
                if j < len(mines[i]) - 1 and i < len(mines) - 1: # South-East
                    values[i+1][j+1] += 1
                if j < len(mines[i]) - 1 and i > 0: # North-East
                    values[i-1][j+1] += 1  

    data = [tiles, values, sizeX, sizeY]
    return data

# Prompt and check user input 
def prompt(sizeX, sizeY, tiles, values):
    flag = '' # Initialize flag

    # Prompt for input
    while True:
        print(end='\n')
        display(sizeX, sizeY, tiles)
        print("A: Open  B: Flag  C: Save & Quit  D: Quit")
        option = input(">> ")

        if option == 'a' or option == 'A' or option == 'b' or option == 'B' or option == 'c' or option == 'C' or option == 'd' or option == 'D':
            break

        print("Error: Invalid input")

    # Flagging a tile
    if option == 'b' or option == 'B':
        while True:
            print("a: Flag  b: Unflag")
            choice = input(">> ")

            if choice == 'a' or choice == 'A':
                flag = 'P'
                break
            elif choice == 'b' or choice == 'B':
                flag = '-'
                break

            print("Error: Invalid input")
            
        option = 'A' # Determine flag and move on to option A

    # Opening a tile
    if option == 'a' or option == 'A':
        while True:
            choice = input("Choose a tile >> ")
            
            if len(choice) > 3 or len(choice) < 2:
                print("Error: Input must be either 2 or 3 characters")
                continue

            char = choice[0]
            
            if char.isalpha():
                if char.islower() and ord(char) - 70 > sizeX:
                    print("Error: Tile does not exist (X)")
                    continue
                elif char.isupper() and ord(char) - 64 > sizeX:
                    print("Error: Tile does not exist (X)")
                    continue

            if char.isdigit():
                print("Error: Invalid input")
                continue

            char = ord(char)
            
            if len(choice) == 2:
                num = int(choice[1])
            else:
                num = int(choice[1] + choice[2])

            if num > sizeY:
                print("Error: Tile does not exist (Y)")
                continue

            # Translate input into index of position
            if (char >= 65 and char <= 90):
                char = char - 65
            elif (char >= 97 and char <= 122):
                char = char - 71
            num = num - 1
                
            coord = [char, num, flag]
            return coord

    # Saving and quitting
    if option == 'c' or option == 'C':
        
        # Put data into text file
        with open('savegame.csv', 'w') as save:
            saveData = csv.writer(save, delimiter = '|')
            saveData.writerow(tiles)
            saveData.writerow(values)

        print(end='\n')
        print("Saved")

        sys.exit()

    # Quit
    if option == 'd' or option == 'D':
        print(end='\n')
        print("Goodbye")
        sys.exit()
        
# Reveal what is under a tile
def reveal(x, y, tiles, values):
    if tiles[y][x] == '-':
        if values[y][x] < 9 and values[y][x] > 0:
            tiles[y][x] = values[y][x]

        # Revealing a landmine    
        elif values[y][x] >= 9:
            for i in range(len(tiles)):
                for j in range(len(tiles[0])):
                    if values[i][j] >= 9:
                        tiles[i][j] = 'X'
                    elif values[i][j] == 0:
                        tiles[i][j] = ' '
                    else:
                        tiles[i][j] = values[i][j]
                    
            print(end='\n')
            display(sizeX, sizeY, tiles)
        
            print(end='\n')
            print("You lost!")

            input("Press Enter to quit")
            sys.exit()
            
        else:
            tiles[y][x] = ' '
            
            if x > 0: # West
                reveal(x-1, y, tiles, values)
            if x < len(tiles[x]) - 1: # East
                reveal(x+1, y, tiles, values)
            if y < len(tiles) - 1: # South
                reveal(x, y+1, tiles, values)
            if y > 0: # North
                reveal(x, y-1, tiles, values)
            if x > 0 and y < len(tiles)-1: # South-West
                reveal(x-1, y+1, tiles, values)
            if x > 0 and y > 0: # North-West
                reveal(x-1, y-1, tiles, values)
            if x < len(tiles[x]) - 1 and y < len(tiles) - 1: # South-East
                reveal(x+1, y+1, tiles, values)
            if x < len(tiles[x]) - 1 and y > 0: # North-East
                reveal(x+1, y-1, tiles, values)                

    return tiles

# Check if game has been solved
def checkWin(sizeX, sizeY, tiles):
    covered = False # Initialize covered
    
    for i in range(sizeY):
        for j in range(sizeX):
            if tiles[i][j] == '-':
                covered = True
                
    if not covered:
        print(end='\n')
        display(sizeX, sizeY, tiles)
        
        print(end='\n')
        print("You win!")

        input("Press Enter to quit")
        sys.exit()

# Start game
while True:
    print("       Minesweeper       ")
    print("-------------------------")
    print("A: New game  B: Load save")

    option = input(">> ")

    if option == 'a' or option == 'A' or option == 'b' or option == 'B':
        print(end='\n')
        break

    print("Error: Invalid input")

# Unpack data from new board
if option == 'a' or option == 'A':
    data = newBoard()
    tiles = data[0]
    values = data[1]
    sizeX = data[2]
    sizeY = data[3]

# Unpack data from save file
if option == 'b' or option == 'B':
    with open('savegame.csv', 'r') as save:
        reader = csv.reader(save, delimiter = '|')
        
        count = 0 # Used for indexing
        for rList in reader:
            string = str(rList)
            
            if count == 0:
                tiles = []
                tempTiles = ast.literal_eval(string)
                for i in tempTiles:
                    temp = str(i)
                    row = ast.literal_eval(temp)
                    tiles.append(row)
                    
            elif count == 2:
                values = []
                tempValues = ast.literal_eval(string)
                for i in tempValues:
                    temp = str(i)
                    row = ast.literal_eval(temp)
                    values.append(row)
                
            count += 1
        
        sizeX = len(tiles[0])
        sizeY = len(tiles)

# Playing the game
while True:
    checkWin(sizeX, sizeY, tiles)
    choice = prompt(sizeX, sizeY, tiles, values)
    char = choice[0]
    num = choice[1]
    flag = choice[2]

    if tiles[num][char] == '-' or tiles[num][char] == 'P': # Only interact with covered or flagged
        if flag == 'P' or flag == '-':
            tiles[num][char] = flag
        else:
            tiles = reveal(char, num, tiles, values)

