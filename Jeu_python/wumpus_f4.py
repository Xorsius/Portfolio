import time
import random as r
from os import system
import warnings

arrow = 0

#ENTITIES--------------------------------------------------------------------------------------------------------------

def Wumpus(action,board = 0):
    """
    Triggers the specified reaction of the Wumpus:
    1-Wumpus eat the player
    2-Wumpus warning
    3-Wumpus awakening by arrow whistle and Wumpus move
    4-Wumpus defeated by the player

    :Parameter:
        - action(int) : selected reaction index
        - board(list) : game board
    """
    if action == 1:
        print("Le Wumpus vous a mangé tout cru !")
        gameover(board)
    elif action == 2:
        print("Un ronflement terrifiant retenti")

    elif action == 3:
        print("Le Wumpus a entendu le sifflement de votre flèche et s'est réveillé")
        wumpus_move(board)
    elif action == 4:
        print("Votre flèche a occis le terrible Wumpus")
        Win(board)

def bat(action,board = 0,C = 0,room = 0):
    """
    Triggers the specified reaction of the bat
    1-Take the player to a random room
    2-bat warning

    :Parameter:
        - action(int) : selected reaction index
        - board(list) : game board
        - C(int) : current player position
        - room(int) : selected room position
    """
    if action == 1:
        print("Une chauve-souris vous emporte jusqu'à une autre salle")
        player_move(board,C,r.randint(0,11))
    elif action == 2:
        print("Vous entendez des battements d'ailes")

def well(action,board = 0):
    """
    Triggers the specified reaction of the well:
    1-Player's fall into the well and die
    2-well warning

    :Parameter:
        - action(int) : selected reaction index
        - room(int) : selected room position
    """
    if action == 1:
        print("Vous trébuchez au fond d'un puit et vous fraccassez la tête en son fond")
        gameover(board)
    elif action == 2:
        print("Vous sentez un courant d'air")

def Room(action,board,C,room = 0):
    """
    Triggers the specified reaction of the room:
    1-entry into an empty room

    :Parameter:
        - action(int) : selected reaction index
        - board(list) : game board
        - C(int) : current player position
        - room(int) : selected room position
    """
    if action == 1:
        print("Vous vous deplacez sans encombre jusqu'à la prochaine salle")
        enterroom(board,C,room)


#BOARD---------------------------------------------------------------------------------------------------------------


def disboard(C,adj):
    """
    Displays the game board
    :Parameters:
        - C(int) : current player position
        - adj(list) : list of selectable adjacent rooms
        - length(int) : size of the game board
    """
    dboard = []
    for i in range(12):
        dboard.append("[]")
    dboard[C] = "C"
    for i in range(len(adj)):
        dboard[adj[i]] = str(i+1)

    print("""
                     {:^3s}---------{:^3s}
                     /  \       /  \\
                    /   {:^3s}---{:^3s}   \\
                   /    /       \    \\
                  {:>2s}---{:>2s}       {:>2s}---{:>2s}
                   \    \       /    /
                    \   {:^3s}---{:^3s}   /
                     \  /       \  /
                     {:^3s}---------{:^3s}""".format(dboard[0],dboard[1],
                     dboard[6],dboard[7], dboard[5],dboard[11],dboard[8],dboard[2],
                     dboard[10],dboard[9], dboard[4],dboard[3]))


def disrealboard(board,length=12):
    dboard=[]
    for i in range(length):
        if board[i]==0:
            dboard.append('[]')
        else:
            dboard.append(str(board[i]))
    print("          {:^3s}---------{:^3s}".format(dboard[0],dboard[1]))
    print("          /  \       /  \ ")
    print("         /   {:^3s}---{:^3s}   \ ".format(dboard[6],dboard[7]))
    print("        /    /       \    \ ")
    print("      {:>2s}---{:>2s}        {:>2s}---{:>2s}".format(dboard[5],dboard[11],dboard[8],dboard[2]))
    print("        \    \       /    / ")
    print("         \   {:^3s}---{:^3s}   / ".format(dboard[10],dboard[9]))
    print("          \  /       \  / ")
    print("          {:^3s}---------{:^3s}".format(dboard[4],dboard[3]))

