
import pygame as py

py.init()

clock = py.time.Clock()

window  = py.display.set_mode((1000,600))

ball_dx = 9
ball_dy = 9
ball_x = 500
ball_y = 300

white = (255,255,255)
black = (0,0,0)
yellow = (65,25,133)
green = (0,255,0)

rows = 5
coloums = 18
gap = 6

x = 700
y = 500
vel = 70

lives = 3

bloc_rect = []

def build_lev1():
    global bloc_rect
    for i in range(rows):
         for j in range(coloums):
            a = j*(50 + gap)
            b = i*(25 + gap)
            bloc = py.Rect((a,b,50,25))
            bloc_rect.append(bloc)
            py.draw.rect(window,green,bloc)

running = True

build_lev1()

while  running:

    window.fill(black)

    ball_rect = py.Rect(ball_x - 10, ball_y + 10, 20, 20)

    clock.tick(60)

    for bloc in bloc_rect:
        py.draw.rect(window, green, bloc)
    py.draw.circle(window,white,(ball_x,ball_y),10)
    py.draw.rect(window,yellow,(x,y,115,20))

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:  
            if event.key == py.K_a and x >= 40:  
                x -= vel              
            elif event.key == py.K_d and x <= 850: 
                x += vel 

    ball_x += ball_dx
    ball_y += ball_dy

    if ball_x - 10 <=0 or ball_x + 10 >= 980:
        ball_dx = -ball_dx

    if ball_y - 10 <= 0 or ball_y + 10 >= 560:
        ball_dy = -ball_dy

    if (x <= ball_x <= x + 115) and (ball_y >= y):
        ball_dy = -ball_dy
        offset = (ball_x - x) - (115 / 2)  
        ball_dx += offset * 0.05

    if ball_y + 10 > 560:
        lives = lives - 1
        py.time.delay(900)
        ball_y = 300
        ball_x = 500
        x = 600

    if lives == 0:
        py.time.delay(800)
        font = py.font.Font(None,40)
        text = font.render("Game Over",True,(255,245,1))
        window.blit(text,(500,300))
        running = False

    fon = py.font.Font(None,40)
    lives_text =  fon.render(f"Lives:{lives}",True,(123,23,3))
    window.blit(lives_text,(600,400))

    for bloc in bloc_rect[:]:
        if ball_rect.colliderect(bloc):
            bloc_rect.remove(bloc)
            if ball_y > 0:
                ball_dy = -ball_dy


    py.display.flip()