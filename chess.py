from tkinter import *


root = Tk()
root.title("Chess")
root.geometry("800x600")




# menu = Menu(root)




# frame1 = Frame(root)
# frame1.pack(side=BOTTOM)



game_Board = Canvas(root, width=600, height=600, bg="#EBE8BE")
game_Board.pack(side=LEFT)




width_symbol = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
height_symbol = ['8', '7', '6', '5', '4', '3', '2', '1']
board_Color = ["#B5E1B2", "#84B661"]

def board_Display():

    for i in range(8):
        game_Board.create_text(10, 55+i*70, text=height_symbol[i])
        game_Board.create_text(55+i*70, 590, text=width_symbol[i])
        for j in range(8):
            game_Board.create_rectangle(20+i*70, 20+j*70, 20+(i+1)*70, 20+(j+1)*70, fill=((i*8+j-i)%2==0) and board_Color[0] or board_Color[1], outline="")

board_Display()




blank = {"chess_piece": "", "color": "", "image": ""}
pieces_Pos = {
    "white": {
        "pawn": [],
        "rook": [],
        "knight": [],
        "bishop": [],
        "queen": [],
        "king": []
    },
    "black": {
        "pawn": [],
        "rook": [],
        "knight": [],
        "bishop": [],
        "queen": [],
        "king": []
    }
}
pieces_Img = {
    "white": {
        "pawn": 0,
        "rook": 0,
        "knight": 0,
        "bishop": 0,
        "queen": 0,
        "king": 0
    },
    "black": {
        "pawn": 0,
        "rook": 0,
        "knight": 0,
        "bishop": 0,
        "queen": 0,
        "king": 0
    }
}
WHITE = "white"
BLACK = "black"
board_State = []

def setup_chess_Pieces():

    global board_State, pieces_Pos, pieces_Img, blank

    for i in range(8):
        temp = [];
        for j in range(8):
            temp.append(blank.copy());
        board_State.append(temp)

    for i in range(8):
        board_State[1][i]["chess_piece"], board_State[1][i]["color"] = ("pawn", BLACK)
        board_State[6][i]["chess_piece"], board_State[6][i]["color"] = ("pawn", WHITE)
        pieces_Pos[BLACK]["pawn"].append((1, i))
        pieces_Pos[WHITE]["pawn"].append((6, i))

    order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
    for i in range(8):
        board_State[0][i]["chess_piece"], board_State[0][i]["color"] = (order[i], BLACK)
        board_State[7][i]["chess_piece"], board_State[7][i]["color"] = (order[i], WHITE)
        pieces_Pos[BLACK][order[i]].append((0, i))
        pieces_Pos[WHITE][order[i]].append((7, i))

    ascending = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    color = [BLACK, WHITE]
    for i in range(2):
        for j in range(6):
            pieces_Img[color[i]][ascending[j]] = PhotoImage(file="./chess_pic/"+color[i]+"_"+ascending[j]+".png")

    for i in range(8):
        for j in range(8):
            if not board_State[i][j]["chess_piece"]=="":
                img = pieces_Img[board_State[i][j]["color"]][board_State[i][j]["chess_piece"]]
                board_State[i][j]["image"] = game_Board.create_image(20+j*70, 20+i*70, anchor=NW, image=img)

setup_chess_Pieces()




frame1 = Frame(root)
frame1.pack(side=RIGHT, fill=)

def Undo():
    pass
undo_Btn = Button(frame1, text="UNDO", command=Undo)
undo_Btn.pack(side=TOP, fill=X)

move_List = Message(frame1, width=200, relief=SUNKEN)
move_List.pack(side=BOTTOM, fill=Y)




player_Turn = WHITE

def next_Move():

    global player_Turn

    if player_Turn == WHITE:
        player_Turn = BLACK
    else:
        player_Turn = WHITE





available_Move = []
available_Show = []

