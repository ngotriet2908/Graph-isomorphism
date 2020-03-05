

def compare_two_list(a, b):
    if len(a) != len(b):
        return False

    a.sort()
    b.sort()

    for i in range(0, len(a)):
        if a[i] != b[i]:
            return False

    return True

def is_in_set(set_of_set, a):
    flag = False
    for sett in set_of_set:
        if a in sett:
            flag = True
            break
    return flag

def is_in_same_set(set_of_set, a, b):
    flag = False
    for sett in set_of_set:
        if a in sett and b in sett:
            flag = True
            break
    return flag