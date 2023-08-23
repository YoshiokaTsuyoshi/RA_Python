import pygame as pg
import sys
import math

SCREEN_SIZE = (600, 400)
BLOCK_SIZE = 50
CLOCK_TICK = 30
PAGE = 0

class Stage():
    def __init__(self):
        self.player = Player((50, 100))
        Enemy((300, 300))
        stage = []
        for i in range(1, 12, 2):
            stage.append(Block((i * BLOCK_SIZE, BLOCK_SIZE * 7)))
        stage.append(Block((BLOCK_SIZE * 3, BLOCK_SIZE * 5)))
        stage.append(Block((BLOCK_SIZE * 5, BLOCK_SIZE * 4)))
        stage.append(Block((BLOCK_SIZE * 6, BLOCK_SIZE * 4)))
        stage.append(Block((BLOCK_SIZE * 7, BLOCK_SIZE * 3)))
        for i in range(1, 7):
            Goal((550, i * BLOCK_SIZE))

class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.blockSize = int(BLOCK_SIZE * 0.9)
        self.image = pg.Surface((self.blockSize, self.blockSize))
        pg.draw.circle(self.image, (255, 0, 0), (self.blockSize / 2, self.blockSize / 2), self.blockSize / 2, 0)
        self.rect = pg.Rect(pos[0], pos[1], self.blockSize, self.blockSize)
        self.image.set_colorkey((0, 0, 0))
        self.speed = [0.0, 0.0]
        self.force = [0.0, 3]
        self.period = 1.0
        self.maxSpeedX = 10
        self.maxForceX = 3
        self.beforePos = [self.rect.x, self.rect.y]
        self.touchFlag = [False, False, 0, [0, 0]]
        self.gameFlag = "None"

    def update(self, *args, **kwargs):
        self.beforePos = [self.rect.x, self.rect.y]
        self.rect.x += self.speed[0] * self.period + self.force[0] * self.period**2
        self.speed[0] = self.speed[0] + self.force[0] * self.period
        self.rect.y += self.speed[1] * self.period + self.force[1] * self.period**2
        self.speed[1] = self.speed[1] + self.force[1] * self.period

        self.colJudge(kwargs["surviver"], kwargs["block"], False)

        if self.speed[0] != 0:
            temp = (self.speed[0] / abs(self.speed[0]))
            self.speed[0] -= temp * 0.5
            if temp * self.speed[0] < 0:
                self.speed[0] = 0
        if self.force[0] != 0:
            temp = (self.force[0] / abs(self.force[0]))
            self.force[0] -= temp * self.force[1] * 0.2
            if temp * self.force[0] < 0:
                self.force[0] = 0

        self.gameOverJudge()

    def move(self, keystate):
        direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        self.force[0] += direction
        if self.touchFlag[1] != 0:
            self.force[0] = 0.0
            if (self.rect.y < self.touchFlag[3][0] or self.rect.y > self.touchFlag[3][1]) or self.rect.x != self.touchFlag[2] or self.touchFlag[1] + direction == 0:
                self.touchFlag[1] = 0
        if abs(self.force[0]) > self.maxForceX:
            self.force[0] = self.maxForceX * (self.force[0] / abs(self.force[0]))
        if abs(self.speed[0]) > self.maxSpeedX:
            self.speed[0] = self.maxSpeedX * (self.speed[0] / abs(self.speed[0]))
        if self.speed[1] == 0 and (keystate[pg.K_UP] or keystate[pg.K_SPACE]) and self.touchFlag[0]:
            self.speed[1] = -30
            self.touchFlag[0] = False

    def colJudge(self, player, blocks, dokill):
        while True:
            tempList = pg.sprite.spritecollide(player, blocks, dokill)
            if len(tempList) == 0:
                break
            for i in tempList:
                #tempVect = [self.rect.x - self.beforePos[0], self.rect.y - self.beforePos[1]]
                if i.rect.y + BLOCK_SIZE > self.rect.y and i.rect.y + BLOCK_SIZE < self.rect.y + self.blockSize:
                    #上ブロックと衝突
                    self.speed[1] = 0.0
                    self.rect.y = i.rect.y + BLOCK_SIZE
                    if self.rect.y > self.beforePos[1]:
                        self.rect.y = self.beforePos[1]
                    break
                elif i.rect.y < self.rect.y + self.blockSize and i.rect.y > self.rect.y:
                    #下ブロックと衝突
                    self.speed[1] = 0.0
                    self.rect.y = i.rect.y - self.blockSize
                    self.touchFlag[0] = True
                    if self.rect.y < self.beforePos[1]:
                        self.rect.y = self.beforePos[1]
                    break
            
            tempList = pg.sprite.spritecollide(player, blocks, dokill)
            if len(tempList) == 0:
                break
            for i in tempList:
                if i.rect.x + BLOCK_SIZE > self.rect.x and i.rect.x + BLOCK_SIZE < self.rect.x + self.blockSize:
                    #左ブロックと衝突
                    self.speed[0] = 0.0
                    self.force[0] = 0.0
                    self.rect.x = i.rect.x + BLOCK_SIZE
                    self.touchFlag[1] = -1
                    self.touchFlag[2] = self.rect.x
                    self.touchFlag[3] = [i.rect.y - self.blockSize, i.rect.y + self.blockSize]
                    if self.rect.x > self.beforePos[0]:
                        self.rect.x = self.beforePos[0]
                    break
                elif i.rect.x < self.rect.x + self.blockSize and i.rect.x > self.rect.x:
                    #右ブロックと衝突
                    self.speed[0] = 0.0
                    self.force[0] = 0.0
                    self.rect.x = i.rect.x - self.blockSize
                    self.touchFlag[1] = 1
                    self.touchFlag[2] = self.rect.x
                    self.touchFlag[3] = [i.rect.y - self.blockSize, i.rect.y + self.blockSize]
                    if self.rect.x < self.beforePos[0]:
                        self.rect.x = self.beforePos[0]
                    break

    def gameOverJudge(self):
        if self.rect.y > SCREEN_SIZE[1] + BLOCK_SIZE:
            self.setFlag("GameOver")

    def getFlag(self):
        return self.gameFlag
    
    def setFlag(self, flag):
        self.gameFlag = flag

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
        pg.draw.polygon(self.image, (165, 42, 42), [(BLOCK_SIZE / 2, 0), (0, BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE)], 0)
        self.image.set_colorkey((0, 0, 0))
        self.rect = pg.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)

    def update(self, *args, **kwargs):
        pass