def find_Check():

    global available_Move, board_State, player_Turn, pieces_Pos

    y = pieces_Pos[player_Turn]["king"][0][0]
    x = pieces_Pos[player_Turn]["king"][0][1]

    for i in range(y+1, 8):
        if board_State[i][x]["chess_piece"] != "":
            if board_State[i][x]["color"] != player_Turn and (board_State[i][x]["chess_piece"] == "queen" or board_State[i][x]["chess_piece"] == "rook"):
                return (i-y, 0)
            break

    for i in range(y-1, -1, -1):
        if board_State[i][x]["chess_piece"] != "":
            if board_State[i][x]["color"] != player_Turn and (board_State[i][x]["chess_piece"] == "queen" or board_State[i][x]["chess_piece"] == "rook"):
                return (i-y, 0)
            break

    for i in range(x+1, 8):
        if board_State[y][i]["chess_piece"] != "":
            if board_State[y][i]["color"] != player_Turn and (board_State[y][i]["chess_piece"] == "queen" or board_State[y][i]["chess_piece"] == "rook"):
                return (0, i-x)
            break
    
    for i in range(x-1, -1, -1):
        if board_State[y][i]["chess_piece"] != "":
            if board_State[y][i]["color"] != player_Turn and (board_State[y][i]["chess_piece"] == "queen" or board_State[y][i]["chess_piece"] == "rook"):
                return (0, i-x)
            break

    for i in range(1, min(8-x, y+1)):
        if board_State[y-i][x+i]["chess_piece"] != "":
            if board_State[y-i][x+i]["color"] != player_Turn:
                if board_State[y-i][x+i]["chess_piece"] == "queen" or board_State[y-i][x+i]["chess_piece"] == "bishop" or (i==1 and board_State[y-i][x+i]["chess_piece"] == "pawn" and player_Turn==WHITE):
                    return (-i, i)
            break

    for i in range(1, min(x+1, 8-y)):
        if board_State[y+i][x-i]["chess_piece"] != "":
            if board_State[y+i][x-i]["color"] != player_Turn:
                if board_State[y+i][x-i]["chess_piece"] == "queen" or board_State[y+i][x-i]["chess_piece"] == "bishop" or (i==1 and board_State[y+i][x-i]["chess_piece"] == "pawn" and player_Turn==BLACK):
                    return (i, -i)
            break

    for i in range(1, min(x+1, y+1)):
        if board_State[y-i][x-i]["chess_piece"] != "":
            if board_State[y-i][x-i]["color"] != player_Turn:
                if board_State[y-i][x-i]["chess_piece"] == "queen" or board_State[y-i][x-i]["chess_piece"] == "bishop" or (i==1 and board_State[y-i][x-i]["chess_piece"] == "pawn" and player_Turn==WHITE):
                    return (-i, -i)
            break

    for i in range(1, min(8-x, 8-y)):
        if board_State[y+i][x+i]["chess_piece"] != "":
            if board_State[y+i][x+i]["color"] != player_Turn:
                if board_State[y+i][x+i]["chess_piece"] == "queen" or board_State[y+i][x+i]["chess_piece"] == "bishop" or (i==1 and board_State[y+i][x+i]["chess_piece"] == "pawn" and player_Turn==BLACK):
                    return (i, i)
            break

    for i in range(8):
        coordY = ((int(i/4)>0) and ((i%4>1) and 2 or -2) or ((i%2) and 1 or -1))
        coordX = ((int(i/4)==0) and ((i%4>1) and 2 or -2) or ((i%2) and 1 or -1))
        if y+coordY>-1 and y+coordY<8 and x+coordX>-1 and x+coordX<8:
            if board_State[y+coordY][x+coordX]["chess_piece"] == "knight" and board_State[y+coordY][x+coordX]["color"]!=board_State[y][x]["color"]:
                return (coordY, coordX)
    
    return -1




check_Dist = -1
moved_State = {
    "white": {
        "0-0": True,
        "0-0-0": True
    },
    "black": {
        "0-0": True,
        "0-0-0": True
    }
}

