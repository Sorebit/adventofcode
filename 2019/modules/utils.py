def check(value, expected):
    if value == expected:
        return "OK %s" % str(value)
    return "Expected %s, got %s" % (str(expected), str(value))
