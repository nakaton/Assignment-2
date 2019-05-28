"""
Network Flow and Planning Assignment

   Input 'X': source nodes
   Input 'Y': transit nodes
   Input 'Z': destination nodes


   x_ikj: flow of each path
   c_ik: capacity of link between source nodes and transit nodes
   d_kj: capacity of link between transit nodes and destination nodes

   u_ikj: binary variables
   n_ij: number of paths that demand volume split over exactly


"""

# Number of nodes
X = None
Y = None
Z = None

# Constraints
demand_constraints = []
capacity_st_constraints = []  # source node to transit node
capacity_td_constraints = []  # transit node to destination node
split_paths_constraints = []
equal_split_flow_constraints = []
balance_load_constraints = []
bounds = []
binaries = []

# OutPut Result String
out_put_result = "Minimize\n    r\nSubject to\n "


#########################################################################################
#                                    Input Node Number                                  #
#########################################################################################
def input_node_number():
    """Config file check"""
    global X, Y, Z
    is_input_correct = True

    # input X
    try:
        X = int(input("Input the number 'X' of source nodes: "))
    except ValueError:
        print("Input 'X' should be positive integer numbers!")
        is_input_correct = False
        return is_input_correct
    else:
        if X <= 0:
            print("Input 'X' should be positive integer numbers!")
            is_input_correct = False
            return is_input_correct

    # input Y
    try:
        Y = int(input("Input the number 'Y' of transit nodes: "))
    except ValueError:
        print("Input 'Y' should be positive integer numbers!")
        is_input_correct = False
        return is_input_correct
    else:
        if Y <= 0:
            print("Input 'Y' should be positive integer numbers!")
            is_input_correct = False
            return is_input_correct

    # input Z
    try:
        Z = int(input("Input the number 'Z' of destination nodes: "))
    except ValueError:
        print("Input 'Z' should be positive integer numbers!")
        is_input_correct = False
        return is_input_correct
    else:
        if Z <= 0:
            print("Input 'Z' should be positive integer numbers!")
            is_input_correct = False
            return is_input_correct

    return is_input_correct


#########################################################################################
#                              Prepare each constraints data                            #
#########################################################################################
def prepare_constraints():
    """Prepare each constraints data"""
    # 1. Demand Constraints
    create_demand_constraints()

    # 2. Capacity Constraints (source node to transit node)
    create_capacity_constraints_st()

    # 3. Capacity Constraints (transit node to destination node)
    create_capacity_constraints_td()

    # 4. Split Paths Constraints
    create_split_paths_constraints()

    # 5. Equal Split Flow Constraints
    create_equal_split_flow_constraints()

    # 6. Transit node's balance load Constraints
    create_balance_load_constraints()

    # 7. Bounds
    create_bounds()

    # 8. Binary
    create_binary()


#########################################################################################
#                                    Generate LP File                                   #
#########################################################################################
def generate_lp_file():
    """Generate LP File"""
    global out_put_result

    out_put_result += "demand_flow: \n"
    for demand_constraint in demand_constraints:
        out_put_result += " " + demand_constraint + '\n'

    out_put_result += "capacity_st: \n"
    for capacity_st_constraint in capacity_st_constraints:
        out_put_result += " " + capacity_st_constraint + '\n'

    out_put_result += "capacity_td: \n"
    for capacity_td_constraint in capacity_td_constraints:
        out_put_result += " " + capacity_td_constraint + '\n'

    out_put_result += "split_paths: \n"
    for split_paths_constraint in split_paths_constraints:
        out_put_result += " " + split_paths_constraint + '\n'

    out_put_result += "equal_split_flow: \n"
    for equal_split_flow_constraint in equal_split_flow_constraints:
        out_put_result += " " + equal_split_flow_constraint + '\n'

    out_put_result += "transit_node_balance_load: \n"
    for balance_load_constraint in balance_load_constraints:
        out_put_result += " " + balance_load_constraint + '\n'

    out_put_result += 'Bounds\n'
    for bound in bounds:
        out_put_result += " " + bound + '\n'

    out_put_result += 'Binary\n'
    for binary in binaries:
        out_put_result += " " + binary + '\n'

    out_put_result += 'End'

    print(out_put_result)

    # Generate LP file
    file_name = 'X' + str(X) + '_Y' + str(Y) + '_Z' + str(Z) + '.lp'

    file = open(file_name, 'w')
    file.write(out_put_result)
    file.close()


#########################################################################################
#                                    Create Constraints                                 #
#########################################################################################
def create_demand_constraints():
    """Demand Constraints"""
    global demand_constraints
    demand_constraint = ""

    for i in range(X):
        for j in range(Z):
            for k in range(Y):
                if k+1 < Y:
                    demand_constraint += 'x_' + str(i+1) + str(k+1) + str(j+1) + ' + '
                else:
                    demand_constraint += 'x_' + str(i+1) + str(k+1) + str(j+1)

            demand_constraint += ' = ' + str(2 * (i+1) + (j+1))
            demand_constraints.append(demand_constraint)
            demand_constraint = ""

    # for item in demand_constraints:
    #     print(str(item) + '\n')


