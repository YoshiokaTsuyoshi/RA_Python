import pygame as pg
import sys
import math
import random

from pygame.sprite import AbstractGroup

SCREEN_SIZE = (400, 600)
BALL_SIZE = [15, 20, 25, 30, 35, 40, 45, 50, 60]
FRAME_RATE = 25

class Ball(pg.sprite.Sprite):
    ballList = []
    ballGroup = pg.sprite.Group()
    updateTime = 0.25
    def __init__(self, pos, radius, index):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.radius = radius
        self.image = pg.Surface((self.radius * 2, self.radius * 2))
        pg.Surface.fill(self.image, (0, 0, 0))
        pg.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius)
        self.imageCopy = self.image.copy()
        self.rect = pg.Rect(pos[0] - self.radius, pos[1] - self.radius, self.radius * 2, self.radius * 2)
        self.image.set_colorkey((0, 0, 0))
        self.speed = [0, 0]
        self.force = [0, 9.8]
        self.tempForce = [0, 0]
        self.angle = 0
        self.wallTouchFlag = [0, 0]
        self.fixedFlag = False
        self.fallFlag = False
        self.ballListIndex = index

    def update(self, *args, **kwargs):
        if self.fallFlag:

            tempX = self.speed[0] * self.updateTime + (self.force[0] + self.tempForce[0]) * self.updateTime**2
            if self.wallTouchFlag[0] == 1:
                if tempX < 0:
                    tempX = 0
                else:
                    self.wallTouchFlag[0] = 0
            elif self.wallTouchFlag[0] == 2:
                if tempX > 0:
                    tempX = 0
                else:
                    self.wallTouchFlag[0] = 0
            self.rect.x += tempX
            tempY = self.speed[1] * self.updateTime + (self.force[1] + self.tempForce[1]) * self.updateTime**2
            if self.wallTouchFlag[1] == 1:
                if tempY > 0:
                    tempY = 0
                else:
                    self.wallTouchFlag[1] = 0
            self.rect.y += tempY

            self.tempForce[0] = 0
            self.tempForce[1] = 0
            
            for index in self.collideList():
                i = self.ballList[index]
                tempR = math.sqrt((i.rect.centerx - self.rect.centerx)**2 + (i.rect.centery - self.rect.centery)**2) + sys.float_info.min
                tempSin = (i.rect.centerx - self.rect.centerx) / tempR
                tempCos = (i.rect.centery - self.rect.centery) / tempR
                if self.wallTouchFlag[0]:
                    pass
                else:
                    self.rect.x = i.rect.centerx - (i.rect.w * 0.5 + self.radius) * tempSin - self.radius
                if self.wallTouchFlag[1]:
                    pass
                else:
                    self.rect.y = i.rect.centery - (i.rect.w * 0.5 + self.radius) * tempCos - self.radius
                tempR = math.sqrt((i.rect.centerx - self.rect.centerx)**2 + (i.rect.centery - self.rect.centery)**2) + sys.float_info.min
                tempSin = (i.rect.centerx - self.rect.centerx) / tempR
                tempCos = (i.rect.centery - self.rect.centery) / tempR
                if self.wallTouchFlag[0]:
                    pass
                else:
                    self.tempForce[0] = -self.force[1] * tempSin / (abs(tempSin) + tempCos + sys.float_info.min)
                if self.wallTouchFlag[1]:
                    pass
                else:
                    self.tempForce[1] = -self.force[1] * tempCos / (abs(tempSin) + tempCos + sys.float_info.min)
                i.tempForce[0] = -self.tempForce[0]
                i.tempForce[1] = -self.tempForce[1]

    def fixedUpdate(self):
        if self.fallFlag:

            self.tempForce[0] *= 0.5
            self.tempForce[1] *= 0.5

            self.speed[0] = self.speed[0] + (self.force[0] + self.tempForce[0]) * self.updateTime
            self.speed[1] = self.speed[1] + (self.force[1] + self.tempForce[1]) * self.updateTime

            self.wallTouchFlag = [0, 0]

            if self.rect.centery >= SCREEN_SIZE[1] - self.radius:
                self.rect.y = SCREEN_SIZE[1] - self.radius * 2
                self.speed[0] *= 0.6
                self.speed[1] = 0
                self.tempForce[1] = -self.force[1]
                self.wallTouchFlag[1] = 1
            if self.rect.centery <= self.radius:
                self.rect.y = 0
            if self.rect.centerx <= self.radius:
                self.rect.x = 0
                self.tempForce[0] = 0
                self.speed[0] *= -1
                self.wallTouchFlag[0] = 1
            if self.rect.centerx >= SCREEN_SIZE[0] - self.radius:
                self.rect.x = SCREEN_SIZE[0] - self.radius * 2
                self.tempForce[0] = 0
                self.speed[0] *= -1
                self.wallTouchFlag[0] = 2

    def collideList(self):
        indexList = []
        for i in range(len(self.ballList)):
            if i == self.ballListIndex:
                continue
            if pg.sprite.collide_circle(self, self.ballList[i]):
                indexList.append(i)
        return indexList

class FallGate(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.font = pg.font.Font(None, 30)
        self.image = self.font.render("V", True, (0, 0, 0))
        self.rect = self.image.get_rect().move(SCREEN_SIZE[0] / 2, 80)
        self.ballRadius = BALL_SIZE[random.randint(0, int(len(BALL_SIZE) * 0.5))]
        Ball.ballList = [Ball((self.rect.centerx, 40), self.ballRadius, len(Ball.ballList))]
        Ball.ballGroup.add(Ball.ballList[-1])
        self.ball = Ball.ballList[-1]
        self.speed = 0
        self.spaceFlag = True

    def update(self, *args, **kwargs) -> None:
        if args[0][pg.K_SPACE]:
            if self.spaceFlag:
                self.ball.fallFlag = True
                self.ball.rect.y = 100
                self.ballRadius = BALL_SIZE[random.randint(0, int(len(BALL_SIZE) * 0.5))]
                Ball.ballList.append(Ball((self.rect.centerx, 50), self.ballRadius, len(Ball.ballList)))
                Ball.ballGroup.add(Ball.ballList[-1])
                self.ball = Ball.ballList[-1]
                self.spaceFlag = False
        else:
            self.spaceFlag = True
        direction = args[0][pg.K_RIGHT] - args[0][pg.K_LEFT]
        if direction == 0:
            self.speed = 0
            return
        else:
            self.speed += 1
        self.rect.x += direction * self.speed
        if self.rect.centerx < self.ballRadius :
            self.rect.x = self.ballRadius - self.rect.w / 2
        if self.rect.centerx > SCREEN_SIZE[0] - self.ballRadius:
            self.rect.x = SCREEN_SIZE[0] - self.ballRadius - self.rect.w / 2
        self.ball.rect.x = self.rect.centerx - self.ballRadius

def main():

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    background = pg.Surface(SCREEN_SIZE)
    background.fill((255, 255, 255))
    pg.draw.rect(background, (0, 0, 0), pg.Rect(0, 100, SCREEN_SIZE[0], SCREEN_SIZE[1] - 100), 1, 1)
    screen.blit(background, (0, 0))
    pg.display.flip()

    all = pg.sprite.RenderUpdates()

    Ball.containers = all
    FallGate.containers = all

    FallGate()
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                
        all.clear(screen, background)
        all.update(pg.key.get_pressed())
        for ball in Ball.ballList:
            ball.fixedUpdate()
        dirty = all.draw(screen)
        pg.display.update(dirty)

        pg.time.wait(int(1000 / FRAME_RATE))

if __name__ == "__main__":
    main()
    pg.quit()
