import pygame as pg
import pygame.camera
import time

SCREEN_SIZE = (640, 480)

pg.init()
pygame.camera.init()
camera = pygame.camera.Camera(pygame.camera.list_cameras()[0], SCREEN_SIZE, "RGB")

camera.start()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()
flag = True

while flag:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            flag = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                flag = False
            elif event.key == pg.K_SPACE:
                timer = time.gmtime()
                pg.image.save(screen, "{}_{}_{}_{}_{}_{}.png".format(timer.tm_year, timer.tm_mon, timer.tm_mday, timer.tm_hour, timer.tm_min, timer.tm_sec))
                pg.time.wait(500)
            
    camera.get_image(screen)
    pg.display.flip()
    clock.tick(60)

camera.stop()
pg.quit()