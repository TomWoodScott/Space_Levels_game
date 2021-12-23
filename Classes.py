import os.path
import time

import pygame


class Ship:
    pygame.mixer.init()
    COOL_DOWN = 30
    BULLETSOUND = pygame.mixer.Sound(os.path.join('Assets', "Game_bullet.wav"))
    HITSOUND = pygame.mixer.Sound(os.path.join('Assets', "Game_hit.wav"))

    def __init__(self, x, y, spaceship_img):
        self.x = x
        self.y = y
        self.image = spaceship_img
        self.bullets = []
        self.cool_down_timer = 0

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

        for bullet in self.bullets:
            bullet.draw(window)

    def bullet_cool_down(self):
        if self.cool_down_timer >= self.COOL_DOWN:
            self.cool_down_timer = 0
        elif self.cool_down_timer > 0:
            self.cool_down_timer += 1


class Player(Ship):

    def __init__(self, x, y, spaceship_img, bullet_img, width=55, height=40, health=100):
        super().__init__(x, y, spaceship_img)
        self.mask = pygame.mask.from_surface(self.image)
        self.max_hp = health
        self.bullet_img = bullet_img
        self.velocity = 5
        self.bullet_vel = -10
        self.width = width
        self.height = height
        self.bullet_dmg = 1
        self.player_score = 0
        self.power_bar = 0
        self.power_bar_times = 0

    def move_bullets(self, enemies):
        self.bullet_cool_down()

        for bullet in self.bullets:
            bullet.move(self.bullet_vel)
            if bullet.off_screen(900):
                self.power_bar = 0
                self.bullets.remove(bullet)
            else:
                for enemy in enemies:
                    for b in self.bullets:
                        if b.collision(enemy):
                            self.power_bar += 1
                            enemy.health -= self.bullet_dmg
                            if enemy.health <= 0:
                                self.HITSOUND.play()
                                self.player_score += enemy.score
                                if enemies:
                                    enemies.remove(enemy)
                                print(self.player_score)
                            self.bullets.remove(b)

    def level_up(self, image, bullet_img):
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.bullet_dmg += 1
        self.velocity += 2
        self.width += 10
        self.bullet_vel -= 10
        self.bullet_img = bullet_img

    # to do: depending on spaceship level
    def shoot(self):
        if self.cool_down_timer == 0:
            bullet = Bullet(self.x + self.width / 2 - 1, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_timer = 1
        if self.power_bar == 20:
            for i in range(0, 400, 10):
                bullet = Bullet(i, self.y, self.bullet_img)
                self.bullets.append(bullet)
            self.power_bar = 0

    @classmethod
    def level_up_shoot_speed(cls):
        cls.COOL_DOWN -= 10

    @staticmethod
    def collide(object1, object2):
        x_difference = object2.x - object1.x
        y_difference = object2.y - object1.y
        return object1.mask.overlap(object2.mask, (x_difference, y_difference)) is not None

    @staticmethod
    def spaceship_movement(keys_pressed, player):
        if keys_pressed[pygame.K_LEFT] and player.x > 0:
            player.x -= player.velocity
        if keys_pressed[pygame.K_RIGHT] and player.x + player.width <= 400:
            player.x += player.velocity
        if keys_pressed[pygame.K_UP] and player.y >= 100:
            player.y -= player.velocity
        if keys_pressed[pygame.K_DOWN] and player.y + player.height <= 900:
            player.y += player.velocity
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player.shoot()
            Player.BULLETSOUND.play()


class Bullet:


    def __init__(self, x, y, bullet_img):
        self.x = x
        self.y = y
        self.bullet_img = bullet_img
        self.mask = pygame.mask.from_surface(self.bullet_img)

    def draw(self, window):
        window.blit(self.bullet_img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (height >= self.y >= 0)

    def collision(self, enemy):
        return Player.collide(enemy, self)


class Enemy:

    def __init__(self, x, y, image, vel=2, health=1, dmg=1, score=5):
        self.x = x
        self.y = y
        self.health = health
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = dmg
        self.vel = vel
        self.score = score

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.vel


