import pygame, sys, random
from pygame import mixer
import math

# ==========
# Change the value of speed in a different branch to make a merge conflict.
speed = 10
# ==========

def background_music():
    # Depending on the menu you're in, just music is on.
    global song, music_check, volume

    if song == 1:
        mixer.music.load("resources/sounds/anomalocaris.mp3")
        mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    # Main Menu Theme
    elif song == 2:
        mixer.music.load("resources/sounds/weevil.mp3")
        mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

        # Loser's Theme
    else:
        mixer.music.load("resources/sounds/snail.mp3")
        mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, game_level, speed, current_color, song, newgame

    # Base Ball Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    if start:
        ball_speed_x = 0  # Randomize initial horizontal direction
        ball_speed_y = 5  # start by going down
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if game_level == -1:
            game_level += 1
            paddle_hit()  # Randomize initial horizontal direction

        # Ball speed increase every paddle hit
        game_level += 1
        if game_level == 5:
            speed += 1
            ball_speed_y = speed
            game_level = 0

        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            # TODO Task 2: Fix score to increase by 1
            global high_score
            score += 1   # Increase player score
            ball_speed_y *= -1  # Reverse ball's vertical direction
            paddle_hit()

            #New paddle color
            current_color = random.choice(paddle_colors)

            # Update high score if current score is higher
            if score > high_score:
                high_score = score

            # Add milestones popups
            if score %5==0:
                milestones_popups.append({
                    "text": random.choice(milestones_messages),
                    "x": player.x,
                    "y": player.y-30,
                    "start_time": pygame.time.get_ticks(),
                })

            # TODO Task 6: Add sound effects HERE
            # Sound effect on hit. BOINK!!!
            sound = random.choice(range(1,3))
            pygame.mixer.Channel(1).set_volume(0.2)

            if sound == 1:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("resources/sounds/boink1.mp3"))
            elif sound == 2:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("resources/sounds/boink2.mp3"))
            else:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("resources/sounds/boink3.mp3"))

    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        restart() # Reset the game

def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score, newgame, speed, song
    ball.center = (int(screen_width / 2), int(screen_height / 2))  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    speed = 5
    score = 0  # Reset player score
    newgame = True
    song = 2
    background_music()
    mainmenu()

def paddle_hit():
    global ball_speed_x, ball_speed_y, score, start, game_level, player, ball, speed, ballphys

    if not ballphys:
        distance = 2 * (ball.centerx - player.centerx) / player.width
        ball_speed_x = distance * speed

    # ==== More realistic vector based engine, kinda boring to play though ====
    elif ballphys:
        distance = ball.center[0] - player.center[0], ball.center[1] - player.center[1]
        magnitude = math.sqrt(distance[0]**2 + distance[1]**2)

        direction = distance[0] / magnitude, distance[1] / magnitude
        ball_speed = speed * direction[0], speed * direction[1]
        ball_speed_y = ball_speed[1]
        ball_speed_x = ball_speed[0]

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

# ==== Main game loop ====
def gameplay():
    global player_speed, newgame, start, song
    while True:
        # Event handling
        # Task 4: Add your name
        # Why is this here? I mean, sure, it's added? but what
        name = "Angel Perez"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_speed -= 6  # Move paddle left
                if event.key == pygame.K_RIGHT:
                    player_speed += 6  # Move paddle right
                if event.key == pygame.K_SPACE and newgame:
                    start = True  # Start the ball movement
                    newgame = False # Indicates whether a new game can be begun.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_speed += 6  # Stop moving left
                if event.key == pygame.K_RIGHT:
                    player_speed -= 6  # Stop moving right

        # ==== Game Logic ====
        ball_movement()
        player_movement()

        # ==== Visuals ====

        light_grey = pygame.Color('grey83')
        screen = pygame.display.get_surface()
        screen.fill(bg_color)
        pygame.draw.rect(screen, current_color, player)  # Draw player paddle

        pygame.draw.ellipse(screen, light_grey, ball)  # Draw ball
        player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
        screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen

        # Display high score below current score
        high_score_text = basic_font.render(f'High Score: {high_score}', False, light_grey)
        screen.blit(high_score_text, (screen_width / 2 - 70, 50))

        # Draw milestone popups
        for popup in milestones_popups[:]:
            popup_text = basic_font.render(popup['text'],True, pygame.Color('yellow'))
            screen.blit(popup_text, (popup['x'],popup['y']))
            popup['y'] -=1 #Make it float upward
            if pygame.time.get_ticks() - popup['start_time'] > 1500: #Remove after 1.5s
                milestones_popups.remove(popup)

        # Update display
        pygame.display.flip()
        clock.tick(60)  # Maintain 60 frames per second

# ======= WIP MAIN MENU =======

def settings():
    global newgame, start, music_check, song, screen, choice2, volume, ballphys
    music_check = False  # Reset music flag
    while True:
        screen = pygame.display.get_surface()
        screen.blit(menu_bg, (0, 0))

        if choice2 < 1:
            choice2 = 1
        elif choice2 > 2:
            choice2 = 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    choice2 -= 1  # Move up an option
                elif event.key == pygame.K_DOWN:
                    choice2 += 1  # Move down an option

                # Press Button
                if event.key == pygame.K_RETURN and choice2 == 1:
                    mainmenu()
                elif event.key == pygame.K_RETURN and choice2 == 2 and not ballphys:
                    ballphys = True
                elif event.key == pygame.K_RETURN and choice2 == 2 and ballphys:
                    ballphys = False

        settings2_rect = settings2_surface.get_rect(center=settings_box.center)
        settings3_rect = settings3_surface.get_rect(center=settings3_box.center)

        if choice2 == 1:
            pygame.draw.rect(screen, "white", settings_outline)
        elif choice2 == 2:
            pygame.draw.rect(screen, "white", settings3_outline)

        # Square
        pygame.draw.rect(screen, box_color, settings_box)
        screen.blit(settings2_surface, settings2_rect)

        pygame.draw.rect(screen, box_color, settings3_box)
        screen.blit(settings3_surface, settings3_rect)

        # Update display
        pygame.display.flip()
        clock.tick(60)

