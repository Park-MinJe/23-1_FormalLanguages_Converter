import FA
import REtoUNFA
import UNFAtoDFA
import DFAtoReducedDFA


exampleRE = open("../resource/example_re.txt", 'r', encoding="UTF-8")

i = 0
while True:
    regex = exampleRE.readline()
    regex = regex.replace("\n", "")
    if not regex: break

    print("regex:",regex)

    unfaResultFile = open("../resource/u-NFA/u-NFA" + str(i) +".txt", 'w', encoding="UTF-8")
    dfaResultFile = open("../resource/DFA/DFA" + str(i) +".txt", 'w', encoding="UTF-8")
    rdfaResultFile = open("../resource/reduced-DFA/reduced-DFA" + str(i) +".txt", 'w', encoding="UTF-8")

    unfaConv = REtoUNFA.UnfaConvertor()
    UNFA = unfaConv.regexToUNFA(regex)
    print("\n***u-NFA***")
    print(UNFA.toString())
    unfaResultFile.write(UNFA.toString())

    dfaConvertor = UNFAtoDFA.DfaConvertor(UNFA)
    dfa = dfaConvertor.unfaToDfa()
    print("\n***DFA***")
    print(dfa.toString())
    dfaResultFile.write(dfa.toString())

    rdfaConv = DFAtoReducedDFA.ReducedDfaConvertor(dfa)
    rdfa = rdfaConv.dfaToReducedDfa()
    print("\n***reduced DFA***")
    print(rdfa.toString())
    rdfaResultFile.write(rdfa.toString())
    
    i += 1
    
    unfaResultFile.close()
    dfaResultFile.close()
    rdfaResultFile.close()

exampleRE.close()
'''

# Example usage

arr = [
    "(a+b)*abb",
    "(b+a(aa*b)*b)*",
    "(b+aa+ac+aaa+aac)*",
    "(1+01)*00(0+1)*",
    "(0+1)*011"
]

regex = arr[4]
unfaConv = REtoUNFA.UnfaConvertor()
UNFA = unfaConv.regexToUNFA(regex)
print("\n***u-NFA***")
print(UNFA.toString())

dfaConvertor = UNFAtoDFA.DfaConvertor(UNFA)
dfa = dfaConvertor.unfaToDfa()
print("\n***DFA***")
print(dfa.toString())

rdfaConv = DFAtoReducedDFA.ReducedDfaConvertor(dfa)
rdfa = rdfaConv.dfaToReducedDfa()
print("\n***reduced DFA***")
print(rdfa.toString())
'''