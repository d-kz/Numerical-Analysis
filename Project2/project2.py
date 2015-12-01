import math
import matplotlib.pyplot as plt
import random

def guessU3():
    return 0.1


def guessU5():
    return -0.1

def rk4(q1, q2, q3, q4, q5, h, Pr):
    t = 0.0
    U1plot = []
    U2plot = []
    U3plot = []
    U4plot = []
    U5plot = []
    tplot = []
    while t <= 30:
        #print("t{}: {}".format(t,(q1,q2,q3,q4,q5)))
        U1plot.append(q1)
        U2plot.append(q2)
        U3plot.append(q3)
        U4plot.append(q4)
        U5plot.append(q5)
        tplot.append(t)

        U1k1 = h * U1prime(t, q2)
        U2k1 = h * U2prime(t, q3)
        U3k1 = h * U3prime(t, q1, q2)
        U4k1 = h * U4prime(t, q5)
        U5k1 = h * U5prime(t, q1, q5, Pr)

        U1k2 = h * U1prime(t + (0.5*h), q2 + (0.5*U2k1))
        U2k2 = h * U2prime(t + (0.5*h), q3 + (0.5*U3k1))
        U3k2 = h * U3prime(t + (0.5*h), q1 + (0.5*U1k1), q2 + (0.5*U2k1))
        U4k2 = h * U4prime(t + (0.5*h), q5 + (0.5*U5k1))
        U5k2 = h * U5prime(t + (0.5*h), q1 + (0.5*U1k1), q5 + (0.5*U5k1), Pr)

        U1k3 = h * U1prime(t + (0.5*h), q2 + (0.5*U2k2))
        U2k3 = h * U2prime(t + (0.5*h), q3 + (0.5*U3k2))
        U3k3 = h * U3prime(t + (0.5*h), q1 + (0.5*U1k2), q2 + (0.5*U2k2))
        U4k3 = h * U4prime(t + (0.5*h), q5 + (0.5*U5k2))
        U5k3 = h * U5prime(t + (0.5*h), q1 + (0.5*U1k2), q5 + (0.5*U5k2), Pr)
        
        U1k4 = h * U1prime(t + h, q2 + U2k3)
        U2k4 = h * U2prime(t + h, q3 + U3k3)
        U3k4 = h * U3prime(t + h, q1 + U1k3, q2 + U2k3)
        U4k4 = h * U4prime(t + h, q5 + U5k3)
        U5k4 = h * U5prime(t + h, q1 + U1k3, q5 + U5k3, Pr)
        
        q1 = q1 + (U1k1 + 2*(U1k2 + U1k3) + U1k4)/6.0
        q2 = q2 + (U2k1 + 2*(U2k2 + U2k3) + U2k4)/6.0
        q3 = q3 + (U3k1 + 2*(U3k2 + U3k3) + U3k4)/6.0
        q4 = q4 + (U4k1 + 2*(U4k2 + U4k3) + U4k4)/6.0
        q5 = q5 + (U5k1 + 2*(U5k2 + U5k3) + U5k4)/6.0

        t += h

    return [tplot, U1plot, U2plot, U3plot, U4plot, U5plot]

def U1prime(t,q2):
    return q2

def U2prime(t,q3):
    return q3

def U3prime(t, q1, q2):
    return -1.0/2.0 * q1 * q2

def U4prime(t, q5):
    return q5

def U5prime(t, q1, q5, Pr):
    return -Pr/2.0 * q1 * q5


def part1():
    u3 = 0.59 
    change = [u3, float("inf")]
    der = [0.0,0.0]
    #while abs(change[1] - change[0]) > 0.0000001:
    h = 0.1
    u1 = 0
    u2 = 0
    u4 = 1
    u5 = guessU5()
    Pr = 5
    points = rk4(u1, u2, u3, u4, u5, h, Pr)
    change[0] = u3
    der[0] = der[1]
    der[1] = points[2][-1]
    forceCheck = len(points[2]) - int(random.random() * (50)) - 1
    u3 += -0.01 * (der[1] - der[0]) * (points[2][forceCheck] - 1) 
    change[1] = u3
    print "for {}, change of u:{} ERROR: {}, forceCheck{}".format(u3, (change[1] - change[0]), points[2][-1] - 1, forceCheck)
    
    plt.plot(points[0], points[1], '#ED5377', label="F")
    plt.plot(points[0], points[2], '#FF0000', label="F\'")
    plt.plot(points[0], points[3], '#FFB8B9', label="F\'\'")
    plt.plot(points[0], points[4], '#004746', label="G")
    plt.plot(points[0], points[5], '#799493', label="G\'")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

    return [points[1], points[2], points[0]]



#PART2

def velocities(f, fPrime, tPoints):
    t = 0.0
    V1plot = []
    V2plot = []
    tplot = []

    # v1 = v/Uinf * (x*Re/L)**(1.0/2.0)
    # v2 = u/Uinf
    for i, t in enumerate(tPoints):
        v1 = 1.0/2.0 * (t * fPrime[i] - f[i])
        v2 = fPrime[i]
        V1plot.append(v1)
        V2plot.append(v2)
        tplot.append(t)
        t += h

    plt.plot(tPoints, V1plot, '#ED5377', tPoints, V2plot, '#004746')
    plt.show()

if __name__ == '__main__':
    f, fprime, t = part1()
    velocities(f, fprime, t)


