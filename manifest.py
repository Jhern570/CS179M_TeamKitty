container_cells = []
containers_index = []
def parseManifest(name):
    manifest_name = name
    #path = "C:\\Users\\julio\\OneDrive\\Desktop\\AI_proj\\ship_cases\\" + manifest_name
    path = name
    manifest_file = open(path, 'r')

    Lines = manifest_file.readlines()
    cells = []
    for i in Lines:
        container = []
        posx = i[1:3]
        posy = i[4:6]
        weight = i[10:15]
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
    return cells

def getCells():
    return container_cells

def appendIndex(index_selected):
    containers_index.append(index_selected)

def getIndex():
    return containers_index