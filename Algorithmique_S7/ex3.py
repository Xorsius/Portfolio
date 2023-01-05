import random

class pile:
    def __init__(self):
        self.pile=[]

def creer_pile():
    return pile()
def empiler(p,e):
    p.pile.append(e)
def depiler(p):
    return p.pile.pop()
def taille(p):
    return len(p.pile)


def trier(pile):
    pile1=creer_pile()
    pile2=creer_pile()
    v1=None
    v2=None

    while taille(pile)>0 or taille(pile2)>0: 
        while taille(pile)>0:
            if taille(pile1)>0:
                v1=depiler(pile)
                empiler(pile,v1)
                v2=depiler(pile1)
                empiler(pile1,v2)
                if v1<=v2:
                    empiler(pile1,depiler(pile))
                else:
                    empiler(pile2,depiler(pile))
            else:
                empiler(pile1,depiler(pile))
        if taille(pile)>0 or taille(pile2)>0:
            while taille(pile1)>0 or taille(pile2)>0:
                if taille(pile1)>0:
                    v1=depiler(pile1)
                    empiler(pile1,v1)
                else:
                    empiler(pile,depiler(pile2))
                    continue
                if taille(pile2)>0:
                    v2=depiler(pile2)
                    empiler(pile2,v2)
                else:
                    empiler(pile,depiler(pile1))
                    continue
                if v1<=v2:
                    empiler(pile,depiler(pile1))
                else:
                    empiler(pile,depiler(pile2))
    while taille(pile1)>0:
        empiler(pile2,depiler(pile1))
    while taille(pile2)>0:
        empiler(pile,depiler(pile2))

def swap(p,k,n):
    pile1=creer_pile()
    pile2=creer_pile()

    for i in range(k):
        empiler(pile1,depiler(p))
    for i in range(n-k):
        empiler(pile2,depiler(p))
    for i in range(k):
        empiler(p,depiler(pile1))
    for i in range(n-k):
        empiler(p,depiler(pile2))




p=creer_pile()
liste=[]
for i in range(10):
    val=random.randint(0,10)
    empiler(p,val)
    liste.append(val)
pilecopy=creer_pile()

print(liste)
# print('\n SWAP !!! \n')
# swap(p,3,7)

trier(p)

while taille(p)!=0:
    print(depiler(p))
