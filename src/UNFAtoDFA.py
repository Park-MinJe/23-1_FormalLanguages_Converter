from FA import FA
from Closure import uClosure
from DeltaFunction import DeltaFunction
import REtoUNFA     # for test

class DfaConvertor:
    '''
    입력 받은 data를 DFA로 변환한다.

    * data
        - unfa: 입력 받은 ε-NFA
        - upsilonDeltaFuncs: unfa의 Delta Function 중 ε을 입력값으로 하는 것을 추출한다.
                            이는 ε-CLOSURE 탐색 시 ε으로 접근할 수 있는 다른 상태를 탐색하는 데 사용한다.
        - nonUpsilonDeltaFuncs: unfa의 Delta Function 중 ε을 입력값으로 하지 않는 것을 추출한다.
                            이는 입력값에 대해 ε-CLOSURE의 우항을 연산하기 위해 사용한다.

    * functions
        - unfaToDfa(): DFA를 입력 받아 ε-NFA로 변환한다.
        - searchUpsilonClosure(states): ε-CLOSURE를 찾는다.
        - searchNextSymbolSet(closure): ε-CLOSURE을 찾기 위해 ε으로 접근할 수 있는 다른 상태를 탐색한다.
    '''
    def __init__(self, unfa):
        self.unfa = unfa
        self.upsilonDeltaFuncs = unfa.getDeltaFuncBySymbol("ε")
        self.nonUpsilonDeltaFuncs = unfa.getDeltaFuncWithoutSymbol("ε")

        self.dfa = FA()
        #self.dfa.TerminalSet = unfa.TerminalSet

    def unfaToDfa(self):
        
        # printing upsilon delta functions test
        rt = "upsilon delta functions = {\n"
        for df in self.upsilonDeltaFuncs:
            rt += "\t" + df.toString() + "\n"
        rt += "}"
        print(rt)

        # printing delta functions upsilon with out upsilon test
        rt = "delta functions upsilon with out upsilon = {\n"
        for df in self.nonUpsilonDeltaFuncs:
            rt += "\t" + df.toString() + "\n"
        rt += "}"
        print(rt)
        
        uClosureStack = []
        uClosureRepo = []

        if len(self.upsilonDeltaFuncs) > 0:
            startState = self.unfa.StartState
            
            # 입실론으로 방문할 수 있는 state로 입실론 closure 생성
            startClosure = self.searchUpsilonClosure([startState])
            startClosure.state = self.dfa.addState()
            uClosureStack.append(startClosure)
            uClosureRepo.append(startClosure)
            
            while len(uClosureStack) > 0:
                closure = uClosureStack.pop()
                print(closure.toString())

                # {...'terminal': ['q001', ...]...}
                nextSymbols = self.searchNextSymbolSet(closure)
                print(nextSymbols)

                # nextSymbols를 이용해 다음 입실론 closure 구하기
                for vt in self.unfa.TerminalSet:
                    nextSymbolsByVt = nextSymbols[vt]
                    if len(nextSymbolsByVt) > 0:
                        newClosure = self.searchUpsilonClosure(nextSymbolsByVt)

                        # 기존에 존재하는 상태인지 확인
                        isStateExist = False
                        for rc in uClosureRepo:
                            if newClosure.visitStates == rc.visitStates:
                                isStateExist = True
                                newClosure.state = rc.state
                                break
                        if not isStateExist:
                            newClosure.state = self.dfa.addState()
                            uClosureStack.append(newClosure)
                            uClosureRepo.append(newClosure)
                            print(newClosure.toString())

                        self.dfa.addTerminal(vt)
                        self.dfa.addDeltaFunc(DeltaFunction(closure.state, vt, newClosure.state))
                        print(self.dfa.toString())
            
            # uClosureStack 내용 확인
            print("\n***uClosureStack 내용 확인***")
            for uc in uClosureStack:
                print(uc.toString())
            
            # 생성된 입실론 closure 출력
            print("\n***생성된 입실론 closure***")
            for uc in uClosureRepo:
                print(uc.toString())

                for vs in uc.visitStates:
                    if vs == self.unfa.StartState:
                        self.dfa.defStartState(uc.state)
                    for fs in self.unfa.FinalStateSet:
                        if vs == fs:
                            self.dfa.addFinalState(uc.state)


            return self.dfa
            
        else:
            return self.unfa
    
    def searchUpsilonClosure(self, states):
        closure = uClosure()
        visitStack = []
        for s in states:
            closure.addSymbol(s)
            closure.addvisitStates(s)
            visitStack.append(s)

        while len(visitStack) > 0:
            symbol = visitStack.pop()
            for udf in self.upsilonDeltaFuncs:
                if udf.preState == symbol:
                    for ns in udf.nextStates:
                        closure.addvisitStates(ns)
                        
                        exist = False
                        for stack in visitStack:
                            if stack == ns:
                                exist = True
                                break
                            else: exist = False
                        if not exist:
                            visitStack.append(ns)
        return closure
    
    def searchNextSymbolSet(self, closure):
        nextSymbolsDict = {}
        for vt in self.unfa.TerminalSet:
            nextSymbols = []
            for vs in closure.visitStates:
                for df in self.nonUpsilonDeltaFuncs:
                    if df.preState == vs and df.symbol == vt:
                        for ns in df.nextStates:
                            exist = False
                            for symbol in nextSymbols:
                                if symbol == ns:
                                    exist = True
                                    break
                                else: exist = False
                            if not exist:
                                nextSymbols.append(ns)
            nextSymbolsDict[vt] = nextSymbols

        return nextSymbolsDict