def move_Set(y, x):

    global available_Move, board_State, player_Turn, pieces_Pos

    chess_Cardinals = [(1, 0),(0, 1),(-1, 0),(0, -1)]
    chess_Diagonals = [(1, 1),(-1, 1),(1, -1),(-1, -1)]

    if board_State[y][x]["chess_piece"] == "pawn":

        if board_State[y][x]["color"] == "black":
            if board_State[y+1][x]["chess_piece"] == "":
                available_Move.append((y+1, x))
                if y == 1 and board_State[y+2][x]["chess_piece"] == "":
                    available_Move.append((y+2, x))
            if x<7 and board_State[y+1][x+1]["chess_piece"]!="" and board_State[y+1][x+1]["color"]=="white":
                available_Move.append((y+1, x+1))
            if x>0 and board_State[y+1][x-1]["chess_piece"]!="" and board_State[y+1][x-1]["color"]=="white": 
                available_Move.append((y+1, x-1))

        if board_State[y][x]["color"] == "white":
            if board_State[y-1][x]["chess_piece"] == "":
                available_Move.append((y-1, x))
                if y == 6 and board_State[y-2][x]["chess_piece"] == "":
                    available_Move.append((y-2, x))
            if x<7 and board_State[y-1][x+1]["chess_piece"]!="" and board_State[y-1][x+1]["color"] == "black":
                available_Move.append((y-1, x+1))
            if x>0 and board_State[y-1][x-1]["chess_piece"]!="" and board_State[y-1][x-1]["color"] == "black": 
                available_Move.append((y-1, x-1))

    elif board_State[y][x]["chess_piece"] == "rook":

        for i in range(4):
            moveY, moveX = chess_Cardinals[i]
            newY, newX = (y, x)
            while newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["chess_piece"] == "":
                available_Move.append((newY+moveY, newX+moveX))
                newY += moveY
                newX += moveX
            if newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((newY+moveY, newX+moveX))

    elif board_State[y][x]["chess_piece"] == "knight":
        
        for i in range(8):
            moveY = ((int(i/4)>0) and ((i%4>1) and 2 or -2) or ((i%2) and 1 or -1))
            moveX = ((int(i/4)==0) and ((i%4>1) and 2 or -2) or ((i%2) and 1 or -1))
            if y+moveY>-1 and y+moveY<8 and x+moveX>-1 and x+moveX<8:
                if board_State[y+moveY][x+moveX]["chess_piece"]=="" or board_State[y+moveY][x+moveX]["color"]!=board_State[y][x]["color"]:
                    available_Move.append((y+moveY, x+moveX))
    
    elif board_State[y][x]["chess_piece"] == "bishop":

        for i in range(4):
            moveY, moveX = chess_Diagonals[i]
            newY, newX = (y, x)
            while newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["chess_piece"] == "":
                available_Move.append((newY+moveY, newX+moveX))
                newY += moveY
                newX += moveX
            if newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((newY+moveY, newX+moveX))

    elif board_State[y][x]["chess_piece"] == "queen":

        for i in range(4):
            moveY, moveX = chess_Cardinals[i]
            newY, newX = (y, x)
            while newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["chess_piece"] == "":
                available_Move.append((newY+moveY, newX+moveX))
                newY += moveY
                newX += moveX
            if newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((newY+moveY, newX+moveX))

        for i in range(4):
            moveY, moveX = chess_Diagonals[i]
            newY, newX = (y, x)
            while newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["chess_piece"] == "":
                available_Move.append((newY+moveY, newX+moveX))
                newY += moveY
                newX += moveX
            if newX+moveX>-1 and newX+moveX<8 and newY+moveY>-1 and newY+moveY<8 and board_State[newY+moveY][newX+moveX]["color"] != board_State[y][x]["color"]:
                available_Move.append((newY+moveY, newX+moveX))
    
    elif board_State[y][x]["chess_piece"] == "king":

        for i in range(4):
            moveY, moveX = chess_Cardinals[i]
            if x+moveX>-1 and x+moveX<8 and y+moveY>-1 and y+moveY<8 and (board_State[y+moveY][x+moveX]["chess_piece"] == "" or board_State[y+moveY][x+moveX]["color"] != board_State[y][x]["color"]):
                available_Move.append((y+moveY, x+moveX))

        for i in range(4):
            moveY, moveX = chess_Diagonals[i]
            if x+moveX>-1 and x+moveX<8 and y+moveY>-1 and y+moveY<8 and (board_State[y+moveY][x+moveX]["chess_piece"] == "" or board_State[y+moveY][x+moveX]["color"] != board_State[y][x]["color"]):
                available_Move.append((y+moveY, x+moveX))

        if moved_State[player_Turn]["0-0"]:
            blocked = False
            for i in range(5, 7):
                if board_State[y][i]["chess_piece"] != "":
                    blocked = True
                    break
            if not blocked:
                available_Move.append((y, x+2))
        
        if moved_State[player_Turn]["0-0-0"]:
            blocked = False
            for i in range(1, 4):
                if board_State[y][i]["chess_piece"] != "":
                    blocked = True
                    break
            if not blocked:
                available_Move.append((y, x-2))

