import pygame
import sys
import os
from random import randint
pygame.mixer.init()
pygame.font.init()

WIDTH, HEIGHT = 450, 650
FPS = 60
pygame.display.set_caption("Flappy Bird")
BIRD_ICON = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bird_icon.jpg")), (32, 32))
pygame.display.set_icon(BIRD_ICON)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN_RECT = WIN.get_rect()


TITLE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "title.png")), (230, 140))
PLAY_BUTTON = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "play_button.png")), (120, 90))
MENU_PLAY_BUTTON = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "play_button.png")), (160, 130))
MENU_PLAY_BUTTON_OVER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "play_button.png")), (165, 135))
MENU_PLAY_BUTTON_RECT = MENU_PLAY_BUTTON.get_rect(center=WIN_RECT.center)
PLAY_BUTTON_RECT = PLAY_BUTTON.get_rect(center=WIN_RECT.center)
GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "game over.png")), (260, 75))
SCORE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "score.png")), (290, 160))
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.png")), (WIDTH, HEIGHT))
GROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "ground.jpg")), (460, HEIGHT * 0.2))
GROUND2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "ground.jpg")), (460, HEIGHT * 0.2))
STANDING_BIRD = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Standing_bird.png")), (51, 39))

PIPES_AMOUNT = 3

PIPES_UP_SPRITES = []
PIPES_DOWN_SPRITES = []
for i in range(PIPES_AMOUNT):
    PIPE_UP_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Pipe_up.png")), (80, 400))
    PIPES_UP_SPRITES.append(PIPE_UP_SPRITE)
    PIPE_DOWN_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Pipe_down.png")), (80, 400))
    PIPES_DOWN_SPRITES.append(PIPE_DOWN_SPRITE)


UP_BIRDS = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "up_bird_normal.png")), (51, 46)),
            pygame.transform.scale(pygame.image.load(os.path.join("Assets", "up_bird_normal.png")), (51, 46)), 
            pygame.transform.scale(pygame.image.load(os.path.join("Assets", "up_bird_up.png")), (51, 46)),
            pygame.transform.scale(pygame.image.load(os.path.join("Assets", "up_bird_normal.png")), (51, 46)),
            pygame.transform.scale(pygame.image.load(os.path.join("Assets", "up_bird_normal.png")), (51, 46)),
            pygame.transform.scale(pygame.image.load(os.path.join("Assets", "up_bird_down.png")), (51, 46))]

STANDING_BIRDS = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "standing bird0.png")), (50, 46)),
                  pygame.transform.scale(pygame.image.load(os.path.join("Assets", "standing bird1.png")), (50, 46)),
                  pygame.transform.scale(pygame.image.load(os.path.join("Assets", "standing bird0.png")), (50, 46)),
                  pygame.transform.scale(pygame.image.load(os.path.join("Assets", "standing bird2.png")), (50, 46))]

FLAP_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Flap sound effect.mp3"))
POINTS_SOUND = pygame.mixer.Sound(os.path.join("Assets", "point sound.mp3"))
DEATH_SOUND = pygame.mixer.Sound(os.path.join("Assets", "death sound.mp3"))
PLAY_AGAIN_SOUND = pygame.mixer.Sound(os.path.join("Assets", "play again sound.mp3"))


POINTS_FONT = pygame.font.Font(os.path.join("Assets", "numbers font.ttf"), 30)
POINTS_FONT_OUTLINE = pygame.font.Font(os.path.join("Assets", "numbers font.ttf"), 35)
SCORE_FONT = pygame.font.Font(os.path.join("Assets", "numbers font.ttf"), 26)
SCORE_FONT_OUTLINE = pygame.font.Font(os.path.join("Assets", "numbers font.ttf"), 31)


PIPE_GAP = 530
GAME_SPEED = 3
pressed = False
can_jump = True
dead = False
duck_hit = False
title_current_sprite = 0
current_sprite = 0
points = 0
record = 0