def mainmenu():
    global newgame, start, music_check, song, screen, choice1, speed, score
    music_check = False  # Reset music flag

    while True:
        screen = pygame.display.get_surface()
        screen.blit(menu_bg, (0, 0))

        if choice1 < 1:
            choice1 = 1
        elif choice1 > 3:
            choice1 = 3

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    choice1 -= 1 # Move up an option
                elif event.key == pygame.K_DOWN:
                    choice1 += 1 # Move down an option

                # Press Button
                if event.key == pygame.K_RETURN and choice1 == 1:
                    song = 1
                    background_music()
                    gameplay()
                elif event.key == pygame.K_RETURN and choice1 == 2:
                    song = 2
                    settings()
                elif event.key == pygame.K_RETURN and choice1 == 3:
                    pygame.quit()
                    sys.exit()


        # Main Menu Outlines
        if choice1 == 1:
            pygame.draw.rect(screen, "white", start_outline)
        elif choice1 == 2:
            pygame.draw.rect(screen, "white", settings_outline)
        elif choice1 == 3:
            pygame.draw.rect(screen, "white", quit_outline)

        # Main Menu Blank Squares
        pygame.draw.rect(screen, box_color, start_box)
        pygame.draw.rect(screen, box_color, settings_box)
        pygame.draw.rect(screen, box_color, quit_box)

        # Main Menu Text
        start_rect = start_surface.get_rect(center=start_box.center)
        settings_rect = settings_surface.get_rect(center=settings_box.center)
        quit_rect = quit_surface.get_rect(center=quit_box.center)

        screen.blit(start_surface, start_rect)
        screen.blit(settings_surface, settings_rect)
        screen.blit(quit_surface, quit_rect)

        # Update display
        pygame.display.flip()
        clock.tick(60)

# General setup
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
mixer.init()
pygame.init()
clock = pygame.time.Clock()

# ==== Main Window setup ====
width, height = (400, 500)
flags = pygame.SCALED
flags |= pygame.RESIZABLE  # optional

screen_width = 400  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((width, height), flags)
pygame.display.set_caption('Pong')  # Set window title

# Colors
menu_bg = pygame.image.load("resources/textures/forest.png")
box_color = pygame.Color("black")
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 15, 20, 20)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 200
player = pygame.Rect(screen_width/2 - 45, screen_height - 30, player_width, player_height)  # Player paddle

# Main Menu Rectangles
box_width = 350
box_height = height / 5
outline_thickness = 4  # Thickness of the outline

start_box = pygame.Rect(25, 75, box_width, box_height)
settings_box = pygame.Rect(25, 200, box_width, box_height)
quit_box = pygame.Rect(25, 325, box_width, box_height)
settings3_box = pygame.Rect(25, 325, box_width, box_height)

start_outline = pygame.Rect(start_box.x - outline_thickness, start_box.y - outline_thickness, start_box.width + outline_thickness * 2, start_box.height + outline_thickness * 2)
settings_outline = pygame.Rect(settings_box.x - outline_thickness, settings_box.y - outline_thickness, start_box.width + outline_thickness * 2, start_box.height + outline_thickness * 2)
quit_outline = pygame.Rect(quit_box.x - outline_thickness, quit_box.y - outline_thickness, start_box.width + outline_thickness * 2, start_box.height + outline_thickness * 2)
settings3_outline = pygame.Rect(settings3_box.x - outline_thickness, settings3_box.y - outline_thickness, start_box.width + outline_thickness * 2, start_box.height + outline_thickness * 2)

# Paddle colors
paddle_colors= [pygame.Color('red'), pygame.Color('green'), pygame.Color('yellow'), pygame.Color('blue')]
current_color = paddle_colors[0]
# ==== Game Variables ====
ball_speed_x = 0.0
ball_speed_y = 0.0
player_speed = 0
game_level = -1 # Resetting value to speed up the ball. Might be redundant.
newgame = True # Indicates whether a new game can be begun.
choice1 = 1
choice2 = 1
volume = 0.4
ballphys = False

song = 2
music_check = False

# Score Text setup
score = 0
high_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font
small_font = pygame.font.Font('freesansbold.ttf', 12)  # Font


start_surface = basic_font.render("Start", True, (255, 255, 255))
settings_surface = basic_font.render("Settings", True, (255, 255, 255))
quit_surface = basic_font.render("Quit", True, (255, 255, 255))

settings2_surface = small_font.render(f"NO SETTINGS!!!! Press Enter To Exit", True, (255, 255, 255))
settings3_surface = small_font.render(f"jk, click on this for realistic ball physics", True, (255, 255, 255))


#Milestones popups
milestones_popups= []
milestones_messages= ["Good job!", "Amazing!", "Nice!", "Keep it up!", "Faster!", "You've got it!"]


start = False  # Indicates if the game has started

background_music()
mainmenu()