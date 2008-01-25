def make_matrix(rows, columns):
    """
      >>> m = make_matrix(3, 5)
      >>> m
      [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
      >>> m = make_matrix(4, 2)
      >>> m
      [[0, 0], [0, 0], [0, 0], [0, 0]]
      >>> m[0][1] = 7
      >>> m
      [[0, 7], [0, 0], [0, 0], [0, 0]]
    """
    m = []
    row = [0] * columns
    for i in range(rows):
        m += [row[:]]
    return m


def add_row(matrix):
    """
      >>> m = [[0, 0], [0, 0]]
      >>> add_row(m)
      [[0, 0], [0, 0], [0, 0]]
      >>> n = [[3, 2, 5], [1, 4, 7]]
      >>> add_row(n)
      [[3, 2, 5], [1, 4, 7], [0, 0, 0]]
      >>> n
      [[3, 2, 5], [1, 4, 7]]
    """
    size = len(matrix[0])
    return matrix[:] + [[0] * size]


def add_column(matrix):
    """
      >>> m = [[0, 0], [0, 0]]
      >>> add_column(m)
      [[0, 0, 0], [0, 0, 0]]
      >>> n = [[3, 2], [5, 1], [4, 7]]
      >>> add_column(n)
      [[3, 2, 0], [5, 1, 0], [4, 7, 0]]
      >>> n
      [[3, 2], [5, 1], [4, 7]]
    """
    new = []
    for row in matrix:
        new += [row + [0]]
    return new 


def add_matrices(m1, m2):
    """
      >>> a = [[1, 2], [3, 4]]
      >>> b = [[2, 2], [2, 2]]
      >>> add_matrices(a, b)
      [[3, 4], [5, 6]]
      >>> c = [[8, 2], [3, 4], [5, 7]]
      >>> d = [[3, 2], [9, 2], [10, 12]]
      >>> add_matrices(c, d)
      [[11, 4], [12, 6], [15, 19]]
      >>> c
      [[8, 2], [3, 4], [5, 7]]
      >>> d
      [[3, 2], [9, 2], [10, 12]]
    """
    sum = make_matrix(len(m1), len(m1[0]))
    for row in range(len(sum)):
        for col in range(len(sum[0])):
            sum[row][col] = m1[row][col] + m2[row][col]
    return sum


def scalar_mult(n, m):
    """
      >>> a = [[1, 2], [3, 4]]
      >>> scalar_mult(3, a)
      [[3, 6], [9, 12]] 
      >>> b = [[3, 5, 7], [1, 1, 1], [0, 2, 0], [2, 2, 3]]
      >>> scalar_mult(10, b)
      [[30, 50, 70], [10, 10, 10], [0, 20, 0], [20, 20, 30]]
      >>> b
      [[3, 5, 7], [1, 1, 1], [0, 2, 0], [2, 2, 3]]
    """
    prod = []
    for row in m:
        newrow = []
        for elem in row:
            newrow += [elem * n]
        prod += [newrow]
    return prod


def mult_lists(a, b):
        """
          >>> mult_lists([1, 1], [1, 1])
          2
          >>> mult_lists([1, 2], [1, 4])
          9
          >>> mult_lists([1, 2, 1], [1, 4, 3])
          12 
        """
        sum = 0
        for i in range(len(a)):
            sum += a[i] * b[i]
        return sum



if __name__ == '__main__':
    import doctest
    doctest.testmod()
