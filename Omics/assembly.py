import itertools as iter

def readFASTQ(filename):
    '''
    Permet de lire un fichier fastq et de rentrer les séquences avec leurs nom dans un dicctionnaire

    Paramètre:
    -filename(str) : nom du fichier avec son extension
    '''
    Dicfastq={}
    with open(filename,"r") as fasta:
        sequence=''
        name=''
        for line in fasta:
            if line.startswith('@'):
                if name!='':
                    Dicfastq[name]=sequence
                    sequence=''
                name=line[1:-1]
            elif line.startswith('A') or line.startswith('C') or line.startswith('T') or line.startswith('G'):
                sequence+=line[:-1]
        Dicfastq[name]=sequence
    return Dicfastq

def overlap(r1,r2):
   '''
    Compare la fin de la séquence r1 avec le début de la séquence r2 et renvoi la longueur et la séquence du chevauchement

    Paramètre:
    r1(str) : séquence 1
    r2(str)  : séquence 2
    '''
    listover=[]
    x=0
    y=0
    while y <= (len(r1)-1):
        if r2[x]==r1[y]:
            listover.append(r2[x])
            x+=1
            y+=1
        elif r2[0]==r1[y]:
            listover=[]
            listover.append(r2[0])
            x=1
            y+=1
        else:
            x=0
            y+=1
            listover=[]
    return x, listover


def compute_assembly_scs(read_set):
    '''
    Assemble les séquences dans toutes les configuration possible et renvoi la chaine la plus courte obtenu

    Paramètre:
    -read_set(list) : liste contenant un ensemble de séquences
    '''
    mini=999999999999999999999999999
    test=iter.permutations(read_set)
    for possib in test:
        ch=str(possib[0])
        for i in range(len(possib)-1):
            seq1=ch
            seq2=possib[i+1]
            res=overlap(seq1, seq2)
            if res[0]!=0:
                lim=res[0]
                seq2cut=seq2[:-lim]
                ch=seq2cut+ch
            else:
                ch=seq2+ch
        if len(ch) < mini:
            mini=len(ch)
            meilleure=ch
    return mini, meilleure
    
    
def find_best_overlap(read_set):
    '''
    Test le chevauchement de toutes les séquences entre elles et renvoi les deux séquence ayant le chevauchement le plus important ainsi que le longueur et la séquence de ce chevauchement

    Paramètre:
    -read_set(list) : liste contenant un ensemble de séquences
    '''
    meilleures=''
    maxi=0
    over=[]
    for i in range(len(read_set)):
        print('best overlap: {:.2f}%'.format(((i/(len(read_set)-1))*100)),end='\r')
        for j in range(len(read_set)):
            if j != i:
                comparaison=overlap(read_set[i], read_set[j])
                if comparaison[0] > maxi:
                    meilleures=[]
                    maxi=comparaison[0]
                    over=comparaison[1]
                    meilleures.append(read_set[j])
                    meilleures.append(read_set[i])
    return meilleures, [maxi, over]
        



def compute_assembly_greedy(read_set):
    '''
    Trouve le chevauchement de séquence le plus important dans la liste de séquence et fusionne ces deux séquence, et répète l'action autant de fois qu'il le faut pour obtenir le nombre minimal de séquences

    Paramètre:
    -read_set(list) : liste contenant un ensemble de séquences
    '''
    tmp=read_set.copy()
    while len(tmp)!=1:
        print('\ngreedy:{:d}'.format(len(tmp)))
        pair=find_best_overlap(tmp)
        if pair[1][0]!=0:
            r1=pair[0][0]
            r2=pair[0][1]
            limite=pair[1][0]
            j=0
            while j <= (len(tmp)-1):
                if tmp[j]==r2:
                    del tmp[j]
                    j=len(tmp)+1
                else:
                    j+=1
            for i in range(len(tmp)):
                if tmp[i]==r1 :
                    r1=r1[:-limite]
                    tmp[i]=r1+r2
        else:
            return tmp
    return tmp


