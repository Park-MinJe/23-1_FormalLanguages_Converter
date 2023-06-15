class uClosure:
    def __init__(self):
        self.state = ""
        self.symbol = []
        self.visitStates = []
    
    def addSymbol(self, start):
        if len(self.symbol) > 0:
            exist = False
            for vs in self.symbol:
                if vs == start:
                    exist = True
                    break
                else: exist = False
            if not exist:
                self.symbol.append(start)
        else:
            self.symbol.append(start)
        return self.symbol
    
    def addSymbolAsArr(self, start):
        if len(self.symbol) > 0:
            exist = False
            for vs in self.symbol:
                for st in start:
                    if vs == st:
                        exist = True
                        break
                    else: exist = False
            if not exist:
                self.symbol + start
        else:
            self.symbol + start
        return self.symbol
    
    def addvisitStates(self, final):
        if len(self.visitStates) > 0:
            exist = False
            for vs in self.visitStates:
                if vs == final:
                    exist = True
                    break
                else: exist = False
            if not exist:
                self.visitStates.append(final)
        else:
            self.visitStates.append(final)
        return self.visitStates
    
    def findSymbol(self, symbol):
        for s in self.symbol:
            if s == symbol:
                return True
        return False
    
    def findVisited(self, state):
        for vs in self.visitStates:
            if vs == state:
                return True
        return False
    
    def toString(self):
        rt = "State: " + self.state + "\n"
        rt += "CLOSURE(" + str(self.symbol) + ") = {"
        for i in range(0, len(self.visitStates)):
            rt += self.visitStates[i]
            if i < len(self.visitStates)-1: rt += ", "
            else: rt += "}"
        return rt