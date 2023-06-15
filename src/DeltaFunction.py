class DeltaFunction:
    def __init__(self, preState, symbol, nextStates):
        self.preState = preState
        self.symbol = symbol

        self.nextStates = [nextStates]

    def findNextState(self, nextState):
        for ns in self.nextStates:
            if ns == nextState:
                return True
        return False

    def addNextState(self, nextState):
        self.nextStates.append(nextState)

    def toString(self):
        rt = "(" + self.preState + ", " + self.symbol + ") = {"
        for i in range(0, len(self.nextStates)):
            rt += self.nextStates[i]
            if i < len(self.nextStates)-1: rt += ", "
            else: rt += "}"
        
        return rt