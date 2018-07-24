import numpy
import matplotlib
#import matplotsave
import matplotlib.pyplot as plt

const = 100000000000

class Master:

    def __init__(self, N, t_end):
        self.num = 0
        self.pos = 0
        self.t_end = t_end*const
        self.dt = 0.01*const

        self.popul = [0.0 for i in range(N)]
        self.rates = [[0.0 for i in range(N)] for j in range(N)]
        self.graph = [[0.0 for i in range(int(self.t_end/self.dt))] for k in range(N)]
        self.times = []
        self.rates_t = [[[0 for i in range(N)] for j in range(N)] for t in range(int(self.t_end*const/self.dt*const))]

        self.reservoir_in = []
        self.reservoir_in_pos = []
        self.reservoir_out = []
        self.reservoir_out_pos = []

    def add(self, value):
        self.popul[self.num] = float(value)
        self.num += 1

    def rate(self, i, j, rate):
        self.rates[i-1][j-1] = float(rate)

    def _reservoir_in_(self, i, rate):
        self.reservoir_in.append(rate)
        self.reservoir_in_pos.append(i-1)

    def _reservoir_out_(self, i, rate):
        self.reservoir_out.append(rate)
        self.reservoir_out_pos.append(i-1)

    def rate_t_manual(self, i, j, rate):
        for t in range(int(self.t_end/self.dt)):
            self.rates_t[i][j][t] = rate[t]

    def rate_t_function(self, i, j, rate_f):
        for t in range(int(self.t_end*const/self.dt*const)):
            self.rates_t[i][j][t] = rate_f(t)

    def rate_const_to_t(self):
        for i in range(self.num):
            print(i)
            for j in range(self.num):
                for t in range(int(self.t_end / self.dt)):
                    self.rates_t[i][j][t] = self.rates[i][j]


    def solve_ME(self):
        t = 0.0
        while (t < self.t_end):
            self.times.append(float(t/const))

            for i in range(len(self.reservoir_in_pos)):
                self.popul[self.reservoir_in_pos[i]] += self.reservoir_in[i] * self.dt / const

            for i in range(len(self.reservoir_out_pos)):
                if (self.popul[self.reservoir_out_pos[i]] >= self.reservoir_out[i] * self.dt / const):
                    self.popul[self.reservoir_out_pos[i]] -= self.reservoir_out[i] * self.dt / const
                else:
                    self.popul[self.reservoir_out_pos[i]] = 0

            for i in range(self.num):
                #plt.scatter(t,self.popul[i])
                for j in range (self.num):
                    self.popul[i] -= self.rates[i][j] * self.popul[i] * self.dt / const
                    self.popul[i] += self.rates[j][i] * self.popul[j] * self.dt / const

            t += self.dt
            print(t)
            self.add_plot()

        print("solved")

    def solve_ME_t(self):
        t = 0.0
        print("resavam")
        self.rate_const_to_t()
        while (t < self.t_end):
            self.times.append(float(t / const))
            for i in range(self.num):
                # plt.scatter(t,self.popul[i])
                for j in range(self.num):
                    self.popul[i] -= self.rates_t[i][j][int(t/const)] * self.popul[i] * self.dt / const
                    self.popul[i] += self.rates_t[j][i][int(t/const)] * self.popul[j] * self.dt / const
            t += self.dt
            print(t)
            self.add_plot()

        print("solved")

    def add_plot(self):
        for i in range(self.num):
            self.graph[i][self.pos] = self.popul[i]
        self.pos += 1

    def plot(self):
        print("grafik")
        for i in range(self.num):
            plt.plot(self.times, self.graph[i], label=str(i+1))
        plt.legend()
        plt.show()



    def reset(self):
        self.num = 0
        self.popul = [0]
        self.rates = [[0]]

    def check(self):
        print("Values:")
        for i in range(self.num):
            print(self.popul[i])

        print("Rates")
        for i in range(self.num):
            for j in range(self.num):
                print(str(i)+str(j)+str(self.rates[i][j]))


#print("poceo")

m = Master(2,1)

def ispitni_zadatak():
    m.add(0.4)
    m.add(0)
    m.add(0)
    m.add(0.6)
    m.add(0)
    m.add(0)
    m.rate(1, 2, 1)
    m.rate(2, 1, 1)
    m.rate(4, 5, 1)
    m.rate(5, 4, 1)
    m.rate(2, 3, 0.8)
    m.rate(5, 6, 0.8)
    m.rate(3, 6, 0.6)
    m.rate(6, 3, 0.6)

def chain_reservoir():

    m.add(1)
    m.add(0)
    m.add(0)
    m.add(0)
    m.add(0)
    m.rate(1, 2, 1)
    m.rate(2, 3, 1)
    m.rate(3, 4, 1)
    m.rate(4, 5, 1)
    m._reservoir_in_(1, 10)
    m._reservoir_out_(4, 1000)

#print("radi")

m.check()
m.solve_ME_t()
m.plot()

