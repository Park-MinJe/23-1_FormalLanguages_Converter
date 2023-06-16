

class ReducedDfaConvertor:
    def __init__(self, dfa):
        self.dfa = dfa
        self.states = dfa.StateSet
        self.finalStates = dfa.FinalStateSet
    
    def dfaToReducedDfa(self):
        # 처음에 final, nonfinal로 분할
        final = self.finalStates
        nonfinal = list(set(self.states) - set(self.finalStates))

        print("final:",final)
        print("non-final:",nonfinal)

        # 입력 조건으로 인해 파티션이 생기지 않을 때까지 반복
        '''isPartitionGenerated = True
        while isPartitionGenerated:
            '''