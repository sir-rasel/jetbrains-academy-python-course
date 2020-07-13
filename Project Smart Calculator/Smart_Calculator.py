from collections import deque

class Smart_Calculator:
    operation_dict = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
        "^": lambda a, b: a ** b
    }
    precedence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "^": 3
    }

    # define constructor
    def __init__(self):
        self.input_status = True
        self.error_message = None
        self.action = None
        self.expression = None
        self.variables = dict()
        self.operations = list()
        self.operations_queue = deque()

    # process the string / main method
    def process_input_expression(self):
        while self.input_status:
            expression = input()
            self.define_operation(expression)
            if self.action == "command":
                if self.expression == "/exit":
                    print('Bye!')
                    self.input_status = False
                elif self.expression == "/help":
                    print('''   The program calculates the expression from input string. 
                                You can use variables.
                                You can Assign variables to others variable.
                                You can check value of a variable by its name.
                        ''')
                else:
                    self.error_message = "Unknown command"
                    print(self.error_message)
            elif self.action == "assign":
                if self.check_assignment():
                    self.assign_value()
                else:
                    print(self.error_message)
            elif self.action == "calculation":
                if self.parse_expression() and self.values_substitution():
                    try:
                        if self.transform_to_postfix_notation():
                            print(int(self.calculate_operations()))
                        else:
                            print(self.error_message)
                    except ValueError:
                        self.error_message = "Invalid expression"
                        print(self.error_message)
                else:
                    print(self.error_message)

    # fill action and expression attributes from the string
    def define_operation(self, expr):
        if len(expr) == 0:
            self.action = "empty"
            self.expression = None
        elif expr[0] == '/':
            self.action = "command"
            self.expression = expr
        elif '=' in expr:
            self.action = 'assign'
            self.expression = expr
        elif self.variables.get(expr):
            self.action = "calculation"
            self.expression = expr
        else:
            self.action = "calculation"
            self.expression = expr

    # return True or False, fill error_message
    def check_assignment(self):
        self.expression = self.expression.replace('=', ' = ')
        self.operations = self.expression.split()
        if len(self.operations) != 3:
            self.error_message = "Invalid assignment"
            return False
        elif not self.operations[0].isalpha():
            self.error_message = "Invalid identifier"
            return False
        elif not (self.operations[2].isalpha() or self.operations[2].isnumeric()):
            self.error_message = "Invalid assignment"
            return False
        elif self.variables.get(self.operations[2]) is None and self.operations[2].isalpha():
            self.error_message = "Unknown variable"
            return False
        return True
    
    # assign variable value
    def assign_value(self):
        self.variables[self.operations[0]] = self.operations[2]

    # brush expression string
    def parse_expression(self):
        if self.expression != None:
            if "**" in self.expression or "//" in self.expression:
                self.error_message = "Invalid expression"
                return False
            self.expression = self.expression.replace("*", " * ")
            self.expression = self.expression.replace("/", " / ")
            self.expression = self.expression.replace("^", " ^ ")
            self.expression = self.expression.replace("(", " ( ")
            self.expression = self.expression.replace(")", " ) ")
            self.operations = [self.reduce_add_sub(token) for token in self.expression.split()]
        return True

    # return string without +- repetitions
    def reduce_add_sub(self, expr):
        if any([True for ch in expr if ch not in "+-="]):
            return expr
        elif len(expr) == 1:
            return expr
        else:
            expr = expr.replace("++", "+")
            expr = expr.replace("+-", "-")
            expr = expr.replace("-+", "-")
            expr = expr.replace("--", "+")
            return self.reduce_add_sub(expr)
    
    # substitute variable variables in operations list
    def values_substitution(self):
        for i in range(len(self.operations)):
            if self.variables.get(self.operations[i]) is not None:
                self.operations[i] = self.variables[self.operations[i]]
            elif self.operations[i].isalpha():
                self.error_message = "Unknown variable"
                return False
        return True
    
    # transform operations list in postfix operations_queue
    def transform_to_postfix_notation(self):
        if self.check_parenthesis():
            que = deque()
            for op in self.operations:
                if op.isnumeric():
                    self.operations_queue.append(int(op))
                elif op == "(":
                    que.append("(")
                elif op == ")":
                    while que[-1] != "(":
                        self.operations_queue.append(que.pop())
                    que.pop()
                elif self.operation_dict.get(op):
                    if len(que) == 0 or que[-1] == "(":
                        que.append(op)
                    elif self.precedence[op] > self.precedence[que[-1]]:
                        que.append(op)
                    elif self.precedence[op] <= self.precedence[que[-1]]:
                        while len(que) > 0:
                            if que[-1] != "(":
                                self.operations_queue.append(que.pop())
                            else:
                                break
                        que.append(op)
            for _ in range(len(que)):
                self.operations_queue.append(que.pop())
            return True
        else:
            self.error_message = "Invalid expression"
            return False

    # check validity of parenthesis in operations list
    def check_parenthesis(self):
        brackets_stack = deque()
        for ch in self.operations:
            if ch == "(":
                brackets_stack.append(ch)
            elif ch == ")":
                if len(brackets_stack) == 0:
                    return False
                brackets_stack.pop()
        if len(brackets_stack) == 0:
            return True
        return False

    # calculate postfix expression
    def calculate_operations(self):
        que = deque()
        for _ in range(len(self.operations_queue)):
            op = self.operations_queue.popleft()
            if type(op) == int:
                que.append(op)
            elif self.operation_dict.get(op):
                a = que.pop()
                b = que.pop()
                res = self.operation_dict[op](b, a)
                que.append(res)
        return que[-1]

if __name__ == '__main__':
    calculator = Smart_Calculator()
    calculator.process_input_expression()
