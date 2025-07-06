import sys
import pygame
import random

pygame.init()

# --- Screen setup ---
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Timbit Buttons")

# --- Assets ---
timbitbg = pygame.transform.scale(pygame.image.load("timbitbg.png"), (WIDTH, HEIGHT))
goodtimbitsbg = pygame.transform.scale(pygame.image.load("goodtimbitsbg.png"), (WIDTH, HEIGHT))
dining_bg = pygame.transform.scale(pygame.image.load("dining.png"), (WIDTH, HEIGHT))

bday_img = pygame.transform.scale(pygame.image.load("bday.png").convert_alpha(), (70, 70))
choco_img = pygame.transform.scale(pygame.image.load("choco.png").convert_alpha(), (70, 70))
plain_img = pygame.transform.scale(pygame.image.load("plain.png").convert_alpha(), (70, 70))
boss_img = pygame.transform.scale(pygame.image.load("boss.png").convert_alpha(), (350, 500))

font = pygame.font.Font('DIN Alternate Bold.ttf', 30)
clock = pygame.time.Clock()

# --- Button setup ---
button_color = (120, 151, 183)
done_button_color = (50, 200, 50)
button_radius = 20

bday_button_rect = pygame.Rect(150, 30, 200, 50)
choco_button_rect = pygame.Rect(400, 30, 200, 50)
plain_button_rect = pygame.Rect(650, 30, 200, 50)
done_button_rect = pygame.Rect(WIDTH - 180, HEIGHT - 80, 150, 50)
speaker_rect = pygame.Rect(50, 170, 100, 200)
bubble_rect = pygame.Rect(350, 150, 500, 170)
ok_button = pygame.Rect(700, 270, 100, 40)


# --- Random Goal Generation ---
def generate_goal():
    a = random.randint(3, 14)
    b = random.randint(1, 20 - a - 1)
    c = 20 - a - b
    return {'bday': a, 'choco': b, 'plain': c}

goal = generate_goal()
counts = {'bday': 0, 'choco': 0, 'plain': 0}

bday = goal["bday"]
choco = goal["choco"]
plain = goal["plain"]

timbit_instruction_sets = [
    ["Congrats on finishing your first task.", "Your next task is to assemble",  "a box of 20 timbits for the customer."],
    ["The customer is requesting", f"{bday} Birthday Cake timbits, {choco} Chocolate", f"timbits, and {plain} Plain timbits."],
    ["Click the flavour buttons at the", "top to add certain flavours", "of timbits."],
    ["Once you've collected", "the right combo of flavours,", "press DONE!"],
]

def draw_speech_bubble(surface, rect, lines):
    pygame.draw.rect(surface, (242, 240, 223), rect, border_radius=20)
    pygame.draw.rect(surface, (0,0,0), rect, 2, border_radius=20)
    
    for i, line in enumerate(lines):
        text_surf = font.render(line, True, (0,0,0))
        surface.blit(text_surf, (rect.x + 20, rect.y + 20 + i * 30))

def draw_ok_button(surface, rect):
    pygame.draw.rect(surface, (100, 150, 255), rect, border_radius=10)
    pygame.draw.rect(surface, (0,0,0), rect, 2, border_radius=10)
    ok_text = font.render("OK", True, (255,255,255))
    text_rect = ok_text.get_rect(center=rect.center)
    surface.blit(ok_text, text_rect)

def timbit_instructions_screen():
    instruction_index = 0

    while instruction_index < len(timbit_instruction_sets):
        screen.blit(dining_bg, (0, 0))  # Set dining background

        # Draw speaker image instead of rectangle
        screen.blit(boss_img, speaker_rect.topleft)

        # Draw speech bubble with current instructions
        draw_speech_bubble(screen, bubble_rect, timbit_instruction_sets[instruction_index])

        # Draw OK button
        draw_ok_button(screen, ok_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(event.pos):
                    instruction_index += 1  # Advance instruction

        pygame.display.flip()
        clock.tick(60)

    return "timbits"

all_sprites = pygame.sprite.Group()

class TimbitSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, flavor):
        super().__init__()
        self.original_image = image
        self.image = image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.flavor = flavor

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.spawn_time
        if elapsed < 200:
            scale_factor = 1 + 0.3 * (1 - abs(100 - elapsed) / 100)
            new_size = (int(self.original_image.get_width() * scale_factor),
                        int(self.original_image.get_height() * scale_factor))
            self.image = pygame.transform.scale(self.original_image, new_size)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = self.original_image
            self.rect = self.image.get_rect(center=self.rect.center)

def draw_button(rect, label, color):
    pygame.draw.rect(screen, color, rect, border_radius=button_radius)
    text = font.render(label, True, (0, 0, 0))
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

def draw_status():
    x = 100
    for flavor in ['bday', 'choco', 'plain']:
        text = f"{flavor.upper()}: {goal[flavor]} needed"
        rendered = font.render(text, True, (0, 0, 0))
        screen.blit(rendered, (x, 100))
        x += 300


def spawn_sprite(image, flavor):
    pos = (random.randint(447, 770), random.randint(450, 600))
    sprite = TimbitSprite(pos, image, flavor)
    all_sprites.add(sprite)
    counts[flavor] += 1

def reset_game():
    all_sprites.empty()
    counts.update({'bday': 0, 'choco': 0, 'plain': 0})

def is_goal_met():
    return counts == goal

# --- Game loop ---
def run_timbit_button_screen(screen):
    won = False
    running = True
    game_state = "playing"  # or "win"
    global goal
    while running:
        # Background
        screen.blit(goodtimbitsbg if game_state == "win" else timbitbg, (0, 0))

        # Draw buttons
        draw_button(bday_button_rect, "BDAY CAKE", button_color)
        draw_button(choco_button_rect, "CHOCOLATE", button_color)
        draw_button(plain_button_rect, "PLAIN", button_color)

        # Button label depends on game state
        if game_state == "win":
            draw_button(done_button_rect, "SERVE", done_button_color)
        else:
            draw_button(done_button_rect, "DONE", done_button_color)

        draw_status()
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if game_state == "playing":
                    if bday_button_rect.collidepoint(pos):
                        spawn_sprite(bday_img, 'bday')
                    elif choco_button_rect.collidepoint(pos):
                        spawn_sprite(choco_img, 'choco')
                    elif plain_button_rect.collidepoint(pos):
                        spawn_sprite(plain_img, 'plain')
                    elif done_button_rect.collidepoint(pos):
                        if is_goal_met():
                            game_state = "win"
                            all_sprites.empty()
                        else:
                            reset_game()
                elif game_state == "win":
                    if done_button_rect.collidepoint(pos):
                        return "racoon"

        clock.tick(60)

    sys.exit()

# Run the game
status = "timbits instructions"
if status == "timbits instructions":
    status = timbit_instructions_screen()
run_timbit_button_screen(screen)


