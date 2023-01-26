import random
import tkinter as tk
from tkinter import font as tkfont
import numpy as np


##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
    T = np.array(L, dtype=np.int32)
    T = T.transpose()  # ainsi, on peut écrire TBL[x][y]
    return T


TBL = CreateArray([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
# attention, on utilise TBL[x][y]

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]

# placements des pacgums et des fantomes


def PlacementsGUM():  # placements des pacgums
    GUM = np.zeros(TBL.shape, dtype=np.int32)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (TBL[x][y] == 0):
                GUM[x][y] = 1

    return GUM


GUM = PlacementsGUM()


PacManPos = [5, 5]

Ghosts = []
Ghosts.append([LARGEUR // 2, HAUTEUR // 2,  "pink"])
Ghosts.append([LARGEUR//2, HAUTEUR // 2,  "orange"])
Ghosts.append([LARGEUR//2, HAUTEUR // 2,  "cyan"])
Ghosts.append([(LARGEUR//2)+1, HAUTEUR // 2,  "red"])

##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL3 = [["" for i in range(LTBL)] for j in range(LTBL)]

# info peut etre une valeur / un string vide / un string...
def SetInfo1(x, y, info):
    info = str(info)
    if x < 0:
        return
    if y < 0:
        return
    if x >= LTBL:
        return
    if y >= LTBL:
        return
    TBL1[x][y] = info


def SetInfo2(x, y, info):
    info = str(info)
    if x < 0:
        return
    if y < 0:
        return
    if x >= LTBL:
        return
    if y >= LTBL:
        return
    TBL2[x][y] = info

def SetInfo3(x, y, info):
    info = str(info)
    if x < 0:
        return
    if y < 0:
        return
    if x >= LTBL:
        return
    if y >= LTBL:
        return
    TBL3[x][y] = info


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################


ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight)
                )   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False


def keydown(e):
    global PAUSE_FLAG
    if e.char == ' ':
        PAUSE_FLAG = not PAUSE_FLAG


Window.bind("<KeyPress>", keydown)


# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages = {}
PageActive = 0


def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame


def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()


def WindowAnim():
    PlayOneTurn()
    Window.after(333, WindowAnim)

# set le tab1 et tab2


def SetTabs():
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 0:
                info = 100
                SetInfo1(x, y, info)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 0:
                if GUM[x][y] == 0:
                    info = 100
                    SetInfo2(x, y, info)
                if GUM[x][y] == 1:
                    info = 0
                    SetInfo2(x, y, info)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 0:
                info = 100
                SetInfo3(x, y, info)

SetTabs()
Window.after(100, WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22,
                          weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas.configure(background='black')


#  FNT AFFICHAGE


def To(coord):
    return coord * ZOOM + ZOOM

# dessine l'ensemble des éléments du jeu par dessus le décor


anim_bouche = 0
animPacman = [5, 10, 15, 10, 5]


def Affiche(PacmanColor, message):
    global anim_bouche

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x-r, y-r, x+r, y+r, fill=coul, width=0)

    canvas.delete("all")

    # murs

    for x in range(LARGEUR-1):
        for y in range(HAUTEUR):
            if (TBL[x][y] == 1 and TBL[x+1][y] == 1):
                xx = To(x)
                xxx = To(x+1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="blue")

    for x in range(LARGEUR):
        for y in range(HAUTEUR-1):
            if (TBL[x][y] == 1 and TBL[x][y+1] == 1):
                xx = To(x)
                yy = To(y)
                yyy = To(y+1)
                canvas.create_line(xx, yy, xx, yyy, width=EPAISS, fill="blue")

    # pacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (GUM[x][y] == 1):
                xx = To(x)
                yy = To(y)
                e = 5
                # placement des super pacgum
                if ([x, y] in arrCorner):
                    canvas.create_oval(xx-e, yy-e, xx+e, yy+e, fill="white")
                    continue
                canvas.create_oval(xx-e, yy-e, xx+e, yy+e, fill="orange")

    # extra info
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) - 11
            txt = TBL1[x][y]
            canvas.create_text(
                xx, yy, text=txt, fill="white", font=("Purisa", 8))

    # extra info 2
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) + 10
            yy = To(y)
            txt = TBL2[x][y]
            canvas.create_text(xx, yy, text=txt, fill="yellow",
                               font=("Purisa", 8))
    
    # extra info 3
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) +11
            txt = TBL3[x][y]
            canvas.create_text(xx, yy, text=txt, fill="green",
                               font=("Purisa", 8))

    # dessine pacman
    xx = To(PacManPos[0])
    yy = To(PacManPos[1])
    e = 20
    anim_bouche = (anim_bouche+1) % len(animPacman)
    ouv_bouche = animPacman[anim_bouche]
    tour = 360 - 2 * ouv_bouche
    canvas.create_oval(xx-e, yy-e, xx+e, yy+e, fill=PacmanColor)
    canvas.create_polygon(xx, yy, xx+e, yy+ouv_bouche, xx+e,
                          yy-ouv_bouche, fill="black")  # bouche

    # dessine les fantomes
    dec = -3
    for P in Ghosts:
        print(P[0], P[1])
        xx = To(P[0])
        yy = To(P[1])
        e = 16

        coul = P[2]
        # corps du fantome
        CreateCircle(dec+xx, dec+yy-e+6, e, coul)
        canvas.create_rectangle(dec+xx-e, dec+yy-e, dec +
                                xx+e+1, dec+yy+e, fill=coul, width=0)

        # oeil gauche
        CreateCircle(dec+xx-7, dec+yy-8, 5, "white")
        CreateCircle(dec+xx-7, dec+yy-8, 3, "black")

        # oeil droit
        CreateCircle(dec+xx+7, dec+yy-8, 5, "white")
        CreateCircle(dec+xx+7, dec+yy-8, 3, "black")

        dec += 3

    # texte

    canvas.create_text(screeenWidth // 2, screenHeight - 50,
                       text="PAUSE : PRESS SPACE", fill="yellow", font=PoliceTexte)
    canvas.create_text(screeenWidth // 2, screenHeight - 20,
                       text=message, fill="yellow", font=PoliceTexte)


AfficherPage(0)

#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################


def CheckCasesGum(x, y):
    list = [100, 100, 100, 100]
    if not (len(TBL[x]) < y+1):
        # HAUT
        if TBL[x][y+1] == 0:  # VIDE PAS DE COULEUR
            list[0] = int(TBL2[x][y+1])
    if not y < 0:
        # BAS
        if TBL[x][y-1] == 0:  # VIDE PAS DE COULEUR
            list[1] = int(TBL2[x][y-1])
    if not x < 0:
        # GAUCHE
        if TBL[x-1][y] == 0:  # VIDE PAS DE COULEUR
            list[2] = int(TBL2[x-1][y])
    if not (len(TBL) < x+1):
        # DROIT
        if TBL[x+1][y] == 0:  # VIDE PAS DE COULEUR
            list[3] = int(TBL2[x+1][y])
    # prendre le min des 4 :
    if (min(list) == 100):
        info = 100
    else:
        info = str(min(list)+1)

    # Ajouter +1
    return info
    # return la valeur info


def CheckCasesPacman(x, y):
    list = [100, 100, 100, 100]
    if not (len(TBL[x]) < y+1):
        # HAUT
        if TBL[x][y+1] == 0:  # VIDE PAS DE COULEUR
            list[0] = int(TBL3[x][y+1])
    if not y < 0:
        # BAS
        if TBL[x][y-1] == 0:  # VIDE PAS DE COULEUR
            list[1] = int(TBL3[x][y-1])
    if not x < 0:
        # GAUCHE
        if TBL[x-1][y] == 0:  # VIDE PAS DE COULEUR
            list[2] = int(TBL3[x-1][y])
    if not (len(TBL) < x+1):
        # DROIT
        if TBL[x+1][y] == 0:  # VIDE PAS DE COULEUR
            list[3] = int(TBL3[x+1][y])
    # prendre le min des 4 :
    if (min(list) == 100):
        info = 100
    else:
        info = str(min(list)+1)

    # Ajouter +1
    return info
    # return la valeur info

def CheckCasesGhost(x, y):
    list = [100, 100, 100, 100]
    if not (len(TBL[x]) < y+1):
        # HAUT
        if TBL[x][y+1] == 0:  # VIDE PAS DE COULEUR
            list[0] = int(TBL1[x][y+1])
    if not y < 0:
        # BAS
        if TBL[x][y-1] == 0:  # VIDE PAS DE COULEUR
            list[1] = int(TBL1[x][y-1])
    if not x < 0:
        # GAUCHE
        if TBL[x-1][y] == 0:  # VIDE PAS DE COULEUR
            list[2] = int(TBL1[x-1][y])
    if not (len(TBL) < x+1):
        # DROIT
        if TBL[x+1][y] == 0:  # VIDE PAS DE COULEUR
            list[3] = int(TBL1[x+1][y])
    # prendre le min des 4 :
    if (min(list) == 100):
        info = 100
    else:
        info = str(min(list)+1)

    # Ajouter +1
    return info
    # return la valeur info


def CasesValuesGum(x, y):
    if TBL[x][y] == 0 and GUM[x][y] == 0:  # VIDE PAS DE COULEUR
        info = CheckCasesGum(x, y)
        SetInfo2(x, y, info)

def CasesValuesGhost(x, y):
      if TBL[x][y] == 0 and TBL1[x][y]:  # VIDE PAS DE COULEUR
         info = CheckCasesGhost(x, y)
         SetInfo1(x, y, info)

def CasesValuesPacMan(x, y):
    if TBL[x][y] == 0 and GUM[x][y] == 0:  # VIDE PAS DE COULEUR
        info = CheckCasesPacman(x, y)
        SetInfo3(x, y, info)

def PacMap():
    # VERIFIE HORIZANTALE
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL2[x][y] != 0:
                CasesValuesPacMan(x, y)

    # VERIFIE VERTICALEMENT
    for y in range(HAUTEUR):
        for x in range(LARGEUR):
            if TBL2[x][y] != 0:
                CasesValuesPacMan(x, y)

def GumMap():
    # VERIFIE HORIZANTALE
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL3[x][y] != 0:
                CasesValuesGum(x, y)

    # VERIFIE VERTICALEMENT
    for y in range(HAUTEUR):
        for x in range(LARGEUR):
            if TBL3[x][y] != 0:
                CasesValuesGum(x, y)


def GhostMap():
   for ghost in Ghosts:  
         # VERIFIE HORIZANTALE
         for x in range(LARGEUR):
            for y in range(HAUTEUR):
                  if ghost != [x, y]:
                     CasesValuesGhost(x, y)

         # VERIFIE VERTICALEMENT
         for y in range(HAUTEUR):
            for x in range(LARGEUR):
                  if ghost != [x, y]:
                     CasesValuesGhost(x, y)


def PacManPossibleMove():
    L = []
    x, y = PacManPos
    if (TBL[x][y-1] == 0):
        L.append((0, -1))
    if (TBL[x][y+1] == 0):
        L.append((0, 1))
    if (TBL[x+1][y] == 0):
        L.append((1, 0))
    if (TBL[x-1][y] == 0):
        L.append((-1, 0))
    return L


def GhostsPossibleMove0(x, y):
    L0 = []
    if (TBL[x][y-1] == 0):
        L0.append((0, -1))
    if (TBL[x][y+1] == 0):
        L0.append((0, 1))
    if (TBL[x+1][y] == 0):
        L0.append((1, 0))
    if (TBL[x-1][y] == 0):
        L0.append((-1, 0))
    return L0
def GhostsPossibleMove2(x, y):
    L2 = []
    if (TBL[x][y-1] == 2):
        L2.append((0, -1))
    if (TBL[x][y+1] == 2):
        L2.append((0, 1))
    if (TBL[x+1][y] == 2):
        L2.append((1, 0))
    if (TBL[x-1][y] == 2):
        L2.append((-1, 0))
    return L2


score = 0
start = True
nbDisplay = 0
isPacmanSuper = False

#  tableau des coins
arrCorner = [[1, 1], [18, 1], [18, 9], [1, 9]]


def IAPacman():
    global PacManPos, Ghosts
    global score
    global start
    global isPacmanSuper
    global nbDisplay
    # deplacement Pacman
    L = PacManPossibleMove()
    SetInfo3(PacManPos[0], PacManPos[1], 0)
    # choix = random.randrange(len(L))
    # PacManPos[0] += L[choix][0]
    # PacManPos[1] += L[choix][1]
    if GUM[PacManPos[0]][PacManPos[1]] == 1:
        GUM[PacManPos[0]][PacManPos[1]] = 0
        score += 100
    if (start == True):
        
        # booleen pour que ça s'effectue qu'une seul fois
        start = False

    # definie map pour pacman
    GumMap()

    # on cherche le min des cases possible en déplacement

    minimum = TBL2[PacManPos[0] + L[0][0]][PacManPos[1] + L[0][1]]
    xAddMin = L[0][0]
    yAddMin = L[0][1]
    for i in range(len(L)):
        if (minimum > TBL2[PacManPos[0] + L[i][0]][PacManPos[1] + L[i][1]]):
            minimum = TBL2[PacManPos[0] + L[i][0]][PacManPos[1] + L[i][1]]
            xAddMin = L[i][0]
            yAddMin = L[i][1]
    PacManPos[0] += xAddMin
    PacManPos[1] += yAddMin

    # pour chaque coins on regarde si Pacman s'y trouve et qu'il y a une pacgum
    # si tel est le cas on passe en "hunting mode"
    # pendant le "hunting mode" on compte le nombre d'affichage
    # si le nombre d'affichage est à 16 Pacman repasse dans le mode "normal"
    for cornerCase in arrCorner:
        if (PacManPos[0] == cornerCase[0] and PacManPos[1] == cornerCase[1] and GUM[PacManPos[0]][PacManPos[1]] == 1):
            print("pass to hunting ghost mode")
            nbDisplay = 0
            isPacmanSuper = True
        if (nbDisplay == 16):
            isPacmanSuper = False
            nbDisplay = 0
    nbDisplay += 1

def GhostsHunted():
   for F in Ghosts: 
         # Boite ghost 
         L0 = GhostsPossibleMove0(F[0], F[1]) 
         L2 = GhostsPossibleMove2(F[0], F[1]) 
         if(L0!=[]):
               print("rentré")
               min = 100
               choix = (0,0)
               for l in L0:
                  if(TBL1[l[0]][l[1]]!= None):
                     res = int(TBL1[F[0] + l[0]][F[1] + l[1]])
                     if min >= res:
                        min = res
                        choix = l
               F[0] += choix[0]
               F[1] += choix[1]
         else:
            #  il reste dans la cage
               choix2 = random.randrange(len(L2))
               F[0] += L2[choix2][0]
               F[1] += L2[choix2][1]

def GhostsHunt():
   for F in Ghosts: 
         # Boite ghost 
         L0 = GhostsPossibleMove0(F[0], F[1]) 
         L2 = GhostsPossibleMove2(F[0], F[1]) 
         if(L0!=[]):
               print("rentré")
               max = 0
               choix = (0,0)
               for l in L0:
                  if(TBL1[l[0]][l[1]]!= None):
                     res = int(TBL1[F[0] + l[0]][F[1] + l[1]])
                     if max <= res:
                        max = res
                        choix = l
               F[0] += choix[0]
               F[1] += choix[1]
         else:
            #  il reste dans la cage
               choix2 = random.randrange(len(L2))
               F[0] += L2[choix2][0]
               F[1] += L2[choix2][1]

def IAGhosts():

    # map fontome
    for ghost in Ghosts:
      TBL1[ghost[0]][ghost[1]] = 0
    GhostMap()
    # deplacement Fantome
    if(isPacmanSuper):
      GhostsHunted()
    else:
      GhostsHunt()
   


#  Boucle principale de votre jeu appelée toutes les 500ms
iteration = 0


def PlayOneTurn():
    global iteration

    if not PAUSE_FLAG:
        iteration += 1
        if iteration % 2 == 0:
            IAPacman()
        else:
            IAGhosts()

    # si la position de pacman est égal à la position d'un ghost

    if (isPacmanSuper):
        Affiche(PacmanColor="red", message=score)
        return
    Affiche(PacmanColor="yellow", message=score)

#  demarrage de la fenetre - ne pas toucher


Window.mainloop()
