#DM algorithmique - Arbres et Graphes
#Master Bio-informatique

import random

#####################   Partie 1  #####################
#####################   Création de l'arbre   #####################

def creer_arbre_vide():
    return {'racine' : None}

def creer_etiquette(hauteur, longueur, orientation,coin_SO, coin_NE):
    return {
        'longueur':longueur, 
        'hauteur':hauteur, 
        'orientation':orientation, 
        'billes':[], 
        'SO':coin_SO, 
        'NE':coin_NE
        } 
        
def creer_sommet(etiquette, pere = None):
    return {'pere': pere, 
    'fils_droit': None,
    'fils_gauche' : None,
    'etiquette': etiquette}

def inserer_racine(arbre, etiquette):
    racine = creer_sommet(etiquette)
    arbre['racine'] = racine

def creer_arbre(etiquette=None):
    arbre = creer_arbre_vide()
    inserer_racine(arbre, etiquette)
    return arbre

def inserer_fils(pere,etiquette,type_fils) :
    fils = creer_sommet(etiquette,pere)
    if type_fils == "gauche":
        pere["fils_gauche"] = fils
    if type_fils == "droit":
        pere["fils_droit"] = fils


#####################   Manipulation de l'arbre   #####################

def filsGauche(pere):
    return pere["fils_gauche"]
    
def filsDroit(pere) :
    return pere["fils_droit"]

def pere(fils) :
    return fils["pere"]

def racine(arbre) :
    return arbre["racine"]

def decoupe(sommet):
    etiquette = sommet["etiquette"]

    if etiquette['orientation'] == "horizontale" :
        H = etiquette['hauteur']/2
        L = etiquette['longueur']

        SO_droit = etiquette['SO']
        NE_droit = (etiquette['NE'][0],(etiquette['SO'][1] + etiquette['NE'][1])/2)
        SO_gauche = (etiquette['SO'][0] , (etiquette['SO'][1] + etiquette['NE'][1])/2)
        NE_gauche = etiquette['NE']

        orientation = "verticale"
        

    elif etiquette['orientation'] == "verticale" :
        H = etiquette['hauteur']
        L = etiquette['longueur']/2

        SO_droit = ((etiquette['SO'][0] + etiquette['NE'][0])/2 , etiquette['SO'][1])
        NE_droit = etiquette['NE']
        SO_gauche = etiquette['SO']
        NE_gauche =((etiquette['SO'][0] + etiquette['NE'][0])/2 , etiquette['NE'][1])

        orientation = "horizontale"
    
    etiquette_D= creer_etiquette(H, L, orientation,SO_droit,NE_droit)
    etiquette_G= creer_etiquette(H, L,  orientation,SO_gauche,NE_gauche)

    inserer_fils(sommet,etiquette_D,"droit")
    inserer_fils(sommet,etiquette_G,"gauche")

def decoupes(sommet_de_depart, num_etapes):
    
    if num_etapes>0:
        decoupe(sommet_de_depart)

        num_etapes -= 1
        decoupes(filsGauche(sommet_de_depart), num_etapes)
        decoupes(filsDroit(sommet_de_depart), num_etapes)

#####################   EXO 1    #####################

def construire_arbre_collision(H,L,nb_etape):

    arbre = creer_arbre_vide()

    etiquette = creer_etiquette(H,L,"horizontale", (0,0),(L,H))

    inserer_racine(arbre,etiquette)

    decoupes(racine(arbre),nb_etape)
    
    return arbre


#####################   EXO 2    #####################

def bille_rentre(salle, position, rayon):
    '''Permet de verifier si la bille rentre dans une salle
    Parametre
    ---------
    salle : salle dans la quelle on vérifie si la bille rentre
    position : position (x,y) de la bille dans la boite la plus grande
    rayon : int, rayon de la bille 
    Return
    ---------
    fit_check : bool, permet de savoir si la bille rentre dans la salle
    '''
    etiquette = salle['etiquette']
    SO = etiquette['SO']
    NE= etiquette['NE']
    fit_check = True


    if position[0] - rayon < SO[0] or position[1] - rayon < SO[1]:
        fit_check = False
    if position[0] + rayon > NE[0] or position[1] + rayon > NE[1]:
        fit_check =False

    return fit_check   


