import pygame
import sys

from settings import *


class Tictaktoe:
    def __init__(self, surface):
        self.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.surface = surface
        self.width = 5
        self.length = 0
        self.pos = 0
        self.color = TICTAKTOE_COLOR
        self.percentageOccupy = 0.8
        self.grid = {(i, j): [] for i in range(3) for j in range(3)}
        self.anchorPoints = {(i, j): [] for i in range(4) for j in range(4)}
        self.x_param = [PLAYER_COLOR, 0.8, 10]
        self.x_add = lambda p1, p2, op: (p1[0] + p2, p1[1] + p2) if op else (p1[0] - p2, p1[1] + p2)
        self.o_param = [AI_COLOR, 0.8, 10]  # color, percentage, width
        self.lineDist = 0
        self.linePos = []
        self.calculateParameters()

        self.turn = "X"
        self.next = "O"
        self.moves = 0
        self.winner = None
        self.gameList = {(i, j): '' for i in range(3) for j in range(3)}
        self.drawList = {}
        self.winner = ""

    def calculateParameters(self):
        dominant = SCREEN_WIDTH
        if SCREEN_WIDTH > SCREEN_HEIGHT:
            dominant = SCREEN_HEIGHT
        self.length = dominant * self.percentageOccupy
        self.pos = (self.center[0]-self.length/2, self.center[1]-self.length/2)

        self.lineDist = self.length/3
        self.linePos = [[(self.pos[0]+self.lineDist*i, self.pos[1]),
                         (self.pos[0]+self.lineDist*i, self.pos[1]+self.length)] for i in range(1, 3)]
        self.linePos = self.linePos + [[(self.pos[0], self.pos[1]+self.lineDist*i),
                                        (self.pos[0]+self.length, self.pos[1]+self.lineDist*i)] for i in range(1, 3)]

        for key in self.anchorPoints:
            if key[0] == 3:
                self.anchorPoints[key] = [self.pos[0]+key[1]*self.lineDist, self.pos[1]+self.length]
            elif key[1] == 3:
                self.anchorPoints[key] = [self.pos[0]+self.length, self.pos[1]+key[0]*self.lineDist]
            else:
                self.anchorPoints[key] = [self.pos[0]+key[1]*self.lineDist, self.pos[1]+key[0]*self.lineDist]

        moderateValues = lambda a, b, c: a + b if c else a - b
        for key in self.grid:
            temp = []
            keys = [key, (key[0], key[1]+1), (key[0]+1, key[1]+1), (key[0]+1, key[1])]
            operations = [(1, 1), (0, 1), (0, 0), (1, 0)]

            for i in range(len(keys)):
                if keys[i][0] in (0, 3) and keys[i][1] in (0, 3):
                    temp.append((moderateValues(self.anchorPoints[keys[i]][0], self.width, operations[i][0]),
                                 moderateValues(self.anchorPoints[keys[i]][1], self.width, operations[i][1])))
                    continue
                if keys[i][0] in (0, 3):
                    temp.append((moderateValues(self.anchorPoints[keys[i]][0], self.width/2, operations[i][0]),
                                 moderateValues(self.anchorPoints[keys[i]][1], self.width, operations[i][1])))
                    continue
                if keys[i][1] in (0, 3):
                    temp.append((moderateValues(self.anchorPoints[keys[i]][0], self.width, operations[i][0]),
                                 moderateValues(self.anchorPoints[keys[i]][1], self.width/2, operations[i][1])))
                    continue
                temp.append((moderateValues(self.anchorPoints[keys[i]][0], self.width/2, operations[i][0]),
                             moderateValues(self.anchorPoints[keys[i]][1], self.width/2, operations[i][1])))
            self.grid[key] = temp

        self.x_param.append((self.grid[(0, 0)][1][0] - self.grid[(0, 0)][0][0])*self.x_param[1])  # length
        self.x_param.append((self.grid[(0, 0)][1][0] - self.grid[(0, 0)][0][0])*((1-self.x_param[1])/2))  # start

        self.o_param.append(((self.grid[(0, 0)][1][0] - self.grid[(0, 0)][0][0])*self.x_param[1])/2)  # radius
        self.o_param.append((self.grid[(0, 0)][1][0] - self.grid[(0, 0)][0][0])/2)  # start

    def drawX(self, coord):
        pygame.draw.line(self.surface, self.x_param[0], self.x_add(self.grid[coord][0], self.x_param[4], 1),
                         self.x_add(self.grid[coord][0], self.x_param[3] + self.x_param[4], 1), self.x_param[2])

        pygame.draw.line(self.surface, self.x_param[0], self.x_add(self.grid[coord][1], self.x_param[4], 0),
                         self.x_add(self.grid[coord][1], self.x_param[3] + self.x_param[4], 0), self.x_param[2])

    def drawO(self, coord):
        pygame.draw.circle(self.surface, self.o_param[0], self.x_add(self.grid[coord][0], self.o_param[4], 1),
                           self.o_param[3], self.o_param[2])

    def draw(self):
        for i in range(4):
            pygame.draw.line(self.surface, self.color, self.linePos[i][0], self.linePos[i][1], self.width)\

        pygame.draw.rect(self.surface, self.color, (self.pos[0], self.pos[1], self.length, self.length), self.width)

        for i in self.drawList:
            if self.drawList[i] == 'X':
                self.drawX(i)
            else:
                self.drawO(i)

        """
        for i in range(3):
            for j in range(4):
                pygame.draw.line(self.surface, (255, 0, 0), (self.anchorPoints[(j, i)]), (self.anchorPoints[(j, i+1)]))
        for i in range(3):
            for j in range(4):
                pygame.draw.line(self.surface, (255, 0, 0), (self.anchorPoints[(i, j)]), (self.anchorPoints[(i+1, j)]))
        
        for i in self.grid:
            pygame.draw.line(self.surface, (255, 0, 0), (self.grid[i][0]),
                             (self.grid[i][1]))
            pygame.draw.line(self.surface, (255, 0, 0), (self.grid[i][1]),
                             (self.grid[i][2]))
            pygame.draw.line(self.surface, (255, 0, 0), (self.grid[i][2]),
                             (self.grid[i][3]))
            pygame.draw.line(self.surface, (255, 0, 0), (self.grid[i][3]),
                             (self.grid[i][0]))"""

    def checkMouse(self, coord):
        for i in self.grid:
            if self.grid[i][0][0] <= coord[0] <= self.grid[i][2][0] and \
                    self.grid[i][0][1] <= coord[1] <= self.grid[i][2][1]:
                if not self.gameList[i]:
                    # Checking if the position already has an X or an O
                    return i

        else:
            return None

    def nextMove(self, pos):
        self.drawList[pos] = self.turn
        self.gameList[pos] = self.turn
        self.turn, self.next = self.next, self.turn
        self.moves += 1

    def checkWinner(self):
        for i in range(3):
            if self.gameList[(i, 0)] == self.gameList[(i, 1)] == self.gameList[(i, 2)] != '':
                return self.next
            if self.gameList[(0, i)] == self.gameList[(1, i)] == self.gameList[(2, i)] != '':
                return self.next
        if self.gameList[(0, 0)] == self.gameList[(1, 1)] == self.gameList[(2, 2)] != '':
            return self.next
        if self.gameList[(1, 1)] == self.gameList[(0, 2)] == self.gameList[(2, 0)] != '':
            return self.next
        if self.moves == 9:
            return "tie"
        return None

    def game(self, coord):
        if self.winner:
            return
        pos = self.checkMouse(coord)
        if not pos:
            return
        self.nextMove(pos)
        self.winner = self.checkWinner()
        if self.winner:
            print(self.winner)


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.tictaktoe = Tictaktoe(self.screen)

    def displayUpdate(self):
        self.screen.fill(SCREEN_COLOR)
        self.tictaktoe.draw()
        pygame.display.update()

    def temp(self):
        print(pygame.mouse.get_pos())

    def eventLoop(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        self.tictaktoe.game(pygame.mouse.get_pos())
            self.displayUpdate()


if __name__ == "__main__":
    main = Main()
    main.eventLoop()
