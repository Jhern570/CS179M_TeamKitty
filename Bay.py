import logging
class Bay:
    def __init__(self):
        self.container_cells = []
        self.containers_index = []
        self.containers_nodes = {}
        self.containers_nodes_keys = []
        
        self.name_new_container = ""
        self.weight_new_container = ""
        self.state = 0
        return
    def restart(self):
        self.container_cells = []
        self.containers_index = []
        self.containers_nodes = {}
        self.containers_nodes_keys = []
        
        self.name_new_container = ""
        self.weight_new_container = ""
    def parseManifest(self,name):
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
        self.container_cells = cells
        return cells

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
