import pygame as py
from sys import exit

# Sets Up Window 
py.init()
screen = py.display.set_mode((800,400))
py.display.set_caption('Runner')

# Clock Object to Control FPS 
clock = py.time.Clock()

test_font = py.font.Font('font/Pixeltype.ttf', 50)

sky_surface = py.image.load('graphics/Sky.png').convert()

ground_surface = py.image.load('graphics/ground.png').convert()

score_surf = test_font.render('My game', False, 'Black')
score_rect = score_surf.get_rect(center = (400, 50))

snail_surf = py.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600, 300))

player_surf = py.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            # Stops Program
            exit()
        #if event.type == py.MOUSEMOTION:
            #if player_rect.collidepoint(event.pos):
                #print('collision')
            
        if event.type == py.KEYDOWN:
            if event.type == py.K_SPACE:
                player_gravity = -20
                print('jump')

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    py.draw.rect(screen, '#c0e8ec', score_rect)
    py.draw.rect(screen, '#c0e8ec', score_rect, 10)
    screen.blit(score_surf, score_rect)

    # Snails Movement
    snail_rect.x -= 4
    if snail_rect.right <= 0: 
        snail_rect.left = 800
    screen.blit(snail_surf, snail_rect)

    # Player
    player_gravity += 1
    player_rect.y += player_gravity
    screen.blit(player_surf, player_rect)

    #keys = py.key.get_pressed()
    #if keys[py.K_SPACE]:
    #    player_rect.bottom -= 1

    #if player_rect.colliderect(snail_rect):
    #    print('collision')

    #mouse_pos = py.mouse.get_pos()
    #if player_rect.collidepoint((mouse_pos)):
        #py.mouse.get.pressed()

    # Draw All Elements 
    # Update Everthing 
    py.display.update()

    # Sets Max Frame Rate 
    clock.tick(60)