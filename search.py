import copy

def calculate_md_out(x, y):
    return abs(x - 1) + abs(y - 9)

def calculate_md_move(x, y, a, b):
    return abs(x -a) + abs(y - b)


def extend_nodes(parent_node, containers_selected, containers_left, total_time):
    new_nodes = []
    temp_new_nodes = []
    distances_ = []
    flag = 0
    containers_ = containers_selected.copy()
    count = 0
    unsused_flag = 0;
    print(containers_selected)
    for i in containers_selected:
        for check in i:
            print(check)
        if flag == 1:
            return new_nodes, containers_selected, containers_left, total_time
        for j in range(7,-1,-1):
            if parent_node[12 * j + (int(i[1]) - 1)][3] == "UNUSED" or parent_node[12 * j + (int(i[1]) - 1)][3] == "NAN":
                continue
            elif parent_node[12 * j + (int(i[1]) - 1)][3] == i[3]:
                manhattan_dist = calculate_md_out((int(i[0]) - 1), (int(i[1]) - 1))
                total_time += manhattan_dist
                containers_left -= 1
                new_node = copy.deepcopy(parent_node)
                new_node[12 * j + (int(i[1]) - 1)][3] = "UNUSED"
                new_nodes.clear()
                new_nodes.append(new_node)
                containers_.pop(count)
                flag = 1
                break # NEED TO FIGURE OUT HOW TO BREAK OUTTER LOOP AS WELL
            else:
                min_dist = 0
                new_start_position = j + 1
                additional_spaces = 0
                columns_used = []
                flag = 0
                for col in range(int(i[1]) - 2, -1, -1 ):
                    for row in range(0,8):
                        if parent_node[12 * row + col][3] == "UNUSED":
                            node_ = copy.deepcopy(parent_node)
                            manhattan_dist = calculate_md_move(row+1, col+1, new_start_position, int(i[1])) + additional_spaces
                            #distances_.append(manhattan_dist)
                            if min_dist == 0 or min_dist > manhattan_dist:
                                print("MANHATTHAN DISTANCE LEFT: " + str(manhattan_dist) + " row: " + str(row) + " col: " + str(col) )
                                new_nodes.clear()
                                min_dist = manhattan_dist
                                node_[12 * row + col][3] = node_[12 * j + (int(i[1]) - 1)][3]
                                node_[12 * j + (int(i[1]) -1)][3] = "UNUSED"
                                new_nodes.append(node_)
                                flag = 1
                                break
                    if flag == 1:
                        flag = 0;
                        break
                    if row == 7:
                         new_start_position = 9 
                         additional_spaces = 9 - int(i[0])
                new_start_position = j  + 1
                addtional_spaces = 0
                for col in range(int(i[1]), 12):
                    for row in range(0,8):
                        if parent_node[12 * row + col][3] == "UNUSED":
                            if unsused_flag == 1:
                                flag = 1
                                break
                            unsused_flag = 1
                            node_ = copy.deepcopy(parent_node)
                            manhattan_dist = calculate_md_move(row+1, col+1, new_start_position, int(i[1])) + additional_spaces
                            #distances_.append(manhattan_dist)
                            if min_dist == 0 or min_dist >= manhattan_dist:
                                print("MANHATTHAN DISTANCE Right: " + str(manhattan_dist) + " row: " + str(row) + " col: " + str(col))
                                new_nodes.clear()
                                min_dist = manhattan_dist
                                node_[12 * row + col][3] = node_[12 * j + (int(i[1]) - 1)][3]
                                node_[12 * j + (int(i[1]) -1)][3] = "UNUSED"
                                new_nodes.append(node_)
                                flag = 1
                                break
                    if flag == 1:
                        flag = 0
                        break
                    if row == 7:
                         new_start_position = 9 
                         additional_spaces = 9 - int(i[0])
                count += 1
                break
    return new_nodes, containers_, containers_left, total_time
          

def search(cells, containers_selected):
    root_  = copy.deepcopy(cells)
    nodes = []
    nodes.append(root_)
    goal = 0
    containers_left = len(containers_selected)
    total_time = 0
    key_ = 0
    nodes_dict = {}
    nodes_dict[key_] = nodes[0]
    key_ += 1
    #print(containers_selected)
    while(len(nodes) != 0):
        if containers_left == goal:
            return nodes_dict
        else:
            new_nodes, containers_selected, containers_left, totel_time = extend_nodes(nodes[0], containers_selected, containers_left, total_time)
            for i in new_nodes: 
                nodes.append(i)
                #nodes_dict[key_] = nodes[-1]
                nodes_dict[key_] = i
                key_ += 1

            nodes.pop(0)
            #print(nodes[0])


