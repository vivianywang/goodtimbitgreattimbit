import sys
import pygame
import random
from pygame.locals import (RLEACCEL, QUIT)
pygame.init()

WIDTH, HEIGHT = 1000, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tim Hortons Game")

# --- Common Assets & Font ---
font = pygame.font.Font('DIN Alternate Bold.ttf', 30)
button_color = (120, 151, 183)
done_button_color = (50, 200, 50)
button_radius = 20
clock = pygame.time.Clock()

# --- Load Images ---
lose1_screen = pygame.image.load("lose1.png").convert_alpha()
win_screen = pygame.image.load("win.png").convert_alpha()
lose2_screen = pygame.image.load("lose2.png").convert_alpha()
start_screen = pygame.image.load("start_screen.png").convert_alpha()
boss_img = pygame.transform.scale(pygame.image.load("boss.png").convert_alpha(), (350, 500))
bubble_rect = pygame.Rect(350, 150, 500, 170)
ok_button = pygame.Rect(700, 270, 100, 40)
dining = pygame.image.load("dining.png").convert_alpha()
coffeebg = pygame.image.load("coffeebg.png").convert_alpha()
timbitbg = pygame.transform.scale(pygame.image.load("timbitbg.png"), (WIDTH, HEIGHT))
goodtimbitsbg = pygame.transform.scale(pygame.image.load("goodtimbitsbg.png"), (WIDTH, HEIGHT))
dining_bg = pygame.transform.scale(pygame.image.load("dining.png"), (WIDTH, HEIGHT))
bday_img = pygame.transform.scale(pygame.image.load("bday.png").convert_alpha(), (70, 70))
choco_img = pygame.transform.scale(pygame.image.load("choco.png").convert_alpha(), (70, 70))
plain_img = pygame.transform.scale(pygame.image.load("plain.png").convert_alpha(), (70, 70))

# --- Shared Drawing Functions ---
def start(screen):
    SCREEN.blit(start_screen, (0, 0)) 
    
    # defines variables for the start button elements then draws the button
    start_button_color = (198, 181, 167)
    start_button_rect = pygame.Rect(400, 600, 200, 50)
    pygame.draw.rect(screen, start_button_color, start_button_rect, border_radius=20)
    
    # puts text in the button then displays the button
    center = start_button_rect.center
    font = pygame.font.Font('DIN Alternate Bold.TTF', 30) 
    text = font.render("START", True, (0, 0, 0))
    text_rect = text.get_rect(center=center)
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    not_clicked = True
    # checks to see if start button is pressed
    while not_clicked:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    not_clicked = False
                    return 'icecapp'
    

def draw_speech_bubble(surface, rect, lines):
    pygame.draw.rect(surface, (242, 240, 223), rect, border_radius=20)
    pygame.draw.rect(surface, (0, 0, 0), rect, 2, border_radius=20)
    for i, line in enumerate(lines):
        text_surf = font.render(line, True, (0, 0, 0))
        surface.blit(text_surf, (rect.x + 20, rect.y + 20 + i * 30))

def draw_ok_button(surface, rect):
    pygame.draw.rect(surface, (100, 150, 255), rect, border_radius=10)
    pygame.draw.rect(surface, (0, 0, 0), rect, 2, border_radius=10)
    ok_text = font.render("OK", True, (255, 255, 255))
    text_rect = ok_text.get_rect(center=rect.center)
    surface.blit(ok_text, text_rect)

def draw_button(surface, rect, label, color):
    pygame.draw.rect(surface, color, rect, border_radius=button_radius)
    text = font.render(label, True, (0, 0, 0))
    text_rect = text.get_rect(center=rect.center)
    surface.blit(text, text_rect)

