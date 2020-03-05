

def compare_two_list(a, b):
    if len(a) != len(b):
        return False

    a.sort()
    b.sort()

    for i in range(0, len(a)):
        if a[i] != b[i]:
            return False

    return True
