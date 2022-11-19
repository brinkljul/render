import os
import pygame
import utils

os.environ["SDL_VIDEO_CENTERED"] = '1'
screenwidth, screenheight = 1200, 800
pygame.init()
pycon = pygame.image.load('cube.png')
pygame.display.set_icon(pycon)
screen = pygame.display.set_mode([screenwidth, screenheight])
pygame.display.set_caption("Projection")
clock = pygame.time.Clock()
fps = 60

pos = [screenwidth // 2, screenheight // 2, screenwidth // 2]
color = [50, 50, 50]
scale = 1200
speed = 0.025
# angle = [0.5, 0.25, 0.5]
cam_pos = [screenwidth // 2, screenheight // 2, screenwidth // 2 - 1000]
light_pos = [screenwidth // 2 - 400, screenheight // 2 - 400, screenwidth // 2 - 1000]

obj_a = utils.custom("teapot-lowpoly.obj")
obj_a.rotate_y(-0.7)
obj_a.rotate_x(-0.45)


running = True

while running:
    clock.tick(fps)
    screen.fill((0, 0, 0))

    # x button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFTBRACKET:
                speed *= 0.8
            elif event.key == pygame.K_RIGHTBRACKET:
                speed *= 1.2
            elif event.key == pygame.K_1:
                obj_a = utils.cube()
                obj_a.rotate_y(-0.7)
                obj_a.rotate_x(-0.45)
            elif event.key == pygame.K_2:
                obj_a = utils.pyramid()
                obj_a.rotate_y(-0.7)
                obj_a.rotate_x(-0.45)
            elif event.key == pygame.K_3:
                obj_a = utils.diamond()
                obj_a.rotate_y(-0.7)
                obj_a.rotate_x(-0.45)
            elif event.key == pygame.K_4:
                obj_a = utils.custom("teapot-lowpoly.obj")
                obj_a.rotate_y(-0.7)
                obj_a.rotate_x(-0.45)
            elif event.key == pygame.K_5:
                obj_a = utils.custom("cat.obj")
                obj_a.rotate_y(-0.7)
                obj_a.rotate_x(-0.45)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        obj_a.rotate_y(speed)
    if keys[pygame.K_RIGHT]:
        obj_a.rotate_y(-speed)
    if keys[pygame.K_UP]:
        obj_a.rotate_x(speed)
    if keys[pygame.K_DOWN]:
        obj_a.rotate_x(-speed)
    if keys[pygame.K_SPACE]:
        obj_a.rotate_z(speed)
    if keys[pygame.K_LSHIFT]:
        obj_a.rotate_z(-speed)
    if keys[pygame.K_n]:
        color = list(map(lambda x: x - 1 if x > 0 else 0, color))
    if keys[pygame.K_m]:
        color = list(map(lambda x: x + 1 if x < 255 else 255, color))
    if keys[pygame.K_MINUS]:
        scale *= 0.99
    if keys[pygame.K_EQUALS]:
        scale *= 1.01
    if keys[pygame.K_w]:
        pos[1] -= speed * 400
    if keys[pygame.K_s]:
        pos[1] += speed * 400
    if keys[pygame.K_d]:
        pos[0] += speed * 400
    if keys[pygame.K_a]:
        pos[0] -= speed * 400
    if keys[pygame.K_e]:
        pos[2] += speed * 400
    if keys[pygame.K_q]:
        pos[2] -= speed * 400

    obj_a.draw(screen, cam_pos, tuple(color), pos, scale, light_pos)

    pygame.display.update()


pygame.quit()