# --- Ice Capp Section ---
def run_icecapp_game():
    espresso_button_rect = pygame.Rect(150, 30, 200, 50)
    blend_button_rect = pygame.Rect(650, 100, 200, 50)
    cream_button_rect = pygame.Rect(400, 30, 200, 50)
    ice_button_rect = pygame.Rect(650, 30, 200, 50)
    serve_button_rect = pygame.Rect(800, 700, 150, 60)

    ice_capp_instruction_sets = [
        ["Welcome to your first day at Tim", "Hortons. Let's start off with", "a simple task: Making an Ice Capp."],
        ["You need 3 pumps of espresso,", "1 pump of cream, and", "4 ice cubes."],
        ["Once all ingredients are in,", "click blend three times.", "Easy peasy lemon squeezy."],
        ["Once you're done, pour it", "in the cup and then click,", "on SERVE"],
    ]

    blender = pygame.sprite.Sprite()
    blenderfull = pygame.sprite.Sprite()
    ice_capp = pygame.sprite.Sprite()

    blendercostume = 0
    espressoclicked = 0
    creamclicked = 0
    iceclicked = 0
    cupcostume = 0
    ready = False
    blender_tilted = False
    blender_visible = True
    pour_timer = 0
    instruction_index = 0
    show_instructions = True
    status = "instructions"
    running = True

    def blender_draw():
        image_names = [
            "emptyblender.png",
            "espresso1.png",
            "espresso2.png",
            "espresso3.png",
            "creamblender.png",
            "ice1.png",
            "ice2.png",
            "ice3.png",
            "ice4.png",
            "blend1.png",
            "blend2.png",
            "blend3.png"
        ]
        blender.images = [pygame.image.load(name).convert_alpha() for name in image_names]
        blender.image = blender.images[min(blendercostume, len(blender.images)-1)]
        blender.rect = blender.image.get_rect()
        SCREEN.blit(blender.image, (-400, 100))


    def blender_pour():
        nonlocal blenderfull
        blenderfull.image = pygame.transform.scale(pygame.image.load("blenderfull.png").convert_alpha(), (400, 500))
        blenderfull.image.set_colorkey((255, 255, 255), RLEACCEL)
        blenderfull.rect = blenderfull.image.get_rect(center=(500, 300))

    def blenderUpdate(pos):
        blenderfull.rect.center = pos
        blenderfull.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def ice_capp_draw():
        ice_capp.images = [pygame.transform.scale(pygame.image.load(img).convert_alpha(), (225, 300)) for img in ["emptycup.png", "halfcup.png", "fullcup.png"]]
        ice_capp.image = ice_capp.images[cupcostume]
        ice_capp.rect = ice_capp.image.get_rect(topleft=(300, 350))
        SCREEN.blit(ice_capp.image, ice_capp.rect)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if show_instructions:
                if event.type == pygame.MOUSEBUTTONDOWN and ok_button.collidepoint(event.pos):
                    instruction_index += 1
                    if instruction_index >= len(ice_capp_instruction_sets):
                        show_instructions = False
                        status = "blend"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if status == "pour" and cupcostume == 2 and not blender_visible and serve_button_rect.collidepoint(event.pos):
                    return  
                elif status == "blend":
                    pos = event.pos
                    if espresso_button_rect.collidepoint(pos) and espressoclicked < 3:
                        espressoclicked += 1; blendercostume += 1
                    elif cream_button_rect.collidepoint(pos) and espressoclicked >= 3 and creamclicked < 1:
                        creamclicked += 1; blendercostume += 1
                    elif ice_button_rect.collidepoint(pos) and creamclicked >= 1 and iceclicked < 4:
                        iceclicked += 1; blendercostume += 1
                    elif ready and blend_button_rect.collidepoint(pos):
                        blendercostume += 1
                        if blendercostume == 12:
                            status = "pour"
                            blender_pour()

        pos = pygame.mouse.get_pos()
        SCREEN.fill((255,255,255))
        if show_instructions:
            SCREEN.blit(dining, (0, 0))
            SCREEN.blit(boss_img, (50, 170))
            draw_speech_bubble(SCREEN, bubble_rect, ice_capp_instruction_sets[instruction_index])
            draw_ok_button(SCREEN, ok_button)
        elif status == "blend":
            SCREEN.blit(coffeebg, (0, 0))
            blender_draw()
            draw_button(SCREEN, espresso_button_rect, "ESPRESSO", button_color)
            draw_button(SCREEN, cream_button_rect, "CREAM", button_color)
            draw_button(SCREEN, ice_button_rect, "ICE", button_color)
            if iceclicked == 4:
                draw_button(SCREEN, blend_button_rect, "BLEND!", button_color)
                ready = True
        elif status == "pour":
            SCREEN.blit(coffeebg, (0, 0))
            ice_capp_draw()
            if blender_visible:
                blenderUpdate(pos)
                SCREEN.blit(blenderfull.image, blenderfull.rect)
                if blenderfull.rect.colliderect(ice_capp.rect) and not blender_tilted:
                    blenderfull.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("blenderpour.png").convert_alpha(), (500, 500)), 45)
                    blenderfull.image.set_colorkey((255, 255, 255), RLEACCEL)
                    blenderfull.rect = blenderfull.image.get_rect(center=blenderfull.rect.center)
                    blender_tilted = True
                    pour_timer = 0
            if blender_tilted and cupcostume < 2:
                pour_timer += 1
                if pour_timer == 30:
                    cupcostume = 1
                elif pour_timer == 60:
                    cupcostume = 2
                    blender_visible = False
        if cupcostume == 2 and not blender_visible and status == "pour":
            draw_button(SCREEN, serve_button_rect, "SERVE", done_button_color)

        pygame.display.update()
        clock.tick(60)

