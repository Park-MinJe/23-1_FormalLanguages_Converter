from FA import FA
from Closure import uClosure
from DeltaFunction import DeltaFunction
import REtoUNFA     # for test

class DfaConvertor:
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

                # {...'terminal': ['q001', ...]...}
                nextSymbols = self.searchNextSymbolSet(closure)

                # nextSymbols를 이용해 다음 입실론 closure 구하기
                for vt in self.unfa.TerminalSet:
                    nextSymbolsByVt = nextSymbols[vt]
                    if len(nextSymbolsByVt) > 0:
                        newClosure = self.searchUpsilonClosure(nextSymbolsByVt)
                        newClosure.state = self.dfa.addState()
                        uClosureStack.append(newClosure)
                        uClosureRepo.append(newClosure)

                        self.dfa.addTerminal(vt)
                        self.dfa.addDeltaFunc(DeltaFunction(closure.state, vt, newClosure.state))
            
            # 생성된 입실론 closure 출력
            print("***생성된 입실론 closure***")
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
                        nextSymbols = []
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