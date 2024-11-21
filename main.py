from importlib.metadata import metadata

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
    def __init__(self, text, action, color=GREEN, font_color=BLACK, metadata=None):
        self.text = text
        self.action = action
        self.color = color
        self.font_color = font_color
        self.metadata = metadata
        self.selected = False
        text_surface = font.render(self.text, True, self.font_color)
        self.width = text_surface.get_width() + 40
        self.height = text_surface.get_height() + 20
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.hovered = False

    def render(self, x, y):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        draw_color = (100, 0, 100) if self.selected else self.color
        pygame.draw.rect(screen, draw_color, self.rect)

        border_box = BLACK if not self.selected else (255, 255, 0)
        pygame.draw.rect(screen, border_box, self.rect, 3)

        text_surface = font.render(self.text, True, self.font_color)
        screen.blit(text_surface, (self.rect.x + 20, self.rect.y + 10))

        if self.hovered and self.metadata:
            self.render_metadata()

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect and self.rect.collidepoint(mouse_pos):
            self.action()

    def render_metadata(self):
        box_padding = 10
        line_height = font.get_height() + 5
        metadata_lines = len(self.metadata)
        box_width = 300
        box_height = metadata_lines * line_height + (2 * box_padding)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        box_x = mouse_x + 15
        box_y = mouse_y + 15

        if box_x + box_width > WIDTH:
            box_x = WIDTH - box_width - 15
        if box_y + box_height > HEIGHT:
            box_y = HEIGHT - box_height - 15

        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2)

        y_offset = box_y + box_padding
        for key, value in self.metadata.items():
            text_surface = font.render(f"{key}: {value}", True, BLACK)
            screen.blit(text_surface, (box_x + box_padding, y_offset))
            y_offset += line_height

class Screen:
    def __init__(self, color=GRAY):
        self.color = color
        self.buttons = []

    def add_button(self, text, action, color=GREEN, metadata=None):
        button = Button(text, action, color, metadata=metadata)
        self.buttons.append(button)

    def render(self):
        screen.fill(self.color)
        total_height = sum(button.height + 20 for button in self.buttons) - 20
        y = (HEIGHT - total_height) // 2
        for button in self.buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.render((WIDTH - button.width) // 2, y)
            y += button.height + 20

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_hover(mouse_pos)

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
            button_spacing = 40
            total_width = self.buttons[0].width + self.buttons[1].width + button_spacing
            left_x = (WIDTH - total_width) // 2
            self.buttons[0].render(left_x, button_y)
            self.buttons[1].render(left_x + self.buttons[0].width + button_spacing, button_y)


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
        self.available_abilities = [
                                    {"Name": "Fireball", "Damage": 20-30, "Mana": 20, "Crit Chance": 35, "Crit Damage": 45-60, "Description": "Throws a fireball that deal massive damage and can inflict burn dot"},
                                    {"Name": "Freeze", "Damage": 10-15, "Mana": 15, "Crit Chance": 20, "Crit Damage": 30-35, "Description": "Cover your enemies in ice and don`t let them move for a time"},
                                    {"Name": "Magical Barrier", "Damage": 0, "Mana": 15, "Crit Chance": 0, "Crit Damage": 0, "Description": "Take a barrier that would defend you from magical damage and dots"},
                                    {"Name": "Pray", "Damage": 0, "Mana": 5, "Crit Chance": 0, "Crit Damage": 0, "Description": "Pray the Gods to restore your wounds and increase your damage"},
                                    {"Name": "Hollow Strike", "Damage": 20, "Mana": 20, "Crit Chance": 20, "CritDamage": 24, "Description": "Use knowledge of saints to punish your enemies and reduce their resistance to hollow magic"},
                                    {"Name": "Search", "Damage": 0, "Mana": 10, "Crit Chance": 0, "Crit Damage": 0, "Description": "Search a place for probability to find some things"},
                                    {"Name": "Trap", "Damage": 12-25, "Mana": 15, "Crit Chance": 25, "Crit Damage": 30-40, "Description": "Install a trap to stop your enemies and bleed them"},
                                    {"Name": "Expel", "Damage": 20-23, "Mana": 30, "Crit Chance": 40, "Crit Damage": 30-45, "Description": "Expel enemies that renounce the Gods and return them to Paradise"},
                                    {"Name": "Poison", "Damage": 20-22, "Mana": 30, "Crit Chance": 40, "Crit Damage": 30-34, "Description": "Expel enemies that renounce the Gods and return them to Paradise"}
                                    ]

        self.buttons = []

        for ability in self.available_abilities:
            self.buttons.append(Button(
                            ability["Name"],
                            lambda a=ability["Name"]: self.select_ability(a),
                            color=GRAY,
                            metadata=ability
                            ))

        self.add_button("Back", self.prev_step, color=GREEN)
        self.add_button("Next", self.next_step, color=GREEN)

    def render(self):
        screen.fill(self.color)
        title_surface = font.render("Step 2: Choose Abilities", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 10))

        button_spacing = 30
        max_button_per_raw = (WIDTH - button_spacing) // (self.buttons[0].width + button_spacing)
        x_start = (WIDTH - (max_button_per_raw * (self.buttons[0].width + button_spacing) - button_spacing)) // 2
        x = x_start
        y = HEIGHT // 2 - 100
        for idx, button in enumerate(self.buttons[:len(self.available_abilities)]):
            button.check_hover(pygame.mouse.get_pos())
            button.render(x, y)
            x += button.width + button_spacing
            if (idx + 1) % max_button_per_raw == 0:
                x = x_start
                y += button.height + button_spacing

        nav_total_width = self.buttons[-2].width + self.buttons[-1].width + button_spacing
        nav_x = (WIDTH - nav_total_width) // 2
        nav_y = y + 80
        self.buttons[-2].render(nav_x, nav_y)
        self.buttons[-1].render(nav_x + self.buttons[-2].width + button_spacing, nav_y)

    def select_ability(self, ability_name):
        for button in self.buttons[:len(self.available_abilities)]:
            if button.text == ability_name:
                if button.selected:
                    button.selected = False
                    self.character_data["abilities"].remove(ability_name)
                else:
                    if len(self.character_data["abilities"]) < 3:
                        button.selected = True
                        self.character_data["abilities"].append(ability_name)
                break

    def next_step(self):
        screen_manager.set_screen("items_step")

    def prev_step(self):
        screen_manager.set_screen("name_health_step")

