from FA import FA
from DeltaFunction import DeltaFunction

class ReducedDfaConvertor:
    '''
    Reduced DFA로의 변환기

    * data
        - dfa: 입력으로 받은 DFA
        - rdfa: 출력할 reduced DFA

    * functions
        - dfaToReducedDfa(): 입력 받은 DFA를 reduced DFA로 반환한다.
        - firstSplit(): Minimization of FA의 첫 번째 과정으로 final state set과 non-final state set으로 split한다.
        - calcDeltaFunc(partitions): partitions에 대해 Delta Function을 연산한다.
        - calcNewPartition(partitions, resultByPartition): Partition이 가능할 때 다음 partition을 진행한다.
    '''
    def __init__(self, dfa):
        self.dfa = dfa
        self.states = dfa.StateSet
        self.finalStates = dfa.FinalStateSet

        self.rdfa = FA()
        self.rdfa.TerminalSet = dfa.TerminalSet
    
    def dfaToReducedDfa(self):
        # 처음에 final, nonfinal로 분할
        partitions = self.firstSplit()

        print("***Initial Partitions***")
        print(partitions)

        # 입력 조건으로 인해 파티션이 생기지 않을 때까지 반복
        isPartitionOccured = True
        while isPartitionOccured:
            # 상태별로 입력값에 의한 결과 도출
            resultByPartition = self.calcDeltaFunc(partitions)
            print("\n***Propagation Results***")
            print(resultByPartition)

            # 상태별로 분리될 partition이 존재하는지 찾고 있다면 분리
            isPartitionOccured, partitions = self.calcNewPartition(partitions, resultByPartition)

            print("\n***Partition by Results***")
            print(partitions)
        
        resultByPartition = self.calcDeltaFunc(partitions)
        print("\n***Final Results***")
        print(resultByPartition)

        for parentKey in resultByPartition.keys():
            for firstChildKey in resultByPartition[parentKey].keys():
                # Start State 정의
                if firstChildKey == self.dfa.StartState:
                    self.rdfa.defStartState(parentKey)
                # Final States 정의
                if firstChildKey in self.dfa.FinalStateSet:
                    self.rdfa.addFinalState(parentKey)
                # Delta functions 정의
                for secondChildKey in resultByPartition[parentKey][firstChildKey].keys():
                    self.rdfa.addDeltaFunc(DeltaFunction(parentKey, secondChildKey, 
                                                         resultByPartition[parentKey][firstChildKey][secondChildKey]))
        
        return self.rdfa
    
    # 첫 partition. Final set과 non-final set으로 나눈다.
    def firstSplit(self):
        final = self.finalStates
        nonfinal = list(set(self.states) - set(self.finalStates))

        print("final:",final)
        print("non-final:",nonfinal)

        partitions = {}
        partitions[self.rdfa.addState()] = final
        partitions[self.rdfa.addState()] = nonfinal

        return partitions
    
    # input에 따른 출력 연산
    def calcDeltaFunc(self, partitions):
        partitionKeys = partitions.keys()
        resultByPartition = {}
        for pk in partitionKeys:
            outputByPreState = {}
            for preSt in partitions[pk]:
                resultByVt = {}
                for vt in self.rdfa.TerminalSet:
                    dfExist, delta = self.dfa.findDeltaFunc(preSt, vt)
                    if dfExist: resultByVt[vt] = [k for k, v in partitions.items() if delta.nextStates[0] in v][0]
                outputByPreState[preSt] = resultByVt
            resultByPartition[pk] = outputByPreState
        
        return resultByPartition
    
    # 연산 결과에 따른 재 partitions
    def calcNewPartition(self, partitions, resultByPartition):
        partitionKeys = partitions.keys()
        partitions = {}
        for parentKey in partitionKeys:
            resultSets = []
            for childKey, value in resultByPartition[parentKey].items():
                isExist = False
                for rs in resultSets:
                    if rs == value:
                        isExist = True
                        break
                if not isExist:
                    resultSets.append(value)

            if len(resultSets) > 1:
                isPartitionOccured = True
                partitions[parentKey] = [k for k, v in resultByPartition[parentKey].items() if v == resultSets[0]]
                for i in range(1, len(resultSets)):
                    partitions[self.rdfa.addState()] = [k for k, v in resultByPartition[parentKey].items() if v == resultSets[i]]
            else:
                isPartitionOccured = False
                partitions[parentKey] = [k for k, v in resultByPartition[parentKey].items()]
        
        return isPartitionOccured, partitions