
def extract_tuple( t, num, padding = None ):
    """This lets us extract a specified number
    of values from a tuple, even if there aren't
    that many in the tuple itself.
    """
    result = list(t)
    if len(result) < num:
        remainder = num - len(result)
        result.extend( [padding] * remainder )
    return tuple(result)
