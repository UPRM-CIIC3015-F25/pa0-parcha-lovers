import pygame, sys, random
from pygame import mixer
import math

# ==========
# TODO Task 5 Create a Merge Conflict
# Change the value of speed in a different branch to make a merge conflict.
speed = 5
# ==========

def background_music():
    # Depending on the menu you're in, just music is on.
    global song, music_check


    mixer.music.load("resources/sounds/anomalocaris.mp3")
    mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    # Main Menu Theme
    if song == 2:
        mixer.music.load("resources/sounds/weevil.mp3")
        mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        # Loser's Theme
        if song == 3:
            mixer.music.load("resources/sounds/snail.mp3")
            mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, game_level, speed, current_color

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
           #Add milestones popups
            if score %5==0:
                milestones_popups.append({
                    "text": random.choice(milestones_messages),
                    "x": player.x,
                    "y": player.y-30,
                    "start_time": pygame.time.get_ticks(),
                })

            # TODO Task 6: Add sound effects HERE
            # Sound effect on hit. BOINK!!!
            sound = random.choice(range(1,4))
            pygame.mixer.Channel(1).set_volume(0.5)

            if sound == 1:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("resources/sounds/boink1.mp3"))
            if sound == 2:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("resources/sounds/boink2.mp3"))
            if sound == 3:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("resources/sounds/boink3.mp3"))

    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        restart()  # Reset the game

def paddle_hit():
    global ball_speed_x, ball_speed_y, score, start, game_level, player, ball, speed

    distance = 2 * (ball.centerx - player.centerx) / player.width
    ball_speed_x = distance * speed

    # ==== More realistic vector based engine, kinda boring to play though ====
    # distance = ball.center[0] - player.center[0], ball.center[1] - player.center[1]
    # magnitude = math.sqrt(distance[0]**2 + distance[1]**2)

    # direction = distance[0] / magnitude, distance[1] / magnitude
    # ball_speed = speed * direction[0], speed * direction[1]
    # ball_speed_y = ball_speed[1]
    # ball_speed_x = ball_speed[0]

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

def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score, newgame, speed
    ball.center = (int(screen_width / 2), int(screen_height / 2))  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    speed = 5
    score = 0  # Reset player score
    newgame = True

# ==== Main game loop ====
def gameplay():
    global player_speed, newgame, start, song
    while True:
        # Event handling
        # Task 4: Add your name
        # Why is this here? I mean, sure, it's added? but what
        name = "Angel and Yaneli?"

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

        # TODO Task 3: Change the Ball Color
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

def clamp(n, min_value, max_value):
    return max(min_value, min(n, max_value))

def shop():
    print("temp")

def cosmetics():
    print("temp")

def mainmenu():
    global newgame, start, music_check, song
    music_check = False  # Reset music flag

    while True:
        screen = pygame.display.get_surface()
        screen.fill("black")

        option = clamp(1, 1, 3)
        choice = [[1, 2, 3], [1, 2]]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    choice[0]# Move up an option
                if event.key == pygame.K_DOWN:
                    choice[0] += 1 # Move down an option

                # Press Button
                if event.key == pygame.K_RETURN and newgame and choice[0] == 1 and choice[1] == 1:
                    song = 1
                    background_music()
                    gameplay()
                if event.key == pygame.K_RETURN and newgame and choice[0] == 2 and choice[1] == 1:
                    song = 2
                    shop()
                if event.key == pygame.K_RETURN and newgame and choice[0] == 3 and choice[1] == 1:
                    song = 2
                    cosmetics()
                if event.key == pygame.K_RETURN and newgame and choice[0] == 4 and choice[1] == 1:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    choice[0] += 1  # Stop moving up
                if event.key == pygame.K_DOWN:
                    choice[0] -= 1  # Stop moving down
        # Update display
        pygame.display.flip()
        clock.tick(60)

def losing_screen():
    print("temp")

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
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 15, 20, 20)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 200
player = pygame.Rect(screen_width/2 - 45, screen_height - 30, player_width, player_height)  # Player paddle

# Paddle colors
paddle_colors= [pygame.Color('red'), pygame.Color('green'), pygame.Color('yellow'), pygame.Color('blue')]
current_color = paddle_colors[0]
# ==== Game Variables ====
ball_speed_x = 0.0
ball_speed_y = 0.0
player_speed = 0
game_level = -1 # Resetting value to speed up the ball. Might be redundant.
newgame = True # Indicates whether a new game can be begun.

song = 1
music_check = False

# Score Text setup
score = 0
high_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score

#Milestones popups
milestones_popups= []
milestones_messages= ["Good job!", "Amazing!", "Nice!", "Keep it up!", "Faster!", "You've got it!"]


start = False  # Indicates if the game has started

gameplay()