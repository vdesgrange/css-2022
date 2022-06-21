import numpy as np

from rules import COEFF, STATES

class Device:
    def __init__(self, id):
        self.id = id
        self.state = STATES["S"]
        self.t = 0
        self.tau = 0


    def run(self, n):
        for _ in range(n):
            self.step()

        return

    def get_number_neighboor(self):
        return 0

    def X(self):
        omega = self.get_number_neighboor()
        p =[COEFF["H"] * omega, 1 - COEFF["H"] * omega]
        return np.random.choice(1, None, p=p)

    def Y(self):
        return np.random.choice(2, None, p=[COEFF["A"], COEFF["B"], 1 - COEFF["A"] - COEFF["B"]])

    def Z(self):
        return np.random.choice(1, None, p=[COEFF["Rs"], 1 - COEFF["Rs"]])


    def step(self):
        self.t += 1
        self.tau += 1

        if self.state == STATES["S"] and self.X():
            self.state = STATES["I"]
            self.t = 0
            return

        if self.state == STATES["I"] and self.t > COEFF["T"]:
            y = self.Y()
            if y == 0:
                self.state = STATES["A"]
                self.tau = 0
            elif y == 1:
                self.state = STATES["S"]
            else:
                self.state = STATES["R"]
            return

        if self.state == STATES["A"] and self.tau > COEFF["Tau"]:
            self.t = 0
            self.tau = 0
            z = self.Z()
            if z:
                self.state = STATES["S"]
            else:
                self.state = STATES["R"]
            return

        return
