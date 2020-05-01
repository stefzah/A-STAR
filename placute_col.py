import copy
import sys
import time
from heapq import heappush, heappop


# clasa care ofera informatii pentru fiecare stare

class Nod:

    # constructorul (primeste ca parametru o matrice)
    def __init__(self, info):
        self.info = info
        self.dictionar = {}
        self.h = self.estimare()

    # euristica eficienta
    # returneaza numarul de culori diferite din matrice
    # este corecta deoarece putem extrage maxim o culoare pe tura
    # practic considera ca fiecare culoare are un singur grup de adiacenta
    def estimare(self):
        s = 0
        for linie in self.info:
            for elem in linie:
                if elem != "#":
                    if elem not in self.dictionar.keys():
                        s += 1
                        self.dictionar[elem] = 0
                    self.dictionar[elem] += 1
        return s

    # euristica ineficienta
    # returneaza 1 daca este cel putin o placuta colorata, si 0 altfel
    # este corecta, insa foarte ineficienta
    # practic considera ca toate placutele colorate au aceeasi culoare)
    def estimare_inef(self):
        s = 0
        for linie in self.info:
            for elem in linie:
                if elem != "#":
                    if elem not in self.dictionar.keys():
                        s += 1
                        self.dictionar[elem] = 0
                    self.dictionar[elem] += 1
        return s >= 1

    # euristica incorecta
    # returneaza numarul total de placute colorate
    # este incorecta deoarece exista posibilitatea ca mai multe placute de aceeasi culoare sa fie adiacente
    def estimare_incorecta(self):
        s = 0
        for linie in self.info:
            for elem in linie:
                if elem != "#":
                    if elem not in self.dictionar.keys():
                        self.dictionar[elem] = 0
                    self.dictionar[elem] += 1
                    s += 1
        return s

    # calculeaza costul cu care se ajunge de la starea curenta la starea matr2
    def calcCost(self, matr2, ch):
        ct = 0
        for i in range(0, len(matr2)):
            for j in range(0, len(matr2[0])):
                if self.info[i][j] != matr2[i][j]:
                    ct += 1
        return 1 + ((self.dictionar[ch] - ct) / self.dictionar[ch])

    # verifica daca starea curenta este ce finala
    def checkScop(self):
        return self.h == 0

    # definirea reprezentarii in format string a unei stari
    def __repr__(self):
        matr = ""
        for i in range(0, len(self.info)):
            for j in range(0, len(self.info[i])):
                matr += self.info[i][j]
            matr += "\n"
        return matr


# clasa nodurilor din arbore
class NodParcurgere:

    # constructor - primeste ca parametru nodul curent, nodul parinte si costul pentru a ajunge la el
    def __init__(self, nod, parinte, g):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        self.f = self.g + self.nod.h

    # genereaza si returneaza lista de stari care deriva din starea curenta
    # pentru fiecare grupare de placute de aceeasi culoare, se apeleaza functia de Fill() si cea de Arrange()
    def expandeaza(self):
        viz = copy.deepcopy(self.nod.info)
        listStari = []
        for i in range(0, len(viz)):
            for j in range(0, len(viz[i])):
                if i != j and viz[i][j] != '#':
                    stare = copy.deepcopy(self.nod.info)
                    ch = stare[i][j]
                    count = Fill(viz, stare, i, j)
                    cost = self.nod.calcCost(stare, ch)
                    Arrange(stare)
                    if count >= 3:
                        listStari.append((stare, cost))
        listVecini = []
        for tuplu in listStari:
            listVecini.append((Nod(tuplu[0]), tuplu[1]))
        return listVecini


# transforma o lista intr-un format de tip string, mai usor de memorat
def codificare(lista2):
    sir = ''
    for x in lista2:
        sir += ''.join(x) + '-'
    sir = sir[:-1]
    return sir


# afiseaza drumul care se termina la parametrul NOD
def AfisareDrum(NOD):
    drum = [NOD]
    while NOD.parinte is not None:
        drum.append(NOD.parinte)
        NOD = NOD.parinte

    fout.write("\nStare initiala: \n" + str(drum[len(drum) - 1].nod))

    fout.write("\nRezolvarea placutelor se face in " + str(len(drum) - 1) + " pasi")

    for i in range(len(drum) - 2, -1, -1):
        fout.write("\nPasul: " + str(len(drum) - 1 - i) + "\nCost: " + str(drum[i].g - drum[i + 1].g) + '\n' + str(drum[i].nod))

    fout.write("\nCostul total: " + str(drum[0].g))


