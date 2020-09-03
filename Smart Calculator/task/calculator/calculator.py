from collections import deque
import sys


class Calculator:

    def __init__(self):
        self.numbers = None
        self.help = 'This program calculates the total of the expression you enter\n' \
                    'You are allowed to use "(", ")", "^", "*", "/", "+", "-" operators\n' \
                    'Enter numbers with the following syntax:\n' \
                    '\t-9 + 10 - 34 - -44\n' \
                    '\ta double negative "--" will turn into "+"\n' \
                    '\texample: -4 -- 4 -- -5 will be converted into: -4 + 4 + -5\n' \
                    'You can enter your equation with or without spaces.\n' \
                    'Entering multiple "^", "*" or "/" will result in an "Invalid expression" error\n' \
                    '\tas well as a lack of an opening "(" or closing ")" parenthesis\n' \
                    'This program also handles using variables\n' \
                    'To use this feature, simply enter your variable and its assignment\n' \
                    '\texample: a = 8, m=4, bb = a\n' \
                    '"/exit" will quit the program\n' \
                    '"/help" brings up this text.\n'
        self.variables = {}
        self.operators = ['^', '*', '/', '+', '-']
        self.stack = deque()
        self.postfix = deque()
        self.holding = []
        self.parsing = []

    def main(self):
        """
        Main method that runs the calculator. It currently prints the total of user inputted expression.
        """
        while True:
            self.numbers = ''.join(input().split())
            if self.check_input():
                self.calculate()

    def check_input(self):
        """
        Method that initially checks the user input to see if a command was entered or the correct
        input was entered
        """
        if len(self.numbers) == 0:
            return False
        elif "=" in self.numbers:
            return self.assign_variables()
        else:
            return self.parse_input()

    def parse_input(self):
        """
        Method for checking when the user only enters one item on the command line
        """
        if self.numbers == '/exit':
            print('Bye!')
            sys.exit()
        elif self.numbers == '/help':
            print(self.help)
            return False
        elif self.numbers.startswith("/"):
            print('Unknown command')
            return False
        elif self.numbers.isalpha():
            try:
                print(self.variables[self.numbers])
                return False
            except KeyError:
                print('Unknown variable')
                return False
        else:
            try:
                print(int(self.numbers))
                return False
            except ValueError:
                if self.numbers.isalnum():
                    print('Invalid identifier')
                    return False
                else:
                    self.parse_infix()
                    return True

    def assign_variables(self):
        """
        Method that checks whether a legal variable statement was entered or not.
        """
        if self.numbers.count('=') > 1:
            print('Invalid assignment')
            return False
        index = self.numbers.index('=')
        if self.numbers[:index].isalpha():
            if self.numbers[index + 1:].isdigit():
                self.variables[self.numbers[:index]] = int(self.numbers[index + 1:])
            elif self.numbers[index + 1:].isalpha():
                try:
                    self.variables[self.numbers[:index]] = self.variables[self.numbers[index + 1:]]
                except KeyError:
                    print('Invalid assignment')
            elif not self.numbers[:index].isalpha():
                print('Invalid identifier')
            elif not self.numbers[index + 1:].isalpha() or not self.numbers[index + 1:].isdigit():
                print('Invalid assignment')
        else:
            print('Invalid identifier')
        return False

    def parse_infix(self):
        """
        Method that parses the input from the user and separates it into operands
        and operators.  It then goes to the remove_duplicates() method to remove
        any duplicate '-' or '+' and check for multiple '^', '*' or '/'
        """
        if self.numbers.count('(') == self.numbers.count(')'):
            i = 0
            while i < len(self.numbers):
                if self.numbers[i].isdigit():
                    while i < len(self.numbers) and self.numbers[i].isdigit():
                        self.holding.append(self.numbers[i])
                        i += 1
                    self.parsing.append(''.join(self.holding))
                    self.holding = []
                elif self.numbers[i].isalpha():
                    while i < len(self.numbers) and self.numbers[i].isalpha():
                        self.holding.append(self.numbers[i])
                        i += 1
                    self.parsing.append(''.join(self.holding))
                    self.holding = []
                elif self.numbers[i] == '-':
                    if self.numbers[i + 1].isdigit() and i == 0 or self.operator(self.numbers[i - 1]) or \
                            self.numbers[i - 1] == '(':
                        self.holding.append(self.numbers[i])
                        i += 1
                        while i < len(self.numbers) and self.numbers[i].isdigit():
                            self.holding.append(self.numbers[i])
                            i += 1
                    else:
                        self.holding.append(self.numbers[i])
                        i += 1
                    self.parsing.append(''.join(self.holding))
                    self.holding = []
                else:
                    self.parsing.append(self.numbers[i])
                    i += 1
            self.parsing.append(')')
            self.numbers = self.parsing
            self.parsing = []
            self.remove_duplicates()
            if self.numbers is not None:
                for i in range(len(self.numbers)):
                    try:
                        self.numbers[i] = int(self.numbers[i])
                    except ValueError:
                        continue
                self.convert_to_postfix()
            else:
                print('Invalid expression')
                self.main()
        else:
            print('Invalid expression')
            self.main()

    def remove_duplicates(self):
        """
        Method that parses the user's input, removes duplicate '-' or '+'
        or returns an error message if multiple '*' or '/'
        i.e. 9 +++ 10 -- 8 turns into 9 + 10 + 8
             3 --- 5 turns into 3 - 5
             14        -   12 turns into 14 - 12
        """
        i = 0
        end = len(self.numbers)
        while i < end:
            if self.numbers[i] == '-' and self.numbers[i + 1] == '-':
                self.holding.append(self.numbers.pop(i))
                first_index = i
                while self.numbers[i] == '-':
                    self.holding.append(self.numbers.pop(i))
                if len(self.holding) % 2 == 0:
                    self.holding = '+'
                else:
                    self.holding = '-'
                self.numbers.insert(first_index, self.holding)
                self.holding = []
                end = len(self.numbers)
                i += 1
            elif self.numbers[i] == '+' and self.numbers[i + 1] == '+':
                self.holding.append(self.numbers.pop(i))
                index = i
                while self.numbers[i] == "+":
                    self.numbers.pop(i)
                self.numbers.insert(index, self.holding[0])
                self.holding = []
                end = len(self.numbers)
                i += 1
            elif self.numbers[i] == '*' and self.numbers[i + 1] == '*' or \
                    self.numbers[i] == '/' and self.numbers[i + 1] == '/' or \
                    self.numbers[i] == '^' and self.numbers[i + 1] == '^':
                self.numbers = None
                break
            else:
                i += 1

    def convert_to_postfix(self):
        """
        Method that converts the parsed infix expression into a postfix expression
        """
        self.stack.append('(')
        for item in self.numbers:
            if item == '(':
                self.stack.append(item)
            elif type(item) == int or item.isalpha():
                self.postfix.append(item)
            elif self.operator(item):
                x = self.stack.pop()
                while self.operator(x) and self.precedence(x) >= self.precedence(item):
                    self.postfix.append(x)
                    x = self.stack.pop()
                self.stack.append(x)
                self.stack.append(item)
            elif item == ')':
                x = self.stack.pop()
                while x != '(':
                    self.postfix.append(x)
                    x = self.stack.pop()
            else:
                print('\nInvalid infix Expression.\n')
                break

    def calculate(self):
        """
        Method that calculates the parsed postfix equation and prints out the answer
        to the screen
        """
        for item in self.postfix:
            if item in self.operators:
                b = self.stack.pop()
                a = self.stack.pop()
                if item == '^':
                    self.stack.append(a ** b)
                elif item == '*':
                    self.stack.append(a * b)
                elif item == '/':
                    self.stack.append(a / b)
                elif item == '+':
                    self.stack.append(a + b)
                elif item == '-':
                    self.stack.append(a - b)
            elif type(item) == str:
                try:
                    self.stack.append(self.variables[item])
                except KeyError:
                    print('Unknown variable')
                    self.stack = deque()
                    self.postfix = deque()
                    self.main()
            else:
                self.stack.append(item)
        if type(self.stack[0]) == float:
            if self.stack[0].is_integer():
                self.stack[0] = int(self.stack[0])
        print(self.stack[0])
        self.stack = deque()
        self.postfix = deque()

    def operator(self, item):
        return item in self.operators

    @staticmethod
    def precedence(item):
        if item == '^':
            return 5
        if item in ['*', '/']:
            return 3
        if item in ['+', '-']:
            return 1
        else:
            return 0


if __name__ == '__main__':
    calc = Calculator()
    calc.main()
