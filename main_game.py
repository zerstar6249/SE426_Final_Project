
import pygame as pg
import numpy as np



COL_BLACK = (  0,  0,  0)
COL_WHITE = (255,255,255)
COL_BLUE  = (  0,  0,255)
COL_GREEN = (  0,255,  0)
COL_RED   = (255,  0,  0)

STATE_IDLE = 0
STATE_MOVL = 1
STATE_MOVR = 2
STATE_MOVU = 3
STATE_MOVD = 4
STATE_ATKL = 5
STATE_ATKR = 6
STATE_ATKU = 7
STATE_ATKD = 8


CONFIG_INSTANCE_COUNT = 1
CONFIG_PLAYER_ENABLE = True

CONFIG_HP_MAX = 100
CONFIG_HP_INITIAL = 50
CONFIG_HP_DECAY_MODE = 0 # 0 = Absoulte, 1 = portion
CONFIG_HP_DECAY_VALUE = 1
CONFIG_DMG_BASE = 5
CONFIG_DMG_COEF_HP = 0.1
CONFIG_DMG_COEF_REFLECT = 0.5

CONFIG_AREA_W = 10
CONFIG_AREA_H = 10

CONFIG_CELL_W = 60
CONFIG_CELL_H = 60



area_w = CONFIG_AREA_W
area_h = CONFIG_AREA_W

area_resource = np.zeros((area_w,area_h),dtype=int)

instances = list()

global_turn = 0

cell_w = CONFIG_CELL_W
cell_h = CONFIG_CELL_H



class instance():
    def __init__(self, idx, initx, inity, player = False):
        self.idx = idx
        self.x = initx
        self.y = inity
        
        self.hp = CONFIG_HP_INITIAL
        self.hp_max = CONFIG_HP_MAX
        self.hp_decay_mode = CONFIG_HP_DECAY_MODE
        self.hp_decay_value = CONFIG_HP_DECAY_VALUE

        self.dmg_base = CONFIG_DMG_BASE
        self.dmg_coef_hp = CONFIG_DMG_COEF_HP
        self.dmg_coef_reflect = CONFIG_DMG_COEF_REFLECT
        
        self.state_reserved = STATE_IDLE

        if player: self.controller = 1
        else: self.controller = 0



def game_init():
    if CONFIG_PLAYER_ENABLE:
        inst = instance(0, 1, 1, True)
        instances.append(inst)
        for i in range(CONFIG_INSTANCE_COUNT-1):
            inst = instance(i+1, np.randint(area_w),np.randint(area_h))
            instances.append(inst)
    else:
        for i in range(CONFIG_INSTANCE_COUNT):
            inst = instance(i, np.randint(area_w),np.randint(area_h))
            instances.append(inst)


def execute_turn():
    global global_turn
    for inst in instances:
        if   inst.state_reserved == STATE_MOVL:
            inst.x -= 1
        elif inst.state_reserved == STATE_MOVR:
            inst.x += 1
        elif inst.state_reserved == STATE_MOVU:
            inst.y -= 1
        elif inst.state_reserved == STATE_MOVD:
            inst.y += 1

    global_turn += 1

def get_state_text(ind):
    if   ind==STATE_IDLE: return "IDLE"
    elif ind==STATE_MOVL: return "MOVL"
    elif ind==STATE_MOVR: return "MOVR"
    elif ind==STATE_MOVU: return "MOVU"
    elif ind==STATE_MOVD: return "MOVD"
    elif ind==STATE_ATKL: return "ATKL"
    elif ind==STATE_ATKR: return "ATKR"
    elif ind==STATE_ATKU: return "ATKU"
    elif ind==STATE_ATKD: return "ATKD"

def get_grid_rectange (xloc,yloc,padding=0):
    return [[(xloc+0)*cell_w+padding,(yloc+0)*cell_h+padding],
        [(xloc+1)*cell_w-padding,(yloc+0)*cell_h+padding],
        [(xloc+1)*cell_w-padding,(yloc+1)*cell_h-padding],
        [(xloc+0)*cell_w+padding,(yloc+1)*cell_h-padding]]

if __name__ == "__main__":
    pg.init()
    
    size = [cell_w*area_w, cell_h*area_h+40]
    scr = pg.display.set_mode(size)

    f_b30 = pg.font.SysFont("comicsansms", 30)
    f_b20 = pg.font.SysFont("comicsansms", 20)

    pg.display.set_caption("Simulation")

    
    done = False
    clock = pg.time.Clock()
    
    game_init()

    while not done:
        clock.tick(60)
        turn_passed = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                turn_passed = True
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: # Temp
                instances[0].state_reserved = STATE_MOVL
                turn_passed = True
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: # Temp
                instances[0].state_reserved = STATE_MOVR
                turn_passed = True
            if event.type == pg.KEYDOWN and event.key == pg.K_UP: # Temp
                instances[0].state_reserved = STATE_MOVU
                turn_passed = True
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN: # Temp
                instances[0].state_reserved = STATE_MOVD
                turn_passed = True
        scr.fill(COL_WHITE)
        text = f_b30.render("Turn:{}".format(global_turn), True, COL_BLACK)
        scr.blit(text, (20,cell_h*area_h+10))
        

        for xi,line in enumerate(area_resource):
            for yi, elem in enumerate(line):
                pg.draw.polygon(scr, COL_BLACK, get_grid_rectange(xi,yi,0),4)
        
        for ii, inst in enumerate(instances):
            pg.draw.polygon(scr,COL_RED,get_grid_rectange(inst.x,inst.y,3),3)
            text = f_b20.render(get_state_text(inst.state_reserved), True, COL_BLUE)
            scr.blit(text, (inst.x*cell_w+5,inst.y*cell_h+5))

        pg.display.flip()

        if turn_passed:
            execute_turn()