def placer_bille(salle,position, rayon):
    '''Permet de placer un bille dans notre boite (salle)
    Paramètre
    ---------
    salle : la boite dans la quelle on place notre bille (sous forme d'arbre binaire)
    position : la position (x,y) à laquelle est placée la bille
    rayon : int, le rayon de la bille

    '''
    if not bille_rentre(salle, position,rayon):
        return
    elif filsGauche(salle)!=None and filsDroit(salle)!=None:
        if bille_rentre(filsGauche(salle), position, rayon):
            placer_bille(filsGauche(salle),position, rayon)
        else :
            salle["etiquette"]["billes"].append((position, rayon))
        if bille_rentre(filsDroit(salle), position, rayon):
            placer_bille(filsDroit(salle),position, rayon)
        else :
            salle["etiquette"]["billes"].append((position, rayon))
    else :
        salle["etiquette"]["billes"].append((position, rayon))
    
#####################   EXO 3    #####################

def dans_la_bille(bille, position):
    '''Permet de verifier si la position rentre dans la bille
    Parametre
    ---------
    bille : bille dans la quelle on vérifie si la position rentre
    position : position (x,y), on vérifie qu'elle appartient à l'aire de la bille
    rayon : int, rayon de la bille 
    Return
    ---------
    fit_check : bool, permet de savoir si la posistion rentre dans l'aire de la bille
    '''
    position_bille = bille[0]
    rayon = bille[1]
    fit_check = False
    #Calcul de la distance entre le point de position(x,y) et le centre de la bille avec le théorème de Pythagore
    distance = ((position_bille[0]-position[0])**2+(position_bille[1]-position[1])**2)**0.5
    # Si la distance ntre le point et le centre de la bille est inférieur au rayon de la bille, le point est dans l'aire de la bille
    if distance <= rayon:
        fit_check=True
    
    return fit_check

'''
Donne la liste des billes qui sont en collisions avec un point donnée
    Parametres
    ----------
    salle : salle dans contenants les billes testé pour la collisions avec le point
    positions: point de coordonée à tester

    Return
    ----------
    results : la liste de toutes les billes en coollision avec bille1
'''
def lister_bille(salle, position):
    results = []
    if filsDroit(salle)!=None:
        if bille_rentre(filsDroit(salle), position, 0):
            results=lister_bille(filsDroit(salle), position)
        if bille_rentre(filsGauche(salle), position, 0):
            results=lister_bille(filsGauche(salle), position)
    billes_possibles = salle['etiquette']['billes']
    for bille in billes_possibles:
        if dans_la_bille(bille, position):
            results.append(bille)

    return results


#####################   EXO 4    #####################
    '''Verifie si il y a collision entre 2 billes
    Parametres
    ----------
    bille1 et bille2 : 2 billes sous la forme ((x,y),r) où x et y leurs positions et r leurs rayons
    Return
    ----------
    check : Vrai si il y a collisions, Faux sinon
    '''
def check_collision(bille1,bille2):
    if bille1==bille2:
        return False
    coor1 = bille1[0]
    coor2 = bille2[0]
    r1 = bille1[1]
    r2 = bille2[1]
    check = False
    #On calcule la distance entre les centres des 2 billes (théorème de Pythagore rpz)
    distance = ((coor1[0]-coor2[0])**2 + (coor1[1]-coor2[1])**2)**0.5
    #Si la distance entre les 2 centres est inférieure ou égale à la sommes des rayons
    #cela signifie que les 2 billes on des points communs
    if distance <= (r1 + r2):
        check = True
    return check


    '''Permet de vérifier si une bille est en collision avec d'autres dans une salle
    Parametres
    ----------
    bille1 : la bille qu'on va choisir pour savoir si elle est en collision avec d'autres
    salle : la salle dans laquelle on véifie si la bille1 est en 
    collision avec les billes contenue dans cette salle
    Return
    ----------
    results : la liste de toutes les billes en coollision avec bille1
    '''

def lister_collisions_bille(salle, bille1) :
    results = []
    billes = salle['etiquette']['billes']
    if filsDroit(salle)!=None:
        results+=lister_collisions_bille(filsDroit(salle), bille1)
        results+=lister_collisions_bille(filsGauche(salle), bille1)
    if len(billes) > 0 :
        for bille2 in billes:
            if check_collision(bille1,bille2):
                results.append(bille2)
    else :
        print("Cette salle ne contient pas de billes")

    return results

#####################   EXO 5    #####################
'''
Liste toute les collisions ayant lieu entre les billes d'une salle
    Parametres
    ----------
    salle : la salle dans laquelle veux tester les collisions
    Return
    ----------
    results : la liste de toutes les paires de billes en collisions dans la salle
'''
def liste_de_toutes_les_collisions(salle):
    results = []
    billes = salle['etiquette']['billes']
    if filsDroit(salle)!=None:
        results+=liste_de_toutes_les_collisions(filsDroit(salle))
        results+=liste_de_toutes_les_collisions(filsGauche(salle))
    if len(billes) > 0 :
        for bille in billes:
            results+=lister_collisions_bille(salle,bille)
            
    else : 
        return "Cette salle ne contient pas de billes"
    return results
