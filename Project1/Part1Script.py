import math
import matplotlib.pyplot as plt
import numpy as np

def makeODE(delta):
    ode = lambda sigma, theta: delta * math.exp(theta) - theta
    return ode

def makeInverseODE(delta):
    ode = lambda theta, sigma: 1/(delta * math.exp(theta) - theta)
    return ode

def rk4(f, initX, initY, h, stop, tolerance = False):
    x = initX
    y = initY
    prevY = float("-inf")
    computeRecord = []
    if tolerance:
        condition = lambda currX, currY, lastY: abs(y - lastY) > stop
    else:
        condition = lambda currX, currY, lastY: currX < stop
    while condition(x, y, prevY):
        ks = []
        ks.append(h * f(x, y))
        for i in range(1, 3):
            ks.append(h * f(x + h/2, y + ks[i-1]/2))
        ks.append(h * f(x + h, y + ks[2]))
        computeRecord.append((x, y, ks))
        prevY = y
        y = y + (ks[0] + 2*ks[1] + 2*ks[2] + ks[3])/6
        x += h
    return computeRecord

def secantMethod(f, guess1, guess2, tolerance):
    x_n1 = guess1
    x_n2 = guess2
    computeRecord = [(0, x_n1), (1, x_n2)]
    counter = 2
    while abs((x_n2 - x_n1)/x_n1) > tolerance:
        tmp = x_n2
        x_n2 = x_n2 - f(x_n2, 0)/((f(x_n2, 0) - f(x_n1, 0))/(x_n2 - x_n1))
        computeRecord.append((counter, x_n2))
        counter += 1
        x_n1 = tmp
    return computeRecord


def printResults(results, amountToDisplay=None):
    if amountToDisplay is not None:
        beginning = results[:amountToDisplay/2]
        ending = results[-1 * amountToDisplay/2:]
        printResults(beginning)
        print "..."
        printResults(ending)
        return
    for r in results:
        if isinstance(r, tuple):
            for i in r:
                if isinstance(i, list):
                    for j in i:
                        print j, '&',
                else:
                    print i, '&',
        else:
            print r, '&',
        print '\\'

def getXCoords(points):
    getFirst = lambda x: x[0]
    return map(getFirst, points)

def getYCoords(points):
    getSec = lambda x: x[1]
    return map(getSec, points)

def earlySolution(delta, xs):
    earlyFunc = (lambda sig: (delta/(delta - 1)) * math.exp((delta - 1) * sig)
            - (delta/(delta - 1)))
    return map(earlyFunc, xs)

def earlySolutionInverse(delta, ys):
    earlyFunc = (lambda theta: (1/(delta - 1))
            * np.log((theta + (delta)/(delta - 1))/(delta/(delta - 1))))
    return map(earlyFunc, ys)

if __name__ == '__main__':
    # 1a) Solve ODE through RK4
    ode1 = makeODE(0.2)
    # RK4 with tolerance
    points = rk4(ode1, 0, 0, 0.00001, 10)
    # points = rk4(ode1, 0, 0, 0.001, 0.000001, True)
    # printResults(points, 10)
    
    # 1b) Find theta fizzle with rootfinding
    # printResults(secantMethod(ode1, 0.0018, 0.019, 0.001))
    
    # 1c) Graph Results
    xs = getXCoords(points)
    earlyX = np.arange(0, 3, 0.00001)
    fizzleLine = lambda x: [0.259 for _ in range(len(xs))]
    eqnPlot, = plt.plot(xs, getYCoords(points), 'k')
    earlySoln, = plt.plot(earlyX, earlySolution(0.2, earlyX), 'r-')
    fizzL, = plt.plot(xs, fizzleLine(xs), 'b--')
    plt.legend([eqnPlot, earlySoln, fizzL],
            ["Integrated ODE", "Early Solution", r'$\theta_{fizzle}$'],
            loc=4)
    plt.xlabel(r'$\sigma$')
    plt.ylabel(r'$\theta$')
    plt.title(r'$\theta$ vs $\sigma$')
    plt.show()
