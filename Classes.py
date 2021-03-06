import os.path
import pygame
from pygame import mixer


class Ship:
    pygame.mixer.init()
    COOL_DOWN = 30
    MAX_HP = 10
    BULLET_SOUND = mixer.Sound(os.path.join('Assets', "Game_bullet.wav"))
    HIT_SOUND = mixer.Sound(os.path.join('Assets', "Game_hit.wav"))

    def __init__(self, x, y, spaceship_img):
        self.x = x
        self.y = y
        self.image = spaceship_img
        self.bullets = []
        self.cool_down_timer = 0


    def bullet_cool_down(self):
        if self.cool_down_timer >= self.COOL_DOWN:
            self.cool_down_timer = 0
        elif self.cool_down_timer > 0:
            self.cool_down_timer += 1


class Player(Ship):

    def __init__(self, x, y, spaceship_img, bullet_img, width=55, height=40, health=10, score=0, level=1,
                 bullet_dmg=1, velocity=5, bullet_vel=-20):
        super().__init__(x, y, spaceship_img)
        self.mask = pygame.mask.from_surface(self.image)
        self.level = level
        self.health = health
        self.bullet_img = bullet_img
        self.velocity = velocity
        self.bullet_vel = bullet_vel
        self.width = width
        self.height = height
        self.bullet_dmg = bullet_dmg
        self.player_score = score

        self.power_bar = 0
        self.spaceship_image_count = 0

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

        if self.health <= 0:
            for enemy in Enemy.ENEMIES:
                Enemy.ENEMIES.remove(enemy)

    def move_bullets(self):
        self.bullet_cool_down()

        for bullet in self.bullets:
            bullet.move(self.bullet_vel)
            if bullet.off_screen(900):
                self.power_bar = 0
                self.bullets.remove(bullet)
            else:
                for enemy in Enemy.ENEMIES:
                    for b in self.bullets:

                        if b.collision(enemy):
                            self.power_bar += 1
                            enemy.health -= self.bullet_dmg
                            if enemy.health <= 0:
                                Ship.HIT_SOUND.play()
                                self.player_score += enemy.score
                                if Enemy.ENEMIES:
                                    Enemy.ENEMIES.remove(enemy)
                                print(self.player_score)
                            self.bullets.remove(b)

    def level_time(self, images_dic):
        # TO DO: condense into 1 statement, maybe combing level_time with level_up
        if self.level == 2:
            if self.player_score >= 50:
                self.level_up(images_dic[self.level + 1][0], images_dic[self.level + 1][1])

        if self.level == 1:
            if self.player_score >= 30:
                self.level_up(images_dic[self.level + 1][0], images_dic[self.level + 1][1])

    def level_up(self, image, bullet_img):
        self.level += 1
        self.image = image
        self.spaceship_image_count += 1
        self.mask = pygame.mask.from_surface(self.image)
        self.bullet_dmg += 1
        self.velocity += 2
        self.width += 10
        self.bullet_vel -= 10
        self.bullet_img = bullet_img
        self.level_up_shoot_speed()

    # to do: depending on spaceship level
    def shoot(self):

        if self.cool_down_timer == 0:
            if self.level < 3:
                bullet = Bullet(self.x + self.width / 2 - 1, self.y, self.bullet_img)
                self.bullets.append(bullet)

            elif self.level < 5:
                bullet1 = Bullet(self.x + 2, self.y, self.bullet_img)
                bullet2 = Bullet((self.x + self.width) - 17, self.y, self.bullet_img)
                self.bullets.append(bullet1)
                self.bullets.append(bullet2)
            else:
                pass
            pygame.mixer.Sound.stop(Player.BULLET_SOUND)
            Player.BULLET_SOUND.play()
            self.cool_down_timer = 1
        if self.power_bar >= 20:
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
    ENEMIES = []

    def __init__(self, x, y, image, vel=2, health=1, dmg=1, score=5):
        self.x = x
        self.y = y
        self.health = health
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = dmg
        self.vel = vel
        self.score = score
        self.weight = 10

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, player):
        self.y += self.vel
        if self.y >= 900:
            player.health -= self.damage
            self.ENEMIES.remove(self)

    @classmethod
    def append(cls, enemy):
        cls.ENEMIES.append(enemy)



class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.clicked = False

    def draw(self, window):
        action = False
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        window.blit(self.image, (self.rect.x, self.rect.y))

        return action

