

def heapify(A, n, i):
    largest, left, right = i, 2*i + 1, 2*i + 2

    if left < n and A[left] > A[largest]:
        largest = left

    if right < n and A[right] > A[largest]:
        largest = right

    if largest != i:
        A[largest], A[i] = A[i], A[largest]
        heapify(A, n, largest)

def heapsort(A):

    n = len(A)

    # build heap
    for i in xrange(n-1, -1, -1):
        heapify(A, n, i)

    # extract elements from heap
    for i in xrange(n-1, 0, -1):
        A[i], A[0] = A[0], A[i]
        heapify(A, i, 0)

if __name__ == '__main__':
    A = [5,4,1,1,3,2,-2]
    heapsort(A)
    print A
