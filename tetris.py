# Crooy's tetris
# Oct 2020

import random
import time
import copy
import pygame
import numpy as np
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_z,
    K_x,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.display.set_caption('Crooytris')

#set frames per second for the game loop
FPS = 10
fpsclock = pygame.time.Clock()
#set block drop rate (number of frames per drop)
dropRate = 12
pygame.key.set_repeat(10000, 10000)

screenWidth = 800
screenHeight = 800
gridWidth = 8
gridHeight = 12
gridSquareSize = 50
gridWidthOffset = 0
gridHeightOffset = 0
maxGridWidthPx = gridWidth * gridSquareSize
maxGridHeightPx = gridHeight * gridSquareSize

# Set up the drawing window
screen = pygame.display.set_mode([screenWidth, screenHeight])

# SEt background colour
background = pygame.Surface(screen.get_size())
background = background.convert()   
background.fill((255,228,181))

# set game surface
gameSurface = pygame.Surface((maxGridWidthPx + 1, maxGridHeightPx + 1))
gameSurface.fill((255,255,255))
gameRect = gameSurface.get_rect()

# fonts
font = pygame.font.Font('freesansbold.ttf', 26)
fontLarge = pygame.font.Font('freesansbold.ttf', 52)

# header
header = fontLarge.render('CROOY\'S TETRIS', True, (0, 0, 0), (255, 255, 255))

# scoreboard
scoreboardText = font.render('Score', True, (0, 0, 0), (255, 255, 255))
scoreboardScore = fontLarge.render('0', True, (0, 0, 0), (255, 255, 255))

# draw grid onto surface
currentXPos = gridWidthOffset
x = 0
while x < gridWidth + 1:
    pygame.draw.line(gameSurface, (0, 0, 0), [currentXPos, gridWidthOffset], [currentXPos, maxGridHeightPx])
    currentXPos = currentXPos + gridSquareSize
    x = x + 1

currentYPos = gridHeightOffset
y = 0
while y < gridHeight + 1:
    pygame.draw.line(gameSurface, (0, 0, 0), [gridHeightOffset, currentYPos], [maxGridWidthPx, currentYPos])
    currentYPos = currentYPos + gridSquareSize
    y = y + 1


#GridSquare class
class GridSquare(pygame.sprite.Sprite):
    def __init__(self, gameSurface, xPos, yPos, size, status):
        super(GridSquare, self).__init__()
        self.surf = pygame.Surface((size - 5, size - 5))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = ((xPos*size)+(size/2), (yPos*size)+(size/2)))
        
        self.gameSurface = gameSurface
        self.xPos = xPos
        self.yPos = yPos
        self.size = size
        self.status = status
        self.colour = 'white'

    def setColour(self,colour):
        if colour == 'random':
            self.surf.fill((random.randint(30,225),random.randint(30,225),random.randint(30,225)))
            
        elif self.status == 'currentBlock':
            if colour == 'red':
                self.surf.fill((106,5,7))
            if colour == 'green':
                self.surf.fill((0, 63, 17))
            if colour == 'orange':
                self.surf.fill((233, 68, 0))
            if colour == 'blue':
                self.surf.fill((0,0,108))
            if colour == 'purple':
                self.surf.fill((60,5,74))
            if colour == 'slate':
                self.surf.fill((93,106,122))
        elif self.status == 'locked':
            if colour == 'red':
                self.surf.fill((166,65,67))
            if colour == 'green':
                self.surf.fill((40,133,57))
            if colour == 'orange':
                self.surf.fill((255,128,40))
            if colour == 'blue':
                self.surf.fill((40,40,168))
            if colour == 'purple':
                self.surf.fill((120,45,134))
            if colour == 'slate':
                self.surf.fill((153,166,182))
                
        if colour == 'white':
            self.surf.fill((255,255,255))              

    def setStatus(self,status):
        self.status = status
        if status == 'currentBlock' or status == 'locked':
            self.setColour(self.colour)

        if status == '-':
            self.surf.fill((255, 255, 255))

      
