import pygame
import time
from constants import *
from ui import Button, draw_rounded_rect, draw_glow
from database import guardar_resultado


class HanoiGame:
    """Lógica pura de la Torre de Hanói."""
    def __init__(self, num_discos):
        self.num_discos = num_discos
        # Cada torre es una lista de enteros (1=más pequeño, num_discos=más grande)
        self.torres = [
            list(range(num_discos, 0, -1)),  # Torre 0: todos los discos
            [],
            []
        ]

    def mover(self, origen, destino):
        """Intenta mover el disco superior de origen a destino.
        Retorna True si el movimiento es válido, False si no."""
        if origen == destino:
            return False
        if not self.torres[origen]:
            return False
        disco = self.torres[origen][-1]
        if self.torres[destino] and self.torres[destino][-1] < disco:
            return False
        self.torres[destino].append(self.torres[origen].pop())
        return True

    def esta_completo(self):
        """El puzzle está completo cuando todos los discos están en la torre 2."""
        return len(self.torres[2]) == self.num_discos


class GameScreen:
    def __init__(self, fonts, usuario, dificultad):
        self.fonts = fonts
        self.usuario = usuario
        self.dificultad = dificultad
        self.num_discos = DIFICULTADES[dificultad]["discos"]
        self.diff_color = DIFICULTADES[dificultad]["color"]

        self.game = HanoiGame(self.num_discos)
        self.torre_seleccionada = None
        self.start_time = time.time()
        self.elapsed = 0
        self.completado = False
        self.completion_timer = 0    # Segundos contados tras completar

        # Animación de disco seleccionado
        self.anim_offset = 0
        self.anim_dir = -1

        # Mensaje de error (movimiento inválido)
        self.error_msg = ""
        self.error_timer = 0

        # Partícula de completado
        self.particles = []

        cx = SCREEN_W // 2
        btn_y = SCREEN_H - 70

        self.btn_menu = Button(cx - 250, btn_y, 220, 48,
                               "← Menú Principal", (30, 30, 60), TEXT_WHITE,
                               fonts["body"], radius=10)
        self.btn_restart = Button(cx + 30, btn_y, 220, 48,
                                  "↺ Reiniciar", (30, 40, 30), ACCENT,
                                  fonts["body"], radius=10)

        # Calcular geometría de discos
        self._calc_geometry()

    def _calc_geometry(self):
        """Precalcula dimensiones de discos según cantidad."""
        self.disk_widths = []
        for i in range(1, self.num_discos + 1):
            # i=1 más pequeño, i=num_discos más grande
            t = (i - 1) / max(self.num_discos - 1, 1)
            w = int(DISK_MIN_W + t * (DISK_MAX_W - DISK_MIN_W))
            self.disk_widths.append(w)

    def _disk_width(self, disco):
        return self.disk_widths[disco - 1]

    def _disk_color(self, disco):
        idx = (disco - 1) % len(DISK_COLORS)
        return DISK_COLORS[idx]

    def _tower_hit(self, mx, my):
        """Devuelve el índice de la torre clickeada (0,1,2) o -1."""
        for i, tx in enumerate(TOWER_XS):
            # Área de clic: base + columna
            base_rect = pygame.Rect(tx - BASE_W // 2, TOWER_Y - BASE_H,
                                    BASE_W, BASE_H + 20)
            tower_rect = pygame.Rect(tx - TOWER_W // 2 - 20, TOWER_Y - TOWER_H,
                                     TOWER_W + 40, TOWER_H)
            if base_rect.collidepoint(mx, my) or tower_rect.collidepoint(mx, my):
                return i
            # Área de los discos apilados
            stack = self.game.torres[i]
            for j, disco in enumerate(stack):
                dw = self._disk_width(disco)
                dx = tx - dw // 2
                dy = TOWER_Y - BASE_H - (j + 1) * DISK_H
                dr = pygame.Rect(dx, dy, dw, DISK_H - 2)
                if dr.collidepoint(mx, my):
                    return i
        return -1

    def handle_events(self, events):
        for event in events:
            if self.btn_menu.handle_event(event):
                return ("goto_menu",)
            if self.btn_restart.handle_event(event):
                self._restart()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.completado:
                    mx, my = event.pos
                    torre = self._tower_hit(mx, my)
                    if torre >= 0:
                        self._on_tower_click(torre)
        return None

    def _restart(self):
        self.game = HanoiGame(self.num_discos)
        self.torre_seleccionada = None
        self.start_time = time.time()
        self.elapsed = 0
        self.completado = False
        self.completion_timer = 0
        self.error_msg = ""
        self.error_timer = 0
        self.particles = []

    def _on_tower_click(self, torre):
        if self.torre_seleccionada is None:
            # Primera selección
            if self.game.torres[torre]:
                self.torre_seleccionada = torre
                self.error_msg = ""
            else:
                self.error_msg = "Esa torre está vacía"
                self.error_timer = 90
        else:
            if torre == self.torre_seleccionada:
                # Deseleccionar
                self.torre_seleccionada = None
                return
            ok = self.game.mover(self.torre_seleccionada, torre)
            if ok:
                self.torre_seleccionada = None
                self.error_msg = ""
                if self.game.esta_completo():
                    self._on_complete()
            else:
                self.error_msg = "¡Movimiento inválido! No puedes poner un disco grande sobre uno pequeño"
                self.error_timer = 120
                self.torre_seleccionada = None

    def _on_complete(self):
        self.completado = True
        self.elapsed = int(time.time() - self.start_time)
        guardar_resultado(self.usuario["id"], self.dificultad, self.elapsed)
        self.completion_timer = 240  # ~4 segundos a 60fps
        self._spawn_particles()

    def _spawn_particles(self):
        import random
        for _ in range(60):
            x = random.randint(200, SCREEN_W - 200)
            y = random.randint(100, SCREEN_H - 100)
            vx = random.uniform(-3, 3)
            vy = random.uniform(-5, 1)
            color = DISK_COLORS[random.randint(0, len(DISK_COLORS) - 1)]
            life = random.randint(60, 180)
            self.particles.append([x, y, vx, vy, color, life, life])

    def update(self):
        self.btn_menu.update()
        self.btn_restart.update()

        if not self.completado:
            self.elapsed = int(time.time() - self.start_time)

        # Animación disco seleccionado
        self.anim_offset += self.anim_dir * 0.8
        if abs(self.anim_offset) > 8:
            self.anim_dir *= -1

        if self.error_timer > 0:
            self.error_timer -= 1

        # Timer de completado -> volver al menú
        if self.completado and self.completion_timer > 0:
            self.completion_timer -= 1
            if self.completion_timer == 0:
                return ("goto_menu",)

        # Partículas
        for p in self.particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.15  # gravedad
            p[5] -= 1
            if p[5] <= 0:
                self.particles.remove(p)

        return None

    def draw(self, surface):
        surface.fill(BG_COLOR)

        # Fondo sutil
        pygame.draw.rect(surface, BG_PANEL,
                         pygame.Rect(0, SCREEN_H - 160, SCREEN_W, 160))
        pygame.draw.line(surface, PANEL_BORDER,
                         (0, SCREEN_H - 160), (SCREEN_W, SCREEN_H - 160), 1)

        # HUD Superior
        self._draw_hud(surface)

        # Torres
        self._draw_towers(surface)

        # Discos
        self._draw_disks(surface)

        # Partículas
        for p in self.particles:
            alpha = int(255 * p[5] / p[6])
            r, g, b = p[4]
            pygame.draw.circle(surface, (r, g, b), (int(p[0]), int(p[1])), 5)

        # Botones
        self.btn_menu.draw(surface)
        self.btn_restart.draw(surface)

        # Mensaje error
        if self.error_msg and self.error_timer > 0:
            alpha_f = min(1.0, self.error_timer / 30)
            alpha = int(255 * alpha_f)
            err_surf = self.fonts["small"].render(self.error_msg, True,
                                                   ERROR_COLOR)
            er = err_surf.get_rect(centerx=SCREEN_W // 2, y=SCREEN_H - 130)
            surface.blit(err_surf, er)

        # Pantalla de completado
        if self.completado:
            self._draw_completion(surface)

    def _draw_hud(self, surface):
        # Dificultad
        diff_label = DIFICULTADES[self.dificultad]["label"]
        dt = self.fonts["heading"].render(f"Dificultad: {diff_label}", True, self.diff_color)
        surface.blit(dt, (30, 20))

        # Tiempo
        secs = self.elapsed
        mins = secs // 60
        s = secs % 60
        if mins > 0:
            t_str = f"{mins}m {s:02d}s"
        else:
            t_str = f"{s}s"

        time_label = self.fonts["small"].render("TIEMPO", True, TEXT_GRAY)
        surface.blit(time_label, (SCREEN_W // 2 - 40, 15))
        time_val = self.fonts["heading"].render(t_str, True, PRIMARY)
        tv_r = time_val.get_rect(centerx=SCREEN_W // 2, y=35)
        surface.blit(time_val, tv_r)

        # Usuario
        user_t = self.fonts["small"].render(self.usuario["nombre_usuario"], True, TEXT_GRAY)
        user_r = user_t.get_rect(right=SCREEN_W - 30, y=20)
        surface.blit(user_t, user_r)

        # Instrucciones
        if self.torre_seleccionada is not None:
            instr = f"Torre {self.torre_seleccionada + 1} seleccionada — Haz clic en la torre destino"
            ic = ACCENT
        else:
            instr = "Haz clic en una torre para seleccionar el disco superior"
            ic = TEXT_GRAY
        it = self.fonts["small"].render(instr, True, ic)
        ir = it.get_rect(centerx=SCREEN_W // 2, y=70)
        surface.blit(it, ir)

    def _draw_towers(self, surface):
        for i, tx in enumerate(TOWER_XS):
            selected = (i == self.torre_seleccionada)
            color = ACCENT if selected else (50, 60, 90)
            border = ACCENT if selected else PANEL_BORDER

            # Base
            base_rect = pygame.Rect(tx - BASE_W // 2, TOWER_Y - BASE_H, BASE_W, BASE_H)
            draw_rounded_rect(surface, color, base_rect, 6)
            if selected:
                draw_glow(surface, ACCENT, base_rect, 6, 50)

            # Palo
            pole_rect = pygame.Rect(tx - TOWER_W // 2, TOWER_Y - TOWER_H,
                                    TOWER_W, TOWER_H - BASE_H)
            draw_rounded_rect(surface, color, pole_rect, 4)

            # Número de torre
            nt = self.fonts["small"].render(f"Torre {i + 1}", True,
                                             ACCENT if selected else TEXT_DIM)
            nr = nt.get_rect(centerx=tx, y=TOWER_Y + 10)
            surface.blit(nt, nr)

    def _draw_disks(self, surface):
        for tower_i, stack in enumerate(self.game.torres):
            for j, disco in enumerate(stack):
                dw = self._disk_width(disco)
                tx = TOWER_XS[tower_i]
                dx = tx - dw // 2
                dy = TOWER_Y - BASE_H - (j + 1) * DISK_H

                is_top = (j == len(stack) - 1)
                is_selected = (tower_i == self.torre_seleccionada and is_top)

                if is_selected:
                    dy += int(self.anim_offset) - 10

                color = self._disk_color(disco)
                rect = pygame.Rect(dx, dy, dw, DISK_H - 4)

                if is_selected:
                    draw_glow(surface, color, rect, 8, 70)

                draw_rounded_rect(surface, color, rect, 8)
                # Highlight
                highlight = tuple(min(255, c + 60) for c in color)
                pygame.draw.rect(surface, highlight,
                                 pygame.Rect(dx + 6, dy + 3, dw - 12, 4),
                                 border_radius=2)
                # Número del disco
                dn = self.fonts["small"].render(str(disco), True, (0, 0, 0))
                dr = dn.get_rect(center=rect.center)
                surface.blit(dn, dr)

    def _draw_completion(self, surface):
        # Overlay semitransparente
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        panel = pygame.Rect(cx - 300, cy - 150, 600, 300)
        draw_glow(surface, SUCCESS, panel, 20, 60)
        draw_rounded_rect(surface, (15, 35, 25), panel, 20)
        draw_rounded_rect(surface, (0, 0, 0, 0), panel, 20,
                         border=2, border_color=SUCCESS)

        t1 = self.fonts["title"].render("¡Completado!", True, SUCCESS)
        t1r = t1.get_rect(centerx=cx, y=cy - 120)
        surface.blit(t1, t1r)

        secs = self.elapsed
        mins = secs // 60
        s = secs % 60
        t_str = f"{mins}m {s:02d}s" if mins > 0 else f"{secs}s"
        t2 = self.fonts["heading"].render(f"Tu tiempo: {t_str}", True, TEXT_WHITE)
        t2r = t2.get_rect(centerx=cx, y=cy - 40)
        surface.blit(t2, t2r)

        diff = DIFICULTADES[self.dificultad]["label"]
        t3 = self.fonts["body"].render(
            f"Dificultad {diff} — Tu mejor tiempo ha sido guardado", True, TEXT_GRAY)
        t3r = t3.get_rect(centerx=cx, y=cy + 20)
        surface.blit(t3, t3r)

        # Barra de progreso para el auto-cierre
        progress = self.completion_timer / 240
        bar_w = 400
        bar_rect = pygame.Rect(cx - bar_w // 2, cy + 80, int(bar_w * progress), 8)
        draw_rounded_rect(surface, (30, 60, 40), pygame.Rect(cx - bar_w // 2, cy + 80, bar_w, 8), 4)
        draw_rounded_rect(surface, SUCCESS, bar_rect, 4)

        hint = self.fonts["small"].render("Volviendo al menú automáticamente...", True, TEXT_DIM)
        hr = hint.get_rect(centerx=cx, y=cy + 100)
        surface.blit(hint, hr)
