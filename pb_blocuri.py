import copy
from heapq import heappush, heappop


class Nod:
    scop = [['c', 'b'], [], ['a', 'd']]

    def __init__(self, info):
        self.info = info
        self.h = self.estimare()

    def estimare(self):
        s = 0
        for i in range(0, len(self.scop)):
            for j in range(0, len(self.scop[i])):
                if j >= len(self.info[i]):
                    s += 1
                else:
                    if self.info[i][j] != self.scop[i][j]:
                        s += 1
        return s

    def checkScop(self):
        return self.h == 0

    def __repr__(self):
        return codificare(self.info)


class NodParcurgere:
    def __init__(self, nod, parinte, g):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        self.f = self.g + self.nod.h

    def expandeaza(self):
        listStari = []
        for i in range(0, len(self.nod.info)):
            for j in range(0, len(self.nod.info)):
                if i != j and len(self.nod.info[i]) > 0:
                    stare = copy.deepcopy(self.nod.info)
                    stare[j].insert(0, stare[i].pop(0))
                    listStari.append(stare)
        listVecini = []
        for stare in listStari:
            listVecini.append(Nod(stare))
        return listVecini


def codificare(lista2):
    sir = ''
    for x in lista2:
        sir += ''.join(x) + '-'
    sir = sir[:-1]
    return sir


def AfisareDrum(NOD):
    drum = [NOD]
    while NOD.parinte is not None:
        drum.append(NOD.parinte)
        NOD = NOD.parinte

    print("Rezolvarea cuburilor se face in " + str(len(drum) - 1) + ' mutari')

    for i in range(len(drum) - 1, -1, -1):
        print(str(len(drum) - 1 - i) + ': ' + str(drum[i].nod))


def CheckDrum(new_nod, curr_nod):
    return curr_nod.parinte == new_nod


nod_initial = Nod([['a'], ['b', 'c'], ['d']])

start = NodParcurgere(nod_initial, None, 0)

OpenHeap = []
heappush(OpenHeap, (start.f, codificare(start.nod.info)))

# Dic = {codificare(start.nod.info): start}
InOpen = {codificare(start.nod.info): start}

while len(OpenHeap) > 0:
    nod_curent = InOpen[heappop(OpenHeap)[1]]
    # print(nod_curent.nod)
    # print(" ")
    if nod_curent.nod.checkScop() is True:
        AfisareDrum(nod_curent)
        break
    for s in nod_curent.expandeaza():
        # print("    " + str(s))
        nod_nou = NodParcurgere(s, nod_curent, nod_curent.g + 1)
        if CheckDrum(nod_nou, nod_curent) is False:

            if codificare(nod_nou.nod.info) in InOpen.keys():
                nod_vechi = InOpen[codificare(nod_nou.nod.info)]
                if nod_nou.f < nod_vechi.f:
                    InOpen[codificare(nod_vechi.nod.info)] = nod_nou
                    heappush(OpenHeap, (nod_nou.f, codificare(nod_nou.nod.info)))
            else:
                InOpen[codificare(nod_nou.nod.info)] = nod_nou
                heappush(OpenHeap, (nod_nou.f, codificare(nod_nou.nod.info)))
