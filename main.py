import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and rotate images
SPACESHIP_IMAGE = pygame.image.load('spaceship.png')
SPACESHIP = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMAGE, (50, 50)), 90)

ENEMY_IMAGE = pygame.image.load('enemy.png')
ENEMY = pygame.transform.rotate(pygame.transform.scale(ENEMY_IMAGE, (50, 50)), 90)

BULLET_IMAGE = pygame.image.load('bullet.png')
BULLET = pygame.transform.scale(BULLET_IMAGE, (10, 20))

# Load sounds
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Play background music in a loop

SHOOT_SOUND = pygame.mixer.Sound('shoot.wav')

# Frame rate
FPS = 60

# Spaceship class
class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []
        self.image = SPACESHIP
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

    def move_bullets(self, vel, enemies):
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for enemy in enemies:
                    if bullet.collision(enemy):
                        enemies.remove(enemy)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = BULLET
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.y -= vel

    def off_screen(self, height):
        return not (0 <= self.y <= height)

    def collision(self, obj):
        return collide(self, obj)

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = ENEMY
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.y += vel

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def main():
    run = True
    clock = pygame.time.Clock()
    player = Spaceship(WIDTH // 2 - 25, HEIGHT - 60)
    enemies = []
    wave_length = 5
    enemy_vel = 1
    bullet_vel = 5

    def redraw_window():
        WIN.fill(BLACK)
        player.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - 5 > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x + 5 + 50 < WIDTH:
            player.x += 5
        if keys[pygame.K_SPACE]:  # Space bar to shoot
            bullet = Bullet(player.x + 20, player.y)
            player.bullets.append(bullet)
            SHOOT_SOUND.play()  # Play shooting sound

        player.move_bullets(bullet_vel, enemies)

        if len(enemies) == 0:
            for i in range(wave_length):
                enemy = Enemy(random.randint(50, WIDTH - 100), random.randint(-1500, -100))
                enemies.append(enemy)

        for enemy in enemies:
            enemy.move(enemy_vel)
            if enemy.y + 50 > HEIGHT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
