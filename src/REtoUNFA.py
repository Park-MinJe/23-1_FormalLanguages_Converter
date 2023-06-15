import FA
import DeltaFunction

class N:
    def __init__(self, start, final):
        self.startState = start
        self.finalState = final

class UnfaConvertor:
    def __init__(self):
        self.fa = FA.FA()
        self.NsStack = []

    def regex_to_UNFA(self, regex):
        postfix = self.infix_to_postfix(regex)
        print(postfix)

        for token in postfix:
            print()
            if token.isalpha() or token.isdigit():
                print("terminal")
                self.vtSymbol(token)
                
            elif token == "+":
                print("+ operand")
                self.plusOperand()

            elif token == "•":
                print("• operand")
                self.dotOperand()
                
            elif token == "*":
                print("* operand")
                self.starOperand()
            print(self.NsStack)

        if len(self.NsStack) != 1:
            raise Exception("Invalid regular expression")

        finalN = self.NsStack.pop()
        self.fa.defStartState(finalN.startState)
        self.fa.addFinalState(finalN.finalState)

        return self.fa


    def infix_to_postfix(self, regex):
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
                '''if i+1 < len(regex):
                    if regex[i+1].isalpha() or regex[i+1].isdigit():
                        while stack and stack[-1] != "(" and precedence[stack[-1]] < precedence["•"]:
                            postfix.append(stack.pop())
                        stack.append("•")
                        
                        if postfix[len(postfix) - 1].isalpha() or postfix[len(postfix) - 1].isdigit():
                            if stack and stack[-1] != "(" and precedence[stack[-1]] == precedence["•"]:
                                postfix.append(regex[i])
                                postfix.append(stack.pop())
                        else: postfix.append(regex[i])
                    else:
                        postfix.append(regex[i])
                else:
                    postfix.append(regex[i])'''
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
        isDeltaExist, delta = self.fa.findDeltaFunc(start, symbol)
        if isDeltaExist:
            delta = self.fa.addDeltaFuncNextState(start, symbol, final)
        else:
            delta = DeltaFunction.DeltaFunction(start, symbol, final)
            self.fa.addDeltaFunc(delta)

    def vtSymbol(self, token):
        state1 = self.fa.addState()
        state2 = self.fa.addState()

        self.fa.addTerminal(token)

        self.defDeltaFunc(state1, token, state2)
        
        self.NsStack.append(N(state1, state2))
    
    def plusOperand(self):
        state1 = self.fa.addState()
        state2 = self.fa.addState()

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
        state1 = self.fa.addState()
        state2 = self.fa.addState()

        n = self.NsStack.pop()
        
        self.defDeltaFunc(state1, "ε", n.startState)
        self.defDeltaFunc(state1, "ε", state2)
        self.defDeltaFunc(n.finalState, "ε", n.startState)
        self.defDeltaFunc(n.finalState, "ε", state2)

        self.NsStack.append(N(state1, state2))