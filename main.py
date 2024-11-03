from Characters import *
from Settings import *
from Difficulty import *

import pygame
import sys

pygame.init()

WIDTH, HEIGHT = screen_sizes[current_size]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption ("Main Menu")

font = pygame.font.SysFont (font_types[current_font], font_size)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (220, 250, 210)

#------------------------------------------------------------------------------------------------Classes for Button, Screen and Positions

class Button:
    def __init__ (self, text, action, color = GREEN, font_color = BLACK):
        self.text = text
        self.action = action
        self.color = color
        self.font_color = font_color
        self.rect = None

    def render (self, x, y):
        text_surface = font.render(self.text, True, self.font_color)
        self.rect = pygame.Rect(x, y, text_surface.get_width() + 40, text_surface.get_height() + 20)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text_surface, (self.rect.x + 20, self.rect.y + 10))

    def check_click(self, mouse_pos):
        if self.rect and self.rect.collidepoint(mouse_pos):
            self.action()

class Screen:
    def __init__ (self, color = GRAY):
        self.color = color
        self.buttons = []

    def add_button(self, text, action, color = GREEN):
        button = Button (text, action, color)
        self.buttons.append(button)

    def render(self):
        screen.fill(self.color)
        total_height = sum(button.rect.height + 20 for button in self.buttons if button.rect) - 20
        y = (HEIGHT - total_height) // 2

        for button in self.buttons:
            button.render((WIDTH - button.rect.width) // 2, y)
            y += button.rect.height + 20

    def handle_event(self):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_click(mouse_pos)

class ScreenManager:
    def __init__ (self):
        self.screen = []
        self.current_screen = None

    def add_screen(self, name, screen):
        self.screen[name] = screen

    def set_screen(self, name):
        self.current_screen = self.current_screen.get(name)

    def render(self):
        if self.current_screen:
            self.current_screen.render()

    def handle_events(self, event):
        if self.current_screen:
            self.current_screen.handle_events(event)

screen_manager = ScreenManager()

#------------------------------------------------------------------------------------------------Main Menu

main_menu = Screen(color = GRAY)
main_menu.add_button("New Game", lambda: screen_manager.set_screen("new_game"))
main_menu.add_button("Setting", lambda: screen_manager.set_screen("settings"))
main_menu.add_button("Exit", sys.exit, color = RED)

#------------------------------------------------------------------------------------------------New Game Menu

new_game = Screen(color = GRAY)
new_game.add_button("Start Game", lambda: screen_manager.set_screen("start_game"))
new_game.add_button("Select Character", lambda: screen_manager.set_screen("select_character"))
new_game.add_button("Select Difficulty", lambda: screen_manager.set_screen("select_difficulty"))
new_game.add_button("Back", lambda: screen_manager.set_screen("main_menu"))

#------------------------------------------------------------------------------------------------Setting Menu

settings = Screen(color = GRAY)
settings.add_button(f"Change Window Resolution: {current_size}", change_window)
settings.add_button(f"Change Font: {current_font}", change_font)
settings.add_button("Back", lambda: screen_manager.set_screen("main_menu"))

start_game = Screen(color = GRAY)

#------------------------------------------------------------------------------------------------Select Character Menu

select_character = Screen(color = GRAY)
select_character.add_button("Warrior", select_warrior)
select_character.add_button("Mage", select_mage)
select_character.add_button("Hunter", select_hunter)
select_character.add_button("Priest", select_priest)
select_character.add_button("Custom", select_custom)
select_character.add_button("Back", lambda: screen_manager.set_screen("new_game"))

#------------------------------------------------------------------------------------------------Selecting Difficulty Menu

selected_difficulty = None

select_difficulty = Screen(color = GRAY)
select_difficulty.add_button("Easy", select_easy)
select_difficulty.add_button("Medium", select_medium)
select_difficulty.add_button("Hard", select_hard)
select_difficulty.add_button("Insane", select_insane)
select_difficulty.add_button("Back", lambda: screen_manager.set_screen("new_game"))

#------------------------------------------------------------------------------------------------Screen Manager Settings

screen_manager.add_screen("main_menu", main_menu)

screen_manager.add_screen("settings", settings)
screen_manager.add_screen("change_window", change_window)
screen_manager.add_screen("change_font", change_font)

screen_manager.add_screen("new_game", new_game)
screen_manager.add_screen("start_game", start_game)
screen_manager.add_screen("select_character", select_character)
screen_manager.add_screen("select_difficulty", select_difficulty)


screen_manager.set_screen("main_menu")

#------------------------------------------------------------------------------------------------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        screen_manager.handle_events(event)

    screen_manager.render()
    pygame.display.update()