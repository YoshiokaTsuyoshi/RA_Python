import pygame as pg
import random
import sys

SCREEN_SIZE = (600, 600)
MASU_SIZE = 50
STONE_RADIUS = 20
FRAME_RATE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Stone(pg.sprite.Sprite):
    def __init__(self, pos, flag):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.Surface((MASU_SIZE, MASU_SIZE))
        self.image.fill((1, 1, 1))
        self.image.set_colorkey((1, 1, 1))
        if flag:
            pg.draw.circle(self.image, WHITE, (MASU_SIZE / 2, MASU_SIZE / 2), STONE_RADIUS)
        else:
            pg.draw.circle(self.image, BLACK, (MASU_SIZE / 2, MASU_SIZE / 2), STONE_RADIUS)
        self.rect = pg.Rect(((SCREEN_SIZE[0]-MASU_SIZE*8)/2+pos[0]*MASU_SIZE, (SCREEN_SIZE[1]-MASU_SIZE*8)/2+pos[1]*MASU_SIZE), (MASU_SIZE, MASU_SIZE))
        self.flag = flag

    def update(self, *args, **kwargs):
        pass

    def turn(self):
        self.flag = not self.flag
        self.image = pg.Surface((MASU_SIZE, MASU_SIZE))
        self.image.fill((1, 1, 1))
        self.image.set_colorkey((1, 1, 1))
        if self.flag:
            pg.draw.circle(self.image, WHITE, (MASU_SIZE / 2, MASU_SIZE / 2), STONE_RADIUS)
        else:
            pg.draw.circle(self.image, BLACK, (MASU_SIZE / 2, MASU_SIZE / 2), STONE_RADIUS)

class Stage(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.Surface((0, 0))
        self.rect = pg.Rect(0, 0, 0, 0)
        self.stage = [[0 for _i in range(8)] for _j in range(8)]
        self.direct = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
        self.turnFlag = False
        self.stage[3][3] = Stone((3, 3), True)
        self.stage[3][4] = Stone((3, 4), False)
        self.stage[4][3] = Stone((4, 3), False)
        self.stage[4][4] = Stone((4, 4), True)

    def update(self, *args, **kwargs):
        mousePos = pg.mouse.get_pos()
        if pg.mouse.get_pressed(3)[0]:
            pos = [int((mousePos[0]-(SCREEN_SIZE[0]-MASU_SIZE*8)/2) / MASU_SIZE), int((mousePos[1]-(SCREEN_SIZE[1]-MASU_SIZE*8)/2) / MASU_SIZE)]
            if (pos[0] >= 0 and pos[0] <= 7) and (pos[1] >= 0 and pos[1] <= 7):
                if self.stage[pos[0]][pos[1]] == 0 and sum(self.judgeStone(pos, self.turnFlag)) > 0:
                    self.setStone(pos, self.turnFlag)
                    self.turnFlag = not self.turnFlag

    def setStone(self, pos, flag):
        self.stage[pos[0]][pos[1]] = Stone(pos, flag)
        self.turnStone(pos, flag)

    def turnStone(self, pos, flag):
        for i, j in zip(self.judgeStone(pos, flag), self.direct):
            if i:
                for h in range(1, 8):
                    tempX = pos[0] + j[0] * h
                    tempY = pos[1] + j[1] * h
                    if self.stage[tempX][tempY].flag != flag:
                        self.stage[tempX][tempY].turn()
                    else:
                        break

    def judgeStone(self, pos, flag):
        directList = [False for _i in range(8)]
        for index, i in enumerate(self.direct):
            for j in range(1, 8):
                tempX = pos[0] + i[0] * j
                tempY = pos[1] + i[1] * j
                if tempX < 0 or tempX > 7 or tempY < 0 or tempY > 7:
                    break
                if self.stage[tempX][tempY] == 0:
                    break
                if self.stage[tempX][tempY].flag == flag:
                    if j != 1:
                        directList[index] = True
                    else:
                        break
        return directList

def main():

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    background = pg.Surface(SCREEN_SIZE)
    background.fill((0, 255, 255))
    for i in range(8):
        for j in range(8):
            pg.draw.rect(background, (0, 255, 0), pg.Rect((SCREEN_SIZE[0]-MASU_SIZE*8)/2+i*MASU_SIZE, (SCREEN_SIZE[1]-MASU_SIZE*8)/2+j*MASU_SIZE, MASU_SIZE, MASU_SIZE))
            pg.draw.rect(background, (0, 0, 0), pg.Rect((SCREEN_SIZE[0]-MASU_SIZE*8)/2+i*MASU_SIZE, (SCREEN_SIZE[1]-MASU_SIZE*8)/2+j*MASU_SIZE, MASU_SIZE, MASU_SIZE), 1)
    screen.blit(background, (0, 0))
    pg.display.flip()

    all = pg.sprite.RenderUpdates()

    Stone.containers = all
    Stage.containers = all
    
    stage = Stage()
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                
        all.clear(screen, background)
        all.update()
        dirty = all.draw(screen)
        pg.display.update(dirty)

        pg.time.wait(int(1000 / FRAME_RATE))

if __name__ == "__main__":
    main()
    pg.quit()