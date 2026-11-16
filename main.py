import pygame
import random

pygame.init()

clock = pygame.time.Clock()

# WINDOW DIMENSIONS
WIDTH = 1000
HEIGHT = 600

#GAME WINDOW
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=1)

#WINDOW TITLE
pygame.display.set_caption("Flappy Papi Bird")


#FONTS
game_over_font = pygame.font.SysFont(None, 80)
restart_font = pygame.font.SysFont(None, 40)
score_font = pygame.font.SysFont(None, 50)


# LOAD BACKGROUND
background_image = pygame.image.load("assets/background3.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


#LOAD BIRD
bird_image = pygame.image.load("assets/bird.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (50, 40))


#BIR POSITION
bird_x = 200 
bird_y = 300

#BIRD RECTANGLE
bird_rect = pygame.Rect(bird_x + 7, bird_y + 5, 36, 30)

#BIRD PHYSICS
bird_velocity = 0
gravity = 1800

#LOAD PIPE
pipe_image = pygame.image.load("assets/pipe.png").convert_alpha()
pipe_image = pygame.transform.scale(pipe_image, (200, 360))

pipe_up_image = pygame.transform.flip(pipe_image, False, True)

#PIPE CAP SETTINGS
PIPE_WIDTH = 200
PIPE_HEIGHT = 360
CAP_HEIGHT = 40

#SEPARATE PIPE AND BODY
pipe_body = pipe_image.subsurface((0, 0, PIPE_WIDTH, 212))
pipe_cap = pipe_image.subsurface((0, 212, PIPE_WIDTH, CAP_HEIGHT))



#BUILD A PIPE WITH A PRESERVED
def make_pipe(body, cap, total_height):

    # CAP NEVER CHANGES SIZE
    body_height = total_height - CAP_HEIGHT

    # ONLY RESIZE THE BODY
    stretched_body = pygame.transform.scale(
        body, (PIPE_WIDTH, body_height)
    )

    # CREATE THE COMPLETE PIPE
    new_pipe = pygame.Surface(
        (PIPE_WIDTH, total_height), pygame.SRCALPHA
    )

    # PUT BODY AND CAP TOGETHER
    new_pipe.blit(stretched_body, (0, 0))
    new_pipe.blit(cap, (0, body_height))

    return new_pipe


#PIPE POSITIONSSS 
pipe_positions = [
    [800, -200],
    [1400, -30]
]
top_pipe_y = -114
bottom_pipe_y = 354

pipe_speed = 240

speed_timer = 0 
speed_increase = 20

#SCORE
score = 0
scored_pipes = []

#GAME LOOP CONTROL
running = True
game_over = False
game_started = False

#GAME LOOP
while running:


    for event in pygame.event.get():

        #BIRD PHYSICS
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not game_over:
                if not game_started:
                    game_started = True
                
                bird_velocity = -500


            if event.key == pygame.K_r and game_over:
                bird_x = 200
                bird_y = 300
                bird_velocity = 0
                score = 0
                scored_pipes = []

                pipe_speed = 240
                speed_timer = 0

                pipe_positions = [
                    [800, -200],
                    [1400, -30]
                ]


                game_over = False
                game_started = False

        #QUIT GAME
        if event.type == pygame.QUIT:
            running = False

    dt = 1 / 60
    clock.tick(60)

    if game_started and not game_over:
        speed_timer += dt

        if speed_timer >= 10:
            pipe_speed += speed_increase
            speed_timer = 0


    if game_started and not game_over:

        #APPLY GRAVITY
        bird_velocity += gravity * dt
        bird_y += bird_velocity * dt

        bird_rect.topleft = (bird_x, bird_y)

        #CHECK IF BIRD HITS THE SCREEN BOUNDRIES
        if bird_y < 0 or bird_y + 40 > HEIGHT:
            game_over = True


        #MOVE PIPES
        for pipe_index, pipe in enumerate(pipe_positions):
            pipe[0] -= pipe_speed * dt

            #RESPAWN PIPES
            if pipe[0] < -200:
                pipe[0] = max(p[0] for p in pipe_positions) + 600
                pipe[1] = random.randint(-200, -30)

                if pipe_index in scored_pipes:
                    scored_pipes.remove(pipe_index)

    
    screen.blit(background_image, (0, 0))
    screen.blit(bird_image, (bird_x, bird_y))

    for pipe_index, pipe in enumerate(pipe_positions):
        pipe_x = pipe[0]

        #CHECK IF BIRD PASSED PIPE
        if pipe_x + PIPE_WIDTH < bird_x and pipe_index not in scored_pipes:
            score += 1
            scored_pipes.append(pipe_index)

        # CALCULATE THE GAP
        gap_top = pipe[1] + 360
        gap_bottom = gap_top + 120

        # CALCULATE PIPE HEIGHTS
        top_pipe_height = gap_top
        bottom_pipe_height = HEIGHT - gap_bottom

        # BUILD TOP PIPE
        top_pipe = make_pipe(pipe_body, pipe_cap, top_pipe_height)

        # BUILT BOTTOM PIPE BY FLAPPIN THE COMPLETED PIPE
        bottom_pipe = make_pipe(pipe_body, pipe_cap, bottom_pipe_height)
        bottom_pipe = pygame.transform.flip(bottom_pipe, False, True)

        #CREATE COLLISION RECTANGLES
        top_pipe_rect = top_pipe.get_bounding_rect().move(pipe_x, 0)
        bottom_pipe_rect = bottom_pipe.get_bounding_rect().move(pipe_x, gap_bottom)

        #CHECK PIPE COLLISION
        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            game_over = True

        # DRAW PIPES
        screen.blit(top_pipe, (pipe_x, 0))
        screen.blit(bottom_pipe, (pipe_x, gap_bottom))


    #GAME START SCREEN
    if not game_started and not game_over:
        start_text = game_over_font.render("FLAPPY PAPI BIRD", True, (255, 0, 0))
        instruction_text = restart_font.render("PRESS SPACE TO START", True, (255,0,0))

        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 200))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width()// 2 , 400))
    
    #GAME OVER SCREEN
    if game_over:
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = restart_font.render("PRESS 'R' TO RESTART", True, (255,0,0))

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(restart_text, (WIDTH // 2 -restart_text.get_width() // 2, 300 ))


    #DISPLAY SCORE
    score_text = score_font.render(str(score), True, (255, 0, 0))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 30))
    
    #UPDATE DISPLAY
    pygame.display.flip()



pygame.quit



