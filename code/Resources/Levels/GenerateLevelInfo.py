from Grid.Vector2Int import Vector2Int
import os

# This file is used to generate information about levels. It should not be imported by any other file

def IndicateGridTiles(file):
    file.write("Positions:\n")
    for x in range(0, 11):
        for y in range(0, 11):
            pos = Vector2Int(x, y)
            if pos.ManhattanDistance(Vector2Int(5, 5)) > 5:
                continue
            reprStr = repr(pos) + "\n"
            file.write(reprStr)

def IndicateItems(file):
    itemNames = []
    for filename in os.listdir("./Resources/Items/"):
        preDot = filename.split(".")[0]
        itemNames.append(preDot)
    values = "Items:\n" + "\n".join(itemNames)
    file.write(values)

def main():
    filename = int(input("Please enter the level number of the file: "))
    file = open("./Resources/Levels/level-" + str(filename) + ".lvl", "x")
    IndicateGridTiles(file)
    IndicateItems(file)
    file.close()

main()