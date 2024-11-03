from main import pygame

screen_sizes = [(800, 600), (1024, 768), (1280, 720), (1680, 1050)]
font_types = ["Times New Roman", "Lucida Calligraphy", "Script MT Bold", "Algerian"]

current_size = 0
current_font = 0
font_size = 24

#------------------------------------------------------------------------------------------------Functions for Changing Window Resolution and Font Type

def change_window():
    global screen, WIDTH, HEIGHT, current_size
    current_size = (current_size + 1) % len(screen_sizes)
    WIDTH, HEIGHT = screen_sizes[current_size]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

def change_font():
    global font, current_font
    current_font = (current_font + 1) % len(font_types)
    font = pygame.font.SysFont (font_types[current_font], font_size)