# verifica daca noul nod nu este defapt nodul parinte
def CheckDrum(new_nod, curr_nod):
    return curr_nod.parinte == new_nod


# citeste, parseaza si returneaza datele din fisierul de intrare
def ReadInput():
    f = open(sys.argv[1], "r")
    input_txt = f.read()
    input_txt = input_txt.split()
    for i in range(0, len(input_txt)):
        input_txt[i] = list(input_txt[i])
    return input_txt


# porneste de la pozitia (x,y) si parcurge toate placutele adiacente de aceeasi culoare
def Fill(viz, matr, x, y):
    viz[x][y] = "#"
    c = matr[x][y]
    matr[x][y] = "#"
    count = 1

    if x - 1 >= 0 and matr[x - 1][y] == c:
        count += Fill(viz, matr, x - 1, y)
    if x + 1 < len(matr) and matr[x + 1][y] == c:
        count += Fill(viz, matr, x + 1, y)
    if y - 1 >= 0 and matr[x][y - 1] == c:
        count += Fill(viz, matr, x, y - 1)
    if y + 1 < len(matr[x]) and matr[x][y + 1] == c:
        count += Fill(viz, matr, x, y + 1)
    return count


# dupa ce s-a apelat functia Fill(), placutele trebuiesc rearanjate dupa regulile din enunt
def Arrange(matr):
    for i in range(len(matr) - 1, -1, -1):
        for j in range(0, len(matr[i])):
            if matr[i][j] != '#':
                k = i
                while k + 1 < len(matr) and matr[k + 1][j] == "#":
                    matr[k + 1][j] = matr[k][j]
                    matr[k][j] = "#"
                    k += 1
    ok = 0
    while ok == 0:
        ok = 1
        x = -1
        for i in range(len(matr[0]) - 1, 0, -1):
            ct = 0
            ct2 = 0
            for j in range(0, len(matr)):
                if matr[j][i] != "#":
                    ct2 += 1
                if matr[j][i - 1] == "#":
                    ct += 1
            if ct == len(matr) and ct2 > 0:
                ok = 0
                x = i - 1
        if x != -1:
            for i in range(0, len(matr)):
                for j in range(x, len(matr[i])):
                    if j + 1 == len(matr[i]):
                        matr[i][j] = "#"
                    else:
                        matr[i][j] = matr[i][j + 1]


# Aici incepe programul efectiv

t0 = time.time()

# Atribuirea starii initiale
nod_initial = Nod(ReadInput())

# Atribuireae nodului de start
start = NodParcurgere(nod_initial, None, 0)

# Adaugarea in lista Open a unui tuplet (estimare stare, codificare stare)
OpenHeap = []
heappush(OpenHeap, (start.f, codificare(start.nod.info)))

# Dictionar ce memoreaza starea corespunzatoare pentru fiecare codificare
InOpen = {codificare(start.nod.info): start}

final = False

fout = open("result.txt", "w")

while len(OpenHeap) > 0:

    nod_curent = InOpen[heappop(OpenHeap)[1]]

    if nod_curent.nod.checkScop() is True:
        AfisareDrum(nod_curent)
        final = True
        break

    for s in nod_curent.expandeaza():
        nod_nou = NodParcurgere(s[0], nod_curent, nod_curent.g + s[1])
        if CheckDrum(nod_nou, nod_curent) is False:

            if codificare(nod_nou.nod.info) in InOpen.keys():
                nod_vechi = InOpen[codificare(nod_nou.nod.info)]
                if nod_nou.f < nod_vechi.f:
                    InOpen[codificare(nod_vechi.nod.info)] = nod_nou
                    heappush(OpenHeap, (nod_nou.f, codificare(nod_nou.nod.info)))
            else:
                InOpen[codificare(nod_nou.nod.info)] = nod_nou
                heappush(OpenHeap, (nod_nou.f, codificare(nod_nou.nod.info)))

if not final:
    fout.write("\nNu avem solutie!")

# Afisarea timpului final de executie
t1 = time.time()
fout.write("\nEXECUTION TIME: " + str(1000 * (t1 - t0) / 2) + "ms")
fout.close()
