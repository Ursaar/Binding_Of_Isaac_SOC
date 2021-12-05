import pygame


pygame.init()

SCREEN_WIDTH = 800
SCREE_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREE_HEIGHT))
pygame.display.set_caption("Binding of Isaac")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define player action variables
moving_up = False
moving_down = False
moving_left = False
moving_right = False

# define colours
BG = (144, 201, 120)


def draw_bg():
    screen.fill(BG)


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()



        temp_list = []
        for i in range(1): # idle
            img = pygame.image.load(f'resources/sprites/{self.char_type}/Idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(10): # moving sides
            img = pygame.image.load(f'resources/sprites/{self.char_type}/Move_sides/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(5): # moving up
            img = pygame.image.load(f'resources/sprites/{self.char_type}/Move_up/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(8): # moving down
            img = pygame.image.load(f'resources/sprites/{self.char_type}/Move_down/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_up, moving_down, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_up:
            dy = -self.speed
            self.direction = 1
        if moving_down:
            dy = self.speed
            self.direction = -1
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Player('Player', 200, 200, 3, 5)

run = True
while run:

    clock.tick(FPS)

    draw_bg()

    player.update_animation()
    player.draw()

    # update player actions
    if player.alive:
        if moving_left or moving_right:
            player.update_action(1)  # 3: left/right
        elif moving_up:
            player.update_action(2)  # 2: up
        elif moving_down:
            player.update_action(3)  # 1: down
        else:
            player.update_action(0)  # 0: idle

    player.move(moving_up, moving_down, moving_left, moving_right)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()

pygame.quit()
