from main import Screen, GRAY, GREEN, BLACK, RED, font, screen, WIDTH, pygame, event

selected_class = ""

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

#------------------------------------------------------------------------------------------------Class of Custom Character

available_abilities = ["Fireball", "Freeze", "Magical Barrier", "Search", "Pray", "Hollow Strike", "Block", "Hunting", "Dispel curse", "Heal", "Expel"]
available_items = ["Shield", "Sword", "Wooden Bow", "Wooden Staff", "Cloak", "Leather Chest", "Hood", "Leather Boots", "Mascot"]

class CustomCharacter(Screen):
    def __init__(self, color = GRAY):
        super().__init__(color)
        self.selected_name = ""
        self.selected_health = 150
        self.selected_abilities = []
        self.selected_items = []
        self.selected_description = ""
        self.name_active = False
        self.description_active = False

        self.available_abilities = ["Fireball", "Freeze", "Magical Barrier", "Search", "Pray", "Hollow Strike", "Block", "Hunting", "Dispel curse", "Heal", "Expel"]
        self.available_items = ["Shield", "Sword", "Wooden Bow", "Wooden Staff", "Cloak", "Leather Chest", "Hood", "Leather Boots", "Mascot"]
        self.add_button("Save Character", self.save_character, color = GREEN)

    def render(self):
        screen.fill(self.color)

        title_surface = font.render("Creating Custom Character", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

        self.draw_text_input_box(self.selected_name, 100, 100, 600, 50, GREEN, self.name_active)
        name_label = font.render("Name of Character:", True, BLACK)
        screen.blit(name_label, (100, 60))

        health_label = font.render(f"Health: {self.selected_health}", True, BLACK)
        screen.blit(health_label, (100, 200))
        self.draw_health_slider()

        ability_label = font.render("Choose Abilities:", True, BLACK)
        screen.blit(ability_label, (100, 300))
        for idx, ability in enumerate(available_abilities):
            self.add_button(ability, lambda a=ability: self.select_ability(a), color = GRAY)

        item_label = font.render("Choose Items:", True, BLACK)
        screen.blit(item_label, (400, 300))
        for idx, item in enumerate(available_items):
            self.add_button(item, lambda i=item: self.select_item(i), color = GRAY)

            self.draw_text_input_box(self.selected_description, 100, 650, 600, 50, GREEN, self.description_active)
            description_label = font.render("Description of Character:", True, BLACK)
            screen.blit(description_label, (100, 610))

            super().render()

#------------------------------------------------------------------------------------------------Functions

    def draw_text_input_box(self, text, x, y, width, height, active_color, active):
        box_color = active_color if active else GRAY
        pygame.draw.rect(screen, box_color, (x, y, width, height))
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (x + 5, y + (height // 2 - text_surface.get_height() // 2)))

    def draw_health_slider(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        slider_x = 150
        slider_y = 250
        slider_width = 500
        slider_height = 20
        pygame.draw.rect(screen, GREEN, (slider_x, slider_y, slider_width, slider_height))

        handle_x = slider_x + (self.selected_health - 50) * 5
        pygame.draw.rect(screen, RED, (handle_x, slider_y, slider_width, slider_height))

        if click[0] ==1 and slider_x <= mouse[0] <= slider_x + slider_width:
            self.selected_health = 50 + (mouse[0] - slider_x) // 5

    def select_ability(self,ability):
        if ability in self.available_abilities:
            self.selected_abilities.remove(ability)
        elif len(self.selected_abilities) < 3:
            self.selected_abilities.append(ability)

    def select_item(self, item):
        if item in self.available_items:
            self.selected_items.remove(item)
        elif len(self.selected_items) < 3:
            self.selected_items.append(item)

    def save_character(self):
        print(f"Character Created with:")
        print(f"Name: {self.selected_name}")
        print(f"Health: {self.selected_health}")
        print(f"Abilities: {self.selected_abilities}")
        print(f"Items: {self.selected_items}")
        print(f"Description: {self.selected_description}")

def handle_events(self):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if self.name_active or self.description_active:
            self.name_active = False
            self.description_active = False
        if self.rect.collidepoint(event.pos):
            self.name_active = True

    if event.type == pygame.KEYDOWN:
        if self.name_active:
            if event.key == pygame.K_BACKSPACE:
                self.selected_name = self.selected_name[:-1]
            elif len(self.selected_name) < 12:
                self.selected_name += event.unicode
        if self.description_active:
            if event.key == pygame.K_BACKSPACE:
                self.description_active = self.description_active[:-1]
            elif len(self.selected_description) < 30:
                self.selected_description += event.unicode

def select_warrior():
    global selected_class
    selected_class = "Warrior"
    print(f"Chosen: {selected_class}")

def select_mage():
    global selected_class
    selected_class = "Mage"
    print(f"Chosen: {selected_class}")

def select_hunter():
    global selected_class
    selected_class = "Hunter"
    print(f"Chosen: {selected_class}")

def select_priest():
    global selected_class
    selected_class = "Priest"
    print(f"Chosen: {selected_class}")

def select_custom():
    global selected_class
    selected_class = "Custom Character"
    print(f"Chosen: {selected_class}")