# --- Timbits Section ---
def run_timbits_game():
    bday_button_rect = pygame.Rect(150, 30, 200, 50)
    choco_button_rect = pygame.Rect(400, 30, 200, 50)
    plain_button_rect = pygame.Rect(650, 30, 200, 50)
    done_button_rect = pygame.Rect(WIDTH - 180, HEIGHT - 80, 150, 50)

    def generate_goal():
        a = random.randint(3, 14)
        b = random.randint(1, 20 - a - 1)
        c = 20 - a - b
        return {'bday': a, 'choco': b, 'plain': c}

    goal = generate_goal()
    counts = {'bday': 0, 'choco': 0, 'plain': 0}
    timbit_instruction_sets = [
        ["Congrats on finishing your first task.", "Your next task is to assemble",  "a box of 20 timbits for the customer."],
        ["The customer is requesting", f"{goal['bday']} Birthday Cake timbits, {goal['choco']} Chocolate", f"timbits, and {goal['plain']} Plain timbits."],
        ["Click the flavour buttons at the", "top to add certain flavours", "of timbits."],
        ["Once you've collected", "the right combo of flavours,", "press DONE!"],
    ]

    def instructions():
        index = 0
        while index < len(timbit_instruction_sets):
            SCREEN.blit(dining_bg, (0, 0))
            SCREEN.blit(boss_img, (50, 170))
            draw_speech_bubble(SCREEN, bubble_rect, timbit_instruction_sets[index])
            draw_ok_button(SCREEN, ok_button)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if ok_button.collidepoint(event.pos):
                        index += 1
            pygame.display.flip()
            clock.tick(60)

    instructions()

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
                scale = 1 + 0.3 * (1 - abs(100 - elapsed)/100)
                new_size = (int(self.original_image.get_width()*scale), int(self.original_image.get_height()*scale))
                self.image = pygame.transform.scale(self.original_image, new_size)
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.image = self.original_image

    def spawn(flavor, image):
        pos = (random.randint(447, 770), random.randint(450, 600))
        sprite = TimbitSprite(pos, image, flavor)
        all_sprites.add(sprite)
        counts[flavor] += 1

    def draw_status():
        x = 100
        for flavor in ['bday', 'choco', 'plain']:
            text = f"{flavor.upper()}: {goal[flavor]} needed"
            rendered = font.render(text, True, (0, 0, 0))
            SCREEN.blit(rendered, (x, 100))
            x += 300

    def is_correct():
        return counts == goal

    state = "playing"
    while True:
        SCREEN.blit(goodtimbitsbg if state == "win" else timbitbg, (0, 0))
        draw_button(SCREEN, bday_button_rect, "BDAY CAKE", button_color)
        draw_button(SCREEN, choco_button_rect, "CHOCOLATE", button_color)
        draw_button(SCREEN, plain_button_rect, "PLAIN", button_color)
        draw_button(SCREEN, done_button_rect, "SERVE" if state == "win" else "DONE", done_button_color)
        draw_status()
        all_sprites.update()
        all_sprites.draw(SCREEN)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if state == "playing":
                    if bday_button_rect.collidepoint(pos): spawn('bday', bday_img)
                    elif choco_button_rect.collidepoint(pos): spawn('choco', choco_img)
                    elif plain_button_rect.collidepoint(pos): spawn('plain', plain_img)
                    elif done_button_rect.collidepoint(pos):
                        if is_correct(): state = "win"; all_sprites.empty()
                        else: all_sprites.empty(); counts.update({'bday': 0, 'choco': 0, 'plain': 0})
                elif state == "win" and done_button_rect.collidepoint(pos):
                    return "raccoon"
        clock.tick(60)

