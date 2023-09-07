import pygame as pg
import sys

SCREEN_SIZE = (600, 600)
MASU_SIZE = 50
FRAME_RATE = 30

class Ball(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.Surface((BALL_SIZE, BALL_SIZE))
        pg.draw.circle(self.image, (255, 0, 0), (BALL_SIZE / 2, BALL_SIZE / 2), BALL_SIZE / 2)
        self.rect = pg.Rect(pos[0], pos[1], BALL_SIZE, BALL_SIZE)
        self.vect = [0, 0]
        self.speed = 0
        self.image.set_colorkey((0, 0, 0))

    def update(self, *args, **kwargs):
        self.rect.x += self.vect[0] * self.speed * 0.001
        self.rect.y += self.vect[1] * self.speed * 0.001

        if self.rect.centerx - BALL_SIZE / 2 < 0 or self.rect.centerx + BALL_SIZE / 2 > SCREEN_SIZE[0]:
            self.rect.x -= self.vect[0] * self.speed * 0.001
            self.vect[0] *= -1
        if self.rect.centery - BALL_SIZE / 2 < 0 or self.rect.centery + BALL_SIZE / 2 > SCREEN_SIZE[1]:
            self.rect.y -= self.vect[1] * self.speed * 0.001
            self.vect[1] *= -1

        if self.speed > 0:
            self.speed -= 1
            if self.speed < 0:
                self.speed = 0

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
    screen.blit(background, (0, 0))
    pg.display.flip()

    all = pg.sprite.RenderUpdates()

    Ball.containers = all
    Arrow.containers = all

    Arrow(Ball((SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)))
    
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