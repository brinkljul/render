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
color = (50, 50, 50)
scale = 1200
speed = 0.025
# angle = [0.5, 0.25, 0.5]
cam_pos = [screenwidth // 2, screenheight // 2, screenwidth // 2 - 1000]
light_pos = [screenwidth // 2 - 400, screenheight // 2 - 400, screenwidth // 2 - 1000]

cube_a = utils.cube()
cube_a.rotate_y(-0.7)
cube_a.rotate_x(-0.45)


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
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cube_a.rotate_y(speed)
    if keys[pygame.K_RIGHT]:
        cube_a.rotate_y(-speed)
    if keys[pygame.K_UP]:
        cube_a.rotate_x(speed)
    if keys[pygame.K_DOWN]:
        cube_a.rotate_x(-speed)
    if keys[pygame.K_SPACE]:
        cube_a.rotate_z(speed)
    if keys[pygame.K_LSHIFT]:
        cube_a.rotate_z(-speed)

    cube_a.draw(screen, cam_pos, color, pos, scale, light_pos)

    pygame.display.update()


pygame.quit()