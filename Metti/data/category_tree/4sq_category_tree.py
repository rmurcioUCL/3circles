def getCateTree():
    f = open('cate4sq.txt', 'r')
    lines = f.readlines()
    f.close()
    result = dict()
    i = 0
    curr = None
    listOfStacks = [[] for j in range(4)]
    while i < len(lines):
        line = lines[i]
        l = line.lstrip(' ')
        if l.startswith('Suggested Countries:'):
            i = i + 1
            continue
        space = len(line) - len(line.lstrip(' '))
        loc = space / 4
        if curr != None:
            if curr <= loc: # it move to right, subcategory
                listOfStacks[loc].append(l.strip('\n'))
            else: # it moves to left, end of subcategory
                index = len(listOfStacks[loc]) - 1 # the last element of stack
                for name in listOfStacks[curr]:
                    result[name] = listOfStacks[loc][index]
                listOfStacks[curr] = []
        i = i + 1
        curr = loc
        listOfStacks[loc].append(l.strip('\n'))
    return result

if __name__ == "__main__":
    result = getCateTree()
    for (k, v) in result.items():
        s = str(k) + ':' + str(v)
        print s