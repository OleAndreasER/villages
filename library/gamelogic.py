from library.tiles import tiles
from library.buildings import House, SawMill

#Selected tile's index
selected = None
turn = 1

def getTurn():
    return turn

def getSelected():
    return selected

def selectTile(x, y):
    global selected
    selected = (x, y) 

def isCitizenSelected():
    if selected == None: return False
    if not tiles[selected[1]][selected[0]].containsCitizen(): return False
    return True

def availableTiles(x, y):
    return [(x + offsetX, y + offsetY)
           for offsetX, offsetY in [(-1, 0), (1,0), ((y%2),1), ((y%2)-1, 1), ((y%2),-1), ((y%2)-1, -1)]
           if tiles[y + offsetY][x + offsetX].totalTileCost() != None]

def moveCitizen(x, y, toX, toY):
    selectedTile = tiles[y][x]

    citizen = selectedTile.getCitizenInTile()
    
    if citizen == None: return
    if citizen.movementPoints == 0: return
    if not (toX, toY) in availableTiles(x, y): return

    selectedTile.popCitizenInTile()

    citizen.useMovementPoints(tiles[toY][toX].totalTileCost())

    tiles[toY][toX].tileTypes.append(citizen)

    selectTile(toX, toY)

def nextSelection():
    return None if len(actionQueue()) == 0 else actionQueue()[0]

def actionButton():
    if len(actionQueue()) == 0:
        endTurn()
    else:
        selectTile(*actionQueue()[0])

def idle():
    global selected
    if not isCitizenSelected(): return
    citizen = tiles[selected[1]][selected[0]].getCitizenInTile()
    citizen.isIdle = True
    selected = nextSelection()

def endTurn():
    global turn
    turn += 1
    for row in tiles:
        for tile in row:
            tile.endTurn()

def actionQueue():
    return [(x,y)
            for x in range(len(tiles[0]))
            for y in range(len(tiles))
            if tiles[y][x].containsCitizen()
            if tiles[y][x].getCitizenInTile().isInQueue()]

def selectedCitizenAction():
    global selected
    if not isCitizenSelected(): return
    tile = tiles[selected[1]][selected[0]]
    if (not tile.containsCitizen()
        or not tile.containsNonCitizen()
        or tile.getCitizenInTile().movementPoints == 0):
        return
    if (tile.getNonCitizen().actionText == None): return

    citizenAction(tile.getCitizenInTile(), tile)
    selected = nextSelection()

def citizenAction(citizen, tile):
    citizen.latestAction = {"action": citizenAction, "args": (citizen, tile)}
    citizen.actOnTile(tile.getNonCitizen())

def lockAction():
    if not isCitizenSelected(): return
    citizen = tiles[selected[1]][selected[0]].getCitizenInTile()
    citizen.toggleLock()

def removeFromTiles(targetTileType):
    for row in tiles:
        for tile in row:
            tile.tileTypes = [tileType
                              for tileType in tile.tileTypes
                              if not tileType is targetTileType]

def tileContainingTileType(targetTileType):
    for row in tiles:
        for tile in row:
            if any(tileType is targetTileType for tileType in tile.tileTypes):
                return tile
    return None

techToBuilding = {
    "house": House,
    "sawMill": SawMill
}

def knownBuildings(citizen):
    return [techToBuilding[tech]
            for tech in citizen.knownTechnologies
            if tech in techToBuilding.keys()]

def spawnCitizen(house):
    tileContainingTileType(house).spawnCitizen()

