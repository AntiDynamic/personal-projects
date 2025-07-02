import pygame as py
import math 
import random
import os

os.chdir(os.path.dirname(__file__))

py.init()

clock = py.time.Clock()

window = py.display.set_mode((800,600))
py.display.set_caption("KILL AND SURVIVE")
py.display.set_mode((800,600), py.FULLSCREEN)

score = 0
Font = py.font.SysFont(None,36)

music_list = ["wave1.mp3","wave2.mp3","wave3.mp3"]
difficulty = [1300,800,400]

current_track = 0

gun_sound = py.mixer.Sound("gun_shot.mp3")
gun_sound.set_volume(0.2)
enemy_hit = py.mixer.Sound("enemy_hit.mp3")

def music_player(index):
    py.mixer.music.load(music_list[index])
    py.mixer.music.play()

def player_hp_system(surface,protag_hp,protag_max_hp):
    x = 10
    y = 10
    length = 200
    breadth = 20
    fraction = max(0,protag_hp)/protag_max_hp
    py.draw.rect(surface,(100,100,100),(x,y,length,breadth))
    py.draw.rect(surface,(0,255,0),(x,y,(length*fraction),breadth))

class protag():
    def __init__(self,pro_x,pro_y,visible):
        self.pro_x = pro_x
        self.pro_y = pro_y
        self.visible = visible 
        self.protag_hp = 300
        self.protag_max_hp = 300
        self.pro_dx = 5
        self.pro_dy = 5

    def protag_move(self,keys):
        if keys[py.K_a]:
            self.pro_x -= self.pro_dx
        if keys[py.K_d]:
            self.pro_x += self.pro_dx
        if keys[py.K_w]: 
            self.pro_y -= self.pro_dy
        if keys[py.K_s]: 
            self.pro_y += self.pro_dy

    def draw(self,surface): 
        if self.visible:
            py.draw.rect(surface,(245,43,250),(self.pro_x,self.pro_y,40,40))

class enemy_class():
    def __init__(self,ene_x,ene_y,visible,ene_hp):
        self.ene_x = ene_x
        self.ene_y = ene_y
        self.visible = visible 
        self.ene_hp = ene_hp
        self.ene_dx = 4
        self.ene_dy = 4

    def enemy_movement(self,pro_x,pro_y):
        diff_x = pro_x - self.ene_x
        diff_y = pro_y - self.ene_y
        distance = math.sqrt(diff_x*diff_x + diff_y*diff_y)
        direction_x = diff_x/distance
        direction_y = diff_y/distance
        self.ene_x += direction_x*self.ene_dx
        self.ene_y += direction_y*self.ene_dy

    def draw(self,surface): 
        if self.visible:
            py.draw.rect(surface,(245,0,25),(self.ene_x,self.ene_y,20,20))

class Bullet():
    def __init__(self,bull_x,bull_y,dir_x,dir_y):
        self.bull_x = bull_x
        self.bull_y = bull_y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.size = 5
        self.speed = 4

    def bullet_movement(self):
        self.bull_x += self.dir_x * self.speed
        self.bull_y += self.dir_y * self.speed

    def draw_bull(self,surface):
        py.draw.circle(surface, (0, 245, 0), (int(self.bull_x), int(self.bull_y)), self.size)

class ene_spawner():
    def __init__(self,last_spawn_time,diff_rate,time_delay):
        self.time_delay = time_delay
        self.last_spawn_time = last_spawn_time
        self.diff_rate = diff_rate
        self.ene_list = []

    def spawn(self):
        select = random.choice(["top","left","bottom","right"])
        if select == "top":
            x = random.randint(0,800)
            y = 0
        elif select == "left":
            y = random.randint(0,600)
            x = 0            
        elif select == "right":
            y = random.randint(0,600)
            x = 800
        elif select == "bottom":
            x = random.randint(0,800)
            y = 600
        new_ene = enemy_class(x,y,True,100)
        self.ene_list.append(new_ene)

    def update_spawn(self):
        current_spawn_time = py.time.get_ticks()
        if current_spawn_time - self.last_spawn_time > self.time_delay:
            self.spawn()
            self.last_spawn_time = current_spawn_time

player = protag(400,300,True)
spawner = ene_spawner(py.time.get_ticks(),0.2,difficulty[0])
bullets = []

py.mixer.music.set_endevent(py.USEREVENT)
music_player(current_track)

def shoot(shooter_x, shooter_y, target_x, target_y):
    bull_x = target_x - shooter_x
    bull_y = target_y - shooter_y
    bull_dist = math.sqrt(bull_x*bull_x + bull_y*bull_y)
    directbull_x = bull_x/bull_dist
    directbull_y = bull_y/bull_dist
    bullet = Bullet(shooter_x,shooter_y,directbull_x,directbull_y)
    return bullet

running = True

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.MOUSEBUTTONDOWN:
            target_x,target_y = py.mouse.get_pos()
            bullet = shoot(player.pro_x,player.pro_y,target_x,target_y)
            bullets.append(bullet)
            gun_sound.play()
        elif event.type == py.USEREVENT:
            current_track += 1
            if current_track < len(music_list):
                music_player(current_track)
                spawner.time_delay = difficulty[current_track]
            else:
                py.mixer.music.stop()

    window.fill((0,0,0))

    for bullet in bullets[:]:
        bullet.bullet_movement()
        bullet.draw_bull(window)

    keys = py.key.get_pressed()
    player.protag_move(keys)
    player.draw(window)

    spawner.update_spawn()

    for ene in spawner.ene_list:
        ene.enemy_movement(player.pro_x,player.pro_y)
        ene.draw(window)

    for bullet in bullets[:]:
        for ene in spawner.ene_list[:]:
            dist = math.sqrt((ene.ene_x - bullet.bull_x)**2 + (ene.ene_y - bullet.bull_y)**2)
            if dist < (20 + bullet.size):
                enemy_hit.play()
                spawner.ene_list.remove(ene)
                bullets.remove(bullet)
                score += 1
                break

    score_create = Font.render(f"Score:{score}",True,(255,255,255))
    window.blit(score_create,(10,40))
    
    player_size = py.Rect(player.pro_x,player.pro_y,40,40)

    for ene in spawner.ene_list:
        enemy_size = py.Rect(ene.ene_x,ene.ene_y,20,20)
        if player_size.colliderect(enemy_size):
            player.protag_hp -= 10
            player.protag_hp = max(0,player.protag_hp)
            spawner.ene_list.remove(ene)

    player_hp_system(window,player.protag_hp,player.protag_max_hp)
    if player.protag_hp <= 0:
        print("Game Fucking Finished You Moron!")
        running = False

    py.display.update()

    player_rect = py.Rect(player.pro_x, player.pro_y, 20, 20)
    player_rect.clamp_ip(window.get_rect())
    player.pro_x, player.pro_y = player_rect.topleft

    clock.tick(60)

py.quit()
score_create