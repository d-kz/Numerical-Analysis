import math
import matplotlib.pyplot as plt
import random


def rk4(q1, q2, q3, q4, q5, h, Pr, timeMax):
    t = 0.0
    U1plot = []
    U2plot = []
    U3plot = []
    U4plot = []
    U5plot = []
    tplot = []
    while t <= timeMax:
        #print("t{}: {}".format(t,(q1,q2,q3,q4,q5)))
        U1plot.append(q1)
        U2plot.append(q2)
        U3plot.append(q3)
        U4plot.append(q4)
        U5plot.append(q5)
        tplot.append(t)

        U1k1 = h * U1prime(t, q2)
        U2k1 = h * U2prime(t, q3)
        U3k1 = h * U3prime(t, q1, q3)
        U4k1 = h * U4prime(t, q5)
        U5k1 = h * U5prime(t, q1, q5, Pr)

        U1k2 = h * U1prime(t + (0.5*h), q2 + (0.5*U2k1))
        U2k2 = h * U2prime(t + (0.5*h), q3 + (0.5*U3k1))
        U3k2 = h * U3prime(t + (0.5*h), q1 + (0.5*U1k1), q3 + (0.5*U3k1))
        U4k2 = h * U4prime(t + (0.5*h), q5 + (0.5*U5k1))
        U5k2 = h * U5prime(t + (0.5*h), q1 + (0.5*U1k1), q5 + (0.5*U5k1), Pr)

        U1k3 = h * U1prime(t + (0.5*h), q2 + (0.5*U2k2))
        U2k3 = h * U2prime(t + (0.5*h), q3 + (0.5*U3k2))
        U3k3 = h * U3prime(t + (0.5*h), q1 + (0.5*U1k2), q3 + (0.5*U3k2))
        U4k3 = h * U4prime(t + (0.5*h), q5 + (0.5*U5k2))
        U5k3 = h * U5prime(t + (0.5*h), q1 + (0.5*U1k2), q5 + (0.5*U5k2), Pr)
        
        U1k4 = h * U1prime(t + h, q2 + U2k3)
        U2k4 = h * U2prime(t + h, q3 + U3k3)
        U3k4 = h * U3prime(t + h, q1 + U1k3, q3 + U3k3)
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

def U3prime(t, q1, q3):
    return -1.0/2.0 * q1 * q3

def U4prime(t, q5):
    return q5

def U5prime(t, q1, q5, Pr):
    return -Pr/2.0 * q1 * q5


def part1F(h, u1, u2, u3, u4, u5, t, Pr):
    change = [u3, float("inf")]
    while abs(change[1] - change[0]) > 0.00000001:
        points = rk4(u1, u2, u3, u4, u5, h, Pr, t)
        change[0] = u3
        lastEl = len(points[2]) - 1
        u3 += -0.01 * (points[2][lastEl] - 1) #gradient descent'ish
        change[1] = u3
        print "for {}, change of u:{} ERROR: {}".format(u3, (change[1] - change[0]), points[2][-1] - 1)
    
    plt.plot(points[0], points[1], '#ED5377', label="F")
    plt.plot(points[0], points[2], '#FF0000', label="F\'")
    plt.plot(points[0], points[3], '#FFB8B9', label="F\'\'")
    plt.title('Graphs of F, F\', F\'\'')
    plt.xlabel('$\eta_t$')
    plt.legend(bbox_to_anchor=(0., 1), loc=2, borderaxespad=0.)
    plt.show()


def part1G(h, u1, u2, u3, u4, u5, t, Pr):
    change = [u5, 0]
    while abs(change[1] - change[0]) > 0.00000001:
        points = rk4(u1, u2, u3, u4, u5, h, Pr, t)
        change[0] = u5
        if Pr == 0.2:
            u5 += -0.01 * (points[4][250])
        else:
            u5 += -0.01 * (points[4][100])  #gradient descent'ish, top at 100, because u5 explodes in RK-4 with small values
        change[1] = u5
        print "for {}, change of u:{} ERROR: {}".format(u5, (change[1] - change[0]), points[5][-1])

    plt.title(str(Pr) + '   Graphs of v, u\'')
    plt.plot(points[0], points[4], '#004746', label="G")
    plt.plot(points[0], points[5], '#799493', label="G\'")
    plt.xlabel('$\eta_t$')
    plt.legend(bbox_to_anchor=(0., 1), loc=2, borderaxespad=0.)
    plt.show()

    return [points[1], points[2], points[0], points[4]]

#PART2

def findAsymptote(yValues, tplot, h, type):
    '''der = [0.0, 0.0]
    timeOfAsymptote = 0.0
    for i in range(0,len(yValues) - 1):
        der[0] = yValues[i]
        der[1] = yValues[i + 1]
        if abs(der[1] - der[0])/h < 0.001:
            timeOfAsymptote = i
            break
    '''
    if type == 'F':
        check = 0.97
    elif type == "G":
        check = 0.03
    else:
        print "you didn't pass the parameter"

    for i in range(0,len(yValues) - 1):
        if type == 'F':
            if yValues[i] > 0.97:
                return i*0.1
        elif type == "G":
            if yValues[i] < 0.03:
                return i*0.1
            

    return 0