#declare a 2d array of GridSquare, size [gridWidth, gridHeight] 
gridSquareList = [[GridSquare(gameSurface, x, y, gridSquareSize, '-') for y in range(int(gridHeight))] for x in range(int(gridWidth))]

def generateTetro(gridSquareList, tetroList, xPos, yPos, shape):
    colour = 'blue'
    if shape == 'random':
        shapeId = random.randint(1,7)
        if shapeId == 1:
            shape = 'line'
            colour = 'blue'
        elif shapeId == 2:
            shape = 'square'
            colour = 'red'
        elif shapeId == 3:
            shape = 'T'
            colour = 'slate'
        elif shapeId == 4:
            shape = 'L'
            colour = 'green'
        elif shapeId == 5:
            shape = 'J'
            colour = 'orange'
        elif shapeId == 6:
            shape = 'skewright'
            colour = 'purple'
        elif shapeId == 7:
            shape = 'skewleft'
            colour = 'purple'
        
    if shape == 'line':
        print('generating line centred from ' + str(xPos) + ',' + str(yPos))
        tetroList = [ [xPos-2,yPos], [xPos-1,yPos], [xPos,yPos], [xPos+1,yPos]  ]
        currentShapeMatrix = np.array([ [0,0,0,0],
                                        [1,1,1,1],
                                        [0,0,0,0],
                                        [0,0,0,0] ])
    elif shape == 'square':
        print('generating square centred from ' + str(xPos) + ',' + str(yPos))
        tetroList = [ [xPos-1,yPos], [xPos,yPos], [xPos-1,yPos+1], [xPos,yPos+1]  ]
        currentShapeMatrix = np.array([ [1,1,0],
                                        [1,1,0],
                                        [0,0,0] ])
    elif shape == 'T':
        print('generating T centred from ' + str(xPos) + ',' + str(yPos))
        tetroList = [ [xPos,yPos], [xPos-1,yPos+1], [xPos,yPos+1], [xPos+1,yPos+1]  ]
        currentShapeMatrix = np.array([ [0,1,0],
                                        [1,1,1],
                                        [0,0,0] ])
    elif shape == 'L':
        print('generating L centred from ' + str(xPos) + ',' + str(yPos))
        tetroList = [ [xPos,yPos], [xPos,yPos+1], [xPos,yPos+2], [xPos+1,yPos+2]  ]
        currentShapeMatrix = np.array([ [0,1,0],
                                        [0,1,0],
                                        [0,1,1] ])
    elif shape == 'J':
        print('generating J centred from ' + str(xPos) + ',' + str(yPos))
        tetroList = [ [xPos,yPos], [xPos,yPos+1], [xPos,yPos+2], [xPos-1,yPos+2]  ]
        currentShapeMatrix = np.array([ [0,1,0],
                                        [0,1,0],
                                        [1,1,0] ])
    elif shape == 'skewright':
        print('generating skewright centred from ' + str(xPos) + ',' + str(yPos))
        tetroList = [ [xPos,yPos], [xPos,yPos+1], [xPos+1,yPos+1], [xPos+1,yPos+2]  ]
        currentShapeMatrix = np.array([ [0,1,0],
                                        [0,1,1],
                                        [0,0,1] ])
    elif shape == 'skewleft':
        print('generating skewleft centred from ' + str(xPos) + ',' + str(yPos))
        tetroList = [ [xPos,yPos], [xPos,yPos+1], [xPos-1,yPos+1], [xPos-1,yPos+2]  ]
        currentShapeMatrix = np.array([ [0,1,0],
                                        [1,1,0],
                                        [1,0,0] ])

    for i in range(len(tetroList)):
        currentBlockXPos = tetroList[i][0]
        currentBlockYPos = tetroList[i][1]
        gridSquareList[currentBlockXPos][currentBlockYPos].setStatus('currentBlock')
        gridSquareList[currentBlockXPos][currentBlockYPos].setColour(colour)
        
    return gridSquareList, tetroList, currentShapeMatrix, 'active', shape, colour

