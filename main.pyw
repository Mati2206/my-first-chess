import pygame
from CONST import *
from Figures import Figures
import os, sys

class Game:
    def load_image(self):
        self.images = {}
        for img in os.listdir("images") :
            self.images[img.replace(".png", "")] = pygame.transform.scale(pygame.image.load("images/" + img), (SQUARE_SIZE, SQUARE_SIZE))
            

    def screen(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)


    def __init__(self):
        self.screen()
        self.load_image()

        self.board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


        self.turn = "w"

        self.click1 = None
        self.click2 = None
        self.white = [(192, 192, 192), (192, 255, 255)]
        self.black = [(128, 0, 128), (128, 255, 255)]
        self.castling_white = [True, True]
        self.castling_black = [True, True]

        self.second_b = False
        self.first = None
        self.circle = False

        self.main()

    def main(self):
        while True:
            self.load_figures()
            self.draw_image()
            self.check_events()

    def load_figures(self):
        self.figures = []
        for i in range(8):
            self.figures.append([])
            for j in range(8):
                self.figures[i].append(Figures((j*SQUARE_SIZE, i*SQUARE_SIZE), self.board[i][j], (i, j), (self.castling_white, self.castling_black)))

    def mouse(self):
        mouse = pygame.mouse.get_pos()
        if self.second_b:
            moves, castling = self.moves()
            for i in range(8):
                for j in range(8):
                    if self.figures[i][j].collidepoint(mouse[0], mouse[1]) and (i, j) in moves:
                        self.move(self.first.np[0], self.first.np[1], i, j)
                        if castling[0][0] == True and (i, j) == (7, 2):
                            self.move(7, 0, 7, 3)
                        if castling[1][0] == True and (i, j) == (7, 6):
                            self.move(7, 7, 7, 5)
                        if castling[0][1] == True and (i, j) == (0, 2):
                            self.move(0, 0, 0, 3)
                        if castling[1][1] == True and (i, j) == (0, 6):
                            self.move(0, 7, 0, 5)
                        self.click2 = (i, j)
                        self.second_b = False
                        if self.first.name == "K" and self.first.color == "w":
                            self.castling_white = [False, False]
                        elif self.first.name == "K" and self.first.color == "b":
                            self.castling_black = [False, False]
                        if self.first.name == "R" and self.first.color == "w" and self.first.np == (7, 0):
                            self.castling_white[0] = False
                        if self.first.name == "R" and self.first.color == "w" and self.first.np == (7, 7):
                            self.castling_white[1] = False
                        if self.first.name == "R" and self.first.color == "b" and self.first.np == (0, 0):
                            self.castling_black[0] = False
                        if self.first.name == "R" and self.first.color == "b" and self.first.np == (0, 7):
                            self.castling_black[1] = False

                        if self.turn == "w":
                            self.turn = "b"
                        else:
                            self.turn = "w"
                    else:
                        self.second_b = False
                        self.click1 = None
        else:
            for i in range(8):
                for j in range(8):
                    if self.figures[i][j].name != "-" and self.figures[i][j].collidepoint(mouse[0], mouse[1]):
                        self.click2 = None
                        self.click1 = (i, j)
                        self.second_b = True
                        self.first = self.figures[i][j]
            if not self.second_b:
                self.click1 = None
                self.click2 = None

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse()


    def move(self, x1, y1, x2, y2):
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = "--"

    def draw_chessboard(self):
        self.circle = False
        for i in range(8):
            for j in range(8):
                rect = pygame.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                if i%2 - j%2:
                    if (j, i) == self.click2:
                        color = self.black[1]
                    elif (j, i) == self.click1:
                        color = self.black[1]
                        self.circle = True
                    else:
                        color = self.black[0]
                else:
                    if (j, i) == self.click1:
                        color = self.white[1]
                        self.circle = True
                    elif (j, i) == self.click2:
                        color = self.white[1]
                    else:
                        color = self.white[0]
                pygame.draw.rect(self.screen, color, rect)
                
    def moves(self):
        for i in range(8):
            for j in range(8):
                if (i, j) == self.click1 and self.figures[i][j].name == "p" and self.figures[i][j].color == self.turn:
                    return self.figures[i][j].pawn(self.figures), ((False, False), (False, False))
                elif (i, j) == self.click1 and self.figures[i][j].name == "N" and self.figures[i][j].color == self.turn:
                    return self.figures[i][j].knight(self.figures), ((False, False), (False, False))
                elif (i, j) == self.click1 and self.figures[i][j].name == "B" and self.figures[i][j].color == self.turn:
                    return self.figures[i][j].bishop(self.figures), ((False, False), (False, False))
                elif (i, j) == self.click1 and self.figures[i][j].name == "R" and self.figures[i][j].color == self.turn:
                    return self.figures[i][j].rock(self.figures), ((False, False), (False, False))
                elif (i, j) == self.click1 and self.figures[i][j].name == "Q" and self.figures[i][j].color == self.turn:
                    return self.figures[i][j].queen(self.figures), ((False, False), (False, False))
                elif (i, j) == self.click1 and self.figures[i][j].name == "K" and self.figures[i][j].color == self.turn:
                    return self.figures[i][j].king(self.figures)
        return [], ((False, False), (False, False))

    def draw_image(self):
        self.draw_chessboard()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != "--":
                    self.screen.blit(self.images[self.board[i][j]], (j*SQUARE_SIZE, i*SQUARE_SIZE))
        if self.circle:
            for i in self.moves()[0]:
                pygame.draw.circle(self.screen, (128, 255, 128), (i[1]*SQUARE_SIZE+SQUARE_SIZE/2, i[0]*SQUARE_SIZE+SQUARE_SIZE/2), 10)            

        pygame.display.flip()
    
    
Game()
