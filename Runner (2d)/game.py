from typing import Any
import pygame as py
from pygame import *
from sys import exit
from random import randint

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0 

    def player_input(self):
        keys = py.key.get_pressed()
        if keys[py.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1 
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()

def display_score():
    current_time = int(py.time.get_ticks() / 1000) - start_time 
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)] 

# Sets Up Window 
py.init()
screen = py.display.set_mode((800,400))
py.display.set_caption('Runner')

game_active = False
start_time = 0
score = 0

player = py.sprite.GroupSingle()
player.add(Player())

# Clock Object to Control FPS 
clock = py.time.Clock()

test_font = py.font.Font('font/Pixeltype.ttf', 50)

sky_surface = py.image.load('graphics/Sky.png').convert()

ground_surface = py.image.load('graphics/ground.png').convert()

# Obstacles
# Snail
snail_frame_1 = py.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = py.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = py.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = py.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = py.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = py.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_2,player_walk_1]
player_index = 0
player_jump = player_surf = py.image.load('graphics/Player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
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
py.time.set_timer(obstacle_timer,1500)

snail_animation_timer = py.USEREVENT + 2
py.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = py.USEREVENT + 3
py.time.set_timer(fly_animation_timer, 200)

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

            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    game_active = True
                    start_time = int(py.time.get_ticks()/1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100), 300)))
                else: 
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 210)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
        

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        #py.draw.rect(screen, '#c0e8ec', score_rect)
        #py.draw.rect(screen, '#c0e8ec', score_rect, 10)
        #screen.blit(score_surf, score_rect)
        score = display_score()

        # Snails Movement
        #snail_rect.x -= 4
        #if snail_rect.right <= 0: 
        #    snail_rect.left = 800
        #screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()

        # Obstacle Movement 
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

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