import matplotlib.pyplot
import numpy as np
from matplotlib import animation
import matplotlib.colors
cmap = matplotlib.colors.ListedColormap(["#2325B9", "#969696", "#00FF00", "#7BA05B", "#00FA9A", "#01796F", "#E00000",
                                         "#BEBEBE"])

def hasard(p):
    """renvoie True avec une probabilite p et False avec une probabilité 1-p"""
    r = np.random.random()
    assert 0 <= p <= 1
    return r <= p


def creerForet(n, m, pcoccup, pw):
    """cree une foret avec des arbres places aleatoirements"""
    foret = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            if hasard(pcoccup):
                k = np.random.random()
                if k < 0.25:
                    foret[i, j] = 1.
                elif k < 0.5:
                    foret[i, j] = 2.
                elif k < 0.75:
                    foret[i, j] = 3.
                else:
                    foret[i, j] = 4.
            elif np.random.random() < pw:
                foret[i, j] = -1.
    return foret

def burnprob(foret, i, j):
    n, m = foret.shape
    u = 0
    for r in range(max(0, i-1), min(n, i+2)):
        for g in range(max(0, j-1), min(m, j+2)):
            if foret[r, g] == -1:
                u += 0.1
    return u

def checkburn(foret, i, j):
    n, m = foret.shape

    for y in range(max(0, i-1), min(n, i+1)):
        if foret[y, j] == 5.:
            return True
    for x in range(max(0, j - 1), min(m, j + 2)):
        if foret[i, x] == 5.:
            return True
    return False

def mapburn(foret):
    n, m = foret.shape
    mb = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            if 1. <= foret[i, j] <= 4.:
                mb[i, j] = 1.
                mb[i, j] = 1 - burnprob(foret, i, j)
                if checkburn(foret, i, j) and not(peutbrulervent_nord(foret, i, j)):
                    mb[i, j] = mb[i, j] - 0.15
    return mb


def mettreLeFeu(foret):
    """met le feu a un arbre"""
    n, m = foret.shape
    i = np.random.randint(0, n + 1)
    j = np.random.randint(0, m + 1)
    while foret[i, j] != 5.:
        if 1. <= foret[i, j] <= 4.:
            foret[i, j] = 5.
        else:
            i = np.random.randint(0, n + 1)
            j = np.random.randint(0, m + 1)
    return foret


def peutbrulervent_nord(foret, i, j):
    n, m = foret.shape
    if i == n-1:
        return False
    elif 1. <= foret[i, j] <= 4.:
        for v in range(max(0, j-1), min(m, j+2)):
            if foret[i+1, v] == 5.:
                return True
    else:
        return False

def propageFeu(foret):
    """les arbres qui peuvent bruler autour d'un arbre en feu prennent feu
    """
    n, m = foret.shape  # n et m respectivement le nombre de lignes et de colonnes
    c = np.copy(foret)
    d = mapburn(c)
    p = np.random.random()
    for i in range(n):
        for j in range(m):
            if peutbrulervent_nord(c, i, j) and p < d[i, j]:
                foret[i, j] = 5.
            elif checkburn(c, i, j) and p < d[i, j]:
                foret[i, j] = 5.
    for i in range(n):
        for j in range(m):
            if c[i, j] == 5. and np.random.random() < p:
                foret[i, j] = 6.
    return foret

def auFeu(foret):
    """verifie si au moins un arbre non en feu peut bruler"""
    n, m = foret.shape
    for i in range(n):
        for j in range(m):
            if peutbrulervent_nord(foret, i, j) or checkburn(foret, i, j) or foret[i, j] == 5.:
                return True
    return False

def metFeuForet(foret):
    """met le feu et propage l'incendie jusqu'a ce que tous les arbres qui peuvent bruler soient en feu"""
    foret = mettreLeFeu(foret)
    while auFeu(foret):
        foret = propageFeu(foret)
    return foret

def animationFeu(foret):
    fig = matplotlib.pyplot.figure()
    film = []

    foretFeu = mettreLeFeu(foret)
    film.append([matplotlib.pyplot.matshow(foret, fignum=False, cmap=cmap, animated=True)])
    matplotlib.pyplot.draw()
    while auFeu(foret):
        foretFeu = propageFeu(foretFeu)
        film.append([matplotlib.pyplot.matshow(foretFeu, fignum=False, cmap=cmap, animated=True)])
        matplotlib.pyplot.draw()

    ani = animation.ArtistAnimation(fig, film, interval=1000, blit=True, repeat_delay=100)
    matplotlib.pyplot.draw()
    matplotlib.pyplot.show()

print(animationFeu(creerForet(50, 50, 0.8, 0.9)))