class ItemsStep(CustomCharacter):
    def __init__(self, color=GRAY):
        super().__init__(color)
        self.available_items = [

            #Weapons
            {"Name": "Wooden Sword", "Damage": 5-8, "Defense": 0, "Crit Chance": 10, "Crit Damage": 12-16, "Description": "Simple wooden sword that uses in training soldiers"},
            {"Name": "Wooden Shield", "Damage": 2-4, "Defense": 10 ,"Crit Chance": 5, "Crit Damage": 8-10, "Description": "Wooden shield that can defend you from simple attacks"},
            {"Name": "Wooden Staff", "Damage": 4-6, "Defense": 0, "Crit Chance": 8, "Crit Damage": 10-12, "Description": "Staff of magical newbie. It can strengthen your base ability"},
            {"Name": "Book of Spells", "Damage": 3-5, "Defense": 0, "Crit Chance": 10, "Crit Damage": 7-9, "Description": "Book that contains spells and knowledge. Written by the most knowledge mages"},

            #Leather Armor
            {"Name": "Lather Helmet", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Helmet made from lather of animals and cover you from wounds"},
            {"Name": "Lather Chest", "Damage": 0, "Defense": 8, "Crit Chance": 0, "Crit Damage": 0, "Description": "Chest made from lather of animals. Can help you live longer"},
            {"Name": "Lather Gloves", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "Gloves made from lather of animals that help your arms be healthier"},
            {"Name": "Leather Boots", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "Boots that uses in our life. Help you to be cleaner and don`t stand on rocks"},

            #Magical Clothes
            {"Name": "Magical Hat", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Hat with mythical runes that cover some power abd knowledge"},
            {"Name": "Cloak", "Damage": 0, "Defense": 4, "Crit Chance": 0, "Crit Damage": 0, "Description": "Base dress of mage, made of different flowers to cover their weaver from different affection"},

            #Arcane Whisper
            {"Name": "Runed Hat", "Damage": 0, "Defense": 2, "Crit Chance": 8, "Crit Damage": 0, "Description": "A conical hat adorned with shimmering runes that enhance critical spell effects."},
            {"Name": "Arcane Cloak", "Damage": 0, "Defense": 4, "Crit Chance": 5, "Crit Damage": 0, "Description": "A glowing blue cloak inscribed with arcane runes, offering magical resistance and amplifying spell power."},
            {"Name": "Gloves of the Adept", "Damage": 0, "Defense": 1, "Crit Chance": 0, "Crit Damage": 0, "Description": "Delicate gloves that improve mana flow and spellcasting precision."},
            {"Name": "Enchanted Boots", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Lightweight boots that allow silent movement and boost magical energy absorption."},

            #Emerald Grace
            {"Name": "Circlet of Harmony", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "A delicate circlet that enhances the wearer's attunement to nature and magic."},
            {"Name": "Nature's Embrace Cloak", "Damage": 0, "Defense": 5, "Crit Chance": 0, "Crit Damage": 0, "Description": "A vibrant green cloak infused with natural magic, increasing resistance to elemental damage."},
            {"Name": "Forestweave Gloves", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "Gloves designed to channel natural magic and protect the hands during spellcasting."},
            {"Name": "Elven Boots", "Damage": 0, "Defense": 4, "Crit Chance": 0, "Crit Damage": 0, "Description": "Crafted from the finest elven leather, these boots enhance agility and silent movement."},

            #Iron Vow
            {"Name": "Steel Helm", "Damage": 0, "Defense": 5, "Crit Chance": 2, "Crit Damage": 0, "Description": "A heavy helmet that safeguards the head while maintaining visibility and awareness."},
            {"Name": "Ironbound Chestplate", "Damage": 0, "Defense": 10, "Crit Chance": 0, "Crit Damage": 0, "Description": "A sturdy chestplate that offers immense protection against physical attacks."},
            {"Name": "Gauntlets of Strength", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Reinforced gauntlets that enhance grip strength and combat power."},
            {"Name": "Plated Greaves", "Damage": 0, "Defense": 6, "Crit Chance": 0, "Crit Damage": 0, "Description": "Heavy boots designed for durability and stability in battle."},

            #Sanctuary`s Light
            {"Name": "Hood of Sanctity", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "A white hood that amplifies the wearer's focus on divine spells."},
            {"Name": "Blessed Robe", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "A flowing white robe blessed with divine power to enhance healing magic."},
            {"Name": "Cleric's Gloves", "Damage": 0, "Defense": 1, "Crit Chance": 0, "Crit Damage": 0, "Description": "Simple gloves that improve control over healing magic and reduce energy drain."},
            {"Name": "Sandals of Grace", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "Comfortable sandals that enhance agility and movement during holy rituals."},

            #Shadow`s Step
            {"Name": "Tracker's Hat", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "A lightweight hat that improves tracking and detection skills."},
            {"Name": "Ranger's Cloak", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "A green hooded cloak that provides camouflage in forests and boosts stealth."},
            {"Name": "Hunter's Gloves", "Damage": 0, "Defense": 1, "Crit Chance": 0, "Crit Damage": 0, "Description": "Gloves with reinforced tips for precision archery and trap-setting."},
            {"Name": "Silent Striders", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Soft-soled boots that allow for silent movement in any terrain."},

            #Phoenix`s Ember
            {"Name": "Silent Striders", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Soft-soled boots that allow for silent movement in any terrain."},
            {"Name": "Phoenix Feather Cloak", "Damage": 0, "Defense": 5, "Crit Chance": 0, "Crit Damage": 0, "Description": "A fiery cloak made from enchanted phoenix feathers, granting fire resistance and a boost to flame magic."},
            {"Name": "Inferno Gloves", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "Gloves imbued with flames, enhancing control over fire-based attacks."},
            {"Name": "Ashen Boots", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Lightweight boots that allow quick movement through fiery terrains."},

            #Frozen Sentinel
            {"Name": "Crown of Ice", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "A crystal circlet forged from eternal ice, amplifying frost-based abilities."},
            {"Name": "Frost Cloak", "Damage": 0, "Defense": 4, "Crit Chance": 0, "Crit Damage": 0, "Description": "A shimmering cloak radiating cold energy, reducing damage from fire attacks."},
            {"Name": "Icy Grasp Gloves", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "Cold-resistant gloves that enhance frost spell damage and critical effects."},
            {"Name": "Frozen Striders", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Boots that allow the wearer to traverse icy surfaces effortlessly."},

            #Venom`s Embrace
            {"Name": "Assassin’s Mask", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "A lightweight mask that conceals the wearer’s identity while boosting perception."},
            {"Name": "Shadow Venom Cloak", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "A cloak infused with toxic magic, granting stealth and poison resistance."},
            {"Name": "Venomous Grip Gloves", "Damage": 0, "Defense": 1, "Crit Chance": 0, "Crit Damage": 0, "Description": "Gloves laced with venom, increasing the potency of poison-based attacks."},
            {"Name": "Silent Shadows Boots", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Silent boots that leave no trace, perfect for sneaking behind enemies."},

            #Draconic Vanguard
            {"Name": "Dragon Crest Helm", "Damage": 0, "Defense": 6, "Crit Chance": 0, "Crit Damage": 0, "Description": "A sturdy helm crafted from dragon bone, enhancing combat awareness and resilience."},
            {"Name": "Dragon Scale Chestplate", "Damage": 0, "Defense": 12, "Crit Chance": 0, "Crit Damage": 0, "Description": "Heavy armor forged from dragon scales, offering immense protection against physical and fire damage."},
            {"Name": "Draconic Gauntlets", "Damage": 0, "Defense": 5, "Crit Chance": 0, "Crit Damage": 0, "Description": "Gauntlets imbued with dragon’s power, increasing attack strength."},
            {"Name": "Scaled Boots", "Damage": 0, "Defense": 5, "Crit Chance": 0, "Crit Damage": 0, "Description": "Heavy boots reinforced with dragon hide, granting stability and fire resistance."},

            #Celestail Radiance
            {"Name": "Halo Hood", "Damage": 0, "Defense": 4, "Crit Chance": 0, "Crit Damage": 0, "Description": "A glowing hood that enhances divine focus and critical healing effects."},
            {"Name": "Celestial Robe", "Damage": 0, "Defense": 6, "Crit Chance": 0, "Crit Damage": 0, "Description": "A radiant robe blessed by celestial beings, amplifying healing and support magic."},
            {"Name": "Sacred Touch Gloves", "Damage": 0, "Defense": 2, "Crit Chance": 0, "Crit Damage": 0, "Description": "Gloves that radiate warmth, soothing allies and boosting healing power."},
            {"Name": "Divine Step Sandals", "Damage": 0, "Defense": 3, "Crit Chance": 0, "Crit Damage": 0, "Description": "Light sandals that allow the wearer to move gracefully and cast healing magic."},

            #Stormbringer`s Might
            {"Name": "Thunder Helm", "Damage": 0, "Defense": 5, "Crit Chance": 0, "Crit Damage": 0, "Description": "A helm that crackles with electricity, intimidating foes and enhancing awareness."},
            {"Name": "Stormforged Plate", "Damage": 0, "Defense": 10, "Crit Chance": 0, "Crit Damage": 0, "Description": "A heavy plate charged with lightning energy, striking enemies who dare attack."},
            {"Name": "Lightning Claw Gauntlets", "Damage": 0, "Defense": 4, "Crit Chance": 8, "Crit Damage": 0, "Description": "Gauntlets infused with lightning, delivering electrifying blows."},
            {"Name": "Stormstep Boots", "Damage": 0, "Defense": 4, "Crit Chance": 0, "Crit Damage": 0, "Description": "Boots that spark with energy, allowing rapid and agile movement."},

        ]

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
                if y_offset + line_height < y + height:
                    rendered_line = self.text_font.render(line, True, BLACK)
                    screen.blit(rendered_line, (x + 5, y_offset))
                    y_offset += line_height
                    line = word + " "
            else:
                line = test_line

        if y_offset + line_height < y + height:
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