def main_menu():
    global title_current_sprite
    TITLE_RECT = TITLE.get_rect(center=WIN_RECT.center)
    title_player = pygame.Rect(200, 200, 50, 46)
    y_momentum = 0
    ground_hitbox = pygame.Rect(0, 545, GROUND.get_width(), GROUND.get_height())
    ground2_hitbox = pygame.Rect(450, 545, GROUND.get_width(), GROUND.get_height())

    while True:
        y_momentum += 0.07
        if y_momentum > 3:
            y_momentum = -2
        title_player.y += y_momentum

        if title_player.y == -100:
            title_player.y = 100

        WIN.blit(BG, (0, 0))
        WIN.blit(TITLE, (TITLE_RECT[0], TITLE_RECT[1] - 200))
        WIN.blit(STANDING_BIRDS[int(title_current_sprite)], (title_player.x, title_player.y))
        WIN.blit(MENU_PLAY_BUTTON, (MENU_PLAY_BUTTON_RECT[0], MENU_PLAY_BUTTON_RECT[1] + 100))

        WIN.blit(GROUND, (ground_hitbox.x, 565))
        WIN.blit(GROUND2, (ground2_hitbox.x, 565))

        if MENU_PLAY_BUTTON.get_rect(x=MENU_PLAY_BUTTON_RECT[0], y=MENU_PLAY_BUTTON_RECT[1] + 100).collidepoint(pygame.mouse.get_pos()):
            WIN.blit(MENU_PLAY_BUTTON_OVER, (MENU_PLAY_BUTTON_RECT[0] - 2, MENU_PLAY_BUTTON_RECT[1] + 98))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    PLAY_AGAIN_SOUND.play()
                    main()


        ground_hitbox.x -= 1
        ground2_hitbox.x -= 1
        if ground_hitbox.x < -460:
            ground_hitbox.x = 438
        if ground2_hitbox.x < -460:
            ground2_hitbox.x = 438

        title_current_sprite += 0.08
        if title_current_sprite > 4:
            title_current_sprite = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        