def velocities(f, fPrime, tPoints):
    t = 0.0
    V1plot = []
    V2plot = []
    tplot = []
    h = 0.1

    # v1 = v/Uinf * (x*Re/L)**(1.0/2.0)
    # v2 = u/Uinf
    for i, t in enumerate(tPoints):
        v1 = 1.0/2.0 * (t * fPrime[i] - f[i])
        v2 = fPrime[i]
        V1plot.append(v1)
        V2plot.append(v2)
        tplot.append(t)
        t += h

    asymptote = findAsymptote(V2plot, tplot, h, 'F')
    print "asymptote", asymptote
    plt.axvline(x=asymptote ,color='k',ls='dashed')
    plt.title('Dimensionless Velocities of v, u')
    plt.plot(tPoints, V1plot, '#ED5377', label="v/Uinf * (x*Re/L)**(1.0/2.0)") 
    plt.plot(tPoints, V2plot, '#004746', label="u/Uinf")
    plt.ylabel('Velocities')
    plt.xlabel('$\eta_t$')
    plt.legend(bbox_to_anchor=(0., 1), loc=2, borderaxespad=0.)
    plt.show()

    return asymptote

def tempPlot(G, tPoints):
    h = 0.1
    asymptote = findAsymptote(G, tPoints, h, 'G')
    print "asymptote", asymptote
    plt.axvline(x=asymptote ,color='k',ls='dashed')
    plt.title('Dimensionless temperature as a function of n')
    plt.plot(tPoints, G, '#ED5377', label="G")
    plt.ylabel('G($\eta_t$)')
    plt.xlabel('$\eta_t$')
    plt.legend(bbox_to_anchor=(0., 1), loc=2, borderaxespad=0.)
    plt.show()

    return asymptote

def prandtlPlot(h, u1, u2, u3, u4, u5, t):
    Pr = [0.2, 2.0, 5.0, 10.0]
    nt = []
    for i, pr in enumerate(Pr):
        f, fprime, tPoints, g = part1G(h, u1, u2, u3, u4, u5, t, pr)
        nt.append(findAsymptote(g, tPoints, h, 'G'))
        print "for {} nt is : {}".format(pr, nt[i])

    plt.title('Graph of nt vs Prandtle Number')
    plt.plot(Pr, nt, '#ED5377', label="G") 
    plt.ylabel('$\eta_t$')
    plt.xlabel('Prandtle Number')
    plt.legend(bbox_to_anchor=(0., 1), loc=2, borderaxespad=0.)
    plt.show()

    return nt

def momentumPlots(nm, ntArray, x):
    tMomentums =  [[] for x in range(5)]
    momentum = []
    prNames = [0.2, 2, 5, 10]
    plt.title('Boundary Layer Thickness vs. Distance on Plate')
    for i, nt in enumerate(ntArray):
        for t in tPoints:
            tMomentums[i].append(ntArray[i]*(t**(1.0/2.0)))
        lbl = "Thermal Layer - Pr: " + str(prNames[i])
        lw = 1.0 + i/1.5
        lines = plt.plot(tPoints, tMomentums[i], label=lbl)
        plt.setp(lines,  color='#F02957', linewidth=lw)

    for t in tPoints:
            momentum.append(nm*(t**(1.0/2.0)))
    plt.plot(tPoints, momentum, 'g--', label="Momentum Layer")
    plt.xlabel(r'$\frac{x}{L}$')
    plt.ylabel(r'$\frac{\delta}{L} \sqrt{Re}$')
    plt.legend(bbox_to_anchor=(0., 1), loc=2, borderaxespad=0.)
    plt.show()



if __name__ == '__main__':
    h = 0.1 
    u1 = 0
    u2 = 0
    u3 = 0.332056861162 # ERROR : -9.90517633026e-07
    u4 = 1
    u5 = 0.2 # ERROR: -1.21703629796e-32
    t = 20
    Pr = 5
    print "part 1, graphs of F:"
    #part1F(h, u1, u2, u3, u4, u5, t, Pr)
    print "part 1, graphs of G:"
    f, fprime, tPoints, g = part1G(h, u1, u2, u3, u4, u5, t, Pr)
    print "part 2"
    nm = velocities(f, fprime, tPoints)
    print "nm is : {}".format(nm)
    print "part 3"
    #nt = tempPlot(g, tPoints)
    #print "nt is : {}".format(nt)

    print "part 6"
    t = 30
    #ntArray = prandtlPlot(h, u1, u2, u3, u4, u5, t)
    print "part 5"
    #print ntArray
    momentumPlots(nm, [8.1, 3.4000000000000004, 2.5, 2.0], tPoints) #we will just reuse tPoints array for plotting function of x

