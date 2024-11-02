import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1680, 1050
screen = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption ("Main Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (220, 250, 210)

font = pygame.font.SysFont (None, 40)
small_font = pygame.font.SysFont(None, 30)

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
        print(f"Changing Screen on: {name}")

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

setting = Screen(color = GRAY)
setting.add_button("Change Window", change_window)
setting.add_button("Change Font", change_font)
setting.add_button("Back", lambda: screen_manager.set_screen("main_menu"))

#------------------------------------------------------------------------------------------------Select Character Menu

start_game = Screen(color = GRAY)

#------------------------------------------------------------------------------------------------Select Character Menu

select_character = Screen(color = GRAY)
select_character.add_button("Warrior", select_warrior)
select_character.add_button("Mage", select_mage)
select_character.add_button("Hunter", select_hunter)
select_character.add_button("Priest", select_priest)
select_character.add_button("Custom", select_custom)
select_character.add_button("Back", lambda: screen_manager.set_screen("new_game"))

#------------------------------------------------------------------------------------------------Class of Characters

class Character:
    def __init__(self, name, hp, abilities, start_item, description):
        self.name = name
        self.hp = hp
        self.abilities = abilities
        self.start_item = start_item
        self.descritption = description

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

#------------------------------------------------------------------------------------------------Functions for Custom Character

selected_name = ""
selected_abilities = []
selected_items = []
selected_health = 150
selected_description = ""

available_abilities = ["Fireball", "Freeze", "Magical Barrier", "Search", "Pray", "Hollow Strike", "Block", "Hunting", "Dispel curse", "Heal", "Expel"]
available_items = ["Shield", "Sword", "Wooden Bow", "Wooden Staff", "Cloak", "Leather Chest", "Hood", "Leather Boots", "Mascot"]

MAX_ITEMS = 3
MAX_ABILITIES = 3
MAX_NAME_LENGTH = 12
MAX_DESCRIPTION_LENGTH = 30

def create_custom_character():
    global selected_health, selected_name, selected_description
    name_active = False
    description_active = False

    screen.fill(GRAY)

    title_surface = font.render ("Creating Custom Character", True, BLACK)
    screen.blit (title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

    draw_text_input_box(selected_name, 100, 100, 600, 50, GREEN, GRAY, name_active)
    name_label = font.render("Name of Character:", True, BLACK)
    screen.blit (name_label, (100, 60))
    draw_text_input_box(selected_name, 100, 100, 600, 50, GREEN, GRAY, name_active)

    health_label = font.render (f"Health: {selected_health}", True, BLACK)
    screen.blit (health_label, (100, 200))
    draw_health_slider()

    ability_label = font.render ("Choose Abilities:", True, BLACK)
    screen.blit (ability_label, (100, 300))
    for idx, ability in enumerate (available_abilities):
        draw_button (ability, 100, 250 + idx * 50, 200, 40, GRAY, GREEN, lambda a = ability: select_ability (a))

    item_label = font.render ("Choose Items:", True, BLACK)
    screen.blit (item_label, (400, 300))
    for idx, item in enumerate (available_items):
        draw_button (item, 400, 250 + idx * 50, 200, 40, GRAY, GREEN, lambda i = item: select_item (i))

    draw_text_input_box(selected_description, 100, 200, 600, 50, GREEN, GRAY, description_active)
    description_label = font.render("Description of Character:", True, BLACK)
    screen.blit(description_label, (100, 160))
    draw_text_input_box(selected_description, 100, 650, 600, 50, GREEN, GRAY, description_active)

    draw_button ("Save Character", 300, 500, 200, 50, GRAY, GREEN, save_character)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if 100 <= event.pos [0] <= 700 and 100 <= event.pos [1] <= 150:
            name_active = True
            description_active = False
        elif 100 <= event.pos [0] <= 700 and 200 <= event.pos [1] <= 250:
            description_active = True
            name_active = False
        else:
            name_active = False
            description_active = False

    if event.type == pygame.KEYDOWN:
        if name_active:
            if event.key == pygame.K_BACKSPACE:
                selected_name = selected_name [:-1]
            elif len (selected_name) < MAX_NAME_LENGTH:
                selected_name += event.unicode
        if description_active:
            if event.key == pygame.K_BACKSPACE:
                selected_description = selected_description [:-1]
            elif len (selected_description) < MAX_DESCRIPTION_LENGTH:
                selected_description += event.unicode

def draw_text_input_box(text, x, y, width, height, active_color, inactive_color, active):
    box_color = active_color if active else inactive_color
    pygame.draw.rect(screen, box_color, (x, y, width, height))

    text_surface = font.render(text, True, BLACK)
    screen.blit (text_surface, (x + 5, y + (height // 2 - text_surface.get_height() // 2)))

def draw_health_slider():
    global selected_health
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    slider_x = 150
    slider_y = 140
    slider_width = 500
    slider_height = 20
    slider_color = GREEN

    pygame.draw.rect (screen, slider_color, (slider_x, slider_y, slider_width, slider_height))

    handle_x = slider_x + (selected_health - 50) * 5
    handle_width = 10

    pygame.draw.rect (screen, RED, (handle_x, slider_y - 5, handle_width, slider_height + 10))

    if click [0] == 1 and slider_x <= mouse [0] <= slider_x + slider_width:
        selected_health = 50 + (mouse [0] - slider_x) // 5

def select_ability(ability):
    global selected_abilities
    if ability in selected_abilities:
        selected_abilities.remove (ability)
        print(f"Deleted: {ability}")
    elif len (selected_abilities) < MAX_ABILITIES:
        selected_abilities.append (ability)
        print (f"Added: {ability}")

def select_item(item):
    global selected_items
    if item in selected_items:
        selected_items.remove (item)
        print (f"Deleted: {item}")
    elif len (selected_items) < MAX_ITEMS:
        selected_items.append (item)
        print (f"Added: {item}")

def save_character():
    print (f"Character Created with those Parameters:")
    if len (selected_name) > MAX_NAME_LENGTH:
        print ("Name is too long")
    else:
        print (f"Character Name: {selected_name}")
    print (f"Health: {selected_health}")
    print (f"Chosen Abilities: {selected_abilities}")
    print (f"Chosen Items: {selected_items}")
    if len (selected_description) > MAX_DESCRIPTION_LENGTH:
        print ("Description is too long")
    else:
        print (f"Character Description: {selected_description}")

#------------------------------------------------------------------------------------------------Selecting Difficulty Menu

selected_class = None
selected_map = None
selected_difficulty = None

select_difficulty = Screen(color = GRAY)
select_difficulty.add_button("Easy", select_easy)
select_difficulty.add_button("Medium", select_medium)
select_difficulty.add_button("Hard", select_hard)
select_difficulty.add_button("Insane", select_insane)
select_difficulty.add_button("Back", lambda: screen_manager.set_screen("new_game"))

#------------------------------------------------------------------------------------------------Screen Manager Settings

screen_manager.add_screen("main_menu", main_menu)

screen_manager.add_screen("settings", setting)
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