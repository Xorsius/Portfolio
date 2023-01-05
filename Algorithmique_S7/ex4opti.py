def rec(ouv,fer,par,liste):
    if ouv>fer:
        return
    if ouv==0 and fer==0:
        liste.append(par)
        return
    if ouv==0:
        rec(ouv,fer-1,(par+')'),liste)
    else:
        rec(ouv-1,fer,(par+'('),liste)
        rec(ouv,fer-1,(par+')'),liste)

def genere_parentheses(n):
    liste=[]
    if n%2==0:
        rec(n/2,n/2,'',liste)
    return liste


def genere_parentnorec(n):
    
    ouv = 0
    fer = n
    list = []
    mot = ")"*n

    t = True
    while t == True:

        m = mot
        m[0] = "("
        ouv1 = 1
        fer1 = fer -1
        if fer == ouv : 
            t = False
        
        


        list.append(m)

            

        


    

    



    return list


    }

        

for i in genere_parentheses(6):
    print(i)



