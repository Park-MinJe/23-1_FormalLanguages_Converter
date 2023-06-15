import FA
import REtoUNFA

# Example usage
regex = "(a+b)*abb"
unfaConv = REtoUNFA.UnfaConvertor()
UNFA = unfaConv.regex_to_UNFA(regex)
print(UNFA.toString())