def block_Check(y, x):

    global board_State, available_Move, player_Turn, pieces_Pos, check_Dist

    pos = pieces_Pos[player_Turn]["king"][0]

    if check_Dist != -1:
        if board_State[y][x]["chess_piece"] == "king":
            return

        elif check_Dist[0] == 0:
            if check_Dist[1] < 0:
                for i in range(len(available_Move)-1, -1, -1):
                    if available_Move[i][0] != pos[0] or available_Move[i][1]-pos[1] < check_Dist[1] or available_Move[i][1] > pos[1]:
                        available_Move.pop(i)

            else:
                for i in range(len(available_Move)-1, -1, -1):
                    if available_Move[i][0] != pos[0] or available_Move[i][1]-pos[1] > check_Dist[1] or available_Move[i][1] < pos[1]:
                        available_Move.pop(i)

        elif check_Dist[1] == 0:
            if check_Dist[0] < 0:
                for i in range(len(available_Move)-1, -1, -1):
                    if available_Move[i][1] != pos[1] or available_Move[i][0]-pos[0] < check_Dist[0] or available_Move[i][0] > pos[0]:
                        available_Move.pop(i)

            else:
                for i in range(len(available_Move)-1, -1, -1):
                    if available_Move[i][1] != pos[1] or available_Move[i][0]-pos[0] > check_Dist[0] or available_Move[i][0] < pos[0]:
                        available_Move.pop(i)

        elif check_Dist[0]*check_Dist[1] < 0:
            if check_Dist[0] < 0:
                for i in range(len(available_Move)-1, -1, -1):
                    if abs(available_Move[i][0]-pos[0]) != abs(available_Move[i][1]-pos[1]) or (available_Move[i][0]-pos[0])*(available_Move[i][1]-pos[1]) >= 0 or available_Move[i][0]-pos[0] < check_Dist[0] or available_Move[i][0] > pos[0]:
                        available_Move.pop(i)

            else:
                for i in range(len(available_Move)-1, -1, -1):
                    if abs(available_Move[i][0]-pos[0]) != abs(available_Move[i][1]-pos[1]) or (available_Move[i][0]-pos[0])*(available_Move[i][1]-pos[1]) >= 0 or available_Move[i][0]-pos[0] > check_Dist[0] or available_Move[i][0] < pos[0]:
                        available_Move.pop(i)

        elif check_Dist[0]*check_Dist[1] > 0:
            if check_Dist[0] < 0:
                for i in range(len(available_Move)-1, -1, -1):
                    if abs(available_Move[i][0]-pos[0]) != abs(available_Move[i][1]-pos[1]) or (available_Move[i][0]-pos[0])*(available_Move[i][1]-pos[1]) <= 0 or available_Move[i][0]-pos[0] < check_Dist[0] or available_Move[i][0] > pos[0]:
                        available_Move.pop(i)

            else:
                for i in range(len(available_Move)-1, -1, -1):
                    if abs(available_Move[i][0]-pos[0]) != abs(available_Move[i][1]-pos[1]) or (available_Move[i][0]-pos[0])*(available_Move[i][1]-pos[1]) <= 0 or available_Move[i][0]-pos[0] > check_Dist[0] or available_Move[i][0] < pos[0]:
                        available_Move.pop(i)

        else:
            available_Move = []

