import pygame, sys, random
from pygame import mixer

def background_music():
    # Depending on the menu you're in, just music is on.
    song = 1

    # In-Game Theme
    if song == 1:
        mixer.music.load("resources/sounds/anomalocaris.mp3")
        mixer.music.set_volume(0.2)

    # Main Menu Theme
    if song == 2:
        mixer.music.load("resources/sounds/weevil.mp3")
        mixer.music.set_volume(0.4)

    # Loser's Theme
    if song == 3:
        mixer.music.load("resources/sounds/snail.mp3")
        mixer.music.set_volume(0.3)

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, game_level

    # Base Ball Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # ==========
    # TODO Task 5 Create a Merge Conflict
    # Change the value of speed in a different branch to make a merge conflict.
    speed = 5
    # ==========

    # Start the ball movement when the game begins
    if start:
        ball_speed_x = 0  # Randomize initial horizontal direction
        ball_speed_y = 5  # start by going down
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if game_level == -1:
            game_level += 1
            ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction

        # Ball speed increase every paddle hit
        game_level += 1
        if game_level == 1:
            speed += 1
            ball_speed_x = speed
            ball_speed_y = speed
            game_level = 0

        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            # TODO Task 2: Fix score to increase by 1
            score = 1  # Increase player score
            ball_speed_y *= -1  # Reverse ball's vertical direction
            ball_speed_x = speed * random.choice(range(-2, 2)) # Randomize the ball speed meaning change in direction. DO NOT INCREASE PAST 3/-3.

            # TODO Task 6: Add sound effects HERE
            # Sound effect on hit. BOINK!!!
            sound = random.choice(range(1,3))
            pygame.mixer.Channel(1).set_volume(0.1)

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
    if ball.left <= 0 or ball.right >= (screen_width):
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        restart()  # Reset the game

# WIP
def paddle_hit():
    global ball_speed_x, ball_speed_y, score, start, game_level

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
    global ball_speed_x, ball_speed_y, score, newgame
    ball.center = (int(screen_width / 2), int(screen_height / 2))  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    score = 0  # Reset player score
    newgame = True

# ==== Main game loop ====
def gameplay():
    global player_speed, newgame, start
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
        pygame.draw.rect(screen, light_grey, player)  # Draw player paddle

        # TODO Task 3: Change the Ball Color
        pygame.draw.ellipse(screen, light_grey, ball)  # Draw ball
        player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
        screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen

        # Update display
        pygame.display.flip()
        clock.tick(60)  # Maintain 60 frames per second

# WIP
def mainmenu():
    while True:

        screen = pygame.display.get_surface()
        screen.fill("black")

        # Update display
        pygame.display.flip()
        clock.tick(60)

# General setup
pygame.mixer.pre_init() # Starting the mixer
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# ==== Main Window setup ====
width, height = (500, 500)
flags = pygame.SCALED
flags |= pygame.RESIZABLE  # optional

screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((width, height), flags)
pygame.display.set_caption('Pong')  # Set window title

# Colors
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 15, 30, 30)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 100
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, player_width, player_height)  # Player paddle


# ==== Game Variables ====
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
game_level = -1 # Resetting value to speed up the ball. Might be redundant.
newgame = True # Indicates whether a new game can be begun.

# Score Text setup
score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score

start = False  # Indicates if the game has started

gameplay()