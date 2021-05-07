import pygame
from CONST import *

class Figures(pygame.Rect):
    def __init__(self, xy, name, np, castiling):
        self.w = SQUARE_SIZE
        self.h = SQUARE_SIZE

        self.x = xy[0]
        self.y = xy[1]
        self.np = np

        self.color = name[0]
        self.name = name[1]
        self.castling_white = castiling[0]
        self.castling_black = castiling[1]

    def pawn(self, figures):
        minus = 1
        moves = []
        if self.color == "w":
            minus = -1
        for i in range(8):
            for j in range(8):
                f = figures[i][j]
                if (i-1*minus, j) == self.np and f.name == "-":
                    moves.append((i, j))
            
                elif (i-2*minus, j) == self.np and f.name == "-" and figures[i-1*minus][j].name == "-" and ((i-2*minus == 6 and self.color == "w") or (i-2*minus == 1 and self.color == "b")):
                    moves.append((i, j))
                
                elif ((i-1*minus, j+1) == self.np or (i-1*minus, j-1) == self.np) and f.color != self.color and f.name != "-":
                    moves.append((i, j))
        return moves
    
    def rock(self, figures):
        minus = 1
        moves = []
        if self.color == "w":
            minus = -1
        N = True
        E = True
        S = True
        W = True
        for k in range(1,8):
            for i in range(8):
                for j in range(8):
                    f = figures[i][j]
                    if f.name != "-" and (i-k*minus, j) == self.np:
                        if f.color != self.color and f.color != "-" and N:
                            moves.append((i, j))
                        N = False     
                    elif f.name != "-" and (i, j-k*minus) == self.np:
                        if f.color != self.color and f.color != "-" and E:
                            moves.append((i, j))
                        E = False
                    elif f.name != "-" and (i+k*minus, j) == self.np:
                        if f.color != self.color and f.color != "-" and S:
                            moves.append((i, j))
                        S = False
                    elif f.name != "-" and (i, j+k*minus) == self.np:
                        if f.color != self.color and f.color != "-" and W:
                            moves.append((i, j))
                        W = False
                    elif (i-k*minus, j) == self.np and N:
                        moves.append((i, j))
                    elif (i, j-k*minus) == self.np and E:
                        moves.append((i, j))
                    elif (i+k*minus, j) == self.np and S:
                        moves.append((i, j))
                    elif (i, j+k*minus) == self.np and W:
                        moves.append((i, j))
        return moves

    def knight(self, figures):
        minus = 1
        moves = []
        if self.color == "w":
            minus = -1
        for i in range(8):
            for j in range(8):
                f = figures[i][j]
                l1 = 1*minus
                l2 = 2*minus
                left = (i-l1, j-l2) == self.np or (i+l1, j+l2) == self.np
                right = (i+l1, j-l2) == self.np or (i-l1, j+l2) == self.np
                top = (i-l2, j-l1) == self.np or (i-l2, j+l1) == self.np
                bottom = (i+l2, j-l1) == self.np or (i+l2, j+l1) == self.np

                if (top or right or bottom or left) and f.color != self.color:
                    moves.append((i, j))
        return moves
    
    def bishop(self, figures):
        minus = 1
        moves = []
        if self.color == "w":
            minus = -1
        NW = True
        NE = True
        SW = True
        SE = True
        for k in range(1,8):
            for i in range(8):
                for j in range(8):
                    f = figures[i][j]
                    if f.name != "-" and (i-k*minus, j-k*minus) == self.np:
                        if f.color != self.color and f.color != "-" and NW:
                            moves.append((i, j))
                        NW = False
                    elif f.name != "-" and (i-k*minus, j+k*minus) == self.np:
                        if f.color != self.color and f.color != "-" and NE:
                            moves.append((i, j))
                        NE = False
                    elif f.name != "-" and (i+k*minus, j-k*minus) == self.np:
                        if f.color != self.color and f.color != "-" and SW:
                            moves.append((i, j))
                        SW = False
                    elif f.name != "-" and (i+k*minus, j+k*minus) == self.np:
                        if f.color != self.color and f.color != "-" and SE:
                            moves.append((i, j))
                        SE = False
                    elif (i-k*minus, j-k*minus) == self.np and NW:
                        moves.append((i, j))
                    elif (i-k*minus, j+k*minus) == self.np and NE:
                        moves.append((i, j))
                    elif (i+k*minus, j-k*minus) == self.np and SW:
                        moves.append((i, j))
                    elif (i+k*minus, j+k*minus) == self.np and SE:
                        moves.append((i, j))
        return moves
    
    def queen(self, figures):
        moves = []
        moves.extend(self.rock(figures))
        moves.extend(self.bishop(figures))
        return moves
        
    def king(self, figures):
        castling_long_white = False
        castling_long_black = False
        castling_short_white = False
        castling_short_black = False
        minus = 1
        moves = []
        if self.color == "w":
            minus = -1
        for i in range(8):
            for j in range(8):
                f = figures[i][j]
                if (i-1, j) == self.np and f.color != self.color:
                    moves.append((i, j))
                elif (i+1, j) == self.np and f.color != self.color:
                    moves.append((i, j))
                elif (i, j-1) == self.np and f.color != self.color:
                    moves.append((i, j))
                elif (i, j+1) == self.np and f.color != self.color:
                    moves.append((i, j))
                elif (i-1, j-1) == self.np and f.color != self.color:
                    moves.append((i, j))
                elif (i-1, j+1) == self.np and f.color != self.color:
                    moves.append((i, j))
                elif (i+1, j-1) == self.np and f.color != self.color:
                    moves.append((i, j))
                elif (i+1, j+1) == self.np and f.color != self.color:
                    moves.append((i, j))

        if self.castling_white[0]:
            f = figures[7]
            if f[1].name == "-" and f[2].name == "-" and f[3].name == "-":
                moves.append((7, 2))
                castling_long_white = True
        if self.castling_white[1]:
            f = figures[7]
            if f[5].name == "-" and f[6].name == "-":
                moves.append((7, 6))
                castling_short_white = True
        if self.castling_black[0]:
            f = figures[0]
            if f[1].name == "-" and f[2].name == "-" and f[3].name == "-":
                moves.append((0, 2))
                castling_long_black = True
        if self.castling_black[1]:
            f = figures[0]
            if f[5].name == "-" and f[6].name == "-":
                moves.append((0, 6))
                castling_short_black = True
        return moves, ((castling_long_white, castling_long_black), (castling_short_white, castling_short_black))