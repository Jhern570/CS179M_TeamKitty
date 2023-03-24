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
    
    for i in containers_selected:
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

def search_load(cells):
    root_ = copy.deepcopy(cells)
    distance_of_shortest_pos = 11
    best_pos = []
    #nodes.append(root_)
    goal = 11

    for column in range(12):
        for row in range(8):
            if root_[12 * row + column][3] != "UNUSED":
                continue
            
            manhattan_dist = calculate_md_move(int(root_[12 * row + column][0]), int(root_[12 * row + column][1]), row + 1, column + 1)
            
            if manhattan_dist < distance_of_shortest_pos:
                distance_of_shortest_pos = manhattan_dist
                best_pos = [row, column]
    return best_pos

def calculate_side_weight(x1,x2,y1,y2, cells):
    sum_of_weights = 0
    for i in range(x1,x2):
        for j in  range(y1,y2):
            if cells[12*i+j][3] == "UNUSED" or cells[12*i+j][3] == "NAN":
                continue
        
            sum_of_weights += int(cells[12*i+j][2])
    return sum_of_weights 

def divide_bay(cells, x1, x2, y1, y2):
    half_bay = []

    for i in range(x1, x2):
        for j in range(y1,y2):
            if cells[12*i+j][3] == "UNUSED" or cells[12*i+j] == "NAN":
                continue
            half_bay.append(cells[12 * i + j])
    return half_bay

def check_if_balance(left, right, balance_mass):
    max_difference = balance_mass * 0.1
    return True if abs(left-right) <= max_difference else False

def possible_containers_to_move(cells, target):
    # Base case
    if target == 0:
        return [[]]
    
    # Recursive case
    result = []
    for i, cell in enumerate(cells):
        # Check if num can be part of the solution
        if int(cell[2]) <= target and int(cell[2]) != 0:
            # Recursively find the rest of the solution
            sub_result = possible_containers_to_move(cells[i+1:], target - int(cell[2]))
            # Add num to each solution found
            for sub_list in sub_result:
                result.append(cell + sub_list)
    
    # Return all solutions found
    return result

def find_closest_weight_to_deficit(cells, target):
    closest = [0,0,0,0]
    for cell in cells:
        if abs(int(cell[2]) - target) < abs(int(closest[2]) - target):
            closest = cell
    return closest


def containers_selected_list(node, side_bay, deficit, prev_closest_to_deficit):
    containers = []
    closest_to_deficit = 0
    possible_to_move_list = possible_containers_to_move(side_bay, deficit)
    if possible_to_move_list == None:
        #find the closest number to deficit:
        closest_to_deficit = find_closest_weight_to_deficit(side_bay, deficit)
        #if repeated container movement, ship cannot be balanced
        if closest_to_deficit == prev_closest_to_deficit:
            return containers, closest_to_deficit
        containers.append(node[12 * (closest_to_deficit[0] - 1) + (closest_to_deficit[1] - 1)])
    else:
        for i in possible_to_move_list:
            containers.append(node[12 * (i[0] - 1) + (i[1] - 1)])
    return containers, closest_to_deficit

