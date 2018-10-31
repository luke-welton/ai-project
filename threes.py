import random
from math import log


class Tile:
    def __init__(self, max_value):
        self.value = 0
        r = random.random()

        if r > 2/3:
            self.value = 2
        elif r > 1/3:
            self.value = 1
        else:
            self_max = max_value / 2
            num_vals = int(log(self_max / 3, 2))
            divisor = 2 ** num_vals - 1  # sum of 2^n for all n < num_vals

            for i in range(num_vals):
                if r < (2 ** i) / divisor * 1/3:
                    self.value = 3 * 2 ** (num_vals - i)
                    break

            # if the value should be 3, then it will currently be 0
            if self.value == 0:
                self.value = 3


def main():
    random.seed()
    for i in range(100):
        t = Tile(3 * 2 ** random.randint(0, 10))
        print(t.value)


if __name__ == "__main__":
    main()
