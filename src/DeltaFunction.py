class DeltaFunction:
    '''
    FA의 Delta Function을 정의.

    * data
        - preState: 연산을 시작할 때의 상태
        - symbol: 연산을 위한 input symbol
        - nextStates: input symbol로 하여 접근 가능한 상태 집합

    * functions
        - findNextState(nextState): 상태를 입력으로 받아 다음 상태에 존재하는지 확인한다.
        - addNextState(nextState): 상태를 입력 받아 다음 상태에 추가한다.
        - toString(self): 구조를 문자열로 출력.
    '''
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
            rt += str(self.nextStates[i])
            if i < len(self.nextStates)-1: rt += ", "
            else: rt += "}"
        
        return rt