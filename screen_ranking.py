import pygame
from constants import *
from ui import Button, draw_rounded_rect, draw_glow
from database import obtener_ranking


class RankingScreen:
    def __init__(self, fonts):
        self.fonts = fonts
        self.dificultad_activa = "facil"
        self.ranking_data = []
        self._load_ranking()

        cx = SCREEN_W // 2
        y_tabs = 160

        self.btn_facil = Button(cx - 270, y_tabs, 160, 44, "Fácil",
                                 (20, 70, 35), SUCCESS, fonts["body"], radius=8)
        self.btn_medio = Button(cx - 80, y_tabs, 160, 44, "Medio",
                                 (70, 55, 10), WARNING, fonts["body"], radius=8)
        self.btn_dificil = Button(cx + 110, y_tabs, 160, 44, "Difícil",
                                   (70, 18, 18), ERROR_COLOR, fonts["body"], radius=8)

        self.btn_menu = Button(cx - 100, 640, 200, 48, "← Volver al Menú",
                                PRIMARY_DARK, TEXT_WHITE, fonts["body"], radius=10)

        self._tab_btns = [
            (self.btn_facil, "facil"),
            (self.btn_medio, "medio"),
            (self.btn_dificil, "dificil"),
        ]

    def _load_ranking(self):
        self.ranking_data = obtener_ranking(self.dificultad_activa)

    def set_dificultad(self, diff):
        self.dificultad_activa = diff
        self._load_ranking()

    def handle_events(self, events):
        for event in events:
            for btn, diff in self._tab_btns:
                if btn.handle_event(event):
                    self.set_dificultad(diff)
            if self.btn_menu.handle_event(event):
                return ("goto_menu",)
        return None

    def update(self):
        for btn, _ in self._tab_btns:
            btn.update()
        self.btn_menu.update()

    def draw(self, surface):
        surface.fill(BG_COLOR)

        title = self.fonts["title"].render("Ranking Global", True, TEXT_WHITE)
        tr = title.get_rect(centerx=SCREEN_W // 2, y=60)
        surface.blit(title, tr)

        sub = self.fonts["body"].render("Top 5 mejores tiempos por dificultad", True, TEXT_GRAY)
        sr = sub.get_rect(centerx=SCREEN_W // 2, y=118)
        surface.blit(sub, sr)

        for btn, diff in self._tab_btns:
            info = DIFICULTADES[diff]
            if diff == self.dificultad_activa:
                draw_glow(surface, info["color"], btn.rect, 8, 60)
                draw_rounded_rect(surface, tuple(max(0, c - 60) for c in info["color"]),
                                  btn.rect, 8)
                draw_rounded_rect(surface, (0, 0, 0, 0), btn.rect, 8,
                                  border=2, border_color=info["color"])
                t = self.fonts["body"].render(DIFICULTADES[diff]["label"], True, info["color"])
            else:
                draw_rounded_rect(surface, BG_PANEL, btn.rect, 8)
                draw_rounded_rect(surface, (0, 0, 0, 0), btn.rect, 8,
                                  border=1, border_color=PANEL_BORDER)
                t = self.fonts["body"].render(DIFICULTADES[diff]["label"], True, TEXT_GRAY)
            tr2 = t.get_rect(center=btn.rect.center)
            surface.blit(t, tr2)

        cx = SCREEN_W // 2
        panel = pygame.Rect(cx - 340, 225, 680, 380)
        draw_rounded_rect(surface, BG_PANEL, panel, 16)
        draw_rounded_rect(surface, (0, 0, 0, 0), panel, 16,
                         border=1, border_color=PANEL_BORDER)

        header_y = panel.y + 20
        headers = [("Pos.", 80), ("Jugador", 320), ("Tiempo", 540)]
        for label, hx in headers:
            ht = self.fonts["small"].render(label, True, TEXT_GRAY)
            surface.blit(ht, (panel.x + hx, header_y))

        pygame.draw.line(surface, PANEL_BORDER,
                         (panel.x + 20, header_y + 28),
                         (panel.right - 20, header_y + 28), 1)

        diff_color = DIFICULTADES[self.dificultad_activa]["color"]

        if not self.ranking_data:
            empty = self.fonts["body"].render("Aún no hay resultados en esta dificultad", True, TEXT_DIM)
            er = empty.get_rect(center=(cx, panel.centery + 20))
            surface.blit(empty, er)
        else:
            medals = ["🥇", "🥈", "🥉", "4", "5"]
            medal_colors = [WARNING, TEXT_GRAY, (180, 100, 40), TEXT_DIM, TEXT_DIM]

            for i, row in enumerate(self.ranking_data):
                row_y = header_y + 50 + i * 58
                row_rect = pygame.Rect(panel.x + 10, row_y - 8, panel.w - 20, 48)

                if i == 0:
                    draw_rounded_rect(surface,
                                      tuple(max(0, c // 5) for c in diff_color),
                                      row_rect, 8)
                    draw_rounded_rect(surface, (0, 0, 0, 0), row_rect, 8,
                                     border=1, border_color=tuple(c // 2 for c in diff_color))

                pos_text = f"#{i+1}"
                pos_surf = self.fonts["heading"].render(pos_text, True, medal_colors[i])
                surface.blit(pos_surf, (panel.x + 80, row_y))

                nombre = row["nombre_usuario"]
                if len(nombre) > 20:
                    nombre = nombre[:18] + "..."
                n_surf = self.fonts["body"].render(nombre, True,
                                                    TEXT_WHITE if i == 0 else TEXT_GRAY)
                surface.blit(n_surf, (panel.x + 180, row_y))

                secs = row["tiempo_segundos"]
                mins = secs // 60
                s = secs % 60
                if mins > 0:
                    t_str = f"{mins}m {s:02d}s"
                else:
                    t_str = f"{s}s"
                t_surf = self.fonts["heading"].render(t_str, True,
                                                       diff_color if i == 0 else TEXT_WHITE)
                surface.blit(t_surf, (panel.x + 520, row_y))

                if i < len(self.ranking_data) - 1:
                    pygame.draw.line(surface, PANEL_BORDER,
                                     (panel.x + 20, row_y + 42),
                                     (panel.right - 20, row_y + 42), 1)

        self.btn_menu.draw(surface)
