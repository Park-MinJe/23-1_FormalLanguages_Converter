class uClosure:
    '''
    ε-CLOSURE에 대한 정의이다.

    * data
        - state: CLOSURE 연산을 시작할 때의 상태
        - symbol: CLOSURE 연산을 위한 input symbol
        - visitStates: ε을 input symbol로 하여 접근 가능한 상태 집합

    * functions
        - addSymbol(start): ε-CLOSURE 탐색 과정에서 사용된 input symbol 원소로 추가.
        - addSymbolAsArr(start): ε-CLOSURE 탐색 과정에서 사용된 input symbol 배열로 추가. 
        - addvisitStates(final): ε을 input symbol로 하여 접근 가능한 상태 집합에 원소 추가.
        - findSymbol(symbol): Input symbol이 존재하는지 확인
        - findVisited(state): 현재 상태를 입력 받아 ε을 input symbol로 하여 접근 가능한 상태 집합을 반환.
        - toString(): 구조를 문자열로 출력.
    '''
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