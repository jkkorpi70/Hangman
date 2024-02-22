
import pygame
import sys
import random
import os

# Change directory to .py dir
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print(os.getcwd())

pygame.init()
random.seed()
clock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode([690, 670])
pygame.display.set_caption('Hangman')

xx = 0 # for mouse
yy = 0
# Default word list
wordsList = ["apple","byretto","celcius","delirium","elephant","fox","grammatic","house","currency","jolly","kaleidoscope","lime"]
try:
    myfile = open("hangman_words.txt", "r") # Try open high scores file
    for i in myfile:
        list = i.strip()
        wordsList.append(list)
    myfile.close                       
except IOError:
    print("Word list not found.\nUsing default word list")

skyImage = [] 
skyImage.append(pygame.image.load("Sky1.jpg").convert())
skyImage.append(pygame.image.load("Sky2.jpg").convert())
skyImage.append(pygame.image.load("Sky3.jpg").convert())
skyImage.append(pygame.image.load("Sky4.jpg").convert())
skyImage.append(pygame.image.load("Sky5.jpg").convert())
skyImage.append(pygame.image.load("Sky6.jpg").convert())
skyImage.append(pygame.image.load("Sky7.jpg").convert())
skyImage.append(pygame.image.load("Sky8.jpg").convert())
skyImage.append(pygame.image.load("Sky9.jpg").convert())

backgroundImage  = pygame.image.load("HangmanBG.png").convert_alpha()

hang1 = pygame.image.load("hang1.png").convert_alpha()
hang2 = pygame.image.load("hang2.png").convert_alpha()
hang3 = pygame.image.load("hang3.png").convert_alpha()
hang4 = pygame.image.load("hang4.png").convert_alpha()
hang5 = pygame.image.load("hang5.png").convert_alpha()
hang6 = pygame.image.load("hang6.png").convert_alpha()

font = pygame.font.SysFont('courier', 32,True)
font2 = pygame.font.SysFont('courier', 24,True)
font3 = pygame.font.SysFont('courier', 16,True)

newGame = True
skyIndex = 0

# Read keyboard and mouse
# Returns 0 if no key pressed and 1 in mouse button
# If key is pressed returns ascii code of key
def eventHandler():
    global xx, yy
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN: 
                return event.key
        # Check if mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            xx,yy=pygame.mouse.get_pos() # Used to see coordinates
            return 1
    return 0
#========================================================================

def addLetterList(keychr):
    global usedLetters, letterList
    keycharacter = chr(keychr) # convert keycode into character
    for i in letterList:
        if i == keycharacter:
            return False
    usedLetters = ""
    letterList.append(keycharacter)
    letterList.sort()
    for i in letterList:
        usedLetters += i
    return True

def checkWord(letter):
    global wordAsList, hiddenAsList
    letterFound = False # Return False if given letter is not found in the word
    for i in range(0, len(wordAsList)):
        if wordAsList[i] == chr(letter):
            hiddenAsList[i] = chr(letter)
            letterFound = True # Letter is in the word
    return letterFound

def updateWord():
    global hiddenWord
    hiddenWord = ""
    win = True
    for i in hiddenAsList: # Change list to string, which is shown in game
        hiddenWord += i
    for j in hiddenAsList:
        if j == "*": # check if word still incomplete
            win = False
    return win

def selectDifficulty():
    global askDifficulty, xx, yy
    askDifficulty = False
    easyText = font2.render('EASY', True, (200,200,200))
    normalText = font2.render('NORMAL', True, (200,200,200))
    hardText = font2.render('HARD', True, (200,200,200))
    pygame.draw.rect(screen,(200,200,200),pygame.Rect(400, 410, 70, 40),2)
    pygame.draw.rect(screen,(200,200,200),pygame.Rect(480, 410, 100, 40),2)
    pygame.draw.rect(screen,(200,200,200),pygame.Rect(590, 410, 70, 40),2)
    screen.blit(easyText, (407, 417))
    screen.blit(normalText, (488, 417))
    screen.blit(hardText, (597, 417))
    levelText = font2.render('Choose difficulty', True, (200,200,200))
    screen.blit(levelText, (410, 470))
    pygame.display.update()
    while True:
        if eventHandler() == 1:
            if yy >= 410 and yy <= 450:
                if xx >= 400 and xx <= 470: # Easy
                    return 1
                elif xx >= 480 and xx <= 580: # Normal
                    return 2
                elif xx >= 590 and xx <= 660: # Hard
                    return 3

