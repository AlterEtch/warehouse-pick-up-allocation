from random import randint

def generateRandomPosition(world):
    pos = [randint(1, world.width/world.gridSize-2),randint(1, world.height/world.gridSize-2)]
    if world.isBlocked(pos):
        return generateRandomPosition(world)
    return pos
