import math
import numpy as np

""" definirea problemei """


class Nod:
    # N=3
    # M=2
    def __init__(self, M, N2, N1, K, oameni, mal,
                 h=0):  # oameni e un tuplu de forma (misioanri_mal_curent, canibali_mal_curent, hrana_mal_curent)
        self.oameni = oameni
        self.mal = mal  # malul curent (pe care se afla barca)
        self.h = h
        self.N1 = N1  ### CANIBALI
        self.N2 = N2  ### MISIONARI
        self.K = K  ### UNITATI DE HRANA
        self.M = M  ### Numar locuri in barca

    def __eq__(self, value):
        return self.oameni == value.oameni and self.mal == value.mal

    def sirAfisare(self):
        if self.mal == 0:
            mis_0 = self.oameni[0]
            can_0 = self.oameni[1]
            hr_0 = self.oameni[2]
            mis_1 = self.N2 - self.oameni[0]
            can_1 = self.N1 - self.oameni[1]
            hr_1 = self.K - self.oameni[2]
            barca_0 = "barca"
            barca_1 = "     "
            locuri_barca = self.M
        else:
            mis_1 = self.oameni[0]
            can_1 = self.oameni[1]
            hr_1 = self.oameni[2]
            mis_0 = self.N2 - self.oameni[0]
            can_0 = self.N1 - self.oameni[1]
            hr_0 = self.K - self.oameni[2]
            barca_1 = "barca"
            barca_0 = "     "
            locuri_barca = self.M
        return str(
            "Mal:0 Misionari: {} Canibali: {} Hrana: {} {} | Mal:1 Misionari: {} Canibali: {} Hrana: {} {} Locuri Barca: {} \n".format(
                mis_0, can_0, float(hr_0), barca_0, mis_1, can_1, float(hr_1), barca_1, locuri_barca))

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Problema:
    def __init__(self, M, N2, N1, K, oameni, mal):
        self.mal = mal
        # 0 - mal stang  ; 1-mal drept
        self.nod_start = Nod(M, N2, N1, K, oameni, mal)  # nu conteaza h-ul
        self.nod_scop = [Nod(x, N2, N1, y, (N2, N1, z), 1 - mal) for x in range(M + 1) for y in np.arange(0, K + 1, 0.5)
                         for z in np.arange(0, K + 1, 0.5)]

    def calculeaza_h(self, nod):
        mis_mal_c = nod.oameni[0]  # mis_mal_c_vechi
        can_mal_c = nod.oameni[1]
        mal_c = nod.mal
        if mal_c == self.mal:
            total_oameni = mis_mal_c + can_mal_c
        else:
            total_oameni = nod.N2 + nod.N1 - (mis_mal_c + can_mal_c)
            # total_oameni cati mai am de mutat
        nr_transporturi = math.ceil(total_oameni / nod.M) * 2
        if mal_c == 0:
            nr_transporturi -= 1
        return nr_transporturi

    `def calculeaza_h2(self, nod):
        mis_mal_c = nod.oameni[0]  # mis_mal_c_vechi
        can_mal_c = nod.oameni[1]
        mal_c = nod.mal
        if mal_c == self.mal:
            total_oameni = mis_mal_c + can_mal_c
        else:
            total_oameni = nod.N2 + nod.N1 - (mis_mal_c + can_mal_c)
            # total_oameni cati mai am de mutat
        nr_transporturi = math.ceil(total_oameni / nod.M) * 2
        if mal_c == 0:
            nr_transporturi -= 1
        return (nr_transporturi > 0)`

""" Sfarsit definire problema """

""" Clase folosite in algoritmul A* """


class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
        Cuprinde o referinta catre nodul in sine (din graf)
        dar are ca proprietati si valorile specifice algoritmului A* (f si g).
        Se presupune ca h este proprietate a nodului din graf

    """
    problema = None

    def __init__(self, nod_graf, succesori=[], parinte=None, g=0, f=None):
        self.nod_graf = nod_graf
        self.succesori = succesori  # optional
        self.parinte = parinte
        self.g = g
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def drum_arbore(self):
        """
            Functie care calculeaza drumul asociat unui nod din arborele de cautare.
            Functia merge din parinte in parinte pana ajunge la radacina
        """
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        """
            Functie care verifica daca nodul se afla in drumul unui alt nod.
            Verificarea se face mergand din parinte in parinte pana la radacina
            Se compara doar informatiile nodurilor(proprietatea info)
        """
        nod_c = self
        while nod_c.parinte is not None:
            if nod == nod_c.nod_graf:
                return True
            nod_c = nod_c.parinte
        return False

        # se modifica in functie de problema

    def expandeaza(self):
        def test_cond(m, c, h):
            return m == 0 or m + 2 * h >= c

        l_succesori = []
        # can si mis pe malul curent, inainte de a plecat barca
        mis_mal_c = self.nod_graf.oameni[0]  # mis_mal_c_vechi
        can_mal_c = self.nod_graf.oameni[1]
        h_mal_c = self.nod_graf.oameni[2]
        mal_c = self.nod_graf.mal
        for nmb in range(min(mis_mal_c, self.nod_graf.M) + 1):

            for nhb in range(min(math.floor(h_mal_c), self.nod_graf.M) + 1):

                if nmb != 0:
                    can_calatori = min(self.nod_graf.M - nmb - nhb, can_mal_c, nmb + 2 * nhb)
                else:
                    continue

                for ncb in range(can_calatori + 1):
                    """
                    Nod.M-nmb - cate locuri au ramas libere dupa ce au urcat misionarii
                    nmb - sa nu depaseasca mis din barca
                    """

                    # if nmb + ncb == 0:
                    #     continue

                    if not test_cond(mis_mal_c - nmb, can_mal_c - ncb, h_mal_c - nhb):
                        continue
                    # inainte de am auns cu barca
                    mis_mal_o_vechi = self.nod_graf.N2 - mis_mal_c
                    can_mal_o_vechi = self.nod_graf.N1 - can_mal_c
                    h_mal_o_vechi = self.nod_graf.K - h_mal_c
                    # dupa ce a ajuns barca
                    mis_mal_o = mis_mal_o_vechi + nmb
                    can_mal_o = can_mal_o_vechi + ncb
                    h_mal_o = h_mal_o_vechi + nhb - max((ncb - nmb) / 2, 0)

                    if not test_cond(mis_mal_o, can_mal_o, h_mal_o):
                        continue

                    if self.nod_graf.M <= 2:
                        continue
                    if self.nod_graf.K - max((ncb - nmb) / 2, 0) - max((can_mal_c - mis_mal_c) / 2, 0) - h_mal_o < 0:
                        continue

                    nodNou = Nod(self.nod_graf.M - 1, self.nod_graf.N2, self.nod_graf.N1,
                                 self.nod_graf.K - max((ncb - nmb) / 2, 0) - max((can_mal_c - mis_mal_c) / 2, 0),
                                 (mis_mal_o, can_mal_o, h_mal_o), 1 - mal_c)
                    nodNou.h = problema.calculeaza_h2(nodNou)
                    l_succesori.append((nodNou, 1))
                    # l_succesori.append( (nod, cost) )
        return l_succesori

    # se modifica in functie de problema
    def test_scop(self):
        return self.nod_graf in self.__class__.problema.nod_scop

    def __str__(self):
        # parinte=self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return str(self.nod_graf);


""" Algoritmul A* """


def str_info_noduri(l):
    """
        o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for x in l:
        sir += str(x) + "\n"

    return sir


