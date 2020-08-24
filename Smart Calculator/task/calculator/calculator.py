import sys


class Calculator:

    def __init__(self):
        self.numbers = None
        self.help = 'This program calculates the total of numbers you enter\n' \
                    'Enter numbers with the following syntax:\n' \
                    '-9 + 10 - 34 - -44\n' \
                    'a double negative "--" will turn into "+"\n' \
                    'example: -4 -- 4 -- -5 will be converted into: -4 + 4 + -5\n' \
                    'if you enter your equation without spaces, the program will print "Invalid expression" error.\n' \
                    '"/exit" will quit the program\n' \
                    '"/help" brings up this text.\n'

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
        elif self.numbers[0] == '/exit':
            print('Bye!')
            sys.exit()
        elif self.numbers[0] == '/help':
            print(self.help)
            return False
        elif self.numbers[0].startswith("/"):
            print('Unknown command')
            return False
        elif len(self.numbers) == 1:
            try:
                print(int(self.numbers[0]))
            except (ValueError, SyntaxError):
                print('Invalid expression')
            finally:
                return False
        return True

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
                    if type(item) == int:
                        continue
                    else:
                        print('Invalid expression')
                        return False
        else:
            print('Invalid expression')
            return False
        return True

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

    def calculate(self):
        """
        Method that calculates the parsed equation and prints the answer
        """
        while len(self.numbers) > 1:
            evaluate = [self.numbers[0], self.numbers[1], self.numbers[2]]
            del self.numbers[:3]
            if '-' in evaluate:
                result = evaluate[0] - evaluate[2]
                self.numbers.insert(0, result)
            elif '+' in evaluate:
                result = evaluate[0] + evaluate[2]
                self.numbers.insert(0, result)
        self.numbers = self.numbers[0]
        print(self.numbers)


if __name__ == '__main__':
    calc = Calculator()
    calc.main()
