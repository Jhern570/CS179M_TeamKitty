
import time
import copy
import os

class Bay:
    def __init__(self):
        self.container_cells = []
        self.containers_index = []
        self.containers_nodes = {}
        self.containers_nodes_keys = []
        self.previousNode = []
        self.currentNode = []
        self.name_new_container = ""
        self.weight_new_container = ""
        self.state = 0
        self.seconds = 0
        self.count = 0
        self.flag = 0
        self.loadFlag = 0
        self.balanceFlag = 0
        self.new_positions = {}
        self.containers_to_move = {}
        self.containers_move = []
        self.new_pos = []
        self.new_load_positions = []
        return
    def restart(self):
        self.container_cells = []
        self.containers_index = []
        self.containers_nodes = {}
        self.new_positions = {}
        self.containers_to_move = {}
        self.containers_nodes_keys = []
        self.previousNode = []
        self.currentNode = []
        self.name_new_container = ""
        self.weight_new_container = ""
        self.new_pos = []
        self.containers_move = []
        self.new_load_positions = []
        self.flag = 0
        self.loadFlag = 0
        self.balanceFlaf = 0
        self.count = 0
    def parseManifest(self,name):
        manifest_name = name
        #path = "C:\\Users\\julio\\OneDrive\\Desktop\\AI_proj\\ship_cases\\" + manifest_name
        path = name
        manifest_file = open(path, 'r')

        Lines = manifest_file.readlines()
        cells = []
        x = 1
        y = 1
        if len(Lines) == 0:
            return -1
        for i in Lines:
            container = []
            posx = i[1:3]
            try:
                w = int(posx)
            except:
                return -1
            if int(posx) > 8 or int(posx) <= 0 or int(posx) != x:
                return -1
            posy = i[4:6]
            try:
                w = int(posy)
            except:
                return -1
            if int(posy) > 12 or int(posy) <= 0 or int(posy) != y:
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
        self.container_cells = cells
        if len(self.container_cells) > 96:
            return -1
        return cells
    
    def createOutputFile(self, node, name):
        old_name = os.path.basename(name)
        new_name = old_name[:len(old_name) - len(".txt")] + "OUTBOUND.txt"
        old_path = name
        new_path = "C:\\Users\\" +  os.environ.get('USERNAME') + "\\Desktop\\" + new_name 
        
        old_path = name

        read_file = ""
        output_file = ""
        # with open(old_path, 'w') as old_file: 
        #     open(old_file, 'w').close()
        flag = 0
        try:
            new_file = open(new_path, 'w')
            flag = 1
        except FileNotFoundError: 
            new_path = ""
        try:
            if flag == 0:
                new_path = "C:\\Users\\" +  os.environ.get('USERNAME') + "\\OneDrive\\Desktop\\" + new_name
                new_file = open(new_path, 'w')
                flag = 1 
        except FileNotFoundError:
            new_path = ""
        try:
            if flag == 0:
                new_path = "C:\\Users\\" +  os.environ.get('USERNAME') + "\\OneDrive\\Desktop\\" + new_name
                new_path = open(new_path, 'w')
                flag = 1
        except:
            new_path = new_name

        for num, i in enumerate(node):
            if num == len(node) - 1:
                line = "[" + i[0] + "," + i[1] + "], {" + i[2] + "}" + ", " + i[3]
            else:
                line = "[" + i[0] + "," + i[1] + "], {" + i[2] + "}" + ", " + i[3] + "\n"
            new_file.write(line)
        # output_file.close()
        # path_dir = path[:len(path) - len(old_name)]
        # os.rename(path, path_dir + new_name)
        # print(path)
        os.remove(old_path)
        new_file.close()
        return

    def getCells(self):
        return self.container_cells

    def appendIndex(self,index_selected):
        if index_selected in self.containers_index:
            return
        self.containers_index.append(index_selected)

    def getIndex(self):
        return self.containers_index
    
    def setContainersNodes(self, nodes):
        self.containers_nodes = nodes
    
    def getContainersNodes(self):
        #container = self.container_nodes.copy()
        return self.containers_nodes
    
    def setContainersNodesKeys(self, keys):
        self.containers_nodes_keys = keys
    
    def getContainersNodesKeys(self):
        #print(len(self.containers_nodes_keys))
        return self.containers_nodes_keys
    
    def getNextContainersNodes(self):
        node = self.containers_nodes[self.containers_nodes_keys[0]]
        if len(self.containers_nodes_keys) != 1 and self.loadFlag == 0 and self.balanceFlag == 0:
            self.new_pos = self.new_positions[self.containers_nodes_keys[1]]
            self.containers_move = self.containers_to_move[self.containers_nodes_keys[1]]
        self.count += 1
        self.containers_nodes_keys.pop(0)
        return node

    def setNameNewContainer(self, name):
        self.name_new_container = name
    
    def setWeightNewContainer(self, weight):
        self.weight_new_container = weight
    
    def getNameNewContainer(self):
        return self.name_new_container
    
    def getWeightNewContainer(self):
        return self.weight_new_container
    
    def setBayState(self):
        self.state = 1
    
    def getBayState(self):
        return self.state
    
    def getPreviousNode(self):
        return self.previouNode
    
    def setPreviousNode(self, cell):
        # if len(self.containers_nodes) > 1:
        #     self.previousNode = self.containers_nodes[self.containers_nodes_keys[1]]
        self.previousNode = cell

    def setCurrentNode(self, cell):
        self.currentNode = cell

    def getCurrentNode(self):
        return self.currentNode
    
    def setTime(self):
        self.seconds = time.time()
    
    def getTime(self):
        return self.seconds

    def getCount(self):
        return self.count

    def setFlag(self, n):
        self.flag = n

    def getFlag(self):
        return self.flag
    
    def setNewPositions(self, pos):
        self.new_positions = pos
    
    def setContainersToMove(self, containers):
        self.containers_to_move = containers
    
    def getNewPositions(self):
        return self.new_pos
    
    def setNewLoadPositions(self, pos):
        self.new_load_positions = pos
    
    def getNewLoadPositions(self):
        new_pos = self.new_load_positions[0]
        self.new_load_positions.pop(0)
        return new_pos
    
    def getContainersToMove(self):
        return self.containers_move
    
    def setLoadFlag(self, b):
        self.loadFlag = b

    def getLoadFlag(self):
        return self.loadFlag
    
    def setBalanceFlag(self, b):
        self.balanceFlag = b
    def getBalanceFlag(self):
        return self.balanceFlag