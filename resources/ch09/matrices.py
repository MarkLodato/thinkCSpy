def make_matrix(rows, columns):
    """
      >>> m = make_matrix(3, 5)
      >>> m
      [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
      >>> m = make_matrix(4, 2)
      >>> m
      [[0, 0], [0, 0], [0, 0], [0, 0]]
    """
    m = []
    row = [0] * columns
    for i in range(rows):
        m += [row[:]]
    return m


def add_row(matrix):
    """
      >>> m = [[0, 0], [0, 0]]
      >>> m = add_row(m)
      >>> m
      [[0, 0], [0, 0], [0, 0]]
      >>> n = [[3, 2, 5], [1, 4, 7]]
      >>> n = add_row(n)
      >>> n
      [[3, 2, 5], [1, 4, 7], [0, 0, 0]]
    """
    size = len(matrix[0])
    matrix += [[0] * size]
    return matrix


def add_column(matrix):
    """
      >>> m = [[0, 0], [0, 0]]
      >>> m = add_column(m)
      >>> m
      [[0, 0, 0], [0, 0, 0]]
      >>> n = [[3, 2], [5, 1], [4, 7]]
      >>> n = add_column(n)
      >>> n
      [[3, 2, 0], [5, 1, 0], [4, 7, 0]]
    """
    new = matrix[:]
    for row in new:
        row += [0]
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
    """
    sum = make_matrix(len(m1), len(m1[0]))
    for row in range(len(sum)):
        for col in range(len(sum[0])):
            sum[row][col] = m1[row][col] + m2[row][col]
    return sum





if __name__ == '__main__':
    import doctest
    doctest.testmod()
