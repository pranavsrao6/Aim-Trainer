import pygame, sys, random

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound('images/gunshot.mp3')
        self.gunshot.set_volume(0.3)
        self.shots_fired = 0
        self.shots_hits = 0

    def create_target(self):
        for targets in range(random.randrange(1,2)):
            overlapping = True
            while overlapping:
                # Generate a new target
                new_target = Target('images/target_red3.png', random.randrange(50, screen_width - 300),
                                    random.randrange(75, screen_height - 150))
                # Check for overlap with existing targets
                overlapping = pygame.sprite.spritecollide(new_target, target_group, False)

                # If there's no overlap and the target is within the screen, add it to the group
                if not overlapping:
                    target_group.add(new_target)
    def scale_image(self):
        self.image = pygame.transform.scale(self.image,(30,30))
        self.rect = self.image.get_rect()

    def shoot(self):
        self.gunshot.play()
        self.shots_fired += 1
        for target in pygame.sprite.spritecollide(crosshair,target_group,True):
            self.shots_hits += 1
            self.create_target()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def getAccuracy(self):
        if self.shots_fired == 0:
            return 0
        accuracy = self.shots_hits/self.shots_fired
        return round(accuracy,4)


class Target(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

# General Setup
pygame.init()
pygame.mixer.pre_init(44100, -16,2, 512 )
clock = pygame.time.Clock()

# Game Screen
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('images/bg_img.png')
background = pygame.transform.scale(background,(screen_width,screen_height))
pygame.mouse.set_visible(False)
game_font = pygame.font.Font("freesansbold.ttf", 64)
stat_font = pygame.font.Font("freesansbold.ttf", 48)

# Pause
pause_text = game_font.render("PAUSED", False, pygame.Color('white'))
is_paused = False


# Crosshair
crosshair = Crosshair('images/crosshair_white_small.png')
crosshair.scale_image()
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Targets
target_group = pygame.sprite.Group()

for targets in range(30):
    overlapping = True
    while overlapping:
        # Generate a new target
        new_target = Target('images/target_red3.png', random.randrange(50, screen_width-300), random.randrange(75, screen_height-150))
        # Check for overlap with existing targets
        overlapping = pygame.sprite.spritecollide(new_target, target_group, False)

        # If there's no overlap and the target is within the screen, add it to the group
        if not overlapping:
            target_group.add(new_target)
# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_paused = not is_paused
    if is_paused:
        screen.fill(pygame.Color('black'))
        screen.blit(pause_text,(screen_width/2 - pause_text.get_width()+45, 100))
        shots_fired = stat_font.render(f"Shots Fired: {crosshair.shots_fired}", False, pygame.Color('white'))
        accuracy = stat_font.render(f"Accuracy: {crosshair.getAccuracy()*100}%", False, pygame.Color('white'))
        screen.blit(shots_fired, (690,400))
        screen.blit(accuracy, (700, 500))

    pygame.display.flip()
    screen.blit(background,(0,0))
    target_group.draw(screen)
    crosshair_group.draw(screen)
    crosshair_group.update()
    clock.tick(60)
