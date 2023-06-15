import FA
import REtoUNFA
import UNFAtoDFA


exampleRE = open("resource/example_re.txt", 'r', encoding="UTF-8")

i = 0
while True:
    unfaResultFile = open("resource/u-NFA/u-NFA" + str(i) +".txt", 'w', encoding="UTF-8")
    dfaResultFile = open("resource/DFA/DFA" + str(i) +".txt", 'w', encoding="UTF-8")

    regex = exampleRE.readline()
    regex = regex.replace("\n", "")
    if not regex: break

    print("regex:",regex)

    unfaConv = REtoUNFA.UnfaConvertor()
    UNFA = unfaConv.regexToUNFA(regex)
    print(UNFA.toString())
    unfaResultFile.write(UNFA.toString())

    dfaConvertor = UNFAtoDFA.DfaConvertor(UNFA)
    dfa = dfaConvertor.unfaToDfa()
    print(dfa.toString())
    dfaResultFile.write(dfa.toString())
    
    i += 1
    
    unfaResultFile.close()
    dfaResultFile.close()

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
print(UNFA.toString())

dfaConvertor = UNFAtoDFA.DfaConvertor(UNFA)
dfa = dfaConvertor.unfaToDfa()
print(dfa.toString())
'''