def commit_Suicide(y, x):

    global pieces_Img, available_Move, player_Turn, pieces_Pos, blank

    blocking = False
    diffY = y - pieces_Pos[player_Turn]["king"][0][0]
    diffX = x - pieces_Pos[player_Turn]["king"][0][1]

    if diffY == 0 and diffX == 0:
        
        for i in range(len(available_Move)-1, -1, -1):
            
            move = available_Move[i]
            temp = blank.copy()
            pos = pieces_Pos[player_Turn]["king"][0]
            BoW = (player_Turn==WHITE) and 7 or 0

            if abs(move[1]-x)==2:

                board_State[move[0]][move[1]] = board_State[pos[0]][pos[1]].copy()
                board_State[pos[0]][pos[1]] = blank.copy()

                if move[1]-x==2:

                    board_State[BoW][5] = board_State[BoW][7].copy()
                    board_State[BoW][7] = blank.copy()

                    pieces_Pos[player_Turn]["king"][0] = move
                    pieces_Pos[player_Turn]["rook"].remove((BoW, 7))
                    pieces_Pos[player_Turn]["rook"].append((BoW, 5))

                    coord_Check = find_Check()

                    pieces_Pos[player_Turn]["king"][0] = pos
                    pieces_Pos[player_Turn]["rook"].remove((BoW, 5))
                    pieces_Pos[player_Turn]["rook"].append((BoW, 7))

                    board_State[pos[0]][pos[1]] = board_State[move[0]][move[1]].copy()
                    board_State[move[0]][move[1]] = blank.copy()

                    board_State[BoW][7] = board_State[BoW][5].copy()
                    board_State[BoW][5] = blank.copy()

                else:

                    board_State[BoW][3] = board_State[BoW][0].copy()
                    board_State[BoW][0] = blank.copy()

                    pieces_Pos[player_Turn]["king"][0] = move
                    pieces_Pos[player_Turn]["rook"].remove((BoW, 0))
                    pieces_Pos[player_Turn]["rook"].append((BoW, 3))

                    coord_Check = find_Check()

                    pieces_Pos[player_Turn]["king"][0] = pos
                    pieces_Pos[player_Turn]["rook"].remove((BoW, 3))
                    pieces_Pos[player_Turn]["rook"].append((BoW, 0))

                    board_State[pos[0]][pos[1]] = board_State[move[0]][move[1]].copy()
                    board_State[move[0]][move[1]] = blank.copy()

                    board_State[BoW][0] = board_State[BoW][3].copy()
                    board_State[BoW][3] = blank.copy()

            else:

                if board_State[move[0]][move[1]]["chess_piece"] != "":
                    game_Board.coords(board_State[move[0]][move[1]]["image"], -70, -70)
                    temp = board_State[move[0]][move[1]].copy()

                board_State[move[0]][move[1]] = board_State[pos[0]][pos[1]].copy()
                board_State[pos[0]][pos[1]] = blank.copy()

                pieces_Pos[player_Turn]["king"][0] = move
                coord_Check = find_Check()
                pieces_Pos[player_Turn]["king"][0] = pos

                board_State[pos[0]][pos[1]] = board_State[move[0]][move[1]].copy()
                board_State[move[0]][move[1]] = temp.copy()

                if board_State[move[0]][move[1]]["chess_piece"] != "":
                    game_Board.coords(board_State[move[0]][move[1]]["image"], move[1]*70+20, move[0]*70+20)
                
            if coord_Check != -1:
                available_Move.pop(i)

    elif diffY == 0:

        if diffX < 0:
            for i in range(x+1, pieces_Pos[player_Turn]["king"][0][1]):
                if board_State[y][i]["chess_piece"] != "":
                    blocking = True
                    break
            if not blocking:
                for i in range(x-1,-1,-1):
                    if board_State[y][i]["chess_piece"] != "":
                        if board_State[y][i]["color"] != player_Turn and (board_State[y][i]["chess_piece"] == "queen" or board_State[y][i]["chess_piece"] == "rook"):
                            for move in range(len(available_Move)-1, -1, -1):
                                if available_Move[move][0] != y:
                                    available_Move.pop(move)
                        break

        elif diffX > 0:
            for i in range(x-1, pieces_Pos[player_Turn]["king"][0][1], -1):
                if board_State[y][i]["chess_piece"] != "":
                    blocking = True
                    break
            if not blocking:
                for i in range(x+1,8):
                    if board_State[y][i]["chess_piece"] != "":
                        if board_State[y][i]["color"] != player_Turn and (board_State[y][i]["chess_piece"] == "queen" or board_State[y][i]["chess_piece"] == "rook"):
                            for move in range(len(available_Move)-1, -1, -1):
                                if available_Move[move][0] != y:
                                    available_Move.pop(move)
                        break

    elif diffX == 0:

        if diffY < 0:
            for i in range(y+1, pieces_Pos[player_Turn]["king"][0][0]):
                if board_State[i][x]["chess_piece"] != "":
                    blocking = True
                    break
            if not blocking:
                for i in range(y-1,-1,-1):
                    if board_State[i][x]["chess_piece"] != "":
                        if board_State[i][x]["color"] != player_Turn and (board_State[i][x]["chess_piece"] == "queen" or board_State[i][x]["chess_piece"] == "rook"):
                            for move in range(len(available_Move)-1, -1, -1):
                                if available_Move[move][1] != x:
                                    available_Move.pop(move)
                        break

        elif diffY > 0:
            for i in range(y-1, pieces_Pos[player_Turn]["king"][0][0], -1):
                if board_State[i][x]["chess_piece"] != "":
                    blocking = True
                    break
            if not blocking:
                for i in range(y+1,8):
                    if board_State[i][x]["chess_piece"] != "":
                        if board_State[i][x]["color"] != player_Turn and (board_State[i][x]["chess_piece"] == "queen" or board_State[i][x]["chess_piece"] == "rook"):
                            for move in range(len(available_Move)-1, -1, -1):
                                if available_Move[move][1] != x:
                                    available_Move.pop(move)
                        break

    elif abs(diffY) == abs(diffX):

        if diffX*diffY < 0:

            if diffY < 0:
                for i in range(1, diffX):
                    if board_State[y+i][x-i]["chess_piece"] != "":
                        blocking = True
                        break
                if not blocking:
                    for i in range(1, min(8-x, y+1)):
                        if board_State[y-i][x+i]["chess_piece"] != "":
                            if board_State[y-i][x+i]["color"] != player_Turn and (board_State[y-i][x+i]["chess_piece"] == "queen" or board_State[y-i][x+i]["chess_piece"] == "bishop"):
                                for move in range(len(available_Move)-1, -1, -1):
                                    if (available_Move[move][0]-y)*(available_Move[move][1]-x) >= 0:
                                        available_Move.pop(move)
                            break

            else:
                for i in range(1, -diffX):
                    if board_State[y-i][x+i]["chess_piece"] != "":
                        blocking = True
                        break
                if not blocking:
                    for i in range(1, min(x+1, 8-y)):
                        if board_State[y+i][x-i]["chess_piece"] != "":
                            if board_State[y+i][x-i]["color"] != player_Turn and (board_State[y+i][x-i]["chess_piece"] == "queen" or board_State[y+i][x-i]["chess_piece"] == "bishop"):
                                for move in range(len(available_Move)-1, -1, -1):
                                    if (available_Move[move][0]-y)*(available_Move[move][1]-x) >= 0:
                                        available_Move.pop(move)
                            break

        elif diffX*diffY > 0:

            if diffY < 0:
                for i in range(1, -diffX):
                    if board_State[y+i][x+i]["chess_piece"] != "":
                        blocking = True
                        break
                if not blocking:
                    for i in range(1, min(x+1, y+1)):
                        if board_State[y-i][x-i]["chess_piece"] != "":
                            if board_State[y-i][x-i]["color"] != player_Turn and (board_State[y-i][x-i]["chess_piece"] == "queen" or board_State[y-i][x-i]["chess_piece"] == "bishop"):
                                for move in range(len(available_Move)-1, -1, -1):
                                    if (available_Move[move][0]-y)*(available_Move[move][1]-x) <= 0:
                                        available_Move.pop(move)
                            break

            else:
                for i in range(1, diffX):
                    if board_State[y-i][x-i]["chess_piece"] != "":
                        blocking = True
                        break
                if not blocking:
                    for i in range(1, min(8-x, 8-y)):
                        if board_State[y+i][x+i]["chess_piece"] != "":
                            if board_State[y+i][x+i]["color"] != player_Turn and (board_State[y+i][x+i]["chess_piece"] == "queen" or board_State[y+i][x+i]["chess_piece"] == "bishop"):
                                for move in range(len(available_Move)-1, -1, -1):
                                    if (available_Move[move][0]-y)*(available_Move[move][1]-x) <= 0:
                                        available_Move.pop(move)
                            break