def battle():
    timer = 0
    clock = pygame.time.Clock()
    clock.tick(60)
    running = True
    raccoons = pygame.sprite.Group()
    
    battle_instruction_sets = [
        ["Uh oh, looks like a swarm of raccoons", "are on their way. You have",  "15 second to defeat the minions."],
        ["To defeat them, click on", "them. Once all minions are defeated,", "The big boss will appear."],
        ["To defeat the big boss, you", "must click on him ten times!", "If you fail, you're fired. Good luck."],
    ]

    def instructions():
        index = 0
        while index < len(battle_instruction_sets):
            SCREEN.blit(dining_bg, (0, 0))
            SCREEN.blit(boss_img, (50, 170))
            draw_speech_bubble(SCREEN, bubble_rect, battle_instruction_sets[index])
            draw_ok_button(SCREEN, ok_button)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if ok_button.collidepoint(event.pos):
                        index += 1
            pygame.display.flip()
            clock.tick(60)
    instructions()

    for i in range(3):
        girl_raccoon = pygame.sprite.Sprite()
        girl_raccoon.image = pygame.image.load('girl_raccoon.png').convert_alpha()
        girl_raccoon.image = pygame.transform.scale(girl_raccoon.image, (200, 300))
        girl_raccoon.rect = girl_raccoon.image.get_rect()
        girl_raccoon.rect.topleft = (random.randint(100, 900), random.randint(100, 700))
        girl_raccoon.speed = [random.choice([-2, 2]), random.choice([-2, 2])]
        girl_raccoon.flavor = "girl"
        raccoons.add(girl_raccoon)

    for i in range(3):
        boy_raccoon = pygame.sprite.Sprite()
        boy_raccoon.image = pygame.image.load('boy_raccoon.png').convert_alpha()
        boy_raccoon.image = pygame.transform.scale(boy_raccoon.image, (200, 300))
        boy_raccoon.rect = boy_raccoon.image.get_rect()
        boy_raccoon.rect.topleft = (random.randint(100, 900), random.randint(100, 700))
        boy_raccoon.speed = [random.choice([-2, 2]), random.choice([-2, 2])]
        boy_raccoon.flavor = "boy"
        raccoons.add(boy_raccoon)

    while running:
        SCREEN.blit(dining, (0, 0))
        clock = 0
        timer += 1
        if timer >= 6600:
            print(1)
            return "lose1"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = [r for r in raccoons if r.rect.collidepoint(event.pos)]
                for r in clicked:
                    raccoons.remove(r)


        # Update positions
        for raccoon in raccoons:
            raccoon.rect.x += raccoon.speed[0]
            raccoon.rect.y += raccoon.speed[1]

            # Bounce off walls
            if raccoon.rect.left <= 0 or raccoon.rect.right >= WIDTH:
                raccoon.speed[0] *= -1
            if raccoon.rect.top <= 0 or raccoon.rect.bottom >= HEIGHT:
                raccoon.speed[1] *= -1

            SCREEN.blit(raccoon.image, raccoon.rect)
        
        pygame.display.flip()
        if len(raccoons) == 0:
            return "minions dead"


def epic_battle():
    health = 10
    big_chungus = pygame.sprite.Sprite()
    big_chungus.image = pygame.transform.scale(pygame.image.load("finalboss.png").convert_alpha(), (650, 800))
    big_chungus.rect = big_chungus.image.get_rect(center=(WIDTH//2, HEIGHT//2-100))
    
    running = True
    while running:
        SCREEN.blit(dining, (0, 0))
        SCREEN.blit(big_chungus.image, big_chungus.rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if big_chungus.rect.collidepoint(event.pos):
                    health -= 1
                    if health > 0:
                        # Shrink the boss
                        w = int(big_chungus.image.get_width() / 1.2)
                        h = int(big_chungus.image.get_height() / 1.2)
                        big_chungus.image = pygame.transform.scale(big_chungus.image, (w, h))
                        big_chungus.rect = big_chungus.image.get_rect(center=big_chungus.rect.center)
                    else:
                        running = False  # End the battle
        
        pygame.display.flip()
        clock.tick(60)
    
    return "win"

    
def win(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Optional: add a way to exit or continue, e.g. press a key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.blit(win_screen, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def lose1(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Optional: add a way to exit or continue, e.g. press a key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.blit(lose1_screen, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def lose2(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Optional: add a way to exit or continue, e.g. press a key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.blit(lose2_screen, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    

        
                


# --- Main Flow ---
status = "start"

while True:
    if status == "start":
        status = start(SCREEN)
    elif status == "icecapp":
        run_icecapp_game()
        status = run_timbits_game()
    elif status == "raccoon":
        status = battle()
    elif status == "minions dead":
        status = epic_battle()
    elif status == "win":
        win(SCREEN)
    elif status == "lose1":
        lose1(SCREEN)

   