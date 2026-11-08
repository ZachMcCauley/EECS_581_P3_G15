def SelectedTile():  #insertParams
    #fill in user input
    #return True if selected 
    return True 

def ValidCheck(Tile1, Tile2): #check if swap is valid 
    if Tile1.IsAdjacentTo(Tile2):
        TileSwap(Tile1, Tile2)
        return True
    else: #play incorrect annimation 
        #animation call here
        return False 


def TileSwap(Tile1, Tile2):
    Tile1.item, Tile2.item = Tile2.item, Tile1.item
    return True
    
