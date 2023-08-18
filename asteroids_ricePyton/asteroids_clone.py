# program template for Spaceship
# Provided via An Introduction to Interactive Programming in Python (Part 2) (Coursera, Rice University)
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from math import cos, pi, sin, sqrt
from random import random, randrange

# Hide the simplegui control panel area
simplegui.Frame._hide_controlpanel = True

# globals for user interface (provided as part of starting template)
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

# New constants I defined
FONT_SIZE = 30
MARGIN = 20
GAP = 300  # Space between ship and any spawning rocks

# New global variables I defined
rock_group = set()
missile_group = set()
explosion_group = set()


class ImageInfo:
    # Class provided as part of starting template)
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float("inf")
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop (provided)

debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui._LocalImage("images/debris2_blue.png")

nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui._LocalImage("images/nebula_blue.f2014.png")

splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui._LocalImage("images/splash.png")

ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui._LocalImage("images/double_ship.png")

missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui._LocalImage("images/shot2.png")

asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui._LocalImage("images/asteroid_blue.png")

explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui._LocalImage("images/explosion_alpha.png")

# These lines provided but I replaced the sound files
# Soundtrack created by Speedenza and obtained from freesound.org
# Creation Commons Attribution noncommercial license http://creativecommons.org/licenses/by-nc/3.0/
soundtrack = simplegui._LocalSound("sounds/soundtrack.ogg")
missile_sound = simplegui._LocalSound("sounds/missile.ogg")
missile_sound.set_volume(0.5)
# Thrust sound created by primeval_polypod and obtained from freesound.org
# Creative Commons Attribution license https://creativecommons.org/licenses/by/3.0/
ship_thrust_sound = simplegui._LocalSound("sounds/thrust.ogg")
# Explosion sound created by LiamG_SFX and obtained from freesound.org
# Creation Commons Attribution noncommercial license http://creativecommons.org/licenses/by-nc/3.0/
explosion_sound = simplegui._LocalSound("sounds/explosion.ogg")


def angle_to_vector(ang):
    # Provided as part of starting template
    return [cos(ang), sin(ang)]


def dist(p, q):
    # Provided as part of starting template
    return sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        # init provided as part of starting template
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle  # In radians, not degrees
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self, canvas):
        # If thrust is on use thrust image
        if self.thrust:
            # Need to specify the center of the thrust image on the ship_image tilesheet
            center = (self.image_center[0] + self.image_size[0], self.image_center[1])
            # draw_image(image, center_source, width_height_source, center_dest, width_height_dest, rotation=0)
            canvas.draw_image(
                self.image,
                center,
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )
        else:
            # Center of non-thrust image and self.image_center are the same
            canvas.draw_image(
                self.image,
                self.image_center,
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )

    def update(self):
        # Update ship position, ensuring ship wraps screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # Update angular position
        self.angle += self.angle_vel
        # Have the ship automatically slow down over time (numbers should be less than, but close to, 1)
        # This also puts an upper limit on ship speed once this decrease is equal to the ship thrust velocity
        self.vel[0] *= 0.98
        self.vel[1] *= 0.98
        # Get unit vector pointing indicating direction the ship is facing
        forward = angle_to_vector(self.angle)
        # Accelerate forward if self.thrust
        if self.thrust:
            # Multipler is arbitrary, larger multipler means more acceleration
            self.vel[0] += forward[0] * 0.25
            self.vel[1] += forward[1] * 0.25

    def set_angle_vel(self, key, key_state):
        # Set angular velocity to -0.1 if left is down and set back to zero if right is released
        if (
            (key == "left" and key_state == "down")
            or (key == "right" and key_state == "up")
            and self.angle_vel != -0.1
        ):
            self.angle_vel -= 0.1
        # Set angular velocity to 0.1 if right is down and set back to zero if left is released
        elif (
            (key == "right" and key_state == "down")
            or (key == "left" and key_state == "up")
            and self.angle_vel != 0.1
        ):
            self.angle_vel += 0.1

    def set_thrust(self, thrust):
        self.thrust = thrust
        if self.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()

    def shoot(self):
        # Set the starting position of the missile to the tip of the ship
        forward = angle_to_vector(self.angle)
        pos = [
            self.pos[0] + (self.image_size[0] / 2) * forward[0],
            self.pos[1] + (self.image_size[1] / 2) * forward[1],
        ]
        # Set the velocity of the missile as the velocity of the ship plus some forward missile velocity
        vel = [self.vel[0] + 5 * forward[0], self.vel[1] + 5 * forward[1]]
        ang = 0
        ang_vel = 0
        missile_group.add(
            Sprite(pos, vel, ang, ang_vel, missile_image, missile_info, missile_sound)
        )

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        # init provided as part of starting template
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        # Measure of how long sprite 'lives' before automatic removal
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if self.animated == False:
            canvas.draw_image(
                self.image,
                self.image_center,
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )
        else:
            pos_x = self.image_center[0] + self.age * self.image_size[0]
            pos_y = self.image_center[1]
            canvas.draw_image(
                self.image,
                [pos_x, pos_y],
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        return self.age >= self.lifespan

    def collide(self, other_object):
        return (
            dist(self.pos, other_object.get_position())
            <= self.radius + other_object.get_radius()
        )

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius


def draw(canvas):
    global time, lives, score, started

    # animate background (this part of the code was provided as part of starting template)
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(
        nebula_image,
        nebula_info.get_center(),
        nebula_info.get_size(),
        [WIDTH / 2, HEIGHT / 2],
        [WIDTH, HEIGHT],
    )
    canvas.draw_image(
        debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT)
    )
    canvas.draw_image(
        debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT)
    )

    # Draw and update ship
    ship.draw(canvas)
    ship.update()

    # Draw lives and score
    pos_lives = [MARGIN, MARGIN + FONT_SIZE]
    canvas.draw_text(f"Lives: {lives}", pos_lives, FONT_SIZE, "White")
    # Length of each character approx 2/3 of font size, 'score' has 5 characters
    pos_score = [WIDTH - MARGIN - 2 / 3 * FONT_SIZE * 5, MARGIN + FONT_SIZE]
    canvas.draw_text(f"Score: {score}", pos_score, FONT_SIZE, "White")

    if started:
        # Draw and update sprites
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)

        # Check for collisions
        if group_collide(rock_group, ship):
            lives -= 1
        if lives == 0:
            started = False
            reset_game()
        score += group_group_collide(missile_group, rock_group)
    else:
        canvas.draw_image(
            splash_image,
            splash_info.get_center(),
            splash_info.get_size(),
            (WIDTH / 2, HEIGHT / 2),
            splash_info.get_size(),
        )


