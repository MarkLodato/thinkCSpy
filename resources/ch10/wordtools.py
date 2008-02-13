#
# wordtools.py
#
def cleanword(word):
    """
      >>> cleanword('what?')
      'what'
      >>> cleanword('"now!"')
      'now'
      >>> cleanword('?,;(.-here=@&!)<{')
      'here'
    """
    word = word.lstrip('\'"?!,;:.-_=@#$%&*()[]{}/\\<>\n~`')
    return word.rstrip('\'"?!,;:.-_=@#$%&*()[]{}/\\<>\n~`')


def has_dashdash(s):
    """
      >>> has_dashdash('distance--but')
      True
      >>> has_dashdash('several')
      False
      >>> has_dashdash('critters')
      False
      >>> has_dashdash('spoke--fancy')
      True
    """
    return '--' in s


if __name__ == '__main__':
    import doctest
    doctest.testmod()
