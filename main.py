import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (220, 250, 210)

screen_sizes = [(800, 600), (1024, 768), (1280, 720), (1680, 1050), (1920, 1080)]
font_types = ["Times New Roman", "Lucida Calligraphy", "Palace Script MT", "Algerian"]

current_size = 0
current_font = 0
font_size = 24
screen_mode = "Windowed"

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
        self.character_data = {
            "name": "",
            "health": 0,
            "abilities": [],
            "items": [],
            "description": ""
        }

class NameHealthStep(CustomCharacter):
    def __init__(self, color=GRAY):
        super().__init__(color)
        self.name_active = False
        self.dragging = False
        self.add_button("Return", self.return_step, color=GREEN)
        self.add_button("Next", self.next_step, color=GREEN)

    def render(self):
        screen.fill(self.color)
        title_surface = font.render("Step 1: Choose Name of Character and Amount of Health Points", True, BLACK)
        screen.blit(title_surface, ((WIDTH - title_surface.get_width()) // 2, HEIGHT // 10))

        name_label_y = HEIGHT // 4
        name_label = font.render("Name:", True, BLACK)
        name_label_x = (WIDTH - (name_label.get_width() + 10 + (WIDTH // 2))) // 2
        screen.blit(name_label, (name_label_x, name_label_y))

        name_box_x = name_label_x + name_label.get_width() + 10
        name_box_width = WIDTH // 2
        name_box_height = HEIGHT // 15
        self.draw_text_input_box(self.character_data["name"], name_box_x, name_label_y, name_box_width, name_box_height, WHITE, self.name_active)

        health_label_y = name_label_y + HEIGHT // 6
        health_label = font.render(f"Health: {self.character_data['health']}", True, BLACK)
        screen.blit(health_label, (WIDTH // 8, health_label_y))

        slider_y = health_label_y + HEIGHT // 12
        self.draw_health_label(slider_y)

        button_y = slider_y + HEIGHT // 15 + 30
        if len(self.buttons) >= 2:
            self.buttons[0].render((WIDTH // 2) - self.buttons[0].width - 20, button_y)
            self.buttons[1].render((WIDTH // 2) + 20, button_y)


    def draw_text_input_box(self, text, x, y, width, height, active_color, active):
        box_color = active_color if active else RED
        pygame.draw.rect(screen, box_color, (x, y, width, height))
        display_text = text if text else ""
        text_surface = font.render(display_text, True, BLACK)
        screen.blit(text_surface, (x + 5, y + (height // 2 - text_surface.get_height() // 2)))

    def draw_health_label(self, slider_y):
        slider_x = WIDTH // 8
        slider_width = WIDTH // 2
        slider_height = HEIGHT // 30
        min_health, max_health = 1, 150
        pygame.draw.rect(screen, GREEN, (slider_x, slider_y, slider_width, slider_height))

        handle_x = slider_x + (self.character_data["health"] - min_health) * (slider_width / (max_health - min_health))
        handle_rect = pygame.Rect(handle_x, slider_y - 5, 10, slider_height + 10)
        pygame.draw.rect(screen, RED, handle_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if mouse_pressed and handle_rect.collidepoint(mouse_x, mouse_y) and not self.dragging:
            self.dragging = True

        if self.dragging:
            if slider_x <= mouse_x <= slider_width + slider_x:
                self.character_data["health"] = min_health + int((mouse_x - slider_x) / slider_width * (max_health - min_health))
                self.character_data["health"] = max(min_health, min(max_health, self.character_data["health"]))

        if not mouse_pressed:
            self.dragging = False

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            name_box_x = (WIDTH - (WIDTH // 2)) // 2 + 80
            name_box_y = HEIGHT // 4
            name_box_width = WIDTH // 2
            name_box_height = HEIGHT // 15
            self.name_active = name_box_x <= mouse_pos[0] <= name_box_x + name_box_width and name_box_y <= mouse_pos[1] <= name_box_y + name_box_height

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_click(mouse_pos)

        if event.type == pygame.KEYDOWN and self.name_active:
            if event.key == pygame.K_BACKSPACE:
                self.character_data["name"] = self.character_data["name"][:-1]
        elif len(self.character_data["name"]) < 12:
                if hasattr(event, 'unicode'):
                    self.character_data["name"] += event.unicode

    def return_step(self):
        screen_manager.set_screen("select_character")

    def next_step(self):
        screen_manager.set_screen("abilities_step")

class AbilitiesStep(CustomCharacter):
    def __init__(self, color=GRAY):
        super().__init__(color)
        self.available_abilities = ["Fireball", "Freeze", "Shield Block", "Heal", "Hunting"]

        self.buttons = []

        for ability in self.available_abilities:
            self.add_button(ability, lambda a=ability: self.select_ability(a), color=GRAY)

        self.add_button("Back", self.prev_step, color=GREEN)
        self.add_button("Next", self.next_step, color=GREEN)

    def render(self):
        screen.fill(self.color)
        title_surface = font.render("Step 2: Choose Abilities", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

        button_spacing = 20
        total_width = sum(button.width + button_spacing for button in self.buttons[:len(self.available_abilities)]) - button_spacing
        x = (WIDTH - total_width) // 2
        y = HEIGHT // 2 - 50
        for idx, button in enumerate(self.buttons[:len(self.available_abilities)]):
            button.render(x, y)
            x += button.width + 20

        nav_total_width = self.buttons[-2].width + self.buttons[-1].width + button_spacing
        nav_x = (WIDTH - nav_total_width) // 2
        nav_y = y + 80
        self.buttons[-2].render(nav_x, nav_y)
        self.buttons[-1].render(nav_x + self.buttons[-2].width + button_spacing, nav_y)

    def select_ability(self, ability):
        if ability in self.character_data["abilities"]:
            self.character_data["abilities"].remove(ability)
        elif len(self.character_data["abilities"]) < 3:
            self.character_data["abilities"].append(ability)
        print("Selected abilities:", self.character_data["abilities"])

    def next_step(self):
        screen_manager.set_screen("items_step")

    def prev_step(self):
        screen_manager.set_screen("name_health_step")

class ItemsStep(CustomCharacter):
    def __init__(self, color=GRAY):
        super().__init__(color)
        self.available_items = ["Sword", "Shield", "Bow", "Staff", "Armor"]

        self.buttons = []

        for item in self.available_items:
            self.add_button(item, lambda i=item: self.select_item(i), color=GRAY)

        self.add_button("Back", self.prev_step, color=GREEN)
        self.add_button("Next", self.next_step, color=GREEN)

    def render(self):
        screen.fill(self.color)
        title_surface = font.render("Step 3: Choose Items", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

        button_spacing = 20
        total_width = sum(button.width + button_spacing for button in self.buttons[:len(self.available_items)]) - button_spacing
        x = (WIDTH - total_width) // 2
        y = HEIGHT // 2 - 50
        for idx, button in enumerate(self.buttons[:len(self.available_items)]):
            button.render(x, y)
            x += button.width + 20

        nav_total_width = self.buttons[-2].width + self.buttons[-1].width + button_spacing
        nav_x = (WIDTH - nav_total_width) // 2
        nav_y = y + 80
        self.buttons[-2].render(nav_x, nav_y)
        self.buttons[-1].render(nav_x + self.buttons[-2].width + button_spacing, nav_y)

    def select_item(self, item):
        if item in self.character_data["items"]:
            self.character_data["items"].remove(item)
        elif len(self.character_data["items"]) < 3:
            self.character_data["items"].append(item)
        print("Selected Items:", self.character_data["items"])

    def next_step(self):
        screen_manager.set_screen("description_step")

    def prev_step(self):
        screen_manager.set_screen("abilities_step")

class DescriptionStep(CustomCharacter):
    def __init__(self, color=GRAY):
        super().__init__(color)
        self.description_active = False
        self.add_button("Back", self.prev_step, color=GREEN)
        self.add_button("Finish", self.finish, color=GREEN)
        self.text_font = pygame.font.SysFont(font_types[current_font], 16)

    def render(self):
        screen.fill(self.color)
        title_surface = font.render("Step 4: Enter Description", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

        box_x, box_y = WIDTH // 10, HEIGHT // 5
        box_width, box_height = WIDTH - 2 * (WIDTH // 10), HEIGHT // 3
        self.draw_text_input_box(self.character_data["description"], box_x, box_y, box_width, box_height, WHITE, self.description_active)
        description_label = font.render("Description:", True, BLACK)
        screen.blit(description_label, (box_x, box_y - 40))

        button_y = box_y + box_height + 20
        if self.buttons:
            self.buttons[0].render((WIDTH // 2) - self.buttons[0].width - 20, button_y)
            self.buttons[1].render((WIDTH // 2) + 20, button_y)

    def draw_text_input_box(self, text, x, y, width, height, active_color, active):
        box_color = active_color if active else RED
        pygame.draw.rect(screen, box_color, (x, y, width, height))

        words = text.split(' ')
        line = ""
        y_offset = y + 5
        line_height = self.text_font.get_height()

        for word in words:
            test_line = line + word + " "
            test_surface = self.text_font.render(test_line, True, BLACK)
            if test_surface.get_width() > width - 10:
                rendered_line = self.text_font.render(line, True, BLACK)
                screen.blit(rendered_line, (x + 5, y_offset))
                y_offset += line_height
                line = word + " "
            else:
                line = test_line

        rendered_line = self.text_font.render(line, True, BLACK)
        screen.blit(rendered_line, (x + 5, y_offset))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            box_x, box_y, box_width, box_height = WIDTH // 10, HEIGHT // 5, WIDTH - 2 * (WIDTH // 10), HEIGHT // 3
            self.description_active = box_x <= mouse_pos[0] <= box_x + box_width and box_y <= mouse_pos[1] <= box_y + box_height

        if event.type == pygame.KEYDOWN and self.description_active:
            if event.key == pygame.K_BACKSPACE:
                self.character_data["description"] = self.character_data["description"][:-1]
            elif len(self.character_data["description"]) < 200:
                if hasattr(event, 'unicode'):
                    self.character_data["description"] += event.unicode

    def finish(self):
        screen_manager.set_screen("summary_step")

    def prev_step(self):
        screen_manager.set_screen("items_step")

class SummaryStep(CustomCharacter):
    def __init__(self, color=GRAY):
        super().__init__(color)
        self.add_button("Back to Select Character", lambda: screen_manager.set_screen("select_character"), color=GREEN)

    def render(self):
        screen.fill(self.color)
        title_surface = font.render("Character Summary", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

        summary_text = [
            f"Name: {self.character_data['name']}",
            f"Health: {self.character_data['health']}",
            f"Abilities: {', '.join(self.character_data['abilities'])}",
            f"Items: {', '.join(self.character_data['items'])}",
            f"Description: {self.character_data['description']}"
        ]
        y_offset = 100
        for line in summary_text:
            line_surface = font.render(line, True, BLACK)
            screen.blit(line_surface, (100, y_offset))
            y_offset += 40

        super().render()


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
    settings.add_button(f"Screen Mode: {screen_mode}", toggle_screen_mode)
    settings.add_button("Back", lambda: screen_manager.set_screen("main_menu"))

def change_window():
    global screen, WIDTH, HEIGHT, current_size
    current_size = (current_size + 1) % len(screen_sizes)
    WIDTH, HEIGHT = screen_sizes[current_size]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    update_display()
    update_settings()

def change_font():
    global font, current_font
    current_font = (current_font + 1) % len(font_types)
    font = pygame.font.SysFont(font_types[current_font], font_size)
    update_settings()

def toggle_screen_mode():
    global screen_mode
    screen_mode = {
        "Windowed": "Fullscreen",
        "Fullscreen": "Borderless",
        "Borderless": "Windowed"
    } [screen_mode]
    update_display()
    update_settings()

def update_display():
    global screen
    flags = 0
    if screen_mode == "Fullscreen":
        flags = pygame.FULLSCREEN
    elif screen_mode == "Borderless":
        flags = pygame.NOFRAME
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

settings = Screen(color=GRAY)
update_settings()

# Select Difficulty Menu
selected_difficulty = ""

def toggle_select_difficulty():
    select_difficulty.buttons.clear()
    select_difficulty.add_button("Select Easy", select_easy)
    select_difficulty.add_button("Select Medium", select_medium)
    select_difficulty.add_button("Select Hard", select_hard)
    select_difficulty.add_button("Select Insane", select_insane)
    select_difficulty.add_button("Back", lambda: screen_manager.set_screen("new_game"))

def select_easy():
    global selected_difficulty
    selected_difficulty = ""
    print(f"Difficulty: {selected_difficulty}")

def select_medium():
    global selected_difficulty
    selected_difficulty = ""
    print(f"Difficulty: {selected_difficulty}")

def select_hard():
    global selected_difficulty
    selected_difficulty = ""
    print(f"Difficulty: {selected_difficulty}")

def select_insane():
    global selected_difficulty
    selected_difficulty = ""
    print(f"Difficulty: {selected_difficulty}")

select_difficulty = Screen(color = GRAY)
toggle_select_difficulty()

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
select_character.add_button("Custom", lambda: screen_manager.set_screen("name_health_step"))
select_character.add_button("Back", lambda: screen_manager.set_screen("new_game"))

# Initialization Screens
name_health_step = NameHealthStep()
abilities_step = AbilitiesStep()
items_step = ItemsStep()
description_step = DescriptionStep()
summary_step = SummaryStep()

# Screen Manager Setup
screen_manager.add_screen("main_menu", main_menu)
screen_manager.add_screen("new_game", new_game)
screen_manager.add_screen("settings", settings)
screen_manager.add_screen("select_character", select_character)
screen_manager.add_screen("select_difficulty", select_difficulty)
screen_manager.add_screen("name_health_step", name_health_step)
screen_manager.add_screen("abilities_step", abilities_step)
screen_manager.add_screen("items_step", items_step)
screen_manager.add_screen("description_step", description_step)
screen_manager.add_screen("summary_step", summary_step)
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
