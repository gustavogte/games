from globals import *
from pygame.locals import *

# taking values from globals
temp_time_interval = time_interval
temp_default_y_chg_asteroid = default_y_chg_asteroid

# PyGame initialized
pygame.init()

# Set FPS
FPS = 60

# Set clock for refresh rate
clock = pygame.time.Clock()

# Font and size
font = pygame.font.Font(font_path, 32)

# start screen text
blink_start = 0
start_text = font.render("Press S to start the game", True, WHITE)
start_text_Rect = start_text.get_rect()
start_text_Rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 60)

# gameover font
gameoverfont = pygame.font.Font(font_path, 60)

# gameover text
gameover_text = gameoverfont.render("GAME OVER", True, RED)
gameover_text_Rect = gameover_text.get_rect()
gameover_text_Rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 60)

# final score text
final_score = font.render(f"FINAL SCORE: {score}", True, AQUA)
final_score_Rect = final_score.get_rect()
final_score_Rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

# gameover under text
blink = 0
gameover_undertext = font.render("Press R to restart the game", True, WHITE)
gameover_undertext_Rect = gameover_undertext.get_rect()
gameover_undertext_Rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 60)

# For performance
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

# Set window name
pygame.display.set_caption("Space Blaster")

# Load logo image and set icon
icon = pygame.image.load(icon_img)
pygame.display.set_icon(icon)

# Create screen
flags = DOUBLEBUF
screen = pygame.display.set_mode(WINDOW_DIMENSIONS, flags, 16)

# Background image
background = pygame.image.load(background_img)

# Overlay screen
transparent_screen = pygame.Surface(WINDOW_DIMENSIONS)
transparent_screen.set_colorkey(BLACK)
transparent_screen.set_alpha(255)
pygame.draw.rect(transparent_screen, BLACK, transparent_screen.get_rect(), 10)

# Blaster declaration
isAlive = True
spaceship = Spaceship(
    spaceship_img, WINDOW_WIDTH / 2, WINDOW_HEIGHT - WINDOW_HEIGHT / 8
)

# Bullets array
lasers = []

# Laser sound
lasersound = pygame.mixer.Sound(laser_sound)

# Last fired time
last_fired = []

# Display available bullets
show_bullets = bullet_limit
available_bullets = [
    DisplayBullet(available_bullet_img, WINDOW_WIDTH - 32 - 32 * i, 96)
    for i in range(bullet_limit, 0, -1)
]

# Universal asteroid available spawns
asteroid_spawn_x = uni_asteroid_spawn_x[
    random.randint(0, len(uni_asteroid_spawn_x) - 1)
][:]

# Asteroids list
asteroids = []

# last time when an asteroid was generated
last_time = time.time()

# The blast images
blasts = []

# Blast sound
blastsound = pygame.mixer.Sound(blast_sound)


# Asteroid Generator with time parameter
def asteroid_generator(time_interval, y_speed):
    global last_time, asteroid_spawn_x
    current_time = time.time()
    if current_time - last_time > time_interval:
        x = random.choice(asteroid_spawn_x)
        del asteroid_spawn_x[asteroid_spawn_x.index(x)]

        # Change to new x-spawn sequence
        if not len(asteroid_spawn_x):
            asteroid_spawn_x = uni_asteroid_spawn_x[
                random.randint(0, len(uni_asteroid_spawn_x) - 1)
            ][:]

        y = uni_asteroid_spawn_y
        asteroids.append(Asteroid(asteroid_imgs[random.randint(0, 3)], x, y, y_speed))
        last_time = current_time


# Draw background
def background_show():
    screen.blit(background, (0, 0))


# Draw spaceship
def spaceship_show():
    global spaceship
    collided, asteroid_num = CollisionDetect(spaceship, asteroids)
    if collided:
        # Add blast object img
        blasts.append(
            Blast(
                blast_imgs[random.randint(0, 2)],
                asteroids[asteroid_num].x,
                asteroids[asteroid_num].y,
            )
        )
        # Play blast sound
        blastsound.play()

        # Add blast object img
        blasts.append(Blast(blast_imgs[random.randint(0, 2)], spaceship.x, spaceship.y))
        # Play blast sound
        blastsound.play()

        del asteroids[asteroid_num]
        del spaceship
        return False
    spaceship.changeXY(WINDOW_DIMENSIONS=WINDOW_DIMENSIONS)
    screen.blit(*spaceship.load())
    return True


# Draw bullets/lasers
def bullets_show():
    global lasers, show_bullets, last_fired
    for num, laser in enumerate(lasers):
        collided, asteroid_num = CollisionDetect(laser, asteroids)
        if collided:
            # Add blast object img
            blasts.append(
                Blast(
                    blast_imgs[random.randint(0, 2)],
                    asteroids[asteroid_num].x,
                    asteroids[asteroid_num].y,
                )
            )
            # Play blast sound
            blastsound.play()
            # deleting residue
            del asteroids[asteroid_num]
            del lasers[num]
            continue

        if laser.changeXY(WINDOW_DIMENSIONS=WINDOW_DIMENSIONS):
            screen.blit(*laser.load())
        else:
            del lasers[num]

    if len(last_fired) and time.time() - last_fired[0] > bullet_restore_time:
        show_bullets += 1
        last_fired = last_fired[1:]

    for bullet in available_bullets[:show_bullets]:
        screen.blit(*bullet.load())
    return True


