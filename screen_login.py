import pygame
from constants import *
from ui import Button, InputField, draw_rounded_rect, draw_glow
from database import registrar_usuario, login_usuario


class LoginScreen:
    def __init__(self, fonts):
        self.fonts = fonts
        self.mode = "login"   # "login" or "register"
        self.message = ""
        self.message_color = ERROR_COLOR
        self.message_timer = 0

        cx = SCREEN_W // 2
        panel_w = 480
        panel_x = cx - panel_w // 2

        self.input_user = InputField(panel_x + 40, 310, panel_w - 80, 52,
                                     "Nombre de usuario", fonts["body"])
        self.input_pass = InputField(panel_x + 40, 385, panel_w - 80, 52,
                                     "Contraseña", fonts["body"], password=True)

        self.btn_submit = Button(panel_x + 40, 465, panel_w - 80, 52,
                                 "Iniciar Sesión", PRIMARY_DARK, TEXT_WHITE,
                                 fonts["body"], radius=10)

        self.btn_toggle = Button(panel_x + 40, 535, panel_w - 80, 44,
                                 "¿No tienes cuenta? Regístrate",
                                 BG_PANEL, PRIMARY, fonts["small"], radius=10, outline=True)

        self.panel_rect = pygame.Rect(panel_x, 240, panel_w, 360)
        self.stars = self._make_stars()

    def _make_stars(self):
        import random
        return [(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H),
                 random.randint(1, 3), random.random()) for _ in range(120)]

    def set_mode(self, mode):
        self.mode = mode
        if mode == "login":
            self.btn_submit.text = "Iniciar Sesión"
            self.btn_toggle.text = "¿No tienes cuenta? Regístrate"
        else:
            self.btn_submit.text = "Crear Cuenta"
            self.btn_toggle.text = "¿Ya tienes cuenta? Inicia Sesión"
        self.input_user.text = ""
        self.input_pass.text = ""
        self.message = ""

    def show_message(self, msg, color=None):
        self.message = msg
        self.message_color = color or ERROR_COLOR
        self.message_timer = 180

    def handle_events(self, events):
        for event in events:
            self.input_user.handle_event(event)
            self.input_pass.handle_event(event)

            if self.btn_submit.handle_event(event):
                return self._on_submit()

            if self.btn_toggle.handle_event(event):
                self.set_mode("register" if self.mode == "login" else "login")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return self._on_submit()

        return None

    def _on_submit(self):
        user = self.input_user.text.strip()
        pwd = self.input_pass.text.strip()

        if not user or not pwd:
            self.show_message("Completa todos los campos")
            return None

        if self.mode == "login":
            usuario, msg = login_usuario(user, pwd)
            if usuario:
                self.show_message("¡Bienvenido!", SUCCESS)
                return ("goto_menu", usuario)
            else:
                self.show_message(msg)
        else:
            if len(user) < 3:
                self.show_message("El usuario debe tener al menos 3 caracteres")
                return None
            if len(pwd) < 3:
                self.show_message("La contraseña debe tener al menos 3 caracteres")
                return None
            ok, msg = registrar_usuario(user, pwd)
            if ok:
                self.show_message("¡Registrado! Ahora inicia sesión", SUCCESS)
                self.set_mode("login")
            else:
                self.show_message(msg)
        return None

    def update(self):
        self.input_user.update()
        self.input_pass.update()
        self.btn_submit.update()
        self.btn_toggle.update()
        if self.message_timer > 0:
            self.message_timer -= 1

    def draw(self, surface):
        surface.fill(BG_COLOR)

        # Estrellas de fondo
        for x, y, r, alpha in self.stars:
            c = int(alpha * 180)
            pygame.draw.circle(surface, (c, c, c + 30), (x, y), r)

        # Título
        title = self.fonts["title"].render("Torre de Hanói", True, TEXT_WHITE)
        tr = title.get_rect(centerx=SCREEN_W // 2, y=80)
        surface.blit(title, tr)

        sub = self.fonts["body"].render("El desafío clásico de lógica y paciencia", True, TEXT_GRAY)
        sr = sub.get_rect(centerx=SCREEN_W // 2, y=150)
        surface.blit(sub, sr)

        # Panel
        draw_glow(surface, PRIMARY_DARK, self.panel_rect, 16, 30)
        draw_rounded_rect(surface, BG_PANEL, self.panel_rect, 16)
        draw_rounded_rect(surface, (0, 0, 0, 0), self.panel_rect, 16,
                         border=1, border_color=PANEL_BORDER)

        # Encabezado panel
        mode_text = "Iniciar Sesión" if self.mode == "login" else "Crear Cuenta"
        ht = self.fonts["heading"].render(mode_text, True, TEXT_WHITE)
        hr = ht.get_rect(centerx=SCREEN_W // 2, y=self.panel_rect.y + 24)
        surface.blit(ht, hr)

        # Labels
        lbl_u = self.fonts["small"].render("Usuario", True, TEXT_GRAY)
        surface.blit(lbl_u, (self.input_user.rect.x, self.input_user.rect.y - 22))
        lbl_p = self.fonts["small"].render("Contraseña", True, TEXT_GRAY)
        surface.blit(lbl_p, (self.input_pass.rect.x, self.input_pass.rect.y - 22))

        self.input_user.draw(surface)
        self.input_pass.draw(surface)
        self.btn_submit.draw(surface)
        self.btn_toggle.draw(surface)

        # Mensaje
        if self.message and self.message_timer > 0:
            alpha = min(255, self.message_timer * 3)
            msg_surf = self.fonts["small"].render(self.message, True, self.message_color)
            mr = msg_surf.get_rect(centerx=SCREEN_W // 2,
                                   y=self.panel_rect.bottom - 28)
            surface.blit(msg_surf, mr)