def rotateTetro(gridSquareList, tetroList, currentShapeMatrix, shape, direction):
    currentTetroList = copy.deepcopy(tetroList)
    newCurrentShapeMatrix = copy.deepcopy(currentShapeMatrix)
    
    if shape != 'square':
        #central pivot point of tetro?
        xPointList = []
        yPointList = []
        #get the min X and Y co-ordinates of the current tetro
        for i in range(len(currentTetroList)):
            xPointList.append(currentTetroList[i][0])
            yPointList.append(currentTetroList[i][1])

        matrixStartXPos = min(xPointList)
        matrixStartYPos = min(yPointList)      
        
        #rotate the currentShapeMatrix
        if (direction == 'clockwise'):
            newCurrentShapeMatrix = np.rot90(newCurrentShapeMatrix, k=1, axes=(0,1)).tolist()
        else:
            newCurrentShapeMatrix = np.rot90(newCurrentShapeMatrix, k=1, axes=(1,0)).tolist()
            
        print('newCurrentShapeMatrix after rotation ' + direction)
        print(newCurrentShapeMatrix)

        if shape == 'line':
            rows = 4
            cols = 4
        else:
            rows = 3
            cols = 3

        newTetroList = []
        #transpose the new currentShapeMatrix onto the gridSquareList and newTetroList
        #if we have exceeded the bounds of the game surface, return the backup versions
        isRotateInBounds = 1
        isRotationSuccesful = 1
        for i in range(0, rows):
            for j in range(0, cols):
                print('grid size is ' + str(gridWidth) + ', ' + str(gridHeight))
                print('checking1 ' + str(i) + ', ' + str(j))
                print('checking2 ' + str(matrixStartXPos + i) + ', ' + str(matrixStartYPos + j))
                if matrixStartXPos + i < gridWidth and matrixStartYPos + j < gridHeight:
                    newStatus = gridSquareList[matrixStartXPos + i][matrixStartYPos + j].status
                    print('newStatus: ' + newStatus)
                else:
                    newStatus = '-'
                    
                if newCurrentShapeMatrix[i][j] == 1:
                    print(str(i) + ', ' + str(j) + ' = 1')
                    if matrixStartXPos + i < gridWidth-1 and matrixStartYPos + j < gridHeight-1 and isRotateInBounds == 1 and newStatus != 'locked':
                        print('transposing: ' + str(matrixStartXPos + i) + ', ' + str(matrixStartYPos + j))
                        newTetroList.append([matrixStartXPos + i, matrixStartYPos + j])                                 
                    else:
                        print('out of bounds or locked - undoing')
                        newTetroList = copy.deepcopy(tetroList)
                        newCurrentShapeMatrix = copy.deepcopy(currentShapeMatrix)
                        isRotateInBounds = 0
                        isRotationSuccesful = 0
                        break
            if isRotateInBounds == 0:
                print('breaking')
                break

        #draw new shape onto grids
        if isRotationSuccesful == 1:
            #deselect old shape
            for i in range(len(tetroList)):
                
                currentBlockXPos = tetroList[i][0]
                currentBlockYPos = tetroList[i][1]
                gridSquareList[currentBlockXPos][currentBlockYPos].setStatus('-')

            #draw new shape
            for i in range(len(newTetroList)):
                print('hello ' + str(newTetroList))
                currentBlockXPos = newTetroList[i][0]
                currentBlockYPos = newTetroList[i][1]
                print('arse ' + str(currentBlockXPos) + ', ' + str(currentBlockYPos))
                gridSquareList[currentBlockXPos][currentBlockYPos].setStatus('currentBlock')
                gridSquareList[currentBlockXPos][currentBlockYPos].setColour(colour) 

    else:
        newTetroList = copy.deepcopy(tetroList)
        
    return gridSquareList, newTetroList, newCurrentShapeMatrix
    
