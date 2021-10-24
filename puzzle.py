import heapq
import numpy as np


def get_position(state, num):
    """
    Gets the position in the form of [x, y] of the number in the current state of the 8-piece puzzle
    :param state: current state of the 8-piece puzzle
    :param num: number to get the position of
    :return: the position in the form of [x, y]
    """
    pos_num = 0
    for x in state:
        pos_num += 1
        if num == x:
            if pos_num == 1:
                return [0, 0]
            elif pos_num == 2:
                return [0, 1]
            elif pos_num == 3:
                return [0, 2]
            elif pos_num == 4:
                return [1, 0]
            elif pos_num == 5:
                return [1, 1]
            elif pos_num == 6:
                return [1, 2]
            elif pos_num == 7:
                return [2, 0]
            elif pos_num == 8:
                return [2, 1]
            elif pos_num == 9:
                return [2, 2]


def swap(state, one, two):
    """
    Swaps piece "one" and piece "two" (not the numbers one and two) on the 8-piece puzzle board
    :param state: current state of the 8-piece puzzle
    :param one: number to replace two
    :param two: number to replace one
    :return: new state after swapping one and two
    """
    skip = None
    for x in range(len(state)):
        if state[x] is one:
            state[x] = two
            skip = x
    for x in range(len(state)):
        if x is not skip:
            if state[x] is two:
                state[x] = one
    return state


def calc_h_val(state):
    """
    Calculates the h value of the 8-piece puzzle
    :param state: current state of the 8-piece puzzle
    :return: h value of the 8-piece puzzle
    """
    sum_h = 0
    for x in state:
        if x != 0:
            pos = get_position(state, x)
            if x == 1:
                sum_h += abs(pos[0] - 0) + abs(pos[1] - 0)
            elif x == 2:
                sum_h += abs(pos[0] - 0) + abs(pos[1] - 1)
            elif x == 3:
                sum_h += abs(pos[0] - 0) + abs(pos[1] - 2)
            elif x == 4:
                sum_h += abs(pos[0] - 1) + abs(pos[1] - 0)
            elif x == 5:
                sum_h += abs(pos[0] - 1) + abs(pos[1] - 1)
            elif x == 6:
                sum_h += abs(pos[0] - 1) + abs(pos[1] - 2)
            elif x == 7:
                sum_h += abs(pos[0] - 2) + abs(pos[1] - 0)
            elif x == 8:
                sum_h += abs(pos[0] - 2) + abs(pos[1] - 1)
    return sum_h


def succ(state):
    """
    Given a state of the puzzle, represented as a single list of integers with a 0 in the empty space, find all of the
    possible successor state
    :param state: current state of the 8-piece puzzle
    :return: a list of the possible successor states
    """
    succs = []
    s = np.reshape(state, (3, 3))
    i, j = np.where(s == 0)

    if i - 1 >= 0:  # swap with piece above
        x = np.copy(s)
        x[i, j], x[i - 1, j] = x[i - 1, j], x[i, j]
        x = x.flatten()
        succs.append(list(x))

    if i + 1 < 3:  # swap with piece below
        x = np.copy(s)
        x[i, j], x[i + 1, j] = x[i + 1, j], x[i, j]
        x = x.flatten()
        succs.append(list(x))

    if j - 1 >= 0:  # swap with piece on left
        x = np.copy(s)
        x[i, j], x[i, j - 1] = x[i, j - 1], x[i, j]
        x = x.flatten()
        succs.append(list(x))

    if j + 1 < 3:  # swap with piece on right
        x = np.copy(s)
        x[i, j], x[i, j + 1] = x[i, j + 1], x[i, j]
        x = x.flatten()
        succs.append(list(x))

    return sorted(succs)


def get_state_index(state, list):
    """
    Finds the given state in the list
    :param state: desired (to find) state of the 8-piece puzzle
    :param list: list to find the state in
    :return: the index of the state in the given list
    """
    for s in list:
        if s == state:
            return list.index(s)
    return -1


def print_succ(state):
    """
    Given a state of the puzzle, represented as a single list of integers with a 0 in the empty space, print to the
    console all of the possible successor state
    :param state: current state of the 8-piece puzzle
    :return: nothing
    """
    succs = succ(state)

    for s in succs:
        st = "["
        for x in range(len(s)):
            if x != len(s) - 1:
                st += str(s[x]) + ", "
            else:
                st += str(s[x]) + "] h=" + str(calc_h_val(s))
        print(st)
    pass


def solve(state):
    """
    given a state of the puzzle, perform the A* search algorithm and print the path from the current state to the goal
    state
    :param state: current state of the 8-piece puzzle
    :return: nothing
    """
    opq = []  # open PQ
    cl = []  # closed list
    g = 0  # moves taken (cost)
    n = -1  # node number
    node = []  # state node
    goal = False
    heapq.heappush(opq, (calc_h_val(state) + g, state, (g, calc_h_val(state), n)))  # initial state

    while goal is False:
        node = heapq.heappop(opq)
        if calc_h_val(node[1]) == 0:  # if h val of the state is 0 (solved!)
            goal = True
        else:  # if not solved
            cl.append(node[1])
            for s in succ(node[1]):  # for each state when generating the successors
                g = node[2][0] + 1
                i = get_state_index(s, opq)
                if i > 0:
                    if g < opq[i][2][0]:
                        heapq.heappush(opq, (g + calc_h_val(s), s, (g, calc_h_val(s), node)))
                if s in cl:
                    continue
                heapq.heappush(opq, (g + calc_h_val(s), s, (g, calc_h_val(s), node)))

    output = []

    while node[2][2] != -1:
        output.append({"state": node[1], "h": node[2][1], "move": node[2][0]})
        node = node[2][2]
    output.append({"state": node[1], "h": node[2][1], "move": node[2][0]})
    output = sorted(output, key=lambda x: x["move"])

    for line in output:
        print("{} h={} moves: {}".format(line["state"], line["h"], line["move"]))

    pass
