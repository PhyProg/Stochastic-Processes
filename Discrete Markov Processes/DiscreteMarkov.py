import numpy
import matplotlib
import matplotsave
import matplotlib.pyplot as plt

const = 100000000000

class Markov_Chain():

    def __init__(self, N):
        self.n = 0
        self.steps = N
        self.total = 0
        self.popul = [0.0 for i in range(self.n)]
        self.rates = [[0.0 for i in range(self.n)] for j in range(self.n)]
        self.times = [0]

    def add(self, popul):
        self.popul.append(popul)
        self.total += popul
        for i in range(self.n):
            self.rates[i].append(0)
        self.n += 1
        self.rates.append([0 for i in range(self.n)])

    def remove(self):
        self.n -= 1
        self.total -= self.popul[self.n]
        self.popul.remove(self.popul[self.n])
        self.rates.remove(self.rates[self.n])
        for i in range(self.n):
            self.rates[i].remove(self.rates[i][self.n])

    def add_rate(self, i, j, rate):
        self.rates[i - 1][j - 1] = rate

    def probabilities(self):
        self.p = [[0 for i in range(self.steps)] for j in range(self.n)]
        for i in range(self.n):
            self.p[i][0] = self.popul[i]/self.total

        for i in range(self.n):
            tot_i = 0
            for j in range(self.n):
                tot_i += self.rates[i][j]
            for j in range(self.n):
                self.rates[i][j] = self.rates[i][j]/tot_i

    def solution(self):
        self.probabilities()

        for k in range(1, self.steps):
            print(self.p)
            self.times.append(k)
            for i in range(self.n):
                for j in range(self.n):
                    self.p[i][k] += self.rates[j][i] * self.p[j][k-1]

    def plot(self):
        for i in range(self.n):
            print(self.times, self.p[i])
            plt.plot(self.times, self.p[i], label=str(i))
        plt.legend()
        plt.show()

    def check(self):
        print(self.popul)
        print(self.rates)

mc = Markov_Chain(100)

def process():
    mc.add(5)
    mc.add(15)
    mc.add(10)
    mc.add_rate(1, 2, 5)
    mc.add_rate(2, 3, 6)
    mc.add_rate(2, 2, 11)
    mc.add_rate(1, 3, 7)
    mc.add_rate(3, 3, 5)
    mc.add_rate(3, 1, 1)


process()

mc.solution()
mc.plot()