def draw_elements(ground_hitbox, player_hitbox, player, ground2_hitbox, pipes_up, pipes_down):
    global pressed, current_sprite, points, dead, record

    WIN.blit(BG, (0, 0))

    for i in range(PIPES_AMOUNT):
        WIN.blit(PIPES_UP_SPRITES[i], (pipes_up[i].x, pipes_up[i].y))
        WIN.blit(PIPES_DOWN_SPRITES[i], (pipes_down[i].x, pipes_down[i].y))
        
    WIN.blit(GROUND, (ground_hitbox.x, 565))
    WIN.blit(GROUND2, (ground2_hitbox.x, 565))

    #GAME OVER SCREEN
    if player_hitbox.y > 529:
        WIN.blit(STANDING_BIRD, (player.x, player.y))
        GAME_OVER_RECT = GAME_OVER.get_rect(center=WIN_RECT.center)
        draw_score = SCORE_FONT.render(f"{points}", 1, (255, 255, 255))
        draw_score_outline = SCORE_FONT_OUTLINE.render(f"{points}", 1, (0, 0, 0))
        draw_record = SCORE_FONT.render(f"{record}", 1, (255, 255, 255))
        draw_record_outline = SCORE_FONT_OUTLINE.render(f"{record}", 1, (0, 0, 0))
        WIN.blit(GAME_OVER, (GAME_OVER_RECT[0], GAME_OVER_RECT[1] - 150))
        WIN.blit(SCORE, (GAME_OVER_RECT[0] - 22, GAME_OVER_RECT[1] - 55))
        WIN.blit(draw_score_outline, (GAME_OVER_RECT[0] + 214, GAME_OVER_RECT[1] - 5))
        WIN.blit(draw_score, (GAME_OVER_RECT[0] + 214, GAME_OVER_RECT[1] - 5))
        WIN.blit(draw_record_outline, (GAME_OVER_RECT[0] + 215, GAME_OVER_RECT[1] + 53))
        WIN.blit(draw_record, (GAME_OVER_RECT[0] + 215, GAME_OVER_RECT[1] + 53))
        WIN.blit(PLAY_BUTTON, (WIDTH//2 - 67, HEIGHT//2 + 90))                      
    
    else:
        draw_points = POINTS_FONT.render(f"{points}", 1, (255, 255, 255))
        draw_points_outline = POINTS_FONT_OUTLINE.render(f"{points}", 1, (0, 0, 0))
        draw_points_rect = draw_points.get_rect(center=WIN_RECT.center)
        WIN.blit(draw_points_outline, (draw_points_rect[0], draw_points_rect[1] - 260))
        WIN.blit(draw_points, (draw_points_rect[0], draw_points_rect[1] - 260))

        if pressed:
            WIN.blit(UP_BIRDS[int(current_sprite)], (player.x, player.y))
            current_sprite += 0.3
            if current_sprite > 6:
                current_sprite = 0
        else:
            WIN.blit(STANDING_BIRD, (player.x, player.y))
    

    pygame.display.update()


def pipes(pipes_up, pipes_down):
    global points, dead, record
    for i in range(PIPES_AMOUNT):
        pipes_up[i].x -= GAME_SPEED
        pipes_down[i].x -= GAME_SPEED

    pipe_random_pos = randint(200, 500)
    for i in range(PIPES_AMOUNT):
        if not dead:
            if pipes_down[i].x == 105 or pipes_down[i].x == 106 or pipes_down[i].x == 107:
                points += 1
                POINTS_SOUND.play()
                if points > record:
                    record = points

        if pipes_up[i].x < -100:
            pipes_up[i] = pygame.Rect(640, pipe_random_pos, 80, 400)
            pipes_down[i] = pygame.Rect(640, pipe_random_pos - PIPE_GAP, 80, 400)


def collision_check(player_hitbox, player, ground_hitbox, ground2_hitbox, pipes_up, pipes_down):
    global can_jump, GAME_SPEED, dead, duck_hit

    for i in range(PIPES_AMOUNT):
        if (player_hitbox.colliderect(pipes_up[i]) or player_hitbox.colliderect(pipes_down[i]) or player_hitbox.colliderect(ground_hitbox) or player_hitbox.colliderect(ground2_hitbox)) and not duck_hit:
            DEATH_SOUND.play()
            can_jump = False
            GAME_SPEED = 0
            dead = True
            duck_hit = True   


def ground(ground_hitbox, ground2_hitbox, player_hitbox, player):
    ground_hitbox.x -= GAME_SPEED
    ground2_hitbox.x -= GAME_SPEED

    if ground_hitbox.x < -460:
        ground_hitbox.x = 438
    if ground2_hitbox.x < -460:
        ground2_hitbox.x = 438

    if player_hitbox.y > 530:
        player.y = 530
        player_hitbox.y = 530
    

def main():
    global pressed, points, duck_hit, can_jump, dead, GAME_SPEED
    pipes_up = []
    pipes_down = []
    points = 0
    clock = pygame.time.Clock()
    ground_hitbox = pygame.Rect(0, 545, GROUND.get_width(), GROUND.get_height())
    ground2_hitbox = pygame.Rect(450, 545, GROUND.get_width(), GROUND.get_height())
    player = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 30, 51, 39)
    player_hitbox = pygame.Rect(WIDTH//2 - 113, HEIGHT//2 - 23, 35, 29)
    player_y_momentum = 0
    duck_hit = False
    can_jump = True
    pressed = False
    dead = False
    GAME_SPEED = 3

    pipe_position = 0
    for i in range(PIPES_AMOUNT):
        pipe_first_random_pos = randint(170, 510)
        pipe_up = pygame.Rect(600 + pipe_position, pipe_first_random_pos, 80, 400)
        pipes_up.append(pipe_up)
        pipe_down = pygame.Rect(600 + pipe_position, pipe_first_random_pos - PIPE_GAP, 80, 400)
        pipes_down.append(pipe_down)
        pipe_position += 250

    while True:
        clock.tick(FPS)

        player_y_momentum += 0.4
        if player_y_momentum > 8:
            player_y_momentum = 8
        player.y += player_y_momentum
        player_hitbox.y += player_y_momentum


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if dead:
                if PLAY_BUTTON.get_rect(x=WIDTH//2 - 67, y=HEIGHT//2 + 90).collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        PLAY_AGAIN_SOUND.play()
                        main()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        PLAY_AGAIN_SOUND.play()
                        main()
                        
            if player.y > -100:           
                if can_jump:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            FLAP_SOUND.play()
                            player_y_momentum = -7
                            pressed = True


        ground(ground_hitbox, ground2_hitbox, player_hitbox, player)
        pipes(pipes_up, pipes_down)
        collision_check(player_hitbox, player, ground_hitbox, ground2_hitbox, pipes_up, pipes_down)
        draw_elements(ground_hitbox, player_hitbox, player, ground2_hitbox, pipes_up, pipes_down)

        pygame.display.update()


if __name__ == "__main__":
    main_menu()