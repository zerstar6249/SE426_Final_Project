
import pygame as pg
import numpy as np



COL_BLACK = (  0,  0,  0)
COL_WHITE = (255,255,255)
COL_BLUE  = (  0,  0,255)
COL_GREEN = (  0,255,  0)
COL_RED   = (255,  0,  0)

CONFIG_HP_MAX = 100
CONFIG_HP_INITIAL = 50
CONFIG_DMG_BASE = 5
CONFIG_DMG_COEF_HP = 0.1
CONFIG_DMG_COEF_REFLECT = 0.5


area_w = 10
area_h = 10

area_resource = np.zeros((area_w,area_h),dtype=int)
area_inst = np.zeros((area_w,area_h),dtype=int)

global_turn = 0

cell_w = 60
cell_h = 60



class instance():
    def __init__(self):
        self.hp = CONFIG_HP_INITIAL
        self.hp_max = CONFIG_HP_MAX
        self.dmg_base = CONFIG_DMG_BASE
        self.dmg_coef_hp = CONFIG_COEF_HP


        self.controller = 1




if __name__ == "__main__":
    pg.init()
    
    size = [cell_w*area_w, cell_h*area_h]
    scr = pg.display.set_mode(size)

    pg.display.set_caption("Simulation")

    done = False
    clock = pg.time.Clock()

    while not done:
        clock.tick(10)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        
        scr.fill(COL_WHITE)
        

        for xi,line in enumerate(area_resource):
            for yi, elem in enumerate(line):
                pg.draw.polygon(scr, COL_BLACK,
                            [[xi*cell_w,yi*cell_h], [(xi+1)*cell_w,yi*cell_h],
                             [(xi+1)*cell_w,(yi+1)*cell_h], [xi*cell_w,(yi+1)*cell_h]], 4)
        
        # Last element 0 = no outline, else = width
        # pg.draw.polygon(scr, COL_RED, [[30, 150], [125, 100], [220, 150]], 0)


        pg.display.flip()
