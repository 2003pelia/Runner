import pygame as py
from pygame import *
from sys import exit
from random import randint, choice

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = py.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = py.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_2,player_walk_1]
        self.player_index = 0
        self.player_jump = py.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0 

        self.jump_sound = py.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.15)

    def player_input(self):
        keys = py.key.get_pressed()
        if keys[py.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1 
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
        self.image = self.player_walk[int(self.player_index)] 


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(py.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_frame_1 = py.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = py.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = py.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = py.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(py.time.get_ticks() / 1000) - start_time 
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collision_sprite():
   if py.sprite.spritecollide(player.sprite, obstacle_group, False):
       obstacle_group.empty()
       return False
   else:
       return True

# Sets Up Window 
py.init()
screen = py.display.set_mode((800,400))
py.display.set_caption('Runner')

# Clock Object to Control FPS 
clock = py.time.Clock()

test_font = py.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_Music = py.mixer.Sound('audio/music.wav')
bg_Music.play(loops= -1)
bg_Music.set_volume(0.05)

#Groups
player = py.sprite.GroupSingle()
player.add(Player())

obstacle_group = py.sprite.Group()

sky_surface = py.image.load('graphics/Sky.png').convert()
ground_surface = py.image.load('graphics/ground.png').convert()

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

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            # Stops Program
            exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

        else:
            if event.type == py.KEYDOWN and event.key == py.K_SPACE:
                game_active = True
                start_time = int(py.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()

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