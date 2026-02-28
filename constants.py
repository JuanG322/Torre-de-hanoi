SCREEN_W = 1280
SCREEN_H = 720

FPS = 60

BG_COLOR        = (10, 12, 20)
BG_PANEL        = (18, 22, 35)
PANEL_BORDER    = (40, 50, 80)

PRIMARY         = (80, 180, 255)      
PRIMARY_DARK    = (40, 100, 180)
SECONDARY       = (255, 100, 180)   
ACCENT          = (100, 255, 200)    
WARNING         = (255, 200, 60)  
ERROR_COLOR     = (255, 80, 80)    
SUCCESS         = (80, 255, 150)   

TEXT_WHITE      = (230, 235, 255)
TEXT_GRAY       = (130, 140, 170)
TEXT_DIM        = (70, 80, 110)


DISK_COLORS = [
    (255,  80,  80),  
    (255, 150,  50), 
    (255, 220,  50),  
    ( 80, 220,  80), 
    ( 50, 180, 255),  
    (160,  80, 255),   
    (255,  80, 180),   
]

TOWER_COUNT    = 3
TOWER_W        = 14
TOWER_H        = 300
BASE_H         = 18
BASE_W         = 260
DISK_H         = 28
DISK_MIN_W     = 60
DISK_MAX_W     = 240


TOWER_XS = [260, 640, 1020]
TOWER_Y  = 480   

DIFICULTADES = {
    "facil":   {"discos": 3, "label": "Fácil",   "color": SUCCESS},
    "medio":   {"discos": 5, "label": "Medio",   "color": WARNING},
    "dificil": {"discos": 7, "label": "Difícil", "color": ERROR_COLOR},
}

STATE_LOGIN   = "login"
STATE_MENU    = "menu"
STATE_GAME    = "game"
STATE_RANKING = "ranking"
