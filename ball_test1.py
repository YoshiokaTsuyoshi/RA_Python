import pygame as pg
import sys
import math

SCREEN_SIZE = (600, 600)
BALL_SIZE = 50
FRAME_RATE = 30

def main():
    global PAGE

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    screen.fill((255, 255, 255))
    pg.display.flip()

    ball_image = pg.Surface((BALL_SIZE, BALL_SIZE))
    ball_rect = pg.draw.circle(ball_image, (255, 0, 0), (BALL_SIZE / 2, BALL_SIZE / 2), BALL_SIZE / 2)
    ball_rect = ball_rect.move(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
    ball_vect = [0, 0]
    ball_speed = 0
    ball_image.set_colorkey((0, 0, 0))

    mouse_start_pos = None
    mouse_end_pos = None

    press_flag = False
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return

        screen.fill((255, 255, 255))
        screen.blit(ball_image, [ball_rect.x, ball_rect.y])

        if press_flag:
            mouse_end_pos = pg.mouse.get_pos()
            mouse_vect = [mouse_end_pos[0] - mouse_start_pos[0], mouse_end_pos[1] - mouse_start_pos[1]]
            vect_end = [ball_rect.centerx + mouse_vect[0], ball_rect.centery + mouse_vect[1]]
            pg.draw.line(screen, (0, 0, 0), ball_rect.center, vect_end)
            if not pg.mouse.get_pressed(3)[0]:
                ball_vect = [mouse_end_pos[0] - mouse_start_pos[0], mouse_end_pos[1] - mouse_start_pos[1]]
                ball_speed = math.sqrt(ball_vect[0]**2 + ball_vect[1]**2)
                press_flag = False
        else:
            if pg.mouse.get_pressed(3)[0]:
                mouse_start_pos = pg.mouse.get_pos()
                press_flag = True

        ball_rect.x += ball_vect[0] * ball_speed * 0.001
        ball_rect.y += ball_vect[1] * ball_speed * 0.001

        if ball_rect.centerx - BALL_SIZE / 2 < 0 or ball_rect.centerx + BALL_SIZE / 2 > SCREEN_SIZE[0]:
            ball_rect.x -= ball_vect[0] * ball_speed * 0.001
            ball_vect[0] *= -1
        if ball_rect.centery - BALL_SIZE / 2 < 0 or ball_rect.centery + BALL_SIZE / 2 > SCREEN_SIZE[1]:
            ball_rect.y -= ball_vect[1] * ball_speed * 0.001
            ball_vect[1] *= -1

        if ball_speed > 0:
            ball_speed -= 1
            if ball_speed < 0:
                ball_speed = 0

        pg.display.flip()
        pg.time.wait(int(1000 / FRAME_RATE))

if __name__ == "__main__":
    main()
    pg.quit()
