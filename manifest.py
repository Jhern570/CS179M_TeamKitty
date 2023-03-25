container_cells = []
containers_index = []
def parseManifest(name):
    manifest_name = name
    #path = "C:\\Users\\julio\\OneDrive\\Desktop\\AI_proj\\ship_cases\\" + manifest_name
    path = name
    manifest_file = open(path, 'r')

    Lines = manifest_file.readlines()
    cells = []
    x = 1
    y = 1
    print("FROM MANIFEST")
    for i in Lines:
        container = []
        posx = i[1:3]
        if int(posx) >= 8 or int(posx) <= 0 or int(posx) != x:
            return -1
        posy = i[4:6]
        print(posy)
        if int(posy) >= 12 or int(posy) <= 0 or int(posy) != y:
            print("ERROR")
            return -1
        y+= 1
        if y == 13:
            x += 1
            y = 1
        weight = i[10:15]
        try:
            w = int(weight)
        except:
            return -1
        
        if int(posx)*int(posy) == len(Lines):
            descrip = i[18:]
        else:
            descrip = i[18:-1]
        container.append(posx)
        container.append(posy)
        container.append(weight)
        container.append(descrip)
        cells.append(container)
    container_cells = cells
    if len(container_cells) > 96:
        return -1
    return cells

def getCells():
    return container_cells

def appendIndex(index_selected):
    containers_index.append(index_selected)

def getIndex():
    return containers_index

def createOutputFile(name):
    path = name
    return