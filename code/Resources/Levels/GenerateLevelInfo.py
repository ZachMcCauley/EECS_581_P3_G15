from Grid.Vector2Int import Vector2Int

# This file is used to generate information about levels. It should not be imported by any other file

def IndicateGridTiles(file):
    file.write("Positions:\n")
    for x in range(0, 7):
        for y in range(0, 7):
            pos = Vector2Int(x, y)
            if pos.x == 3 and pos.y <= 3:
                continue
            reprStr = repr(pos) + "\n"
            file.write(reprStr)

def IndicateItems(file):
    itemNames = []
    itemNames.append("piece_chat")
    itemNames.append("piece_folder")
    itemNames.append("piece_save")
    itemNames.append("piece_mail")
    itemNames.append("piece_notepad")
    values = "Items:\n" + "\n".join(itemNames)
    file.write(values)

def main():
    filename = int(input("Please enter the level number of the file: "))
    file = open("./Resources/Levels/level-" + str(filename) + ".lvl", "x")
    IndicateGridTiles(file)
    IndicateItems(file)
    file.close()

main()