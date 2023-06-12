class State:
    def __init__(self, label=None):
        self.label = label
        self.transitions = []
    
    def toString(self):
        rt = "{ " + self.label
        for t in self.transitions:
            rt += t
        rt += " }"
        return rt


def regex_to_UNFA(regex):
    postfix = infix_to_postfix(regex)
    print(postfix)
    stack = []

    for token in postfix:
        if token.isalpha() or token.isdigit():
            state = State(token)
            stack.append(state)
        elif token == "•":
            state2 = stack.pop()
            state1 = stack.pop()
            new_state = State()
            new_state.transitions.append((state1, epsilon))
            new_state.transitions.append((state2, epsilon))
            stack.append(new_state)
        elif token == "*":
            state = stack.pop()
            new_state = State()
            new_state.transitions.append((state, epsilon))
            new_state.transitions.append((new_state, epsilon))
            stack.append(new_state)
        
        stack_content = ""
        for st in stack:
            stack_content += st.toString()
        print(stack_content)

    if len(stack) != 1:
        raise Exception("Invalid regular expression")

    start_state = stack.pop()
    final_state = State()  # Create a new final state
    UNFA = {
        "start": start_state,
        "final": final_state
    }

    return UNFA


def infix_to_postfix(regex):
    precedence = {
        "+": 3,
        "•": 2,
        "*": 1,
        "(": 0
    }
    postfix = []
    stack = []

    for token in regex:
        if token.isalpha() or token.isdigit():
            postfix.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()  # Discard "("
        else:
            while stack and stack[-1] != "(" and precedence[stack[-1]] >= precedence[token]:
                postfix.append(stack.pop())
            stack.append(token)

    while stack:
        postfix.append(stack.pop())

    return postfix


# Example usage
regex = "(a+b)*abb"
UNFA = regex_to_UNFA(regex)
print(UNFA)
