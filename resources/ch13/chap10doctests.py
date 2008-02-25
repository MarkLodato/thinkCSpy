def make_dictionary(pairs):
    """
      >>> d1 = make_dictionary([('this', 'that')])
      >>> d1
      {'this': 'that'}
      >>> d2 = make_dictionary([('this', 'that'), ('some', 'other'), (4, 'cheese')])
      >>> d2.has_key('some')
      True
      >>> d2.has_key('other')
      False
      >>> d2[4]
      'cheese'
    """
    d = {}
    for pair in pairs:
        d[pair[0]] = pair[1]
    return d

if __name__ == '__main__':
    import doctest
    doctest.testmod()