def extend_node_balance(parent_node, containers_selected, containers_left, total_time):
    new_nodes = []
    temp_new_nodes = []
    distances_ = []
    flag = 0
    containers_ = containers_selected.copy()
    count = 0
    unsused_flag = 0;
    
    for i in containers_selected:
        if flag == 1:
            return new_nodes, containers_selected, containers_left, total_time
        for j in range(7,-1,-1):
            if parent_node[12 * j + (int(i[1]) - 1)][3] == "UNUSED" or parent_node[12 * j + (int(i[1]) - 1)][3] == "NAN":
                continue
            elif parent_node[12 * j + (int(i[1]) - 1)][3] == i[3]:
                min_dist = 0
                new_start_position = j + 1
                additional_spaces = 0
                columns_used = []
                flag = 0
                
                if int(i[1]) < 7:
                    half_init, half_end = 6, 12
                else:
                    half_init, half_end = 0, 6

                if half_init == 6:
                    for col in range(half_init, half_end):
                        for row in range(8):
                            if parent_node[12 * row + col][3] == "UNUSED":
                                node_ = copy.deepcopy(parent_node)
                                manhattan_dist = calculate_md_move(row + 1, col + 1, new_start_position, int(i[1])) + additional_spaces
                                if min_dist == 0 or min_dist > manhattan_dist:
                                    new_nodes.clear()
                                    containers_left -= 1
                                    min_dist = manhattan_dist
                                    node_[12 * row + col][3] = node_[12 * j + (int(i[1]) - 1)][3]
                                    node_[12 * row + col][2] = node_[12 * j + (int(i[1]) - 1)][2]
                                    node_[12 * j + (int(i[1]) -1)][3] = "UNUSED"
                                    node_[12 * j + (int(i[1]) -1)][2] = "00000"
                                    new_nodes.append(node_)
                                    
                                    containers_.pop(count)
                                    flag = 1
                                    break   
                        if len(containers_) != len(containers_selected):
                            break    
                        if flag == 1:
                            flag = 0
                            break
                        if row == 7:
                            new_start_position = 9 
                            additional_spaces = 9 - int(i[0])
                    new_start_position = j  + 1
                    addtional_spaces = 0
                    if flag == 1:
                        break
                else:
                    for col in range(half_end - 1  , half_init - 1, -1):
                        for row in range(8):
                            if parent_node[12 * row + col][3] == "UNUSED":
                                node_ = copy.deepcopy(parent_node)
                                manhattan_dist = calculate_md_move(row + 1, col + 1, new_start_position, int(i[1])) + additional_spaces
                                if min_dist == 0 or min_dist > manhattan_dist:
                                    new_nodes.clear()
                                    min_dist = manhattan_dist
                                    containers_left -= 1
                                    node_[12 * row + col][3] = node_[12 * j + (int(i[1]) - 1)][3]
                                    node_[12 * row + col][2] = node_[12 * j + (int(i[1]) - 1)][2]
                                    node_[12 * j + (int(i[1]) -1)][3] = "UNUSED"
                                    node_[12 * j + (int(i[1]) -1)][2] = "00000"
                                    new_nodes.append(node_)
                                    containers_.pop(count)
                                    flag = 1
                                    break       
                        if len(containers_) != len(containers_selected):
                            break
                        if flag == 1:
                            flag = 0
                            break
                        if row == 7:
                            new_start_position = 9 
                            additional_spaces = 9 - int(i[0])
                    new_start_position = j  + 1
                    addtional_spaces = 0
                    if flag == 1:
                        break
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
                                new_nodes.clear()
                                min_dist = manhattan_dist
                                node_[12 * row + col][3] = node_[12 * j + (int(i[1]) - 1)][3]
                                node_[12 * row + col][2] = node_[12 * j + (int(i[1]) - 1)][2]
                                node_[12 * j + (int(i[1]) -1)][3] = "UNUSED"
                                node_[12 * j + (int(i[1]) -1)][2] = "00000"
                                new_nodes.append(node_)
                                flag = 1
                                break
                    if flag == 1:
                        flag = 0
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
                                new_nodes.clear()
                                min_dist = manhattan_dist
                                node_[12 * row + col][3] = node_[12 * j + (int(i[1]) - 1)][3]
                                node_[12 * row + col][2] = node_[12 * j + (int(i[1]) - 1)][2]
                                node_[12 * j + (int(i[1]) -1)][3] = "UNUSED"
                                node_[12 * j + (int(i[1]) -1)][2] = "00000"
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


def search_for_balance(cells, containers_selected, key_pos):
    root_  = copy.deepcopy(cells)
    nodes = []
    nodes.append(root_)
    goal = 0
    cannot_balance = False 
    containers_left = len(containers_selected)
    #GOAL IS TO CHECK IF BALANCE IS TRUE or cannot balance is true
    #WE CALCULATE THE BALANCE MASS WHICH IS ALWAYS CONSTANT
    #DEFICIT IS WHAT IS CHANGING
    #containers_left = len(containers_selected)
    #WE SEPERATE LEFT AND RIGHT SIDES OF THE BAY AND CALCULATE THE DEFICIT
    
    total_time = 0
    nodes_dict = {}
    nodes_dict[key_pos] = nodes[0]
    key_pos = key_pos+1
    #print(containers_selected)
    while(len(nodes) != 0):
        if containers_left == goal: #IF THE CHECK BALANCE IS TRUE WE HAVE MOVEMENTS
    
            return nodes_dict
        else:
            #For extend nodes, we see first if there a possible number of containers that can be equal to the deficit
            #if not grab the container that if values is closest to the deficit
            #extend nodes will move the containers depeding of the if statement:
            #if containers weight is equal to the deficit than move than containers selected will equal 0
            #else search will continue with new deficit . 

            new_nodes, containers_selected, containers_left, totel_time = extend_node_balance(nodes[0], containers_selected, containers_left, total_time)
            for i in new_nodes: 
                nodes.append(i)
                #nodes_dict[key_] = nodes[-1]
                nodes_dict[key_pos] = i
                key_pos += 1
            nodes.pop(0)
            #print(nodes[0])