def moveTetro(gridSquareList, tetroList, direction):
    print('status of 2,5 = ' + gridSquareList[2][5].status)
    currentTetroList = copy.deepcopy(tetroList)
    newTetroList = copy.deepcopy(tetroList)
    currentTetroStatus = 'active'
    
    print('moving shape in direction ' + direction)
    #loop through newTetroList and set new positions
    for i in range(len(newTetroList)):
        newXPos = newTetroList[i][0]
        newYPos = newTetroList[i][1]        
        if direction == 'down':
            newYPos = newYPos + 1
            #break
        if direction == 'left':
            newXPos = newXPos - 1
            #break
        if direction == 'right':
            newXPos = newXPos + 1
            #break

        newTetroList[i][0] = newXPos  
        newTetroList[i][1] = newYPos
    
    #loop through currentTetroList and deselect
    print('moving shape: deselecting old shape:')
    print(currentTetroList)
    for i in range(len(currentTetroList)):
        currentBlockXPos = currentTetroList[i][0]
        currentBlockYPos = currentTetroList[i][1]
        gridSquareList[currentBlockXPos][currentBlockYPos].setStatus('-')
        
    #check if new tetro position is in range
    isNewPositionInRange = 1
    for i in range(len(newTetroList)):
        currentBlockXPos = newTetroList[i][0]
        currentBlockYPos = newTetroList[i][1]
        if currentBlockYPos < gridHeight-1:
            print('atempting to move: ' + str(currentBlockXPos) + ', ' + str(currentBlockYPos))

            if (currentBlockXPos < 0 or currentBlockXPos > gridWidth-1):
                print('new pos will be out of bounds - ignoring')
                isNewPositionInRange = 0

    #check if new tetro pos is at the bottom or blocked - lock if it is
    isNewPositionLocked = 0
    isNewPositionLockedContinue = 0
    isNewPositionBottom = 0
    
    if isNewPositionInRange == 1:
       #is the new position locked?
        for i in range(len(newTetroList)):
            currentBlockXPos = newTetroList[i][0]
            currentBlockYPos = newTetroList[i][1]
            
            newStatus = gridSquareList[currentBlockXPos][currentBlockYPos].status
            print('status of ' + str(currentBlockXPos) + ',' + str(currentBlockYPos) + ' is ' + newStatus)
            
            if newStatus == 'locked' and direction == 'down':
                isNewPositionLocked = 1    
                print('locking shape')
                currentTetroStatus = 'locked'
                print('found a locked cell at ' + str(currentBlockXPos) + ',' + str(currentBlockYPos))
                break
            elif newStatus == 'locked' and direction != 'down':
                isNewPositionLockedContinue = 1
                print('found a locked cell at ' + str(currentBlockXPos) + ',' + str(currentBlockYPos) + ' but we can continue')
                break
            
        #are we at the bottom?
        if isNewPositionLocked == 0:
            for i in range(len(newTetroList)):
                currentBlockXPos = newTetroList[i][0]
                currentBlockYPos = newTetroList[i][1]

                if currentBlockYPos == gridHeight-1:
                    isNewPositionBottom = 1
                    currentTetroStatus = 'locked'
                    print('we are at the bottom ' + str(currentBlockYPos))

    print('isNewPositionBottom = ' + str(isNewPositionBottom) + ', isNewPositionLocked = ' + str(isNewPositionLocked) + ', isNewPositionInRange = ' + str(isNewPositionInRange) + ', isNewPositionLockedContinue = ' + str(isNewPositionLockedContinue))
    time.sleep(0.1)
    
    if isNewPositionInRange == 0 or isNewPositionLockedContinue == 1:
        #we are out of range, therefore use currentTetroList
        for i in range(len(currentTetroList)):
            currentBlockXPos = currentTetroList[i][0]
            currentBlockYPos = currentTetroList[i][1]
            gridSquareList[currentBlockXPos][currentBlockYPos].setStatus('currentBlock')
            gridSquareList[currentBlockXPos][currentBlockYPos].setColour(colour)
        currentTetroStatus = 'active'
        return gridSquareList, currentTetroList, currentTetroStatus
    
    elif isNewPositionInRange == 1 and isNewPositionBottom == 1 and isNewPositionLocked == 0:
        #we are at the bottom, therefore use newTetroList
        for i in range(len(newTetroList)):
            currentBlockXPos = newTetroList[i][0]
            currentBlockYPos = newTetroList[i][1]
            gridSquareList[currentBlockXPos][currentBlockYPos].setStatus('locked')
            gridSquareList[currentBlockXPos][currentBlockYPos].setColour(colour)
            currentTetroStatus = 'locked'
        return gridSquareList, newTetroList, currentTetroStatus
    
    elif isNewPositionInRange == 1 and isNewPositionBottom == 0 and isNewPositionLocked == 1:
        #we have hit a locked square, therefore use currentTetroList
        for i in range(len(currentTetroList)):
            currentBlockXPos = currentTetroList[i][0]
            currentBlockYPos = currentTetroList[i][1]
            if isNewPositionLocked == 1:
                gridSquareList[currentBlockXPos][currentBlockYPos].setStatus('locked')
                gridSquareList[currentBlockXPos][currentBlockYPos].setColour(colour)
                currentTetroStatus = 'locked'
        return gridSquareList, currentTetroList, currentTetroStatus
    else:
        #normal drop
        for i in range(len(newTetroList)):
            currentBlockXPos = newTetroList[i][0]
            currentBlockYPos = newTetroList[i][1]
            print('normal drop ' + str(currentBlockXPos) + ', ' + str(currentBlockYPos))
            gridSquareList[currentBlockXPos][currentBlockYPos].setStatus('currentBlock')
            gridSquareList[currentBlockXPos][currentBlockYPos].setColour(colour)
              
    return gridSquareList, newTetroList, currentTetroStatus

