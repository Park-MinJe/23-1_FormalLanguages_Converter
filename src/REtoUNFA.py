from FA import FA
from DeltaFunction import DeltaFunction

class N:
    def __init__(self, start, final):
        self.startState = start
        self.finalState = final

class UnfaConvertor:
    def __init__(self):
        self.unfa = FA()
        self.NsStack = []

    def regexToUNFA(self, regex):
        postfix = self.infixToPostfix(regex)
        print(postfix)

        for token in postfix:
            #print()
            if token.isalpha() or token.isdigit():
                #print("terminal")
                self.vtSymbol(token)
                
            elif token == "+":
                #print("+ operand")
                self.plusOperand()

            elif token == "•":
                #print("• operand")
                self.dotOperand()
                
            elif token == "*":
                #print("* operand")
                self.starOperand()
            #print(self.NsStack)

        if len(self.NsStack) != 1:
            raise Exception("Invalid regular expression")

        finalN = self.NsStack.pop()
        self.unfa.defStartState(finalN.startState)
        self.unfa.addFinalState(finalN.finalState)

        return self.unfa


    def infixToPostfix(self, regex):
        precedence = {
            "+": 3,
            "•": 2,
            "*": 1,
            "(": 0
        }
        postfix = []
        stack = []

        for i in range(0, len(regex)):
            if regex[i].isalpha() or regex[i].isdigit():
                if i-1 > 0:
                    if regex[i-1] != "+" and regex[i-1] != "•" and regex[i-1] != "(":
                        while stack and stack[-1] != "(" and precedence[stack[-1]] < precedence["•"]:
                            postfix.append(stack.pop())
                        if stack and stack[-1] != "(" and precedence[stack[-1]] == precedence["•"]:
                            postfix.append(stack.pop())
                        stack.append("•")
                postfix.append(regex[i])
            elif regex[i] == "(":
                if i-1 > 0:
                    if regex[i-1] != "+" and regex[i-1] != "•" and regex[i-1] != "(":
                        while stack and stack[-1] != "(" and precedence[stack[-1]] < precedence["•"]:
                            postfix.append(stack.pop())
                        if stack and stack[-1] != "(" and precedence[stack[-1]] == precedence["•"]:
                            postfix.append(stack.pop())
                        stack.append("•")
                stack.append(regex[i])
            elif regex[i] == ")":
                while stack and stack[-1] != "(":
                    postfix.append(stack.pop())
                stack.pop()  # Discard "("
            else:
                while stack and stack[-1] != "(" and precedence[stack[-1]] <= precedence[regex[i]]:
                    postfix.append(stack.pop())
                stack.append(regex[i])
            print("\ntoken:",regex[i])
            print("stack:",stack)
            print("postfix:",postfix)

        while stack:
            postfix.append(stack.pop())
            print("\ntoken:",regex[i])
            print("stack:",stack)
            print("postfix:",postfix)

        return postfix
    
    def defDeltaFunc(self, start, symbol, final):
        isDeltaExist, delta = self.unfa.findDeltaFunc(start, symbol)
        if isDeltaExist:
            delta = self.unfa.addDeltaFuncNextState(start, symbol, final)
        else:
            delta = DeltaFunction(start, symbol, final)
            self.unfa.addDeltaFunc(delta)

    def vtSymbol(self, token):
        state1 = self.unfa.addState()
        state2 = self.unfa.addState()

        self.unfa.addTerminal(token)

        self.defDeltaFunc(state1, token, state2)
        
        self.NsStack.append(N(state1, state2))
    
    def plusOperand(self):
        state1 = self.unfa.addState()
        state2 = self.unfa.addState()

        Ns = []
        Ns.append(self.NsStack.pop())
        Ns.append(self.NsStack.pop())
        
        for n in Ns:
            self.defDeltaFunc(state1, "ε", n.finalState)
        
        for n in Ns:
            self.defDeltaFunc(n.startState, "ε", state2)

        self.NsStack.append(N(state1, state2))

    def dotOperand(self):
        n2 = self.NsStack.pop()
        n1 = self.NsStack.pop()
        
        self.defDeltaFunc(n1.finalState, "ε", n2.startState)

        self.NsStack.append(N(n1.startState, n2.finalState))
    
    def starOperand(self):
        state1 = self.unfa.addState()
        state2 = self.unfa.addState()

        n = self.NsStack.pop()
        
        self.defDeltaFunc(state1, "ε", n.startState)
        self.defDeltaFunc(state1, "ε", state2)
        self.defDeltaFunc(n.finalState, "ε", n.startState)
        self.defDeltaFunc(n.finalState, "ε", state2)

        self.NsStack.append(N(state1, state2))