class Block(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
        pg.draw.rect(self.image, (255, 215, 0), pg.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE), 0)
        pg.draw.rect(self.image, (165, 42, 42), pg.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
        self.image.set_colorkey((0, 0, 0))
        self.rect = pg.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)

    def update(self, *args, **kwargs):
        pass

class Goal(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.Surface((BLOCK_SIZE / 3, BLOCK_SIZE))
        pg.draw.rect(self.image, (255, 255, 255), pg.Rect(0, 0, BLOCK_SIZE / 3, BLOCK_SIZE), 0)
        self.rect = pg.Rect(pos[0] + BLOCK_SIZE / 3, pos[1], BLOCK_SIZE / 3, BLOCK_SIZE)

    def update(self, *args, **kwargs):
        for i in pg.sprite.spritecollide(kwargs["surviver"], kwargs["goal"], False):
            kwargs["surviver"].setFlag("GameClear")

class GarbageCollection():
    def __init__(self, *args):
        self.GC = args

    def delete(self):
        for i in self.GC:
            i.empty()

def Start(screen, background):
    screen.fill((0, 0, 0))
    font = pg.font.Font(None, 50)
    image1 = font.render("Like Mario Game", True, (255, 255, 255))
    image2 = font.render("Please push SPACE key to start", True, (255, 255, 255))
    rect1 = image1.get_rect()
    rect2 = image2.get_rect()
    rect1 = rect1.move((SCREEN_SIZE[0] - rect1.w) / 2, 50)
    rect2 = rect2.move((SCREEN_SIZE[0] - rect2.w) / 2, 250)
    screen.blit(image1, rect1.topleft)
    screen.blit(image2, rect2.topleft)
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 999
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return 999
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                screen.blit(background, (0, 0))
                pg.display.flip()
                return 1

def GameOver(screen):
    screen.fill((255, 0, 0))
    font = pg.font.Font(None, 50)
    image1 = font.render("RETRY: push R key", True, (255, 255, 255))
    image2 = font.render("FINISH: push F key", True, (255, 255, 255))
    rect1 = image1.get_rect()
    rect2 = image2.get_rect()
    rect1 = rect1.move((SCREEN_SIZE[0] - rect1.w) / 2, 50)
    rect2 = rect2.move((SCREEN_SIZE[0] - rect2.w) / 2, 250)
    screen.blit(image1, rect1.topleft)
    screen.blit(image2, rect2.topleft)
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 999
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return 999
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                return 0
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                return 999

def GameClear(screen):
    screen.fill((200, 255, 0))
    font = pg.font.Font(None, 50)
    image1 = font.render("Congratulations", True, (255, 255, 255))
    image2 = font.render("RETRY: push R key", True, (255, 255, 255))
    image3 = font.render("FINISH: push F key", True, (255, 255, 255))
    rect1 = image1.get_rect()
    rect2 = image2.get_rect()
    rect3 = image3.get_rect()
    rect1 = rect1.move((SCREEN_SIZE[0] - rect1.w) / 2, 50)
    rect2 = rect2.move((SCREEN_SIZE[0] - rect2.w) / 2, 200)
    rect3 = rect3.move((SCREEN_SIZE[0] - rect1.w) / 2, 300)
    screen.blit(image1, rect1.topleft)
    screen.blit(image2, rect2.topleft)
    screen.blit(image3, rect3.topleft)
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 999
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return 999
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                return 0
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                return 999

def main():
    global PAGE

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    background = pg.Surface(SCREEN_SIZE)
    background.fill((0, 255, 255))
    screen.blit(background, (0, 0))
    pg.display.flip()

    all = pg.sprite.RenderUpdates()
    blocks = pg.sprite.Group()
    enemys = pg.sprite.Group()
    goals = pg.sprite.Group()

    Player.containers = all
    Block.containers = all, blocks
    Enemy.containers = all, enemys
    Goal.containers = all, goals

    """
    player = Player((50, 100))
    Enemy((300, 300))
    stage = []
    for i in range(1, 12, 2):
        stage.append(Block((i * BLOCK_SIZE, BLOCK_SIZE * 7)))
    stage.append(Block((BLOCK_SIZE * 3, BLOCK_SIZE * 5)))
    stage.append(Block((BLOCK_SIZE * 5, BLOCK_SIZE * 4)))
    stage.append(Block((BLOCK_SIZE * 6, BLOCK_SIZE * 4)))
    stage.append(Block((BLOCK_SIZE * 7, BLOCK_SIZE * 3)))
    for i in range(7):
        Goal((550, i * BLOCK_SIZE))
    """
    clock = pg.time.Clock()
    player = None
    stage = None
    gc = GarbageCollection(all, blocks, enemys, goals)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                                
        keystate = pg.key.get_pressed()
        if PAGE == 0:
            PAGE = Start(screen, background)
            stage = Stage()
            player = stage.player
            player.setFlag("Running")
        elif PAGE == 1:
            player.move(keystate)
            all.clear(screen, background)
            all.update(keystate, surviver=player, block=blocks, enemy=enemys, goal=goals)
            dirty = all.draw(screen)
            pg.display.update(dirty)

            if player.getFlag() == "GameOver":
                PAGE = 2
            elif player.getFlag() == "GameClear":
                PAGE = 3
        elif PAGE == 2:
            PAGE = GameOver(screen)
            del stage
            gc.delete()
        elif PAGE == 3:
            PAGE = GameClear(screen)
            del stage
            gc.delete()
        elif PAGE == 999:
            return
        pg.time.wait(int(1000 / CLOCK_TICK))

if __name__ == "__main__":
    main()
    pg.quit()