def check(gridSquareList,score,currentXPos,currentYPos):
    #loop through each row to check if row is completely locked = score 1 point
    
    scoreThisCheck = 0
    startRow = 0
    for j in reversed(range(gridHeight)):
        currentRowLockCount = 0
        for i in range(gridWidth):
            
            if gridSquareList[i][j].status == 'locked':
                currentRowLockCount = currentRowLockCount + 1
                    
                #if locked, increase the score and remove the row
                if currentRowLockCount == gridWidth:
                    score = score + 1
                    scoreThisCheck = scoreThisCheck  + 1
                    startRow = j
                    
                    #remove whole row
                    for x in range(gridWidth):
                        print('removing ' + str(x) + ', ' + str(j))
                        gridSquareList[x][j].setStatus('-')

    #now loop through and drop every cell above the dropped rows
    if scoreThisCheck > 0:
        for i in range(gridWidth):
            for j in reversed(range(startRow)):
                newStatus = gridSquareList[i][j].status
                if newStatus == 'locked':
                    print('dropping cell: ' + str(i) + ', ' + str(j))
                    gridSquareList[i][j].setStatus('-')
                    gridSquareList[i][j+scoreThisCheck].setStatus(newStatus)
                    gridSquareList[i][j+scoreThisCheck].setColour('random')
                                
        currentRowLockCount = 0
    #also check if we are at the bottom
    if currentYPos == gridHeight-1:
        gridSquareList[currentXPos][currentYPos].setStatus('locked')
        gridSquareList[currentBlockXPos][currentBlockYPos].setColour(colour)

    scoreboardText = font.render('Score', True, (255, 255, 255), (0, 0, 0))
    scoreboardScore = fontLarge.render(str(score), True, (255, 255, 255), (0, 0, 0))
  
    scoreboard = pygame.Surface((100,100))
    scoreboard.fill((0,0,0))
    scoreboard.blit(scoreboardText, (15,10))
    scoreboard.blit(scoreboardScore, (40,40))

    return gridSquareList, score, scoreboard
 
        
# Main loop
running = True
loopCount = 0
currentXPos = int(gridWidth/2)
currentYPos = 0
score = 0
currentTetroList = [currentXPos,currentYPos]
result = generateTetro(gridSquareList,currentTetroList,currentXPos,currentYPos,'random')
gridSquareList = result[0]
currentTetroList = result[1]
currentShapeMatrix = result[2]
currentTetroStatus = result[3]
currentShape = result[4]
colour = result[5]

