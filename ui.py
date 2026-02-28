import pygame
from constants import *


def draw_rounded_rect(surface, color, rect, radius=12, border=0, border_color=None):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)


def draw_glow(surface, color, rect, radius=12, intensity=60):
    glow_surf = pygame.Surface((rect[2] + 20, rect[3] + 20), pygame.SRCALPHA)
    r, g, b = color
    pygame.draw.rect(glow_surf, (r, g, b, intensity),
                     (10, 10, rect[2], rect[3]), border_radius=radius + 4)
    surface.blit(glow_surf, (rect[0] - 10, rect[1] - 10))


class Button:
    def __init__(self, x, y, w, h, text, color=None, text_color=None,
                 font=None, radius=10, outline=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color or PRIMARY_DARK
        self.hover_color = tuple(min(255, c + 40) for c in self.color)
        self.text_color = text_color or TEXT_WHITE
        self.font = font
        self.radius = radius
        self.outline = outline
        self.hovered = False
        self.clicked = False
        self._click_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                self._click_timer = 8
                return True
        return False

    def update(self):
        if self._click_timer > 0:
            self._click_timer -= 1
        else:
            self.clicked = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        if self.clicked:
            color = tuple(min(255, c + 80) for c in self.color)

        if self.hovered:
            draw_glow(surface, self.color, self.rect, self.radius, 50)

        draw_rounded_rect(surface, color, self.rect, self.radius)
        if self.outline:
            draw_rounded_rect(surface, color, self.rect, self.radius,
                              border=2, border_color=tuple(min(255, c + 60) for c in self.color))

        if self.font:
            txt = self.font.render(self.text, True, self.text_color)
            tr = txt.get_rect(center=self.rect.center)
            surface.blit(txt, tr)


class InputField:
    def __init__(self, x, y, w, h, placeholder="", font=None, password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.placeholder = placeholder
        self.font = font
        self.password = password
        self.text = ""
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE):
                if len(self.text) < 30:
                    self.text += event.unicode

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, surface):
        border_color = PRIMARY if self.active else PANEL_BORDER
        draw_rounded_rect(surface, BG_PANEL, self.rect, 8)
        draw_rounded_rect(surface, (0, 0, 0, 0), self.rect, 8,
                         border=2, border_color=border_color)

        if self.font:
            display = ("•" * len(self.text)) if self.password else self.text
            if display:
                txt = self.font.render(display, True, TEXT_WHITE)
            else:
                txt = self.font.render(self.placeholder, True, TEXT_DIM)
            surface.blit(txt, (self.rect.x + 14, self.rect.y + (self.rect.h - txt.get_height()) // 2))

            if self.active and self.cursor_visible:
                cx = self.rect.x + 14
                if display:
                    cw = self.font.size(display)[0]
                    cx += cw
                cy = self.rect.y + 10
                pygame.draw.line(surface, PRIMARY, (cx, cy), (cx, cy + self.rect.h - 20), 2)
