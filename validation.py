from relationFunctions import getFunc

def getRelationQuantities(state, relation):
    entity1, quan1 = relation["Q1"]
    entity2, quan2 = relation["Q2"]
    head = state[entity1][quan1]
    tail = state[entity2][quan2]
    return head, tail


def isStateValid(state, relations):
    isValid = True

    # TODO fix rule interaction with same tail
    possibleDerivatives = {}
    magnitudes = {}

    for rel in relations:
        # get implemetation for relation
        func = getFunc(rel["type"], rel["args"])
        # get head and tail quantity
        head, tail = getRelationQuantities(state, rel)
        new_tail = tail.copy()

        # apply relation
        func(head, new_tail)

        if rel["type"] == "VC":
            if new_tail != tail:
                magnitudes[rel["Q2"]] = new_tail.magnitude.value
        else:
            if not rel["Q2"] in possibleDerivatives:
                possibleDerivatives[rel["Q2"]] = []

            if not new_tail.derivative.value in possibleDerivatives[rel["Q2"]]:
                possibleDerivatives[rel["Q2"]].append(new_tail.derivative.value)

            if len(possibleDerivatives[rel["Q2"]]) == 2 and possibleDerivatives[rel["Q2"]][0]== -1 * possibleDerivatives[rel["Q2"]][1]:
                # add derivative = 0 for continuity
                possibleDerivatives[rel["Q2"]].append(0)
    for rel in relations:
        head, tail = getRelationQuantities(state, rel)
        # check if state changed to valid option
        if not tail.derivative.value in possibleDerivatives[rel["Q2"]]:
            isValid = False
            break

        if rel["Q2"] in magnitudes and magnitudes[rel["Q2"]] != tail.magnitude.value:
            isValid = False
            break

    return isValid
