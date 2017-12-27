'''In the game, the player controls a spaceship via four buttons: 
two buttons that rotate the spaceship clockwise or counterclockwise 
(independent of its current velocity), a thrust button that accelerates 
the ship in its forward direction and a fire button that shoots missiles. 
Large asteroids spawn randomly on the screen with random velocities. 
The player's goal is to destroy these asteroids before they strike the player's ship.
Press the play button on the top left corner to play.
Controls: 
1. Press Arrow Keys to move the Spaceship.
2. Spacebar to destroy the Asteroids.'''



import simplegui
import math
import random
# globals for user interface
started = False
WIDTH = 800
HEIGHT = 600
FIRING_POSITION = [WIDTH // 2, HEIGHT]
FIRING_LINE_LENGTH = 60
temp_group = []
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
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

    

debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")


nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")


splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")


ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")


missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")


asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")


def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


class Ship:
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def shoot(self):        
        missile_pos = [0, 0]
        missile_vel = [0, 0]        
        forward = angle_to_vector(self.angle)
        missile_vel[0] = self.vel[0] + 6*forward[0]
        missile_vel[1] = self.vel[1] + 6*forward[1]
        missile_pos[0] = self.pos[0] + self.radius*forward[0]
        missile_pos[1] = self.pos[1] + self.radius*forward[1]
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    def draw(self,canvas):
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center,
                          self.image_size, self.pos, self.image_size, self.angle)
        else:
            
            canvas.draw_image(self.image, [self.image_center[0]*3,self.image_center[1]] ,
                          self.image_size, self.pos, self.image_size, self.angle)
    
       
    def update(self):
        forward = angle_to_vector(self.angle)
        self.angle += self.angle_vel
        if self.pos[0]*forward[0] + 45 >= WIDTH or self.pos[0]*forward[0] - 45 <= 0:
            self.pos[0] %= WIDTH
        if self.pos[1]*forward[1] + 45 >= HEIGHT or self.pos[1]*forward[1] - 45 <= 0:
    
    
            self.pos[1] %= HEIGHT                  
        if self.thrust:            
            self.vel[0] += .1 * forward[0]
            self.vel[1] += .1 * forward[1]             
        else:            
            self.vel[0] *= (.99)
            self.vel[1] *= (.99)   
            
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]


class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    
    
    
    def draw(self, canvas):
        if self.animated:
            center = explosion_info.get_center() 
            index = self.age  
            canvas.draw_image(explosion_image, [center[0] + 128*index, center[1]],
                          explosion_info.get_size(), self.pos, explosion_info.get_size())
        else:            
            canvas.draw_image(self.image, self.image_center ,
                          self.image_size, self.pos, self.image_size, self.angle)
        
        
        
        
        if self.animated:
            index = self.age 
        
        
    
    def update(self):
       
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        
        self.angle += self.angle_vel
        
        
        forward = angle_to_vector(self.angle)
        
        if self.pos[0]*forward[0] + 45 >= WIDTH or self.pos[0]*forward[0] - 45 <= 0:
            self.pos[0] %= WIDTH
        if self.pos[1]*forward[1] + 45 >= HEIGHT or self.pos[1]*forward[1] - 45 <= 0:   
            self.pos[1] %= HEIGHT  
        
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
        
        
        
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) <= self.radius + other_object.radius:
            return True
        return False
            
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        
def keydown(key): 
    global firing_angle_vel
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel -= .08
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrust = True
    elif simplegui.KEY_MAP["space"] == key:        
        my_ship.shoot()
        
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel += .08 
        
def keyup(key):
    global firing_angle_vel
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel += .08
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrust = False
        
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel -= .08         

        
def draw(canvas):
    
    global time, score, lives, started
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives: "+str(lives), [10,40], 26, "WHITE")
    canvas.draw_text("Score: "+str(score), [700,40], 26, "WHITE")
    
    if not started:
        reset()
        my_ship.draw(canvas)
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(),
                          [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        
    
    if started: 
      
        my_ship.draw(canvas)
        process_sprite_group(explosion_group, canvas)
        process_sprite_group(missile_group,canvas)    
        process_sprite_group(rock_group,canvas)
        if group_collide(rock_group,my_ship):
            lives -= 1    
        if group_group_collide(missile_group,rock_group):
            score += 1    
       
        my_ship.update()
        if lives == 0:
            started = False
   
      
def process_sprite_group(rock_group_temp,canvas):
    global rock_group
    for rock in rock_group_temp:
        rock.draw(canvas)
        rock.update()
    for rock in list(rock_group_temp):
        if rock.update():
            rock_group_temp.remove(rock)
               
    
        
   
def rock_spawner():
    global rock_group
    a_rock = Sprite([random.randrange(0,WIDTH), random.randrange(0,HEIGHT)], [random.random() * .6 - .3, random.random() * .6 - .3],
                     0, random.random() * .2 - .1, asteroid_image, asteroid_info, None) 
    
    if a_rock.pos[0] + a_rock.radius <= my_ship.pos[0] + my_ship.radius and a_rock.pos[1] + a_rock.radius <= my_ship.pos[1] + my_ship.radius:
        if a_rock.pos[0] - a_rock.radius <= my_ship.pos[0] - my_ship.radius and a_rock.pos[1] - a_rock.radius <= my_ship.pos[1] - my_ship.radius:
            rock_spawner()
    if len(rock_group) < 12:
        rock_group.add(a_rock)
        

        
        
        
        


frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)


my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

def group_collide(group, other_object):
    for member in list(group):
        if member.collide(other_object):
            
            
            
            explosion_member = Sprite(member.pos, member.vel,
                     0, 0, explosion_image, explosion_info, explosion_sound)
            group.remove(member)
            explosion_group.add(explosion_member)
            return True
        
def group_group_collide(group_object_1, group_object_2):
    count = 0
    for item in list(group_object_1):
        if group_collide(group_object_2, item):
            group_object_1.remove(item)
            
            
            count += 1
    return count 

def reset():
    global started, missile_group, my_ship, rock_group, lives, soundtrack, score
    if not started:
        lives = 3
        score = 0
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        missile_group = set([])
        rock_group = set([])
        soundtrack.rewind()
        soundtrack.play()
        

frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)


timer.start()
frame.start()