#########################################################################################
def create_capacity_constraints_st():
    """Capacity Constraints (source node to transit node)"""
    global capacity_st_constraints
    capacity_st_constraint = ""

    for i in range(X):
        for k in range(Y):
            for j in range(Z):
                if j+1 < Z:
                    capacity_st_constraint += 'x_' + str(i+1) + str(k+1) + str(j+1) + ' + '
                else:
                    capacity_st_constraint += 'x_' + str(i+1) + str(k+1) + str(j+1)

            capacity_st_constraint += ' - c_' + str(i+1) + str(k+1) + ' <= 0'
            capacity_st_constraints.append(capacity_st_constraint)
            capacity_st_constraint = ""

    # for item in capacity_st_constraints:
    #     print(str(item) + '\n')


#########################################################################################
def create_capacity_constraints_td():
    """Capacity Constraints (transit node to destination node)"""
    global capacity_td_constraints
    capacity_td_constraint = ""

    for j in range(Z):
        for k in range(Y):
            for i in range(X):
                if i+1 < X:
                    capacity_td_constraint += 'x_' + str(i+1) + str(k+1) + str(j+1) + ' + '
                else:
                    capacity_td_constraint += 'x_' + str(i+1) + str(k+1) + str(j+1)

            capacity_td_constraint += ' - d_' + str(k+1) + str(j+1) + ' <= 0'
            capacity_td_constraints.append(capacity_td_constraint)
            capacity_td_constraint = ""

    # for item in capacity_td_constraints:
    #     print(str(item) + '\n')


#########################################################################################
def create_split_paths_constraints():
    """Split Paths Constraints"""
    global split_paths_constraints
    split_paths_constraint = ""

    for i in range(X):
        for j in range(Z):
            for k in range(Y):
                if k+1 < Y:
                    split_paths_constraint += 'u_' + str(i+1) + str(k+1) + str(j+1) + ' + '
                else:
                    split_paths_constraint += 'u_' + str(i+1) + str(k+1) + str(j+1)

            split_paths_constraint += ' = 2'
            split_paths_constraints.append(split_paths_constraint)
            split_paths_constraint = ""

    # for item in split_paths_constraints:
    #     print(str(item) + '\n')


#########################################################################################
def create_equal_split_flow_constraints():
    """Equal Split Flow Constraints"""
    global equal_split_flow_constraints
    equal_split_flow_constraint = ""

    for i in range(X):
        for k in range(Y):
            for j in range(Z):
                equal_split_flow_constraint = '2 x_' + str(i+1) + str(k+1) + str(j+1) + ' - ' + str(2 * (i+1) + (j+1)) \
                                              + ' u_' + str(i+1) + str(k+1) + str(j+1) + ' = 0'

                equal_split_flow_constraints.append(equal_split_flow_constraint)
                equal_split_flow_constraint = ""

    # for item in equal_split_flow_constraints:
    #     print(str(item) + '\n')


#########################################################################################
def create_balance_load_constraints():
    """Transit node's balance load Constraints"""
    global balance_load_constraints
    balance_load_constraint = ""

    for k in range(Y):
        for i in range(X):
            for j in range(Z):
                if i+1 < X:
                    balance_load_constraint += 'x_' + str(i+1) + str(k+1) + str(j+1) + ' + '
                else:
                    if j+1 < Z:
                        balance_load_constraint += 'x_' + str(i + 1) + str(k + 1) + str(j + 1) + ' + '
                    else:
                        balance_load_constraint += 'x_' + str(i+1) + str(k+1) + str(j+1)

        balance_load_constraint += ' -r <= 0'
        balance_load_constraints.append(balance_load_constraint)
        balance_load_constraint = ""

    # for item in balance_load_constraints:
    #     print(str(item) + '\n')


#########################################################################################
def create_bounds():
    """Bounds"""
    global bounds
    bound = ""

    for i in range(X):
        for k in range(Y):
            for j in range(Z):
                bound += '0 <= x_' + str(i+1) + str(k+1) + str(j+1)

                bounds.append(bound)
                bound = ""

    bounds.append("0 <= r")

    # for item in bounds:
    #     print(str(item) + '\n')


#########################################################################################
def create_binary():
    """Binary"""
    global binaries
    binary = ""

    for i in range(X):
        for k in range(Y):
            for j in range(Z):
                binary += 'u_' + str(i+1) + str(k+1) + str(j+1)

                binaries.append(binary)
                binary = ""

    # for item in binaries:
    #     print(str(item) + '\n')


#########################################################################################
#                                    Main                                               #
#########################################################################################
def main():
    """Generate LP File"""

    # <Beginning stage>: Input three positive integer numbers X, Y and Z
    is_input_correct = input_node_number()

    # When any checking error from input numbers, following logic does not execute
    if is_input_correct:
        # <Next stage>: Prepare each constraints data
        prepare_constraints()

        # <Final stage>: Generate LP File
        generate_lp_file()

        print(">> End Network Flow and Planning Successfully")
    else:
        print(">> End Network Flow and Planning with ERROR!")


if __name__ == '__main__':
    print('>> Start Network Flow and Planning')
    main()
