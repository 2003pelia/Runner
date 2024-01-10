import pygame as py
from sys import exit

def display_score():
    current_time = int(py.time.get_ticks() / 1000) - start_time 
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

# Sets Up Window 
py.init()
screen = py.display.set_mode((800,400))
py.display.set_caption('Runner')

game_active = False
start_time = 0
score = 0

# Clock Object to Control FPS 
clock = py.time.Clock()

test_font = py.font.Font('font/Pixeltype.ttf', 50)

sky_surface = py.image.load('graphics/Sky.png').convert()

ground_surface = py.image.load('graphics/ground.png').convert()

snail_surf = py.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600, 300))

player_surf = py.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

# Intro Screen
player_stand = py.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = py.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 330))

# Timer
obstacle_timer = py.USEREVENT + 1
py.time.set_timer(obstacle_timer,900)

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            # Stops Program
            exit()
        if game_active:    
            if event.type == py.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -20
                    print('jump')
                
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
                    print('jump')
        else:
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    game_active = True
                    snail_rect.left = 800
                    start_time = int(py.time.get_ticks()/1000)

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        #py.draw.rect(screen, '#c0e8ec', score_rect)
        #py.draw.rect(screen, '#c0e8ec', score_rect, 10)
        #screen.blit(score_surf, score_rect)
        score = display_score()

        # Snails Movement
        snail_rect.x -= 4
        if snail_rect.right <= 0: 
            snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))

        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    # Draw All Elements 
    # Update Everthing 
    py.display.update()

    # Sets Max Frame Rate 
    clock.tick(60)

    #22708