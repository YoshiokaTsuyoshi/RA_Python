import pygame as pg
import pygame.camera

SCREEN_SIZE = (640, 480)

pg.init()
pygame.camera.init()
camera = pygame.camera.Camera(pygame.camera.list_cameras()[0], SCREEN_SIZE, "RGB")

camera.start()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()
flag = True
count = 0

while flag:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            flag = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                flag = False
            elif event.key == pg.K_SPACE:
                pg.image.save(screen, "picture{}.png".format(count))
                count += 1
            
    camera.get_image(screen)
    pg.display.flip()
    clock.tick(100)

camera.stop()
pg.quit()