def rock_spawner():
    # Timer handler that spawns a rock
    if started:
        if len(rock_group) == 12:  # Maximum number of rocks on screen at a time
            return
        else:
            pos = [randrange(WIDTH), randrange(HEIGHT)]
            # Make sure new rocks spawn a reasonable distance from the ship
            while dist(pos, ship.get_position()) <= GAP:
                pos = [randrange(WIDTH), randrange(HEIGHT)]
            # Numbers here are fairly arbitrary, they give velocities that seem reasonable to me
            # Velocities components can range from -6 to 6
            vel = [6 * (random() - 1), 6 * (random() - 1)]
            ang = random() * 2 * pi  # Number between 0 and 2pi for initial angle
            ang_vel = random() / 5 - 0.1  # Angular velocity can range from -0.1 to 0.1
            rock_group.add(
                Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info)
            )


def process_sprite_group(group, canvas):
    new_set = set(group)
    for obj in new_set:
        # Delete sprite if it's reached its lifespan
        if obj.update():
            group.discard(obj)
        obj.draw(canvas)


def group_collide(group, other_object):
    new_set = set(group)
    for obj in group:
        if obj.collide(other_object):
            group.discard(obj)
            explosion_group.add(
                Sprite(
                    obj.get_position(),
                    [0, 0],
                    0,
                    0,
                    explosion_image,
                    explosion_info,
                    explosion_sound,
                )
            )
            return True


def group_group_collide(group1, group2):
    # Track number of missile-rock collision to add to score
    num_collisions = 0
    for obj in set(group1):
        if group_collide(group2, obj):
            num_collisions += 1
    return num_collisions


def reset_game():
    global rock_group, missile_group, explosion_group, lives, score, ship
    rock_group = set()
    missile_group = set()
    explosion_group = set()
    lives = 3
    score = 0
    ship = Ship(ship.get_position(), [0, 0], 0, ship_image, ship_info)
    soundtrack.rewind()
    ship_thrust_sound.rewind()


def key_down(key):
    if started:
        if key == simplegui.KEY_MAP["left"]:
            ship.set_angle_vel("left", "down")
        elif key == simplegui.KEY_MAP["right"]:
            ship.set_angle_vel("right", "down")
        elif key == simplegui.KEY_MAP["up"]:
            ship.set_thrust(True)
        elif key == simplegui.KEY_MAP["space"]:
            ship.shoot()


def key_up(key):
    if started:
        if key == simplegui.KEY_MAP["left"]:
            ship.set_angle_vel("left", "up")
        elif key == simplegui.KEY_MAP["right"]:
            ship.set_angle_vel("right", "up")
        elif key == simplegui.KEY_MAP["up"]:
            ship.set_thrust(False)


def mouse_click(pos):
    global started
    # Start the game if user clicks in play area
    if pos[0] < WIDTH and pos[1] < HEIGHT and not started:
        started = True
        soundtrack.rewind()
        soundtrack.play()


# initialize frame (provided as part of starting template)
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship (provided as part of starting template)
ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers (provided as part of starting template except for mouseclick_handler)
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_click)

# Set timers to automatically stop when frame is closed
simplegui.Frame._keep_timers = False

# Provided as part of starting template
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling (provided as part of starting template)
timer.start()
frame.start()


# To do
# 1. Find sounds I can use

# 260 lines of code (exlcuding comments and blank lines)
# 95 lines of code provided (most of it the art/sound assets, ImageInfo class, and Ship/Sprite init)
# 164 lines of code my own
