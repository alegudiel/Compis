"""
Clase para transformar una expresión regular, pasarlo a infix, 
chequear que este balanceada 
y convertirlo a su forma postfix
"""
class InfixToPostfix:
    PRECEDENCE = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}

    def __init__(self, regex):
        self.regex = regex
        self.stack = []
        self.postfix = []
        self.formatted_regex = None

    def isOperator(self, char):
        return char in self.PRECEDENCE.keys() or char in {'(', ')'}

    def isOperand(self, char):
        return char.isalpha() or char.isdigit()
    
    def isBalanced(self):
        stack = []
        for char in self.regex:
            if char == '(' or char == '[' or char == '{' :
                stack.append(char)
            elif char == ')' or char == ']' or char == '}':
                if not stack:
                    return False
                stack.pop()
        return not stack

    def formatRegex(self):
        regex_str = str(self.regex)
        if not self.regex:
            return ''

        allOperators = {'*', '+', '.', '|'}
        binOperators = {'|'}
        res = ''

        i = 0
        while i < len(regex_str):
            c1 = regex_str[i]

            if i+1 < len(regex_str):
                c2 = regex_str[i+1]
            else:
                c2 = ''

            if c2 == '?':
                res += f'({c1}|ε)'
                i += 1 
            elif self.isOperand(c1) and c2 == '+':
                res += c1 + c1
                i += 1 
            else:
                res += c1
                if c1 != '(' and c2 != ')' and c2 not in allOperators and c1 not in binOperators and i != len(regex_str)-1:
                    res += '.'
                if res[-1] == '.' and c2 == '(':
                    res = res[:-1]
            i += 1

        self.formatted_regex = res
        return res

    # Shunting-yard algorithm
    def postfixExp(self):
        if self.postfix:
            return self.postfix
        elif not self.formatted_regex:
            self.formatRegex()

        infixList = list(self.formatted_regex)  
        prec = self.PRECEDENCE
        opStack = []
        postfixList = []

        for token in infixList:
            if token == '(': 
                opStack.append(token)
            elif token == ')':
                while opStack[-1] != '(':
                    postfixList.append(opStack.pop())
                opStack.pop()
            elif token in prec:
                while opStack and opStack[-1] != '(' and prec[token] <= prec[opStack[-1]]:
                    postfixList.append(opStack.pop())
                opStack.append(token)
            else:
                postfixList.append(token)

        while opStack:
            postfixList.append(opStack.pop())

        self.postfix = ''.join(postfixList)
        return self.postfix


    def __str__(self):
        return self.postfix if self.postfix else self.postfixExp()

# if __name__ == '__main__':
#     regex = InfixToPostfix('(a|b)*c').postfixExp()
#     print(regex)