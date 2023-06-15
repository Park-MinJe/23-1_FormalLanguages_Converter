import FA
import REtoUNFA


exampleRE = open("resource/example_re.txt", 'r', encoding="UTF-8")

i = 0
while True:
    unfaResultFile = open("resource/u-NFA/u-NFA" + str(i) +".txt", 'w', encoding="UTF-8")

    regex = exampleRE.readline()
    regex = regex.replace("\n", "")
    if not regex: break

    print("regex:",regex)

    unfaConv = REtoUNFA.UnfaConvertor()
    UNFA = unfaConv.regex_to_UNFA(regex)
    print(UNFA.toString())
    unfaResultFile.write(UNFA.toString())
    
    i += 1
    
    unfaResultFile.close()

exampleRE.close()


# Example usage
'''
regex = "(a+b)*abb"
unfaConv = REtoUNFA.UnfaConvertor()
UNFA = unfaConv.regex_to_UNFA(regex)
print(UNFA.toString())
unfaResultFile.write(UNFA.toString())
'''