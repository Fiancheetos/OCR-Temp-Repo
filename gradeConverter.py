def alphaToNumeric(alpha):
    conversion_table = {
        "A": 1,
        "A-": 1.333,
        "B+": 1.6667,
        "B": 2,
        "B-": 2.333,
        "C+": 2.6667,
        "C": 3
    }
    numeric = conversion_table.get(alpha.upper(), None)
    return numeric


alphaToNumeric("A")