def find_Moves(y, x):

    move_Set(y, x)
    block_Check(y, x)
    commit_Suicide(y, x)






def check_Or_checkmate():

    global available_Move, pieces_Pos, player_Turn, check_Dist

    ascending = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    moves = []

    for i in range(6):
        coord_arr = pieces_Pos[player_Turn][ascending[i]]
        for j in range(len(coord_arr)):
            find_Moves(coord_arr[j][0], coord_arr[j][1])
            moves.append(available_Move)
            del_Move()

    for move in moves:
        if len(move) > 0:
            return False

    return True

def disable(y, x):
    
    global board_State, player_Turn, moved_State

    if moved_State[(player_Turn==WHITE) and BLACK or WHITE]["0-0"]:
        if y==((player_Turn==WHITE) and 0 or 7) and x==7:
            moved_State[(player_Turn==WHITE) and BLACK or WHITE]["0-0"] = False

    if moved_State[(player_Turn==WHITE) and BLACK or WHITE]["0-0-0"]:
        if y==((player_Turn==WHITE) and 0 or 7) and x==0:
            moved_State[(player_Turn==WHITE) and BLACK or WHITE]["0-0-0"] = False




def display_Move():

    global available_Move, available_Show

    for i in range(len(available_Move)):
        avail_X = available_Move[i][1]
        avail_Y = available_Move[i][0]
        available_Show.append(game_Board.create_oval(45+avail_X*70, 45+avail_Y*70, 65+avail_X*70, 65+avail_Y*70, fill="#A9A9A9", outline=""))

