import sys
import pygame
from constants import *
from database import init_database
from screen_login import LoginScreen
from screen_menu import MenuScreen
from screen_game import GameScreen
from screen_ranking import RankingScreen


def load_fonts():
    fonts = {}
    try:
        candidates_title = ["Segoe UI", "Arial", "Tahoma", "Verdana"]
        candidates_mono  = ["Consolas", "Courier New", "Lucida Console"]

        def best_font(candidates, size, bold=False):
            for name in candidates:
                try:
                    f = pygame.font.SysFont(name, size, bold=bold)
                    return f
                except Exception:
                    continue
            return pygame.font.Font(None, size)

        fonts["title"]   = best_font(candidates_title, 64, bold=True)
        fonts["heading"] = best_font(candidates_title, 28, bold=True)
        fonts["body"]    = best_font(candidates_title, 24)
        fonts["small"]   = best_font(candidates_title, 18)
        fonts["tiny"]    = best_font(candidates_title, 14)
    except Exception as e:
        print(f"Error cargando fuentes: {e}")
        fonts["title"]   = pygame.font.Font(None, 72)
        fonts["heading"] = pygame.font.Font(None, 36)
        fonts["body"]    = pygame.font.Font(None, 28)
        fonts["small"]   = pygame.font.Font(None, 22)
        fonts["tiny"]    = pygame.font.Font(None, 18)
    return fonts


def main():
    pygame.init()
    pygame.display.set_caption("Torre de Hanói")

    try:
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(icon, (80, 180, 255), (10, 24, 12, 6), border_radius=2)
        pygame.draw.rect(icon, (255, 100, 180), (12, 18, 8, 6), border_radius=2)
        pygame.draw.rect(icon, (100, 255, 200), (14, 12, 4, 6), border_radius=2)
        pygame.draw.rect(icon, (200, 200, 200), (15, 4, 2, 8))
        pygame.display.set_icon(icon)
    except Exception:
        pass

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()

    print("Inicializando base de datos...")
    if not init_database():
        print("ERROR: No se pudo conectar a MySQL.")
        print("Asegúrate de que MySQL esté corriendo y las credenciales sean correctas.")
        print("Credenciales configuradas: host=localhost, user=root, password=''")
        pygame.quit()
        sys.exit(1)
    print("Base de datos lista.")

    fonts = load_fonts()

    current_state = STATE_LOGIN
    usuario_activo = None

    login_screen  = LoginScreen(fonts)
    menu_screen   = None
    game_screen   = None
    ranking_screen = None

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_state == STATE_GAME:
                        current_state = STATE_MENU
                    elif current_state == STATE_RANKING:
                        current_state = STATE_MENU

        if current_state == STATE_LOGIN:
            result = login_screen.handle_events(events)
            login_screen.update()
            login_screen.draw(screen)

            if result:
                action = result[0]
                if action == "goto_menu":
                    usuario_activo = result[1]
                    menu_screen = MenuScreen(fonts, usuario_activo)
                    current_state = STATE_MENU

        elif current_state == STATE_MENU:
            result = menu_screen.handle_events(events)
            menu_screen.update()
            menu_screen.draw(screen)

            if result:
                action = result[0]
                if action == "goto_game":
                    dificultad = result[1]
                    game_screen = GameScreen(fonts, usuario_activo, dificultad)
                    current_state = STATE_GAME
                elif action == "goto_ranking":
                    ranking_screen = RankingScreen(fonts)
                    current_state = STATE_RANKING
                elif action == "logout":
                    usuario_activo = None
                    login_screen = LoginScreen(fonts)
                    current_state = STATE_LOGIN

        elif current_state == STATE_GAME:
            result_events = game_screen.handle_events(events)
            result_update = game_screen.update()
            game_screen.draw(screen)

            result = result_events or result_update
            if result:
                action = result[0]
                if action == "goto_menu":
                    menu_screen = MenuScreen(fonts, usuario_activo)
                    current_state = STATE_MENU
                    
        elif current_state == STATE_RANKING:
            result = ranking_screen.handle_events(events)
            ranking_screen.update()
            ranking_screen.draw(screen)

            if result:
                action = result[0]
                if action == "goto_menu":
                    current_state = STATE_MENU

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