def getEmptyRoom(board, length):
    """
    Return a list of cells on the board that does not contain any element
    :Parameters:
        - board(list) : game board
        - length(int) : size of the game board
    :Returns:
        - empty(list) : list of empty cells
    """
    empty  =  []
    for i in range(length):
        if board[i] == 0:
            empty.append(i)
    return empty


def initialize(board, length = 12):
    """
    Place each element of the game randomly
    :Parameters:
        - board(list) : game board
        - length(int) : size of the game board
    """
    global arrow
    arrow = 3
    if board != []:
        for i in range(length):
            board.pop(0)
    for i in range(length):
        board.append(0)
    board[0] = 'C'
    for pop in ['W', 'P1', 'P2', 'B1', 'B2']:
        pos  =  r.choice(getEmptyRoom(board, length))
        board[pos]  =  pop

def getPosition(board,entity):
    """
    Returns the current position of the entity
    :Parameters:
        - board(list) : game board
        - entity(str) : board symbol of the wanted entity
    :Returns:
        - i(int) : index of the cell where the entity is located
    """
    for i in range(12):
        if board[i] == entity:
            return i


def choosePossibilities(board,C,length = 12):
    """
    Returns a list of 3 cells around the player
    :Parameters:
        - board(list) : game board
        - length(int) : size of the game board
        - C(int) : current player position current player position

    :Returns:
        - choice(list)
    """
    choice  =  []
    if C < length/2:
        if C == 0:
            choice.append((C + 1))
            choice.append(length//2)
            choice.append(int((length//2)-1  ) )
        else :
            if C == int((length -1)/2):
                choice.append(0)
            else :
                choice.append(C+1)
            choice.append(C-1)
            choice.append(int((C%(length//2)+length/2)))
    else :
        if C == length - 1 :
            choice.append((length - 1) - 1)
            choice.append((length-1)//2)
            choice.append(int(((length-1)//2)+1    ))
        else:
            if C == length/2:
                choice.append(length-1)
            else :
                choice.append(C-1)
            choice.append(C+1)
            choice.append(int(C%((length//2))))
    return choice


def disrule():
    """
    Display the rules
    """
    rule = input("THE RULES !\n\n\n Appuyez sur entrée pour quitter.")

#EVENTS------------------------------------------------------------------------------------------------------------------


def player_move(board,C,room):
    """
    Check the type of the action(choice) selected rooms and execute
    the respective fucntion 1st reaction:

    :Parameter:
        - board(list) : game board
        - C(int) : current player position
        - room(int) : selected room position
    """
    if board[room] == "W":
        Wumpus(1,board)
    elif board[room] == "B1" or board[room] == "B2":
        bat(1,board,C,room)
    elif board[room] == "P1" or board[room] == "P2":
        well(1,board)
    elif board[room] == 0:
        Room(1,board,C,room)


def wumpus_move(board):
    """
    Change the Wumpus position to a random adjacent non occupied by bat
    or well rooms, if this is the current player rooms execute the
    gameover(function)

    :Parameter:
        - board(list) : game board
    """
    print("Le Wumpus s'éveil et se déplace de salle !")
    W=getPosition(board,'W')
    moves_p=choosePossibilities(board,W)
    i=0
    while i<(len(moves_p)-1):
        if board[moves_p[i]]!=0 and board[moves_p[i]]!='C':
            moves_p.pop(i)
        i+=1
    move=r.choice(moves_p)
    if board[move]=='C':
        print("Le Wumpus vous a trouvé et dévoré !")
        gameover(board)
    else:
        board[W]=0
        board[move]='W'




def alert(board,adj):
    """
    Test if the adjacent rooms of the player current location are occupied
    by entity and execute the 2nd reaction of the respectives functions

    :Parameter:
        - board(list) : game board
        - adj(list) : list of selectable adjacent rooms
    """
    for i in adj:
        if board[i] == "W":
            Wumpus(2, board)
        if board[i] == "B1" or board[i] == "B2":
            bat(2)
        if board[i] == "P1" or board[i] == "P2":
            well(2)

def enterroom(board,C,room):
    """
    Replace the player and target empty rooms position on the board

    :Parameter:
        - board(list) : game board
        - C(int) : current player position
        - room(int) : selected room position
    """
    board[C] = 0
    board[room] = 'C'


def shoot(board,target,adj):
    """
    Decrement the arrow counter by 1 and test and allows to test the different
    consequences of a shot

    :Parameter:
        - board(list) : game board
        - target(int) : the selected by the action() choice
        - adj(list) : list of selectable adjacent rooms the adjacent rooms of the player location
    """
    global arrow
    arrow -= 1
    if board[target] == "W":
        Wumpus(4,board)
    else:
        for i in adj:
            if board[i] == "W":
                Wumpus(3, board)
    if arrow == 0:
        print("Vous êtes à court de flèches !")
        gameover(board)

def Arrow():
    global arrow
    print("{:>100s} {} flèches".format("Vous avez encore",arrow))


def displayArrow(board):
    """
    Allows the player to shoot when he has the opportunity

    :Parameter:
        - board(list) : game board
    """
    print("Voulez-vous tirer une flèche ? (Y/N)")
    i = 0
    while i != "N" and i != "Y":
        i = input()
        if i != "N" and i != "Y" :
            print("Choix invalide, veuillez réessayer.")
    if i == "N" :
        return 0
    elif i == "Y":
        print("Où voulez-vous tirer ?\nroom 1\nroom 2\nroom 3")
        shootchoice = 0
        while shootchoice != 1 and shootchoice != 2 and shootchoice != 3:
            shootchoice = int(input())
            if shootchoice != 1 and shootchoice != 2 and shootchoice != 3:
                print("Choix invalide, veuillez réessayer.")
        adj = choosePossibilities(board,getPosition(board,'C'))
        shoot(board,adj[shootchoice-1],adj)
    else :
        print("Choix invalide, veuillez réessayer.")




def menu(board):
    system('clear')
    C=getPosition(board,'C')
    adj=choosePossibilities(board,C)
    # disrealboard(board)
    disboard(C,adj)
    global arrow
    print("{:>100s} {} flèches".format("Vous avez encore",arrow))
    alert(board,adj)
    if board[adj[0]]=='W' or board[adj[1]]=='W' or board[adj[2]]=='W':
        suite=displayArrow(board)
        if suite!=0:
            return

    dep  =  input("Voulez vous vous déplacer ? (Y/N): ")
    if dep == "Y" or dep =='y':
        print("Où voulez-vous vous déplacer ?\nroom 1\nroom 2\nroom 3")
        player_movechoice = 0
        while player_movechoice != 1 and player_movechoice != 2 and player_movechoice != 3:
            player_movechoice = int(input())
            if player_movechoice != 1 and player_movechoice != 2 and player_movechoice != 3:
                print("Choix invalide, veuillez réessayer.")
        player_move(board,C,adj[player_movechoice-1])
    else :
        print("1 - Retour ")
        print("2 - Rules   ")
        print("0 - Quitter  ")
        choice = int(input())
        if choice == 1:
            return
        if choice == 2:
            disrule()
        if choice == 0:
            print("bonne journée bisou !")
            exit()

def gameover(board):
    """
    Display a loosing message and propose to restart

    :Parameter:
        - board(list) : game board
    """
    print('\n'*5)
    for i in range(5):
        print("{:^100}".format("GAME OVER"),end = "\r")
        time.sleep(0.5)
        print("{:^100}".format("                          "),end = "\r")
        time.sleep(0.5)
    exit = input("Appuyez sur entrée pour recommencer")
    initialize(board)

def Win(board):
    """
    Display winning message

    :Parameter:
        - board(list) : game board
    """
    print('\n'*5)
    for i in range(5):
        print("{:^100}".format("You Win !!!"),end = "\r")
        time.sleep(0.5)
        print("{:^100}".format("                          "),end = "\r")
        time.sleep(0.5)
    exit = input("appuyez sur entrée pour recommencer")
    initialize(board)
    p = getPosition(board, "C")
    disboard(p, choosePossibilities(board, p))