def setDifficultyLevel(level):
    if level == 1: # Easy level
        checkWord(ord(wordAsList[len(wordAsList)-1])) # Reveal last letter and all its kind
        updateWord()
        addLetterList(ord(wordAsList[len(wordAsList)-1])) # Add letter to used list
    if level < 3: # Easy and normal level
        checkWord(ord(wordAsList[0])) # Reveal first letter and all its kind
        updateWord()
        addLetterList(ord(wordAsList[0])) # Add letter to used list

def gameOver():
    global newGame, gameEnd, skyIndex
    skyIndex += 1
    if skyIndex > 8: skyIndex = 0
    while True:
        if eventHandler() == 1: # Mouse button
            newGame = True  # New game available here
            gameEnd = False # and here
            break

#====================================================================
# MAIN LOOP
#====================================================================   
while True:
    if newGame == True: # Initialize new game
        wordAsList = []
        hiddenAsList = []
        errors = 0
        randomNumber = random.randint(0,len(wordsList)-1)
        wordAsList[:0] = wordsList[randomNumber]
        hiddenWord = ""
        for i in wordAsList:
            hiddenWord += "*"
        hiddenAsList[:0] = hiddenWord
        wordLenght = len(wordAsList)
        usedLetters = ""
        letterList = []
        letterXPos = 390
        gameWon = False
        newGame = False
        gameEnd = False
        textColor = (200,200,200)
        askDifficulty = True # First ask difficulty level
        difficultyLevel = 0

    if gameEnd == True:
        gameOver()
    
    # Set the background image
    screen.blit(skyImage[skyIndex], (0, 0))
    screen.blit(backgroundImage, (0, 0))

    # Read inputs = keyboard and mouse
    if askDifficulty == False:
        keys = eventHandler()
        if keys > 64 and keys < 91: # If capital letter - change to lower case
            keys += 32
        if keys > 96 and keys < 123: # It's a letter a-z
            if addLetterList(keys):
                if checkWord(keys):
                    gameWon = updateWord()
                else:
                    errors += 1 # wrong letter
  
    # Draw gallow and hanging man
    if errors >= 1: screen.blit(hang1, (65, 80))
    if errors >= 2: screen.blit(hang2, (119, 90)) 
    if errors >= 3: screen.blit(hang3, (215, 140))
    if errors >= 4: screen.blit(hang4, (220, 232))
    if errors >= 5: screen.blit(hang5, (183, 252))
    if errors >= 6: screen.blit(hang6, (182, 365))

    if gameWon == True:
        textWon = font.render('You won!', True, (50,200,50))
        screen.blit(textWon, (450, 460))
        textColor = (50,200,50)
        gameEnd = True
    if errors >= 6:
        textLost = font.render('You lost!', True, (200,50,50))
        screen.blit(textLost, (450, 460))
        gameEnd = True
        textColor = (200,50,50)
        hiddenWord = ""
        for i in wordAsList:
            hiddenWord += i
    
    if len(usedLetters)>14: letterXPos = 320
    lettersText = font.render(usedLetters.upper(), True, (20,20,20))
    screen.blit(lettersText, (letterXPos, 270))
    # Print word of screen
    text = font.render(hiddenWord.upper(), True, textColor)
    screen.blit(text, (410, 360))

    if gameEnd:
        lettersText = font.render('CLICK MOUSE BUTTON', True, (20,20,20))
        screen.blit(lettersText, (320, 190))
        lettersText = font.render('CLICK MOUSE BUTTON', True, (200,200,200))
        screen.blit(lettersText, (322, 192))
    
    if difficultyLevel == 1:
        easyText = font2.render('EASY', True, (200,200,200))
        pygame.draw.rect(screen,(200,200,200),pygame.Rect(400, 410, 70, 40),2)
        screen.blit(easyText, (407, 417))
    if difficultyLevel == 2:
        normalText = font2.render('NORMAL', True, (200,200,200))
        pygame.draw.rect(screen,(200,200,200),pygame.Rect(480, 410, 100, 40),2)
        screen.blit(normalText, (488, 417))
    if difficultyLevel == 3:
        hardText = font2.render('HARD', True, (200,200,200))
        pygame.draw.rect(screen,(200,200,200),pygame.Rect(590, 410, 70, 40),2)
        screen.blit(hardText, (597, 417))

    pygame.display.set_caption(str(xx)+ ", " + str(yy))
    pygame.display.flip()
    
    if askDifficulty == True:
        difficultyLevel = selectDifficulty()
        setDifficultyLevel(difficultyLevel)

    clock.tick(30)  # 30 frames per second