# Draw asteroids
def asteroid_show():
    global asteroids
    for num, asteroid in enumerate(asteroids):
        if asteroid.changeXY(WINDOW_DIMENSIONS=WINDOW_DIMENSIONS):
            screen.blit(*asteroid.load())
        else:
            del asteroids[num]


def blast_show():
    global blasts
    for num, blast in enumerate(blasts):
        try:
            screen.blit(*blast.load())
        except:
            del blasts[num]


# Score text
score_text = font.render(f"SCORE: {score}", True, WHITE)
score_text_Rect = score_text.get_rect()
score_text_Rect.topleft = (40, 40)

last_chg = -1


def resetGame():
    global time_interval, default_y_chg_asteroid, last_fired, show_bullets, isAlive, spaceship, asteroids, lasers, score, start_time, last_chg, temp_default_y_chg_asteroid, temp_time_interval

    # Reset score
    score = 0

    # New game start time
    start_time = time.time()

    # Reference for increasing score
    last_increment = start_time

    # clear fire timings
    last_fired = []

    # taking values from globals
    temp_time_interval = time_interval
    temp_default_y_chg_asteroid = default_y_chg_asteroid

    # show bullets reset
    show_bullets = bullet_limit

    # Reinitializing
    isAlive = True
    spaceship = Spaceship(
        spaceship_img, WINDOW_WIDTH / 2, WINDOW_HEIGHT - WINDOW_HEIGHT / 8
    )
    start_time = time.time()
    asteroids = []
    lasers = []


# has the game started ?? (First run initiated?)
started = False


def gameLoop():
    global start_time, last_increment, started, blink_start, temp_time_interval, temp_default_y_chg_asteroid, isAlive, show_bullets, last_increment, score, blink, time_interval, default_y_chg_asteroid, last_chg
    clock.tick(FPS)
    if not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_s]:
                    started = True

                    # record time at which the game starts
                    start_time = time.time()

                    # Reference for increasing score
                    last_increment = start_time

        screen.fill((0, 0, 0))
        background_show()

        if blink_start % FPS > FPS // 2:
            screen.blit(start_text, start_text_Rect)

        blink_start += 1

        pygame.display.update()
        return True
    if not isAlive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_r]:
                    resetGame()
                    print(time_interval)
                    print(default_y_chg_asteroid)

        screen.fill((0, 0, 0))
        background_show()
        asteroid_generator(time_interval, default_y_chg_asteroid)
        asteroid_show()
        blast_show()

        # final score text
        final_score = font.render(f"FINAL SCORE: {score}", True, AQUA)
        final_score_Rect = final_score.get_rect()
        final_score_Rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

        screen.blit(gameover_text, gameover_text_Rect)
        screen.blit(final_score, final_score_Rect)

        if blink % FPS > FPS // 2:
            screen.blit(gameover_undertext, gameover_undertext_Rect)
        blink += 1

        pygame.display.update()
        return True

    if time.time() - start_time > 2 and time.time() - last_increment > 3.5:
        score += 10
        last_increment = time.time()

    if score % score_step == 0 and score // score_step != last_chg:
        temp_time_interval -= time_increment
        temp_default_y_chg_asteroid += speed_increment
        print("Change in Difficulty", temp_time_interval, temp_default_y_chg_asteroid)
        last_chg = score // score_step

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                spaceship.x_chg = -spaceship.default_x

            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                spaceship.x_chg = spaceship.default_x

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_a] and not (
                pygame.key.get_pressed()[79] or pygame.key.get_pressed()[7]
            ):
                spaceship.x_chg = 0

            if event.key in [pygame.K_RIGHT, pygame.K_d] and not (
                pygame.key.get_pressed()[80] or pygame.key.get_pressed()[4]
            ):
                spaceship.x_chg = 0

            if event.key == pygame.K_SPACE:
                if show_bullets:
                    show_bullets -= 1
                    last_fired.append(time.time())
                    lasers.append(Laser(laser_img, spaceship.x, spaceship.y))
                    lasersound.play()

    screen.fill((0, 0, 0))

    background_show()

    # Score counter
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    score_text_Rect = score_text.get_rect()
    score_text_Rect.topleft = (40, 40)

    screen.blit(score_text, score_text_Rect)

    if time.time() - start_time > 2:
        asteroid_generator(temp_time_interval, temp_default_y_chg_asteroid)

    asteroid_show()
    bullets_show()

    if not (spaceship_show()):
        isAlive = False

    blast_show()

    # Update all changes to the display
    pygame.display.update()

    return True


while 1:
    if not gameLoop():
        break

print("over")