def del_Move():

    global available_Move, available_Show

    for i in range(len(available_Show)-1, -1, -1):
        game_Board.delete(available_Show[i])
    available_Move = []
    available_Show = []




checkMate = False
pickup = False
col, row = (0, 0)

def coord_pickup(e):

    global pieces_Img, player_Turn, board_State, pickup, col, row, checkMate

    row, col = (int((e.y-20)/70), int((e.x-20)/70))
    if not checkMate:
        if row>=0 and row<8 and col>=0 and col<8:
            if board_State[row][col]["chess_piece"]!="" and board_State[row][col]["color"]==player_Turn:
                find_Moves(row, col)
                display_Move()
                game_Board.delete(board_State[row][col]["image"])
                img = pieces_Img[board_State[row][col]["color"]][board_State[row][col]["chess_piece"]]
                board_State[row][col]["image"] = game_Board.create_image(e.x, e.y, image=img)
                pickup = True

def move(e):
    
    global board_State, pickup, col, row

    if pickup:
        game_Board.coords(board_State[row][col]["image"], e.x, e.y)

def coord_drop(e):

    global player_Turn, board_State, available_Move, pieces_Pos, pickup, col, row, check_Dist, checkMate, moved_State, blank, pieces_Img, game_Board

    if pickup:
        new_imgx = int((e.x-20)/70)
        new_imgy = int((e.y-20)/70)
        if new_imgx>=0 and new_imgx<8 and new_imgy>=0 and new_imgy<8 and (new_imgx!=col or new_imgy!=row) and (new_imgy, new_imgx) in available_Move:

            if board_State[new_imgy][new_imgx]["chess_piece"] != "":
                disable(new_imgy, new_imgx)
                game_Board.delete(board_State[new_imgy][new_imgx]["image"])
                pieces_Pos[board_State[new_imgy][new_imgx]["color"]][board_State[new_imgy][new_imgx]["chess_piece"]].remove((new_imgy, new_imgx))

            if moved_State[player_Turn]["0-0"]:
                if board_State[row][col]["chess_piece"] == "rook" and col==7:
                    moved_State[player_Turn]["0-0"] = False

                elif board_State[row][col]["chess_piece"] == "king":
                    moved_State[player_Turn]["0-0"] = False
                    if new_imgx-col==2:
                        moved_State[player_Turn]["0-0"] = False
                        BoW = (player_Turn==WHITE) and 7 or 0
                        board_State[BoW][5] = board_State[BoW][7].copy()
                        board_State[BoW][7] = blank.copy()
                        pieces_Pos[player_Turn]["rook"].remove((BoW, 7))
                        pieces_Pos[player_Turn]["rook"].append((BoW, 5))
                        game_Board.coords(board_State[BoW][5]["image"], 5*70+20, BoW*70+20)

            if moved_State[player_Turn]["0-0-0"]:

                if board_State[row][col]["chess_piece"] == "rook" and col==0:
                    moved_State[player_Turn]["0-0-0"] = False

                elif board_State[row][col]["chess_piece"] == "king":
                    moved_State[player_Turn]["0-0-0"] = False
                    if col-new_imgx==2:
                        BoW = (player_Turn==WHITE) and 7 or 0
                        board_State[BoW][3] = board_State[BoW][0].copy()
                        board_State[BoW][0] = blank.copy()
                        pieces_Pos[player_Turn]["rook"].remove((BoW, 0))
                        pieces_Pos[player_Turn]["rook"].append((BoW, 3))
                        game_Board.coords(board_State[BoW][3]["image"], 3*70+20, BoW*70+20)

            board_State[new_imgy][new_imgx] = board_State[row][col].copy()
            board_State[row][col] = blank.copy()
            pieces_Pos[player_Turn][board_State[new_imgy][new_imgx]["chess_piece"]].remove((row, col))

            if board_State[new_imgy][new_imgx]["chess_piece"] == "pawn":
                if (player_Turn==WHITE and new_imgy==0) or (player_Turn==BLACK and new_imgy==7):

                    ask = Toplevel()
                    ask.title("Promote to")
                    ask.focus_set()
                    ask.grab_set()

                    def delete():
                        ask.destroy()

                    def change(piece):
                        board_State[new_imgy][new_imgx]["chess_piece"] = piece
                        game_Board.delete(board_State[new_imgy][new_imgx]["image"])
                        img = pieces_Img[board_State[new_imgy][new_imgx]["color"]][board_State[new_imgy][new_imgx]["chess_piece"]]
                        board_State[new_imgy][new_imgx]["image"] = game_Board.create_image(new_imgx*70+20, new_imgy*70+20, anchor=NW, image=img)
                        root.focus_set()
                        ask.protocol("WM_DELETE_WINDOW", delete)

                    ask.protocol("WM_DELETE_WINDOW", lambda:0)
                    rook = Button(ask, text="ROOK", command=lambda : change("rook"))
                    knight = Button(ask, text="KNIGHT", command=lambda : change("knight"))
                    bishop = Button(ask, text="BISHOP", command=lambda : change("bishop"))
                    queen = Button(ask, text="QUEEN", command=lambda : change("queen"))
                    rook.pack()
                    knight.pack()
                    bishop.pack()
                    queen.pack()
                    root.wait_window(ask)

            pieces_Pos[player_Turn][board_State[new_imgy][new_imgx]["chess_piece"]].append((new_imgy, new_imgx))

            next_Move()
            check_Dist = find_Check()
            if check_Dist != -1:
                del_Move()
                checkMate = check_Or_checkmate()
                if checkMate:
                    # move_List.insert(END, "checkmate")
                    game_Board.coords(board_State[new_imgy][new_imgx]["image"], new_imgx*70+20, new_imgy*70+20)
                    game_Board.itemconfig(board_State[new_imgy][new_imgx]["image"], anchor=NW)
                    pickup = False
                    return
                # move_List.insert(END, "check")
        else:
            new_imgx = col
            new_imgy = row
        del_Move()
        game_Board.coords(board_State[new_imgy][new_imgx]["image"], new_imgx*70+20, new_imgy*70+20)
        game_Board.itemconfig(board_State[new_imgy][new_imgx]["image"], anchor=NW)
        pickup = False




game_Board.bind("<Button-1>", coord_pickup)
game_Board.bind("<B1-Motion>", move)
game_Board.bind("<ButtonRelease-1>", coord_drop)




root.mainloop()