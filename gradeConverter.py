def alphaToUPG(alpha):
    conversion_table = {
        "A": 1.0,
        "A-": 1.333,
        "B+": 1.6667,
        "B": 2.0,
        "B-": 2.333,
        "C+": 2.6667,
        "C": 3.0
    }
    upg = conversion_table.get(alpha.upper(), None)
    return upg

def invertedToUPG(inverted):
    conversion_table = {
        4.0: 1.0,
        3.5: 1.3333,
        3.0: 1.6667,
        2.5: 2.0,
        2.0: 2.3333,
        1.5: 2.6667,
        1.0: 3.0
    }
    upg = conversion_table.get(inverted, None)
    return upg

def preciseToUPG(precise):
    conversion_table ={
        1.0: 1.0, 1.1: 1.067, 1.2: 1.133, 1.3: 1.2, 1.4: 1.267, 1.5: 1.333, 1.6: 1.4, 1.7: 1.467, 1.8: 1.533, 1.9: 1.6,
        2.0: 1.667, 2.1: 1.733, 2.2: 1.8, 2.3: 1.867, 2.4: 1.933, 2.5: 2.0, 2.6: 2.067, 2.7: 2.133, 2.8: 2.2, 2.9: 2.267,
        3.0: 2.333, 3.1: 2.4, 3.2: 2.467, 3.3: 2.533, 3.4: 2.6, 3.5: 2.667, 3.6: 2.733, 3.7: 2.8, 3.8: 2.867, 3.9: 2.933,
        4.0: 3.0
    }
    upg = conversion_table.get(precise, None)
    return upg


print(alphaToUPG("B-"))
print(invertedToUPG(3.5))
print(preciseToUPG(2.4))