'''
En utilisant notre programme qui découpe la salle en sous-salle rangé dans un arbre lorsque l'on test tout les collisions ayant lieux pour les billes de la salle
les collisions à tester sont celle des billes avec elles-même ainsi que les billes des salles filles puisqu'il s'agit de l'ensemble des billes de la salle.
Les collisions entre billes issu de salles "soeurs" sont ainsi économiser des comparaison puisque impossible.
Ainsi prenons l'arbre d'exemple à sa racine:
Avec la structure en arbre les comparaison effectués seront: 
6-3,6-4,6-7,6-1,6-2,6-5 3-4,3-1,3-2,3-5, 4-1,4-2,4-5, 1-2, soit 14 comparaisons
Sans la structure en arbre, avec des comparaison simple paire à paire, les comparaisons effectués seront:
6-3,6-4,-6-7,6-1,6-2,6-5, 7-1,7-2,7-5, 3-4,3-7,3-1,3-2,3-5, 4-7,4-1,4-2,4-5, 1-2,1-5, 2-5, soit 21 comparaisons

Et cette différence varie exponentiellement avec le nombre de billes et le nombre d'étage de l'arbre.
'''

####################### MAIN #####################
H=1500.0
L=2000.0
nb=4
    

if H>L:
    rayonmax=L/2
else:
    rayonmax=H/2

compteur=0
arbre=construire_arbre_collision(H, L, nb)
salle=racine(arbre)
for i in range(nb-1):
    salle=filsDroit(salle)

for i in range(10000):
    rayon=random.random()*rayonmax
    x=rayon+random.random()*(L-2*rayon)
    y=rayon+random.random()*(H-2*rayon)
    if placer_bille(arbre['racine'], (x,y),rayon)==True:
        compteur+=1
ptx=random.random()*L
pty=random.random()*H
listbille=lister_bille(racine(arbre), (ptx,pty))
print('\n',len(salle['etiquette']['billes']),'billes dans la salle')
print(len(listbille),'billes au point (x,y)')

listcol=lister_collisions_bille(salle, salle['etiquette']['billes'][0])
print(len(listcol),'collisions avec la bille 1')

listallcol=liste_de_toutes_les_collisions(salle)
print(len(listallcol),'collisions totales dans la salle')



#####################   Partie 2  #####################
#####################   EX 1    #####################
'''
Les cycles appartiennent aux graphes non orientés, les circuits aux graphes orientés.
Un cycle (circuit) est un chemin (de tailles supérieure) commençant et se terminant par le
le même sommet. Ce cycle(circuit) est élémentaire si il ne passe q'un seul fois par un
même
sommet (sauf son premier/dernier).
'''
#####################   EX 2    #####################
def chemin_existe(matAdj,depart, arrivee):
    '''Permet de vérifier si il existe un chemin entre les sommets depart et arrivée
    Parametre
    ---------
    matAdj : notre graphe prenant la forme d'un matrice adjacente
    depart : sommet de depart
    arrivée : sommet d'arrivee
    Return
    ---------
    Un boolean indiquant si il existe un chemin ou pas
    '''
    parcours= [depart]
    chemin = [False]*len(matAdj) # Liste qui sert à checker si on est deja passe par un sommet
    while len(parcours) > 0:
        temp = parcours.pop(0)
        chemin[temp] = True
        for i in range(len(matAdj)):
            # On verifie si il y a un arc qui part de notre sommet et si 
            # le sommet de destination n' pas été déjà utilisé dans le chemin
            if matAdj[temp][i] > 0 and not chemin[i]:
                    parcours.append(i)
                    chemin [i] = True
            # On verifie la condition d'arrivee
            elif matAdj[temp][i] > 0 and i == arrivee:
                return True
    return False

def cycle_existe(matAdj):
    '''Permet de vérifier si il existe un cycle dans notre graphe
    ---------
    matAdj : notre graphe prenant la forme d'un matrice adjacente

    Return
    ---------
    Un boolean indiquant si il existe un cycle ou pas
    '''
    for i in range(len(matAdj)):
        # Onverfie si il existe un chemin qui part et arrive du meme sommet, donc un cycle
        if chemin_existe(matAdj,i,i): 
            return True
    return False