import sys


class Calculator:

    def __init__(self):
        self.numbers = None
        self.help = 'This program calculates the total of the numbers you enter\n' \
                    'Enter numbers with the following syntax:\n' \
                    '-9 + 10 - 34 - -44\n' \
                    'a double negative "--" will turn into "+"\n' \
                    'example: -4 -- 4 -- -5 will be converted into: -4 + 4 + -5\n' \
                    'if you enter your equation without spaces, the program will print "Invalid expression" error.\n' \
                    'This program also handles using variables\n' \
                    'To use this feature, simply enter your variable and its assignment\n' \
                    'example: a = 8, m=4, bb = a\n' \
                    '"/exit" will quit the program\n' \
                    '"/help" brings up this text.\n'
        self.variables = {}

    def main(self):
        """
        Main method that runs the calculator. It currently prints the total of user inputted numbers.
        """
        while True:
            self.numbers = input().split()
            if self.check_input():
                self.parse_input()
                if self.check_parsed_input():
                    self.calculate()

    def check_input(self):
        """
        Method that initially checks the user input to see if a command was entered or the correct
        input was entered
        """
        if len(self.numbers) == 0:
            return False
        elif len(self.numbers) == 1:
            self.numbers = self.numbers[0]
            self.check_input_length_one()
        elif self.numbers.count('=') > 1:
            print('Invalid assignment')
            return False
        elif 1 < len(self.numbers) <= 3:
            self.check_variable()
            return False
        return True

    def check_input_length_one(self):
        """
        Method for checking when the user only enters one item on the command line
        """
        if self.numbers == '/exit':
            print('Bye!')
            sys.exit()
        elif self.numbers == '/help':
            print(self.help)
        elif self.numbers.startswith("/"):
            print('Unknown command')
        elif '=' in self.numbers:
            self.check_variable()
        else:
            try:
                print(self.variables[self.numbers])
            except KeyError:
                try:
                    print(int(self.numbers))
                except (ValueError, SyntaxError):
                    if not self.numbers.isalpha():
                        print('Invalid identifier')
                    else:
                        print('Unknown Variable')
        self.main()

    def check_variable(self):
        """
        Method that checks whether a legal variable statement was entered or not.
        """
        if "=" not in self.numbers and '+' in self.numbers or '-' in self.numbers:
            self.calculate()
        elif len(self.numbers) == 3 and self.numbers[1] == '=':
            if not self.numbers[0].isalpha():
                print('Invalid identifier')
                self.main()
            elif not self.numbers[2].isdigit() and not self.numbers[2].isalpha():
                print('Invalid assignment')
                self.main()
            else:
                self.dictionary_variable_check(self.numbers[0], self.numbers[2])
        else:
            for i, item in enumerate(self.numbers):
                if i == 0 and len(item) > 1 and item.index('=') != 0:
                    self.dictionary_variable_check(item[:item.index('=')], self.numbers[1])
                elif i == 1 and len(item) > 1 and item.index('=') == 0:
                    self.dictionary_variable_check(self.numbers[0], item[1:])

    def dictionary_variable_check(self, key, value):
        """
        Method that checks the dictionary for any corresponding variable values.
        """
        try:
            self.variables[key] = int(value)
        except ValueError:
            try:
                if self.variables[value]:
                    self.variables[key] = self.variables[value]
            except KeyError:
                print('Unknown variable')
                self.main()

    def parse_input(self):
        """
        Method that parses the user's input into a functional equation
        i.e. 9 +++ 10 -- 8 turns into 9 + 10 + 8
             3 --- 5 turns into 3 - 5
             14        -   12 turns into 14 - 12
        """
        for i, item in enumerate(self.numbers):
            try:
                self.numbers[i] = int(item)
            except ValueError:
                if len(self.numbers[i]) > 1:
                    if '+' in self.numbers[i]:
                        self.numbers[i] = '+'
                    elif len(self.numbers[i]) % 2 == 0:
                        self.numbers[i] = '+'
                    else:
                        self.numbers[i] = '-'

    def check_parsed_input(self):
        """
        Method that checks that the user entered equation is syntactically correct
        """
        if '-' not in self.numbers and '+' not in self.numbers:
            print('Invalid expression')
            return False
        if len(self.numbers) % 2 == 1:
            for i, item in enumerate(self.numbers):
                if i % 2 == 0:
                    try:
                        if type(item) == int or self.variables[item]:
                            continue
                    except ValueError:
                        print('Invalid expression')
                        return False
                    except KeyError:
                        print(f'Unknown variable "{item}" in equation')
                        return False
        else:
            print('Invalid expression')
            return False
        return True

    def calculate(self):
        """
        Method that calculates the parsed equation and prints the answer
        """
        while len(self.numbers) > 1:
            evaluate = [self.numbers[0], self.numbers[1], self.numbers[2]]
            for i, item in enumerate(evaluate):
                if item in self.variables:
                    evaluate[i] = self.variables[item]
            del self.numbers[:3]
            if '-' in evaluate:
                result = evaluate[0] - evaluate[2]
            elif '+' in evaluate:
                result = evaluate[0] + evaluate[2]
            self.numbers.insert(0, result)
        print(self.numbers[0])


if __name__ == '__main__':
    calc = Calculator()
    calc.main()
