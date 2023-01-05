import random

def Tri(L):
    pair=0
    i=0
    while pair==0 and i<len(L):
        if L[i]%2==0:
            pair=L[i]
        i+=1
    impair=0
    i=0
    while impair==0 and i<len(L):
        if L[i]%2!=0:
            impair=L[i]
        i+=1

    for i in L:
        if i%2==0:
            if pair<=i:
                pair=i
                continue
            else:
                return False
        else:
            if impair>=i:
                impair=i
                continue
            else:
                return False
    return True

result=False
while result==False:
    L=[]
    for i in range(10):
        L.append(random.randint(0,20))
    print(L)

    Lpair=[]
    Limpair=[]
    for i in L:
        if i%2==0:
            Lpair.append(i)
        else:
            Limpair.append(i)
    print (Lpair,'\n',Limpair)
    print(Tri(L))
    result=Tri(L)



