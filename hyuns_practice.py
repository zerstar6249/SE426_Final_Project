import pygame as pg
import random


SIZE=500
num_wide=10
MAX_MAP_DATA=9
MAX_HEALTH=50

rec_size=SIZE//num_wide

size=[SIZE,SIZE]
pg.init()
screen=pg.display.set_mode(size,0,32)
clock = pg.time.Clock()
pg.display.set_caption("Game Title")


WHITE=[255,255,255]
BLACK = [0,0,0]
RED=[255,0,0]
GREEN=[0,255,0]
BLUE=[0,0,255]

DONE=True
screen.fill(WHITE)

baseFont=pg.font.SysFont(None,32)
a= 1
b=str(a).encode("UTF-8")
text= baseFont.render(b,True,BLACK)
textRect=text.get_rect()
map_data=[]
for i in range(0, 10):
    for i2 in range(0, 10):
        map_data.append(0)
health=10
position =[1,1]
new_position=[1,1]
while DONE:
    screen.fill(WHITE)
    for i in range(num_wide):
        for i2 in range(num_wide):
            rand=random.random()
            if rand>0.95:
                if not (i==position[0] and i2==position[1]):
                    map_data[num_wide*i+i2]+=2
            elif rand>0.85:
                if not (i==position[0] and i2==position[1]):
                    map_data[num_wide * i + i2] += 1
            if map_data[num_wide * i + i2]>MAX_MAP_DATA:
                map_data[num_wide * i + i2]=MAX_MAP_DATA
    for i in range(num_wide):
        for i2 in range(num_wide):
            a=map_data[num_wide*i+i2]
            b=str(a).encode("UTF-8")
            text= baseFont.render(b,True,BLACK)
            textRect.centerx=(i+0.5)*rec_size
            textRect.centery=(i2+0.5)*rec_size
            screen.blit(text, textRect)

    for i in range(1,num_wide):
        pg.draw.line(screen,BLACK,[rec_size*i,0],[rec_size*i,SIZE],1)
    for i in range(1,num_wide):
        pg.draw.line(screen,BLACK,[0,rec_size*i],[SIZE,rec_size*i],1)
    clock.tick(10)
    act=True
    while(act):
        for event in pg.event.get():
            new_position[0] = position[0]
            new_position[1] = position[1]
            if event.type ==pg.QUIT:
                DONE=False
            if event.type ==pg.KEYDOWN:
                if event.key == ord('a'):
                    if act==False:
                        act=True
                    elif(position[0]>1):
                        new_position[0]-=1
                        act=False
                if event.key == ord('d'):
                    if act==False:
                        act=True
                    elif(position[0]<num_wide):
                        new_position[0]+=1
                        act = False
                if event.key == ord('w'):
                    if act==False:
                        act=True
                    elif(position[1]>1):
                        new_position[1]-=1
                        act = False
                if event.key == ord('s'):
                    if act==False:
                        act=True
                    elif(position[1]<num_wide):
                        new_position[1]+=1
                        act=False
    position[0]=new_position[0]
    position[1]=new_position[1]
    health+=map_data[position[0]*num_wide+position[1]]
    if health>MAX_HEALTH:
        health=MAX_HEALTH
    map_data[position[0] * num_wide + position[1]]=0

    a = health
    b = str(a).encode("UTF-8")
    pg.draw.rect(screen, BLUE, [(position[0] - 1) * rec_size, (position[1] - 1) * rec_size, rec_size, rec_size], 0)
    text = baseFont.render(b, True, BLACK)
    textRect.centerx = (position[0] - 0.5) * rec_size
    textRect.centery = (position[1] - 0.5) * rec_size
    screen.blit(text, textRect)
    pg.display.update()
    pg.display.flip()
