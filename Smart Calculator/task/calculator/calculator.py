import sys

class Calculator:

    def __init__(self):
        self.numbers = None
        self.flag = None
        self.help = 'This program calculates the sum of numbers you enter\n' \
                    '"/exit" will quit the program\n' \
                    '"/help" brings up this text.\n'

    def main(self):
        """
        Main method that runs the calculator. It currently prints the sum of user inputted numbers.
        """
        while True:
            self.flag = True
            self.numbers = input('Enter numbers: ').split()
            for input_ in self.numbers:
                if input_ == '/exit':
                    print('Bye!')
                    sys.exit()
                if input_ == '/help':
                    print(self.help)
                    self.flag = False
                    break
                # Makes sure the user enters numbers (1, 823, 7732, etc.) not text
                try:
                    int(input_)
                except ValueError:  # If text is entered, returns error message and starts loop over.
                    print('Please enter numbers only.')
                    print('')
                    self.flag = False
                    break
            if self.flag:
                if len(self.numbers) == 0:
                    continue
                if len(self.numbers) == 1:
                    print(self.numbers[0])
                else:
                    print(sum(int(i) for i in self.numbers))
                    print('')


if __name__ == '__main__':
    calc = Calculator()
    calc.main()
