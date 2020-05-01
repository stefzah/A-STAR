import copy
import sys
import time
from heapq import heappush, heappop


class Nod:
    scop = [[0, 0], [0, 0], [3, 3], [0, 1]]

    def __init__(self, info):
        self.info = info
        self.h = self.estimare()

    def estimare(self):
        return int((2 * N - self.info[2][0] - self.info[2][1]) / M) + (
                (2 * N - self.info[2][0] - self.info[2][1]) % M != 0)

    def checkScop(self):
        return self.h == 0

    def __repr__(self):
        txt = "Prima insula: " + str(self.info[0])
        txt += ", Barca " + str(self.info[1])
        txt += ", A doua insula: " + str(self.info[2])
        if self.info[3][0] == 1:
            txt += " | Barca este langa prima insula"
        else:
            txt += " | Barca este langa a doua insula"
        return txt


class NodParcurgere:
    def __init__(self, nod, parinte, g):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        self.f = self.g + self.nod.h

    def expandeaza(self):
        listStari = []

        barca = self.nod.info[3]
        if barca[0] == 1:
            for i in range(0, self.nod.info[1][0] + 1):
                for j in range(0, self.nod.info[1][1] + 1):
                    stare = copy.deepcopy(self.nod.info)
                    stare[0][0] += i
                    stare[0][1] += j
                    stare[1][0] -= i
                    stare[1][1] -= j
                    if Valid(stare):
                        listStari.append(stare)
            for i in range(0, self.nod.info[0][0] + 1):
                for j in range(0, self.nod.info[0][1] + 1):
                    if i + j >= 1:
                        stare = copy.deepcopy(self.nod.info)
                        stare[1][0] += i
                        stare[1][1] += j
                        stare[0][0] -= i
                        stare[0][1] -= j
                        stare[3][0] = 0
                        stare[3][1] = 1
                        if Valid(stare):
                            listStari.append(stare)

        if barca[1] == 1:
            for i in range(0, self.nod.info[1][0] + 1):
                for j in range(0, self.nod.info[1][1] + 1):
                    stare = copy.deepcopy(self.nod.info)
                    stare[2][0] += i
                    stare[2][1] += j
                    stare[1][0] -= i
                    stare[1][1] -= j
                    if Valid(stare):
                        listStari.append(stare)
            for i in range(0, self.nod.info[2][0] + 1):
                for j in range(0, self.nod.info[2][1] + 1):
                    if i + j >= 1:
                        stare = copy.deepcopy(self.nod.info)
                        stare[1][0] += i
                        stare[1][1] += j
                        stare[2][0] -= i
                        stare[2][1] -= j
                        stare[3][0] = 1
                        stare[3][1] = 0
                        if Valid(stare):
                            listStari.append(stare)

        listVecini = []
        for stare in listStari:
            listVecini.append(Nod(stare))
        return listVecini


def codificare(lista2):
    sir = ''
    for x in lista2:
        sir += str(x[0]) + ',' + str(x[1]) + '-'
    sir = sir[:-1]
    return sir


def AfisareDrum(NOD):
    drum = [NOD]
    while NOD.parinte is not None:
        drum.append(NOD.parinte)
        NOD = NOD.parinte

    print("Mutarea canibalilor si a misionarilor se face in " + str(drum[0].g) + ' drumuri')

    for i in range(len(drum) - 1, -1, -1):
        if i == len(drum) - 1 or drum[i + 1].g != drum[i].g:
            print("")
        print(str(drum[i].g) + ': ' + str(drum[i].nod))


def CheckDrum(new_nod, curr_nod):
    return curr_nod.parinte == new_nod


def Valid(stare):
    if stare[1][0] + stare[1][1] > M:
        return False
    if stare[0][0] > stare[0][1] >= 1:
        return False
    if stare[1][0] > stare[1][1] >= 1:
        return False
    if stare[2][0] > stare[2][1] >= 1:
        return False
    return True


t0 = time.time()

N = int(sys.argv[1])
M = int(sys.argv[2])

nod_initial = Nod([[N, N], [0, 0], [0, 0], [1, 0]])

start = NodParcurgere(nod_initial, None, 0)
OpenHeap = []
heappush(OpenHeap, (start.f, codificare(start.nod.info)))

InOpen = {codificare(start.nod.info): start}

while len(OpenHeap) > 0:
    nod_curent = InOpen[heappop(OpenHeap)[1]]
    if nod_curent.nod.checkScop() is True:
        AfisareDrum(nod_curent)
        break
    for s in nod_curent.expandeaza():
        # print("    " + str(s))
        cost = 0
        if nod_curent.nod.info[3][0] != s.info[3][0]:
            cost += 1
        nod_nou = NodParcurgere(s, nod_curent, nod_curent.g + cost)

        if CheckDrum(nod_nou, nod_curent) is False:

            if codificare(nod_nou.nod.info) in InOpen.keys():
                nod_vechi = InOpen[codificare(nod_nou.nod.info)]
                if nod_nou.f < nod_vechi.f:
                    InOpen[codificare(nod_vechi.nod.info)] = nod_nou
                    heappush(OpenHeap, (nod_nou.f, codificare(nod_nou.nod.info)))
            else:
                InOpen[codificare(nod_nou.nod.info)] = nod_nou
                heappush(OpenHeap, (nod_nou.f, codificare(nod_nou.nod.info)))

t1 = time.time()
print("EXECUTION TIME: " + str(1000 * (t1 - t0) / 2) + "ms")
