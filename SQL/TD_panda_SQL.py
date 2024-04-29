# import xlsxwriter
import pandas as pd
import psycopg2  # Python SQL driver for PostgreSQL
import psycopg2.extras
import numpy
import unidecode


def connexion(usr, psw):
    print("connexion a la base de donnees...")
    USERNAME = usr
    PASSWORD = psw  # à remplacer par le mot de passe d’accès aux bases
    try:
        conn = psycopg2.connect(
            host="pgsql", dbname=USERNAME, user=USERNAME, password=PASSWORD)
    except Exception as e:
        exit("connexion impossible à la base de données: " + str(e))
    print("connecté à la base de données")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cur, conn


def insert(conn, cur, table, keys, keyid, values):
    #préparation de l’exécution des requêtes (à ne faire qu’une fois)
    cur.execute("CREATE TABLE public.{}({}); ".format(table, keyid))
    print("Table person créée avec succès dans PostgreSQL")
    for i in range(len(values)):
        command = "INSERT INTO {}({}) VALUES ({})".format(
            table, keys, values[i])
        print(
            "Execution sur la base de donn ́ees de la commande d'insertion avec les valeurs", values[i])
        try:
            # Lancement de la requete.
            cur.execute(command)
        except Exception as e:
            # en cas d’erreur, fermeture de la connexion
            cur.close()
            conn.close()
            exit("error when running: " + command + " : " + str(e))
        # Nombre de lignes inserees
        count = cur.rowcount
        print(count, "enregistrement(s) insere(s) avec succes dans la table {} .".format(table))


def selectwhere(select, table, where, keys, conn, cur):
    command = "SELECT DISTINCT {} FROM {} WHERE {}".format(
        select, table, where)
    cur.execute(command)
    rows = cur.fetchall()
    if(not rows):
        print("No result found")
    # pour chaque ligne r du dictionnaire, affiche les données associées aux différentes
    for r in rows:
        print("\n")
        for key in keys:
            print("{} = {}".format(key, r[key]))


def disconnect(conn, cur):
    cur.close()
    conn.commit()
    conn.close()
    print("La connexion PostgreSQL est fermée")


def watisit(keys, value):
    keyid = []
    for i in range(len(value[1])):
        wut = keys[i]
        if value[1][i].isdigit():
            wut += " TEXT NOT NULL , "  # ça casse tout si y'a pas que des chiffre donc inutile
        else:
            wut += " TEXT NOT NULL, "
        keyid += [wut]
    keystr = "".join(keyid)
    return keystr[:-2]


def data(dataframe, keys):
    values = []
    valstr = []
    for i in range(len(dataframe)):
        line = list(dataframe.iloc[i])
        words = []
        for j in line:
            word = "".join(str(j))
            word = word.replace("'", "’")
            words += [word]
        values += [words]
        valstr += ["'"+"','".join(values[i])+"'"]

    keyid = watisit(keys, values)
    keystr = ",".join(keys)

    return valstr, keyid, keystr


def preselectwhere(tables, selectArrays, JOIN=[]):
    selectStr = ""
    tableStr = tables[0]
    keys = []
    for i in range(len(tables)):
        for j in selectArrays[i]:
            selectStr += "{}.{},".format(tables[i], j)
            keys += [j]
    if len(tables) > 1:
        for i in range(1, len(tables)):
            tableStr += " JOIN {} on {}".format(tables[i], JOIN[i-1])
        tableStr = tableStr
    return selectStr[:-1], tableStr, keys

##########################################################################


# Ex 1

df = pd.read_csv("oligo.csv", sep=';')  # import csv
columnname = list(df.keys())  # colonne nom
linename = list(df[columnname[0]])
df = df.set_index(df.columns[0])
print(df)
print(columnname)
print(linename)
diseases = list(df[columnname[1]])
print(diseases)
print(df.iloc[0:3], '\n')
print(df.iloc[1])

try:
    writer = pd.ExcelWriter('exemple.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')  # export
    writer.save()
except Exception:
    print(Exception)

# Ex 2
#1

ec_parc_s = pd.read_csv("ec_parc_s.csv", sep=';')  # import csv
sv_arret_p = pd.read_csv("sv_arret_p.csv", sep=';')  # import csv
arretKey = list(sv_arret_p.keys())
parcKey = list(ec_parc_s.keys())
print(parcKey)
print(arretKey)
nbLineParc = len(list(ec_parc_s[parcKey[1]]))
nbLineArret = len(list(sv_arret_p[arretKey[1]]))
print(nbLineParc)
print(nbLineParc)
print(ec_parc_s.iloc[0:10])
print(sv_arret_p.iloc[0:10], "\n"*5)


#2

arretValStr, arretKeyId, arretKeyStr = data(sv_arret_p, arretKey)
parcValStr, parcKeyId, parcKeyStr = data(ec_parc_s, parcKey)

log = connexion("bgottis", #ton mot de passe)
cur = log[0]
conn = log[1]
insert(conn, cur, "parcs", parcKeyStr, parcKeyId, parcValStr)  # parctable
insert(conn, cur, "arretsbus", arretKeyStr,
       arretKeyId, arretValStr)  # arrettable

#3a
tables = ["parcs", "arretsbus"]
JOIN = ["nom = LIBELLE"]
selectArrays = [["nom", "milieu", "service"], ["vehicule"]]

selectStr, tableStr, keys = preselectwhere(tables, selectArrays, JOIN)
where = "service LIKE '%HANDICAPES_TOTAL%' OR service LIKE '%HANDICAPES_PARTIEL%' AND vehicule='BUS'"


selectwhere(selectStr, tableStr, where, keys, conn, cur)

#3b

env = input("choississez un environnement: ")
env = unidecode.unidecode(env)
env = env.replace("d'", "")
env = env.replace("D'", "")
env = env.replace(" ", "_")
env = env.upper()
tables2 = ["parcs"]
selectArrays2 = [["nom", "milieu", "paysage"]]
selectStr2, tableStr2, keys2 = preselectwhere(tables2, selectArrays2)
where2 = "milieu LIKE '%{}%' OR paysage LIKE '%{}%'".format(env, env)

selectwhere(selectStr2, tableStr2, where2, keys2, conn, cur)

#4

sqlQuery = pd.read_sql_query(
    "SELECT DISTINCT {} FROM {} WHERE {}".format(selectStr, tableStr, where), conn)
df = pd.DataFrame(sqlQuery, columns=keys)
df = df.set_index(df.columns[0])

try:
    writer = pd.ExcelWriter('Query4.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Query4')  # export
    writer.save()
except Exception:
    print(Exception)

disconnect(conn, cur)
