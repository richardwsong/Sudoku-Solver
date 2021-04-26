import math
import time
import sys

calls = 0
N = -1
subblock_height = -1
subblock_width = -1
characters = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
symbol_set = ""
neigh = dict()
con = dict()

def check(state):
    for ch in symbol_set:
        print(ch, len([i for i, ltr in enumerate(state) if ltr == ch]))


def findOccurances(s, poss):
    ret = set(i for i, letter in enumerate(s) if letter == ".")
    return ret


def gen(length):
    global N
    global subblock_height
    global subblock_width
    global symbol_set
    N = int(math.sqrt(length))

    symbol_set = characters[0:N]
    val = math.sqrt(N)
    if val % 1 == 0:
        subblock_width = int(val)
        subblock_height = int(val)
    else:
        temp = math.floor(val)
        while temp > 0:
            if N%temp == 0:
                subblock_height = temp
                subblock_width = int(N/temp)
                break
            temp -= 1


def print_puzzle(x):
    # index = 0
    # for z in range(0, subblock_width):
    #     for a in range(0, subblock_height):
    #         for b in range(0, subblock_height):
    #             print(x[index: index+subblock_width], end="")
    #             print("|", end="")
    #             index += subblock_width
    #         print()
    #     for a in range(0, N+subblock_height):
    #         print("-", end="")
    #     print()
    print(x)

def constraint_set(board):
    ret = []
    for x in range(0, N):  # by row
        start = x*N
        temp = set()
        for y in range(start, start + N):
            temp.add(y)
        ret.append(temp)

    for x in range(0, N):  # by column
        start = x
        temp = set()
        for y in range(0, N):
            temp.add(start + y*N)
        ret.append(temp)

    for x in range(0, N):  # by subblock
        temp = set()
        start = x
        for y in range(0, subblock_height):
            for a in range(0, subblock_width):
                temp.add(int(x/subblock_height)*N*subblock_height + y*N + x%subblock_height*subblock_width + a)
        ret.append(temp)
    return ret


def neighbors(constraint):
    ret = dict()
    for x in range(0, N*N):
        ret[x] = set()
        for y in constraint:
            if int(x) in y:
                for z in y:
                    if z != int(x):
                        ret[x].add(z)
    return ret


# def get_next(board):
#     index = 0
#     for x in board:
#         if x == ".":
#             return index
#         index += 1
#     return -1


# def get_next(board, poss):
#     min = sys.maxsize
#     index = -1
#     for x in poss:
#         if len(poss[x]) < min and board[x] == ".":
#             min = len(poss[x])
#             if len(poss[x]) == 1:
#                 return x
#             index = x
#     return index


def get_next(board, poss, period):
    min = sys.maxsize
    index = -1
    for x in period:
        if len(poss[x]) < min and board[x] == ".":
            min = len(poss[x])
            if len(poss[x]) == 1:
                return x
            index = x
    return index


def get_sorted_values(neigh, board):
    ret = []
    for x in symbol_set:
        bad = False
        for y in neigh:
            if board[y] == x:
                bad = True
                break
        if bad == False:
            ret.append(x)
    return ret


def get_possible_values(neigh, board):
    poss = dict()
    for x in range(0, N*N):
        if board[x] != ".":
            poss[x] = board[x]
            continue
        ind = neigh[x]
        symbol = symbol_set
        for y in ind:
            if board[y] != "." and board[y] in symbol:
                symbol = symbol.replace(board[y], "")
        poss[x] = symbol
    return poss


def constraint_propogation(board, num, next, period):
    global neigh
    ret = []
    poss = num.copy()
    for x in period:
        if len(poss[x]) == 1:
            board = board[0:x] + poss[x] + board[x+1:]
            ret.append(x)

    # ret.append(next)
    # ret = solved
    # ret = ret + str(next)
    while len(ret) > 0:
        temp = ret.pop()
        for y in neigh[temp]:
            oldlength = len(poss[y])
            if str(poss[temp]) in poss[y]:
                poss[y] = poss[y].replace(str(poss[temp]), "")
            if len(poss[y]) == 1 and oldlength != 1:
                board = board[0:y] + poss[y] + board[y+1:]
                ret.append(y)
            if len(poss[y]) == 0:
                return False
    return poss, board


