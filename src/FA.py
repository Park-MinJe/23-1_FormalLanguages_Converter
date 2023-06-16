import DeltaFunction

class FA:
    '''
    - 유한 오토마타의 내용은 아래 5가지 항목이 순서대로 나와야 함.
    - 각 항목은 아래와 같은 StateSet, TerminalSet, DeltaFunctions, StartState, FinalStateSet 의 키워드로 구분되며, 원소를 표현하기 위한 구분자는 {}를 이용
    - 상태는 q로 시작하고 숫자 3자리로 구성됨
    - 터미널 심볼은 a~z, A~Z, 0~9 로 제한 함
    - 입실론 심볼은 ε를 사용
    - 상태전이함수는 아래 예시와 같이 (상태, 터미널) = { 출력상태1, 출력상태2 } 와 같이 구성됨
    - 시작 상태와 종결 상태는 아래와 같이 임의의 상태, 상태 집합으로 정의함

    ex)
    StateSet = { q000, q001, q002 }

    TerminalSet = { a, b, c, d }

    DeltaFunctions = {
    (q000, a) = {q000, q001, ...}
    (q000, b) = {q000, q002, ...}
    (q001, a) = {q000, q005, ...}
    (q001, ε) = {q000, q001, ...}
    }

    StartState = q000

    FinalStateSet = { q100, q220 }
    '''

    # 초기화
    def __init__(self):
        self.StateSet = []
        self.TerminalSet = []
        self.DeltaFunctions = []
        self.StartState = ""
        self.FinalStateSet = []

    '''
    setter
    '''

    # state 추가
    def addState(self):
        stateSetLen = len(self.StateSet)

        newState = "q"
        if stateSetLen<10: newState += "00"
        elif stateSetLen<100: newState += "0"
        newState += str(stateSetLen)

        self.StateSet.append(newState)

        return newState

    # terminal 추가
    def addTerminal(self, vt):
        if len(self.TerminalSet) > 0:
            isTerminalExist = False
            for t in self.TerminalSet:
                if t == vt: 
                    isTerminalExist = True
                    break
                else: 
                    isTerminalExist = False
            if not isTerminalExist:
                self.TerminalSet.append(vt)
        else:
            self.TerminalSet.append(vt)
        
    # delta function 추가
    def addDeltaFunc(self, df):
        if len(self.DeltaFunctions) > 0:
            isDeltaExist = False
            for d in self.DeltaFunctions:
                if df.preState == d.preState and df.symbol == d.symbol and df.nextStates == d.nextStates:
                    isDeltaExist = True
                    break
                else:
                    isDeltaExist = False
            if not isDeltaExist:
                self.DeltaFunctions.append(df)
            else:
                for ns in df.nextStates:
                    self.addDeltaFuncNextState(df.preState, df.symbol, ns)
        else:
            self.DeltaFunctions.append(df)
    
    # delta function의 next state 추가
    def addDeltaFuncNextState(self, preState, symbol, nextState):
        isDeltaExist, delta = self.findDeltaFunc(preState, symbol)
        if isDeltaExist: 
            if not delta.findNextState(nextState):
                delta.addNextState(nextState)
        return delta

    # start state 정의
    def defStartState(self, state):
        self.StartState = state

    # final state 추가
    def addFinalState(self, state):
        self.FinalStateSet.append(state)

    '''
    getter
    '''

    # delta function 탐색
    def findDeltaFunc(self, preState, symbol):
        for delta in self.DeltaFunctions:
            if delta.preState == preState and delta.symbol == symbol:
                return True, delta
        return False, None
    
    # symbol로 delta function 반환
    def getDeltaFuncBySymbol(self, symbol):
        rt = []
        for df in self.DeltaFunctions:
            if df.symbol == symbol: rt.append(df)
        return rt
    
    # 입력 받은 symbol 제외 delta function 반환
    def getDeltaFuncWithoutSymbol(self, symbol):
        rt = []
        for df in self.DeltaFunctions:
            if df.symbol != symbol: rt.append(df)
        return rt
    
    # print FA as string
    def toString(self):
        rt = "StateSet = { "
        for i in range(0, len(self.StateSet)):
            rt += self.StateSet[i]
            if i < len(self.StateSet)-1: rt += ", "
        rt += " }\n"

        rt += "TerminalSet = { "
        for i in range(0, len(self.TerminalSet)):
            rt += self.TerminalSet[i]
            if i < len(self.TerminalSet)-1: rt += ", "
        rt += " }\n"

        rt += "DeltaFunctions = {\n"
        for df in self.DeltaFunctions:
            rt += "\t" + df.toString() + "\n"
        rt += "}\n"

        rt += "StartState = " + self.StartState + "\n"

        rt += "FinalState = { "
        for i in range(0, len(self.FinalStateSet)):
            rt += self.FinalStateSet[i]
            if i < len(self.FinalStateSet)-1: rt += ", "
        rt += " }\n"

        return rt


# test
#fa = FA()
#for i in range(0,20):
#    fa.addState()
#print(fa.StateSet)
