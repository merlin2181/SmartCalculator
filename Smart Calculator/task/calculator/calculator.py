import sys


class Calculator:

    def __init__(self):
        self.numbers = None
        self.help = 'This program calculates the total of numbers you enter\n' \
                    'Enter numbers with the following syntax:\n' \
                    '-9 + 10 - 34 - -44\n' \
                    'a double negative "--" will turn into "+"\n' \
                    'example: -4 -- 4 -- -5 will be converted into: -4 + 4 + -5\n' \
                    'if you enter your equation without spaces, the program will just return it.\n' \
                    '"/exit" will quit the program\n' \
                    '"/help" brings up this text.\n'

    def main(self):
        """
        Main method that runs the calculator. It currently prints the sum of user inputted numbers.
        """
        while True:
            flag = True
            self.numbers = input().split()
            for input_ in self.numbers:
                if input_ == '/exit':
                    print('Bye!')
                    sys.exit()
                if input_ == '/help':
                    print(self.help)
                    flag = False
                    break
            if flag:
                if len(self.numbers) == 0:
                    continue
                if len(self.numbers) == 1:
                    print(self.numbers[0])
                else:
                    self.parse_input()
                    self.calculate()

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
