import FA
import REtoUNFA

exampleRE = [
    "(a+b)*abb",
    "(b+a(aa*b)*b)*",
    "(b+aa+ac+aaa+aac)*",
    "(1+01)*00(0+1)*",
    "(0+1)*011"
]

exampleRE = open("resource/example_re.txt", 'r', encoding="UTF-8")


# Example usage
i = 0
while True:
    unfaResultFile = open("resource/u-NFA/u-NFA" + str(i) +".txt", 'w', encoding="UTF-8")

    regex = exampleRE.readline()
    if not regex: break
    
    regex = "(a+b)*abb"
    unfaConv = REtoUNFA.UnfaConvertor()
    UNFA = unfaConv.regex_to_UNFA(regex)
    print(UNFA.toString())
    unfaResultFile.write(UNFA.toString())
    
    i += 1
    
    unfaResultFile.close()

exampleRE.close()