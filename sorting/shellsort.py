def swap(data, i, j):
    data[i], data[j] = data[j], data[i]
    try:
        data[i].counter.being_swapped()
    except AttributeError:
        pass


def shell_sort(data, steps):
    last_index = len(data) - 1
    for step in steps:
        for i in range(step, last_index + 1, 1):
            j = i
            delta = j - step
            while delta >= 0 and data[delta] > data[j]:
                # data[delta], data[j] = data[j], data[delta]
                swap(data, delta, j)
                j = delta
                delta = j - step
    return data


def knutt_seq_generator(N, m=3):
    h = 1
    while h < N / m:
        h = m * h + 1
    
    while h >= 1:
        yield h
        h //= m


def kernigan_richi_generator(N):
    h = N // 2
    while h > 0:
        yield h
        h //= 2


def knutt_shellsort(data):
    N = len(data)
    return shell_sort(data, knutt_seq_generator(N))


def kernigan_richi_shellsort(data):
    N = len(data)
    return shell_sort(data, kernigan_richi_generator(N))

if __name__ == "__main__":
    for i in knutt_seq_generator(1000, 3):
        print(i)
    # Driver code

    arr = [24, 8, 42, 75, 29, 77, 38, 57]
    knutt_shellsort(arr)

    print('Sorted array: ', end='')
    for i in arr:
        print(i, end=' ')

    print()