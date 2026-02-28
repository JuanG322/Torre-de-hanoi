import pygame
from constants import *
from ui import Button, draw_rounded_rect, draw_glow


class MenuScreen:
    def __init__(self, fonts, usuario):
        self.fonts = fonts
        self.usuario = usuario

        cx = SCREEN_W // 2

        # Título sección jugar
        self.btn_facil = Button(cx - 310, 270, 200, 70, "Fácil\n(3 discos)",
                                 (20, 80, 40), SUCCESS, fonts["body"], radius=12)
        self.btn_medio = Button(cx - 100, 270, 200, 70, "Medio\n(5 discos)",
                                 (80, 60, 10), WARNING, fonts["body"], radius=12)
        self.btn_dificil = Button(cx + 110, 270, 200, 70, "Difícil\n(7 discos)",
                                   (80, 20, 20), ERROR_COLOR, fonts["body"], radius=12)

        self.btn_ranking = Button(cx - 120, 400, 240, 56, "Ver Ranking",
                                   PRIMARY_DARK, TEXT_WHITE, fonts["body"], radius=12)

        self.btn_logout = Button(cx - 80, 480, 160, 44, "Cerrar Sesión",
                                  (40, 20, 20), TEXT_GRAY, fonts["small"], radius=8)

        # Etiquetas especiales para los botones de dificultad
        self._diff_btns = [
            (self.btn_facil, "facil"),
            (self.btn_medio, "medio"),
            (self.btn_dificil, "dificil"),
        ]

        self.stars = self._make_stars()

    def _make_stars(self):
        import random
        return [(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H),
                 random.randint(1, 2), random.random()) for _ in range(100)]

    def handle_events(self, events):
        for event in events:
            for btn, diff in self._diff_btns:
                if btn.handle_event(event):
                    return ("goto_game", diff)
            if self.btn_ranking.handle_event(event):
                return ("goto_ranking",)
            if self.btn_logout.handle_event(event):
                return ("logout",)
        return None

    def update(self):
        for btn, _ in self._diff_btns:
            btn.update()
        self.btn_ranking.update()
        self.btn_logout.update()

    def draw(self, surface):
        surface.fill(BG_COLOR)

        # Título
        title = self.fonts["title"].render("Torre de Hanói", True, TEXT_WHITE)
        tr = title.get_rect(centerx=SCREEN_W // 2, y=60)
        surface.blit(title, tr)

        # Bienvenida
        welcome = self.fonts["body"].render(
            f"Bienvenido, {self.usuario['nombre_usuario']}", True, ACCENT)
        wr = welcome.get_rect(centerx=SCREEN_W // 2, y=148)
        surface.blit(welcome, wr)

        # Separador
        pygame.draw.line(surface, PANEL_BORDER,
                         (SCREEN_W // 2 - 300, 195), (SCREEN_W // 2 + 300, 195), 1)

        # Etiqueta "Selecciona dificultad"
        label = self.fonts["heading"].render("Selecciona una dificultad para jugar", True, TEXT_GRAY)
        lr = label.get_rect(centerx=SCREEN_W // 2, y=215)
        surface.blit(label, lr)

        # Botones de dificultad — dibujamos manualmente sin usar btn.draw()
        # para evitar que el texto del Button se superponga con el texto personalizado
        diff_configs = [
            (self.btn_facil,   "facil",   "Fácil",   SUCCESS,      "3 discos"),
            (self.btn_medio,   "medio",   "Medio",   WARNING,      "5 discos"),
            (self.btn_dificil, "dificil", "Difícil", ERROR_COLOR,  "7 discos"),
        ]

        for btn, diff, lbl, col, sub in diff_configs:
            # Fondo del botón
            bg = tuple(max(0, c - 80) for c in col)
            hover_bg = tuple(max(0, c - 50) for c in col)
            draw_glow(surface, col, btn.rect, 12, 25)
            draw_rounded_rect(surface, hover_bg if btn.hovered else bg, btn.rect, 12)
            draw_rounded_rect(surface, (0, 0, 0, 0), btn.rect, 12,
                              border=2, border_color=col)

            # Texto de dificultad
            t = self.fonts["heading"].render(lbl, True, col)
            tr2 = t.get_rect(centerx=btn.rect.centerx, y=btn.rect.y + 12)
            surface.blit(t, tr2)

            # Subtexto de discos
            t2 = self.fonts["small"].render(sub, True, TEXT_GRAY)
            tr3 = t2.get_rect(centerx=btn.rect.centerx, y=btn.rect.y + 42)
            surface.blit(t2, tr3)

        # Separador
        pygame.draw.line(surface, PANEL_BORDER,
                         (SCREEN_W // 2 - 200, 370), (SCREEN_W // 2 + 200, 370), 1)

        self.btn_ranking.draw(surface)
        self.btn_logout.draw(surface)

        # Decoración torres pequeñas al fondo
        self._draw_mini_towers(surface)

    def _draw_mini_towers(self, surface):
        # Torres decorativas en el fondo
        for i, tx in enumerate([180, 640, 1100]):
            pygame.draw.rect(surface, (25, 30, 50),
                             (tx - 5, 560, 10, 120))
            pygame.draw.rect(surface, (25, 30, 50),
                             (tx - 80, 672, 160, 12), border_radius=4)
