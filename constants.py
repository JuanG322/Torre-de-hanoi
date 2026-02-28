# Dimensiones
SCREEN_W = 1280
SCREEN_H = 720

# FPS
FPS = 60

# Colores - Tema oscuro con acentos neón
BG_COLOR        = (12, 16, 30)
BG_PANEL        = (20, 26, 44)
PANEL_BORDER    = (40, 50, 80)

PRIMARY         = (80, 180, 255)      # Azul neón
PRIMARY_DARK    = (40, 100, 180)
SECONDARY       = (255, 100, 180)     # Rosa neón
ACCENT          = (100, 255, 200)     # Verde menta
WARNING         = (255, 200, 60)      # Amarillo
ERROR_COLOR     = (255, 80, 80)       # Rojo
SUCCESS         = (80, 255, 150)      # Verde

TEXT_WHITE      = (230, 235, 255)
TEXT_GRAY       = (130, 140, 170)
TEXT_DIM        = (70, 80, 110)

# Colores de los discos (7 discos)
DISK_COLORS = [
    (255,  80,  80),   # Rojo
    (255, 150,  50),   # Naranja
    (255, 220,  50),   # Amarillo
    ( 80, 220,  80),   # Verde
    ( 50, 180, 255),   # Azul
    (160,  80, 255),   # Violeta
    (255,  80, 180),   # Rosa
]

# Torres
TOWER_COUNT    = 3
TOWER_W        = 14
TOWER_H        = 300
BASE_H         = 18
BASE_W         = 260
DISK_H         = 28
DISK_MIN_W     = 60
DISK_MAX_W     = 240

# Posiciones X de las torres
TOWER_XS = [260, 640, 1020]
TOWER_Y  = 480   # base inferior de la torre

# Dificultades
DIFICULTADES = {
    "facil":   {"discos": 3, "label": "Fácil",   "color": SUCCESS},
    "medio":   {"discos": 5, "label": "Medio",   "color": WARNING},
    "dificil": {"discos": 7, "label": "Difícil", "color": ERROR_COLOR},
}

# Estados del juego
STATE_LOGIN   = "login"
STATE_MENU    = "menu"
STATE_GAME    = "game"
STATE_RANKING = "ranking"
