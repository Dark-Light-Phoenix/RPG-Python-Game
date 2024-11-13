import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (220, 250, 210)

screen_sizes = [(800, 600), (1024, 768), (1280, 720), (1680, 1050)]
font_types = ["Times New Roman", "Lucida Calligraphy", "Script MT Bold", "Algerian"]

current_size = 0
current_font = 0
font_size = 24

WIDTH, HEIGHT = screen_sizes[current_size]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

font = pygame.font.SysFont(font_types[current_font], font_size)


class Button:
    def __init__(self, text, action, color=GREEN, font_color=BLACK):
        self.text = text
        self.action = action
        self.color = color
        self.font_color = font_color
        text_surface = font.render(self.text, True, self.font_color)
        self.width = text_surface.get_width() + 40
        self.height = text_surface.get_height() + 20
        self.rect = None

    def render(self, x, y):
        text_surface = font.render(self.text, True, self.font_color)
        self.rect = pygame.Rect(x, y, text_surface.get_width() + 40, text_surface.get_height() + 20)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text_surface, (self.rect.x + 20, self.rect.y + 10))

    def check_click(self, mouse_pos):
        if self.rect and self.rect.collidepoint(mouse_pos):
            self.action()


class Screen:
    def __init__(self, color=GRAY):
        self.color = color
        self.buttons = []

    def add_button(self, text, action, color=GREEN):
        button = Button(text, action, color)
        self.buttons.append(button)

    def render(self):
        screen.fill(self.color)
        total_height = sum(button.height + 20 for button in self.buttons) - 20
        y = (HEIGHT - total_height) // 2
        for button in self.buttons:
            button.render((WIDTH - button.width) // 2, y)
            y += button.height + 20

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_click(mouse_pos)


class ScreenManager:
    def __init__(self):
        self.screens = {}
        self.current_screen = None

    def add_screen(self, name, screen):
        self.screens[name] = screen

    def set_screen(self, name):
        self.current_screen = self.screens.get(name)

    def render(self):
        if self.current_screen:
            self.current_screen.render()

    def handle_events(self, event):
        if self.current_screen:
            self.current_screen.handle_events(event)


screen_manager = ScreenManager()

# Main Menu
main_menu = Screen(color=GRAY)
main_menu.add_button("New Game", lambda: screen_manager.set_screen("new_game"))
main_menu.add_button("Setting", lambda: screen_manager.set_screen("settings"))
main_menu.add_button("Exit", sys.exit, color=RED)

# New Game Menu
new_game = Screen(color=GRAY)
new_game.add_button("Start Game", lambda: screen_manager.set_screen("start_game"))
new_game.add_button("Select Character", lambda: screen_manager.set_screen("select_character"))
new_game.add_button("Select Difficulty", lambda: screen_manager.set_screen("select_difficulty"))
new_game.add_button("Back", lambda: screen_manager.set_screen("main_menu"))

# Settings Menu
def update_settings():
    settings.buttons.clear()
    settings.add_button(f"Change Window Resolution: {screen_sizes[current_size]}", change_window)
    settings.add_button(f"Change Font: {font_types[current_font]}", change_font)
    settings.add_button("Back", lambda: screen_manager.set_screen("main_menu"))

def change_window():
    global screen, WIDTH, HEIGHT, current_size
    current_size = (current_size + 1) % len(screen_sizes)
    WIDTH, HEIGHT = screen_sizes[current_size]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    update_settings()

def change_font():
    global font, current_font
    current_font = (current_font + 1) % len(font_types)
    font = pygame.font.SysFont(font_types[current_font], font_size)
    update_settings()

settings = Screen(color=GRAY)
update_settings()

# Select Character Menu
selected_class = ""

def select_character_class(name):
    global selected_class
    selected_class = name
    print(f"Selected class: {selected_class}")

select_character = Screen(color=GRAY)
select_character.add_button("Warrior", lambda: select_character_class("Warrior"))
select_character.add_button("Mage", lambda: select_character_class("Mage"))
select_character.add_button("Hunter", lambda: select_character_class("Hunter"))
select_character.add_button("Priest", lambda: select_character_class("Priest"))
select_character.add_button("Custom", lambda: select_character_class("Custom"))
select_character.add_button("Back", lambda: screen_manager.set_screen("new_game"))

# Custom Character Screen
class CustomCharacter(Screen):
    def __init__(self, color=GRAY):
        super().__init__(color)
        self.selected_name = ""
        self.selected_health = 150
        self.selected_abilities = []
        self.selected_items = []
        self.name_active = False
        self.description_active = False
        self.add_button("Save Character", self.save_character, color=GREEN)

    def render(self):
        screen.fill(self.color)
        title_surface = font.render("Creating Custom Character", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))
        self.draw_text_input_box(self.selected_name, 100, 100, 600, 50, GREEN, self.name_active)
        super().render()

    def draw_text_input_box(self, text, x, y, width, height, active_color, active):
        box_color = active_color if active else GRAY
        pygame.draw.rect(screen, box_color, (x, y, width, height))
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (x + 5, y + (height // 2 - text_surface.get_height() // 2)))

    def save_character(self):
        print(f"Custom Character Saved: {self.selected_name}")

custom_character = CustomCharacter()
screen_manager.add_screen("custom_character", custom_character)

# Screen Manager Setup
screen_manager.add_screen("main_menu", main_menu)
screen_manager.add_screen("new_game", new_game)
screen_manager.add_screen("settings", settings)
screen_manager.add_screen("select_character", select_character)
screen_manager.set_screen("main_menu")

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        screen_manager.handle_events(event)

    screen_manager.render()
    pygame.display.update()
import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (220, 250, 210)

screen_sizes = [(800, 600), (1024, 768), (1280, 720), (1680, 1050)]
font_types = ["Times New Roman", "Lucida Calligraphy", "Script MT Bold", "Algerian"]

current_size = 0
current_font = 0
font_size = 24

WIDTH, HEIGHT = screen_sizes[current_size]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

font = pygame.font.SysFont(font_types[current_font], font_size)


class Button:
    def __init__(self, text, action, color=GREEN, font_color=BLACK):
        self.text = text
        self.action = action
        self.color = color
        self.font_color = font_color
        self.rect = None

    def render(self, x, y):
        text_surface = font.render(self.text, True, self.font_color)
        self.rect = pygame.Rect(x, y, text_surface.get_width() + 40, text_surface.get_height() + 20)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text_surface, (self.rect.x + 20, self.rect.y + 10))

    def check_click(self, mouse_pos):
        if self.rect and self.rect.collidepoint(mouse_pos):
            self.action()


class Screen:
    def __init__(self, color=GRAY):
        self.color = color
        self.buttons = []

    def add_button(self, text, action, color=GREEN):
        button = Button(text, action, color)
        self.buttons.append(button)

    def render(self):
        screen.fill(self.color)
        y = (HEIGHT - sum([font.size(button.text)[1] + 20 for button in self.buttons])) // 2
        for button in self.buttons:
            button.render((WIDTH - button.rect.width) // 2, y)
            y += button.rect.height + 20

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_click(mouse_pos)


class ScreenManager:
    def __init__(self):
        self.screens = {}
        self.current_screen = None

    def add_screen(self, name, screen):
        self.screens[name] = screen

    def set_screen(self, name):
        self.current_screen = self.screens.get(name)

    def render(self):
        if self.current_screen:
            self.current_screen.render()

    def handle_events(self, event):
        if self.current_screen:
            self.current_screen.handle_events(event)


screen_manager = ScreenManager()

# Main Menu
main_menu = Screen(color=GRAY)
main_menu.add_button("New Game", lambda: screen_manager.set_screen("new_game"))
main_menu.add_button("Setting", lambda: screen_manager.set_screen("settings"))
main_menu.add_button("Exit", sys.exit, color=RED)

# New Game Menu
new_game = Screen(color=GRAY)
new_game.add_button("Start Game", lambda: screen_manager.set_screen("start_game"))
new_game.add_button("Select Character", lambda: screen_manager.set_screen("select_character"))
new_game.add_button("Select Difficulty", lambda: screen_manager.set_screen("select_difficulty"))
new_game.add_button("Back", lambda: screen_manager.set_screen("main_menu"))

# Settings Menu
def update_settings():
    settings.buttons.clear()
    settings.add_button(f"Change Window Resolution: {screen_sizes[current_size]}", change_window)
    settings.add_button(f"Change Font: {font_types[current_font]}", change_font)
    settings.add_button("Back", lambda: screen_manager.set_screen("main_menu"))

def change_window():
    global screen, WIDTH, HEIGHT, current_size
    current_size = (current_size + 1) % len(screen_sizes)
    WIDTH, HEIGHT = screen_sizes[current_size]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    update_settings()

def change_font():
    global font, current_font
    current_font = (current_font + 1) % len(font_types)
    font = pygame.font.SysFont(font_types[current_font], font_size)
    update_settings()

settings = Screen(color=GRAY)
update_settings()

# Select Character Menu
selected_class = ""

def select_character_class(name):
    global selected_class
    selected_class = name
    if name == "Custom":
        screen_manager.set_screen("custom_character")

select_character = Screen(color=GRAY)
select_character.add_button("Warrior", lambda: select_character_class("Warrior"))
select_character.add_button("Mage", lambda: select_character_class("Mage"))
select_character.add_button("Hunter", lambda: select_character_class("Hunter"))
select_character.add_button("Priest", lambda: select_character_class("Priest"))
select_character.add_button("Custom", custom_character)
select_character.add_button("Back", lambda: screen_manager.set_screen("new_game"))

# Class of Characters

class Character:
    def __init__(self, name, hp, abilities, start_item, description):
        self.name = name
        self.hp = hp
        self.abilities = abilities
        self.start_item = start_item
        self.description = description

characters = {
    "Warrior": Character (
        name = "Warrior",
        hp = "200",
        abilities = ["Strong attack", "Block"],
        start_item = ["Sword", "Shield", "Lather Chest"],
        description = "Strong and brave warrior, that can bear a lot of damage."
    ),
    "Mage": Character (
        name = "Mage",
        hp = "75",
        abilities = ["Magical Barrier", "Fireball", "Freeze"],
        start_item = ["Wooden Staff", "Cloak", "Book of Spells"],
        description = "Master of magic. Has a great knowledge and experience. Can deal a huge magical damage and support yourself."
    ),
    "Hunter": Character (
        name = "Hunter",
        hp = "120",
        abilities = ["Search", "Trap", "Hunting"],
        start_item = ["Wooden Bow", "Hood", "Leather Boots"],
        description = "Master of hunting. Very clever in using traps and searching hes enemies."
    ),
    "Priest": Character (
        name = "Priest",
        hp = "75",
        abilities = ["Pray", "Expel", "Hollow Strike"],
        start_item = ["Rod", "Cloak", "Mascot"],
        description = "Healer that use hollow spells against evil. Support everybody and heal all kind of wounds, including curses."
    ),
    "Custom": Character (
        name = "Unknown",
        hp = "Unknown",
        abilities = [],
        start_item = [],
        description = "Unknown"
    )
}

# Custom Character Screen
class CustomCharacter(Screen):
    def __init__(self, color=GRAY):
        super().__init__(color)
        self.selected_name = ""
        self.selected_health = 150
        self.selected_abilities = []
        self.selected_items = []
        self.name_active = False
        self.description_active = False
        self.add_button("Save Character", self.save_character, color=GREEN)

    def render(self):
        screen.fill(self.color)
        title_surface = font.render("Creating Custom Character", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))
        self.draw_text_input_box(self.selected_name, 100, 100, 600, 50, GREEN, self.name_active)
        super().render()

    def draw_text_input_box(self, text, x, y, width, height, active_color, active):
        box_color = active_color if active else GRAY
        pygame.draw.rect(screen, box_color, (x, y, width, height))
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (x + 5, y + (height // 2 - text_surface.get_height() // 2)))

    def save_character(self):
        print(f"Custom Character Saved: {self.selected_name}")

custom_character = CustomCharacter()
screen_manager.add_screen("custom_character", custom_character)

# Screen Manager Setup
screen_manager.add_screen("main_menu", main_menu)
screen_manager.add_screen("new_game", new_game)
screen_manager.add_screen("settings", settings)
screen_manager.add_screen("select_character", select_character)
screen_manager.set_screen("main_menu")

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        screen_manager.handle_events(event)

    screen_manager.render()
    pygame.display.update()