while running:
    loopCount = loopCount + 1                                 
        
    # loop through the list and blit onto the gameSurface 
    for i in range(gridWidth):
        for j in range(gridHeight):
            gameSurface.blit(gridSquareList[i][j].surf, gridSquareList[i][j].rect)

    result = check(gridSquareList,score,currentXPos,currentYPos)
    gridSquareList = result[0]
    score = result[1]
    scoreboard = result[2]
    
    if currentTetroStatus == 'locked':
        result = generateTetro(gridSquareList,currentTetroList,currentXPos,currentYPos,'random')
        gridSquareList = result[0]
        currentTetroList = result[1]
        currentShapeMatrix = result[2]
        currentTetroStatus = result[3]
        currentShape = result[4]
        colour = result[5]

    screen.blit(background, ( 0, 0 ))
    screen.blit(header, ((screenWidth - gameSurface.get_width()) / 2, 10))
    screen.blit(scoreboard, (10, (screenHeight - gameSurface.get_height()) / 2))
    screen.blit(gameSurface, ( (screenWidth - gameSurface.get_width()) / 2, (screenHeight - gameSurface.get_height()) / 2) )
     
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user close the window?
        if event.type == QUIT:
            pygame.quit()
            running = False

    pressedKeys = pygame.key.get_pressed()
    
    #deselect current pos
    if pressedKeys[K_DOWN] or pressedKeys[K_LEFT] or pressedKeys[K_RIGHT]:
        #deselect
        if (pressedKeys[K_LEFT] and currentXPos > 0) or (pressedKeys[K_RIGHT] and currentXPos < gridWidth-1) or (pressedKeys[K_DOWN]):
            #loop through currentTetroList and deselect
            for i in range(len(currentTetroList)):
                currentBlockXPos = currentTetroList[i][0]
                currentBlockYPos = currentTetroList[i][1]
                print('keypress: deselecting ' + str(currentBlockXPos) + ',' + str(currentBlockYPos))
                gridSquareList[currentBlockXPos][currentBlockYPos].setStatus('-')
                break
                
        #keydown left/right/down - select new pos - do not allow diagonals
        if pressedKeys[K_DOWN] and not(pressedKeys[K_LEFT]) and not(pressedKeys[K_RIGHT]) and currentYPos < gridHeight-1:
            print('down key press')
            result = moveTetro(gridSquareList,currentTetroList,'down')
            gridSquareList = result[0]
            currentTetroList = result[1]
            currentTetroStatus = result[2]
            continue 

        if pressedKeys[K_LEFT] and not(pressedKeys[K_DOWN]) and not(pressedKeys[K_RIGHT]) and currentXPos > 0:
            print('left key press')
            result = moveTetro(gridSquareList,currentTetroList,'left')
            gridSquareList = result[0]
            currentTetroList = result[1]
            currentTetroStatus = result[2]
            continue 

        if pressedKeys[K_RIGHT] and not(pressedKeys[K_DOWN]) and not(pressedKeys[K_LEFT]) and currentXPos < gridWidth-1:
            print('right key press')
            result = moveTetro(gridSquareList,currentTetroList,'right')
            gridSquareList = result[0]
            currentTetroList = result[1]
            currentTetroStatus = result[2]
            continue

    #keydown z/x 
    if pressedKeys[K_x]:
        result = rotateTetro(gridSquareList, currentTetroList, currentShapeMatrix, currentShape, 'clockwise')
        gridSquareList = result[0]
        currentTetroList = result[1]
        currentShapeMatrix = result[2]
        print(currentTetroList)
        continue
    
    if pressedKeys[K_z]:
        result = rotateTetro(gridSquareList, currentTetroList, currentShapeMatrix, currentShape, 'anticlockwise')
        gridSquareList = result[0]
        currentTetroList = result[1]
        currentShapeMatrix = result[2]
        print(currentTetroList)
        continue
    
##    #automatically drop the current block
##    if loopCount % dropRate == 0:
##        #print('autodrop started')
##        result = moveTetro(gridSquareList,currentTetroList,'down')
##        gridSquareList = result[0]
##        currentTetroList = result[1]
##        currentTetroStatus = result[2]
##        loopCount=0
##        continue 
    
    #update display
    pygame.display.flip()
    fpsclock.tick(FPS)


    


