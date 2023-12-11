from typing import Any
import pygame as pg
import sys
import math
import random

from pygame.sprite import AbstractGroup

SCREEN_SIZE = (400, 600)
BALL_SIZE = [4, 7, 10, 14, 18, 23, 28, 34, 40]
FRAME_RATE = 30

class Ball(pg.sprite.Sprite):
    def __init__(self, pos, radius):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.radius = radius
        self.image = pg.Surface((self.radius * 2, self.radius * 2))
        pg.Surface.fill(self.image, (0, 0, 0))
        pg.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius)
        self.rect = pg.Rect(pos[0] - self.radius, pos[1] - self.radius, self.radius * 2, self.radius * 2)
        self.image.set_colorkey((0, 0, 0))
        self.speed = 20
        self.fallFlag = False

    def update(self, *args, **kwargs):
        if self.fallFlag:
            self.rect.y += self.speed
            if self.rect.centery > SCREEN_SIZE[1] - self.radius:
                self.rect.y = SCREEN_SIZE[1] - self.radius * 2

class FallGate(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.font = pg.font.Font(None, 30)
        self.image = self.font.render("V", True, (0, 0, 0))
        self.rect = self.image.get_rect().move(SCREEN_SIZE[0] / 2, 80)
        self.ballRadius = BALL_SIZE[random.randint(0, int(len(BALL_SIZE) * 0.5))]
        self.ballList = [Ball((self.rect.centerx, 40), self.ballRadius)]
        self.ball = self.ballList[-1]
        self.speed = 0
        self.spaceFlag = True

    def update(self, *args: Any, **kwargs: Any) -> None:
        if args[0][pg.K_SPACE]:
            if self.spaceFlag:
                self.ball.fallFlag = True
                self.ballRadius = BALL_SIZE[random.randint(0, int(len(BALL_SIZE) * 0.5))]
                self.ballList.append(Ball((self.rect.centerx, 50), self.ballRadius))
                self.ball = self.ballList[-1]
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

class Arrow(pg.sprite.Sprite):
    def __init__(self, ball : Ball):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen = pg.Surface(SCREEN_SIZE)
        self.screen.fill((255, 255, 255))
        self.image = pg.Surface((0, 0))
        self.rect = pg.Rect(0, 0, 0, 0)
        self.press_flag = False
        self.mouse_start_pos = None
        self.mouse_end_pos = None
        self.ball = ball

    def update(self, *args, **kwargs):
        if self.press_flag:
            self.mouse_end_pos = pg.mouse.get_pos()
            self.mouse_vect = [self.mouse_end_pos[0] - self.mouse_start_pos[0], self.mouse_end_pos[1] - self.mouse_start_pos[1]]
            vect_end = [self.ball.rect.centerx + self.mouse_vect[0], self.ball.rect.centery + self.mouse_vect[1]]
            self.rect = pg.draw.line(self.screen, (0, 0, 0), self.ball.rect.center, vect_end)
            self.image = pg.Surface((self.rect.w, self.rect.h))
            self.image.blit(self.screen, (0, 0), self.rect)
            self.image.set_colorkey((255, 255, 255))
            self.screen.fill((255, 255, 255))
            if not pg.mouse.get_pressed(3)[0]:
                self.ball.vect = [self.mouse_end_pos[0] - self.mouse_start_pos[0], self.mouse_end_pos[1] - self.mouse_start_pos[1]]
                self.ball.speed = math.sqrt(self.ball.vect[0]**2 + self.ball.vect[1]**2)
                self.press_flag = False
                self.image = pg.Surface((0, 0))
        else:
            if pg.mouse.get_pressed(3)[0]:
                self.mouse_start_pos = pg.mouse.get_pos()
                self.press_flag = True

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
    Arrow.containers = all

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
        dirty = all.draw(screen)
        pg.display.update(dirty)

        pg.time.wait(int(1000 / FRAME_RATE))

if __name__ == "__main__":
    main()
    pg.quit()
