import pygame as pg
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
        if self.flag:
            pg.draw.circle(self.image, WHITE, (MASU_SIZE / 2, MASU_SIZE / 2), STONE_RADIUS)
        else:
            pg.draw.circle(self.image, BLACK, (MASU_SIZE / 2, MASU_SIZE / 2), STONE_RADIUS)

class Stage():
    def __init__(self):
        self.stage = [[0 for _i in range(8)] for _j in range(8)]
        self.stage[3][3] = Stone((3, 3), True)
        self.stage[3][4] = Stone((3, 4), False)
        self.stage[4][3] = Stone((4, 3), False)
        self.stage[4][4] = Stone((4, 4), True)

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