def afis_succesori_cost(l):
    """
        o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: " + str(x) + ", cost arc:" + str(cost)

    return sir


def in_lista(l, nod):
    for i in range(len(l)):
        if l[i].nod_graf == nod:
            return l[i]
    return None


def a_star():
    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start);
    open = [rad_arbore]
    closed = []
    while len(open) > 0:
        # print(str_info_noduri(open))

        nod_curent = open.pop(0)
        closed.append(nod_curent)
        if nod_curent.test_scop():  # testez daca nodul extras din lista open este nod scop (si daca da, ies din bucla while)
            break

        # print(str_info_noduri(nod_curent.drum_arbore()))

        l_succesori = nod_curent.expandeaza()
        for (nod_succesor, cost_succesor) in l_succesori:
            # daca nu e in drum
            if (not nod_curent.contine_in_drum(nod_succesor)):
                g_succesor = nod_curent.g + cost_succesor
                f = g_succesor + nod_succesor.h
                # verific daca se afla in closed (si il si sterg, returnand nodul sters in nod_parcg_vechi
                nod_parcg_vechi = in_lista(closed, nod_succesor)

                if nod_parcg_vechi is not None:
                    if (f < nod_parcg_vechi.f):
                        closed.remove(nod_parcg_vechi)
                        nod_parcg_vechi.parinte = nod_curent
                        nod_parcg_vechi.g = g_succesor
                        nod_parcg_vechi.f = f
                        nod_nou = nod_parcg_vechi
                else:
                    # verific daca se afla in open
                    nod_parcg_vechi = in_lista(open, nod_succesor)
                    if nod_parcg_vechi is not None:
                        if (f < nod_parcg_vechi.f):
                            # if(nod_parcg_vechi.g>g_succesor):
                            open.remove(nod_parcg_vechi)
                            nod_parcg_vechi.parinte = nod_curent
                            nod_parcg_vechi.g = g_succesor
                            nod_parcg_vechi.f = f
                            nod_nou = nod_parcg_vechi
                    else:  # cand nu e nici in closed nici in open

                        nod_nou = NodParcurgere(nod_graf=nod_succesor, parinte=nod_curent,
                                                g=g_succesor);  # se calculeaza f automat in constructor
                if nod_nou:
                    # inserare in lista sortata crescator dupa f (si pentru f-uri egale descrescator dupa g
                    i = 0
                    while i < len(open):
                        if open[i].f < nod_nou.f:
                            i += 1
                        else:
                            while i < len(open) and open[i].f == nod_nou.f and open[i].g > nod_nou.g:
                                i += 1
                            break

                    open.insert(i, nod_nou)

    print("\n------------------ Concluzie -----------------------")
    if (len(open) == 0):
        print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
        print("Drum de cost minim:\n" + str_info_noduri(nod_curent.drum_arbore()))


if __name__ == "__main__":

    files = ['input_1.txt', 'input_3.txt', 'input_4.txt']

    for file in files:
        with open(file, 'r') as f:
            for line in f.readlines():
                splitted_line = line.split(' ')
                M = int(splitted_line[0])
                N2 = int(splitted_line[1])
                N1 = int(splitted_line[2])
                K = int(splitted_line[3])
                oameni = (int(splitted_line[4]), int(splitted_line[5]), int(splitted_line[6]))
                mal = int(splitted_line[7])

            problema = Problema(M, N2, N1, K, oameni, mal)
            # N1 = canibali, N2 = misionari, M = locuri in barca, K = unitati de hrana,
            # oameni = (misioanri_mal_curent, canibali_mal_curent, hrana_mal_curent)
            NodParcurgere.problema = problema
            a_star()