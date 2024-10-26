import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1680, 1050
screen = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption ("Головне меню")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (250, 250, 250)

font = pygame.font.SysFont (None, 40)
small_font = pygame.font.SysFont(None, 30)

#------------------------------------------------------------------------------------------------Function of drawing button

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x + (width / 2 - text_surface.get_width() / 2),
                               y + (height / 2 - text_surface.get_height() / 2)))

#------------------------------------------------------------------------------------------------New Game Menu

selected_class = None
selected_map = None
selected_difficulty = None

def NewGame():
    while True:
        screen.fill(WHITE)

        draw_button("Почати гру", 300, 150, 200, 50, GREEN, RED, start_game)
        draw_button("Вибрати складність", 300, 250, 200, 50, GREEN, RED, select_difficulty)
        draw_button("Вибрати клас персонажа", 300, 350, 200, 50, GREEN, RED, select_character)
        draw_button("Вибрати розмір карти", 300, 450, 200, 50, GREEN, RED, select_map)
        draw_button("Назад", 300, 550, 200, 50, GREEN, RED, main_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


#------------------------------------------------------------------------------------------------Selecting Difficulty Menu

def select_difficulty():
    while True:
        screen.fill(WHITE)

        draw_button ("Легкий", 300, 150, 200, 50, GREEN, RED, select_easy)
        draw_button("Середній", 300, 250, 200, 50, GREEN, RED, select_medium)
        draw_button("Важкий", 300, 350, 200, 50, GREEN, RED, select_hard)
        draw_button("Назад", 300, 450, 200, 50, GREEN, RED, NewGame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def select_easy():
    global selected_difficulty
    selected_difficulty = "Легкий"
    print(f"Вибраний рівень складності: {selected_difficulty}")

def select_medium():
    global selected_difficulty
    selected_difficulty = "Середній"
    print(f"Вибраний рівень складності: {selected_difficulty}")

def select_hard():
    global selected_difficulty
    selected_difficulty = "Важкий"
    print(f"Вибраний рівень складності: {selected_difficulty}")

#------------------------------------------------------------------------------------------------Selecting Character Menu

def select_character():
    while True:
        screen.fill(WHITE)

        draw_button ("Воїн", 300, 150, 200, 50, GREEN, RED, select_warrior)
        draw_button("Маг", 300, 250, 200, 50, GREEN, RED, select_mage)
        draw_button("Мисливець", 300, 350, 200, 50, GREEN, RED, select_hunter)
        draw_button("Священник", 300, 450, 200, 50, GREEN, RED, select_priest)
        draw_button("Свій персонаж", 300, 550, 200, 50, GREEN, RED, select_custom)
        draw_button("Назад", 300, 650, 200, 50, GREEN, RED, NewGame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def select_warrior():
    global selected_class
    selected_class = "Воїн"
    print(f"Вибрано: {selected_class}")

def select_mage():
    global selected_class
    selected_class = "Маг"
    print(f"Вибрано: {selected_class}")

def select_hunter():
    global selected_class
    selected_class = "Мисливець"
    print(f"Вибрано: {selected_class}")

def select_priest():
    global selected_class
    selected_class = "Священник"
    print(f"Вибрано: {selected_class}")

def select_custom():
    global selected_class
    selected_class = "Свій персонаж"
    print(f"Вибрано: {selected_class}")
    create_custom_character()

#------------------------------------------------------------------------------------------------Class of Characters

class Character:
    def __init__(self, name, hp, abilities, start_item, description):
        self.name = name
        self.hp = hp
        self.abilities = abilities
        self.start_item = start_item
        self.descritption = description

characters = {
    "Воїн": Character (
        name = "Воїн",
        hp = "200",
        abilities = ["Сильний удар", "Блокування щитом"],
        start_item = ["Меч", "Щит", "Шкіряний нагрудник"],
        description = "Сильний і витривалий боєць, здатний витримувати сильні атаки."
    ),
    "Маг": Character (
        name = "Маг",
        hp = "75",
        abilities = ["Магічний бар'єр", "Вогняна куля", "Заморозка"],
        start_item = ["Дерев'яний посох", "Мантія", "Книга заклять"],
        description = "Майстер магії, здатний наносити сильні магічні атаки."
    ),
    "Мисливець": Character (
        name = "Мисливець",
        hp = "120",
        abilities = ["Обшук", "Пастка", "Полювання"],
        start_item = ["Дерев'яний лук", "Капюшон", "Шкіряні ботинки"],
        description = "Майстер лука і пасток, що використовує свою спритність для полювання."
    ),
    "Священник": Character (
        name = "Священник",
        hp = "75",
        abilities = ["Молитва", "Вигнання", "Святий удар"],
        start_item = ["Жезл", "Мантія", "Талісман"],
        description = "Лікувальник, який підтримує команду і завдає святої шкоди ворогам."
    ),
    "Свій персонаж": Character (
        name = "Невідомо",
        hp = "Невідомо",
        abilities = [],
        start_item = [],
        description = "Невідомо"
    )
}

#------------------------------------------------------------------------------------------------Functions for Custom Character

selected_name = ""
selected_abilities = []
selected_items = []
selected_health = 150
selected_description = ""

avaible_abilities = ["Вогняна куля", "Заморозка", "Блокування", "Обшук", "Молитва", "Святий удар", "Блокування щитом", "Полювання", "Жертвоприношення"]
avaible_items = ["Щит", "Меч", "Дерев'яний лук", "Дерев'яний посох", "Мантія", "Шкіряний нагрудник", "Капюшон", "Шкіряні ботинки", "Талісман"]

MAX_ITEMS = 3
MAX_ABILITIES = 3
MAX_NAME_LENGTH = 12
MAX_DESCRIPTION_LENGTH = 30

def create_custom_character():
    global selected_health, selected_name, selected_description
    name_active = False
    description_active = False

    while True:
        screen.fill(WHITE)

        title_surface = font.render ("Створення свого персонажа", True, BLACK)
        screen.blit (title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

        draw_text_input_box(selected_name, 100, 100, 600, 50, GREEN, GRAY, name_active)
        name_label = font.render("Ім'я персонажа:", True, BLACK)
        screen.blit (name_label, (100, 60))

        health_label = font.render (f"Здоров'я: {selected_health}", True, BLACK)
        screen.blit (health_label, (100, 200))
        draw_health_slider()

        ability_label = font.render ("Виберіть здібності:", True, BLACK)
        screen.blit (ability_label, (100, 300))
        for idx, ability in enumerate (avaible_abilities):
            draw_button (ability, 100, 250 + idx * 50, 200, 40, GRAY, GREEN, lambda a = ability: select_ability (a))

        item_label = font.render ("Виберіть предмети:", True, BLACK)
        screen.blit (item_label, (400, 300))
        for idx, item in enumerate (avaible_items):
            draw_button (item, 400, 250 + idx * 50, 200, 40, GRAY, GREEN, lambda i = item: select_item (i))

        draw_text_input_box(selected_description, 100, 200, 600, 50, GREEN, GRAY, description_active)
        description_label = font.render("Опис персонажа:", True, BLACK)
        screen.blit(description_label, (100, 160))

        draw_button ("Зберегти персонажа", 300, 500, 200, 50, GRAY, GREEN, save_character)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        pygame.display.update()


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
        print(f"Видалено: {ability}")
    elif len (selected_abilities) < MAX_ABILITIES:
        selected_abilities.append (ability)
        print (f"Додано: {ability}")

def select_item(item):
    global selected_items
    if item in selected_items:
        selected_items.remove (item)
        print (f"Видалено: {item}")
    elif len (selected_items) < MAX_ITEMS:
        selected_items.append (item)
        print (f"Додано: {item}")

def save_character():
    print (f"Персонажа створено з параметрами:")
    if len (selected_name) > MAX_NAME_LENGTH:
        print ("Ім'я занадто довге")
    else:
        print (f"Ім'я персонажа: {selected_name}")
    print (f"Здоров'я: {selected_health}")
    print (f"Вибрані здібності: {selected_abilities}")
    print (f"Вибрані предмети: {selected_items}")
    if len (selected_description) > MAX_DESCRIPTION_LENGTH:
        print ("Опис занадто довгий")
    else:
        print (f"Опис персонажа: {selected_description}")



#------------------------------------------------------------------------------------------------Selecting Map

def select_map():
    while True:
        screen.fill(WHITE)

        draw_button ("Малий", 300, 150, 200, 50, GREEN, RED, select_map_small)
        draw_button("Середній", 300, 250, 200, 50, GREEN, RED, select_map_medium)
        draw_button("Великий", 300, 350, 200, 50, GREEN, RED, select_map_large)
        draw_button("Гігантський", 300, 450, 200, 50, GREEN, RED, select_map_enormous)
        draw_button("Назад", 300, 550, 200, 50, GREEN, RED, NewGame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def select_map_small():
    global selected_map
    selected_map = "Малий"
    print(f"Вибраний розмір карти: {selected_map}")

def select_map_medium():
    global selected_map
    selected_map = "Середній"
    print(f"Вибраний розмір карти: {selected_map}")

def select_map_large():
    global selected_map
    selected_map = "Великий"
    print(f"Вибраний розмір карти: {selected_map}")

def select_map_enormous():
    global selected_map
    selected_map = "Гігантський"
    print(f"Вибраний розмір карти: {selected_map}")

#------------------------------------------------------------------------------------------------Start_game

def start_game():
    while True:
        screen.fill(WHITE)

#------------------------------------------------------------------------------------------------Main Menu

def main_menu():
    while True:
        screen.fill(WHITE)

        draw_button ("Нова гра", 300, 150, 200, 50, GREEN, RED, NewGame)
        draw_button("Налаштування", 300, 250, 200, 50, GREEN, RED, Setting)
        draw_button("Вихід", 300, 350, 200, 50, GREEN, RED, Exit)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def Setting():
    draw_button("Нова гра", 300, 150, 200, 50, GREEN, RED, NewGame)

def Exit():
    pygame.quit()
    sys.exit()

main_menu()