def logic_two(board, poss):
    global con
    changed = False
    #print(poss)
    for x in con:
        temp = []
        allsolved = True
        for y in x:
            temp.append((poss[y], y))
            if len(poss[y]) > 1:
                allsolved = False
        if allsolved:
            continue
        for y in symbol_set:
            index = []
            counter = 0
            bad = False
            for z in temp:
                if y in z[0] and len(index) == 0:
                    index.append(z[1])
                elif y in z[0] and len(index) > 0:
                    bad = True
                    break
                counter+=1
            if bad:
                continue
            elif len(index) == 1:
                old = poss[index[0]]
                poss[index[0]] = y
                if old != poss[index[0]]:
                    changed = True
                    board = board[0: index[0]] + y + board[index[0] + 1:]
        #print(poss)
    return poss, changed, board


def logic_three(poss):
    global con
    for x in con:
        temp = dict()
        ret = []
        for y in x:
            # if poss[y] in temp and len(poss[y]) == 2:
            if poss[y] in temp and len(poss[y]) == 2:
                temp[poss[y]] = temp[poss[y]] + 1
                ret.append(y)
            else:
                temp[poss[y]] = 1
        for y in ret:
            n = -1
            if len(poss[y]) == temp[poss[y]]:
                n = len(poss[y])
            else:
                continue
            if temp[poss[y]] != n:
                continue
            for z in x:
                if poss[z] == poss[y] or len(poss[z]) == n:
                    continue
                for q in range (0, n):
                    if poss[y][q] in poss[z]:
                        poss[z] = poss[z].replace(poss[y][q], "")

    return poss

def csp(board, poss, period):
    global calls
    global neigh
    global con
    next = get_next(board, poss, period)
    if next == -1:
        return board
    #ret = get_sorted_values(neigh[next], board)
    for x in poss[next]:
        temp = board[0:next] + x + board[next+1:]
        #poss1 = poss.copy()
        poss[next] = x
        cp = constraint_propogation(board, poss, next, period)
        if cp == False:
            continue
        val = cp[0]
        temp = cp[1]

        new_period = period.copy()
        new_period.remove(next)
        opta = logic_two(temp, val)

        val = opta[0]
        change = opta[1]
        temp = opta[2]
        while change == True:
            opta = logic_two(temp, val)
            val = opta[0]
            change = opta[1]
            temp = opta[2]
        val = logic_three(val)
        result = csp(temp, val, new_period)
        calls+=1
        if result is not None:
            return result
    return None


def init(file):
    global calls
    global neigh
    global con
    file = open(file, "r")

    x = file.readline().strip()
    map = dict()
    map1 = dict()
    counter = 1
    total = 0
    while len(x) > 0:
        # if counter == 51:
        #     break
        length = len(x)
        gen(length)
        if length in map:
            temp = map[length]
            constraint = map1[length]
        else:
            constraint = constraint_set(x)
            temp = neighbors(constraint)
            map[length] = temp
            map1[length] = constraint

        start = time.perf_counter()
        poss = get_possible_values(temp, x)
        period = findOccurances(x, poss)
        neigh = temp
        con = constraint

        change = True
        cp = constraint_propogation(x, poss, 0, period)
        val = cp[0]
        x = cp[1]
        while change == True:
            opta = logic_two(x, val)
            val = opta[0]
            change = opta[1]
            x = opta[2]
            cp = constraint_propogation(x, val, 0, period)
            val = cp[0]
            x = cp[1]
        start_call = calls
        ans = csp(x, val, period)
        calls += 1
        end_call = calls
        end = time.perf_counter()

        total += (end-start)
        print("N:", N)
        #print(counter)
        print("Time:", end-start)
        print("Number of Calls:", end_call - start_call)
        print_puzzle(ans)
        counter += 1
        print()
        # check(ans)
        x = file.readline().strip()
    print("Total time", total)
    print("Total calls", calls)
# gen(81)
# print(neighbors(constraint_set(".17369825632158947958724316825437169791586432346912758289643571573291684164875293")))


file = sys.argv[1]
init(file)

