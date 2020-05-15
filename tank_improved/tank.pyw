from pygame import *
from random import randint
from uuid import uuid4

# import time
CELL_WIDTH = 8
CELL_HEIGHT = 8


class Timer:
    def __init__(self):
        self.timers = []

    def add(self, time, f, params, interval=0):
        options = {
            "interval": interval,
            "callback": f,
            "params": params,
            "time": time,
            "id": uuid4()}
        self.timers.append(options)
        # print(options)
        return options["id"]

    def destroy(self, id1):
        for timer in self.timers:
            if timer.id == id1:
                self.timers.remove(timer)
                return

    def update(self, t):
        for timer in self.timers:
            if t >= timer["time"]:
                timer["callback"](*timer["params"])
                if timer["interval"]:
                    timer["time"] += timer["interval"]  # !!!!!!!1!!1
                else:  # !!!!!!!!!!!!!!
                    self.timers.remove(timer)  # !!!!!!!!!!!!!!


class Tank:
    def __init__(self, direction, x, y, left, top, width, height):
        global sprites
        self.x = x
        self.y = y
        self.speed = [0, 0]
        self.health = 100
        self.direction = direction
        self.sprite = sprites.subsurface(left, top, width, height)
        self.rect = Rect(self.x, self.y, width, height)
        self.width = width
        self.height = height

    def draw(self):
        global screen
        screen.blit(self.sprite, (self.x, self.y))

    def move(self, level):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect = Rect(self.x, self.y, 13, 13)
        if self.rect.collidelist(level.walls) != -1:
            self.x -= self.speed[0]
            self.y -= self.speed[1]
            self.speed[0] = -self.speed[0]
            self.speed[1] = - self.speed[1]
            self.sprite = transform.rotate(self.sprite, 180)
            self.rect = Rect(self.x, self.y, self.width, self.height)

    def shoot(self, level):
        bul_speed = [0, 0]
        bul_position = [self.x, self.y]
        if self.direction == 0:
            bul_speed = [0, -5]
            bul_position = [self.x + 3, self.y - 16]
        elif self.direction == 1:
            bul_speed = [5, 0]
            bul_position = [self.x + 16, self.y + 3]
        elif self.direction == 3:
            bul_speed = [-5, 0]
            bul_position = [self.x - 16, self.y + 3]
        elif self.direction == 2:
            bul_speed = [0, 5]
            bul_position = [self.x + 3, self.y + 16]
        game.bullets.append(Bullet(bul_speed, bul_position[0], bul_position[1], 6, 6, game.level, 0))


class EnemyTank(Tank):
    def __init__(self, direction, x, y, left, top, width, height, level):
        Tank.__init__(self, direction, x, y, left, top, width, height)
        self.timer = Timer()
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.timer.add(0, self.move, [level], 1)
        self.speed = [0, -1]

    def move(self, level):
        # self.speed = [1, 0]
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect = Rect(self.x, self.y, 13, 13)
        if self.rect.collidelist(level.walls) != -1:
            self.x -= self.speed[0]
            self.y -= self.speed[1]
            if self.direction == 1:
                self.direction = 3
            elif self.direction == 0:
                self.direction = 2
            elif self.direction == 3:
                self.direction = 1
            elif self.direction == 2:
                self.direction = 0
            self.speed[0] = -self.speed[0]
            self.speed[1] = -self.speed[1]
            self.sprite = transform.rotate(self.sprite, 180)
            self.rect = Rect(self.x, self.y, self.width, self.height)
        self.a = randint(0, 100)
        if self.a == 1:
            self.shoot(game.level)
        if self.a == 2:
            self.direction = 0
            self.speed = [0, -1]
            self.sprite = transform.rotate(sprites.subsurface(self.left, self.top, self.width, self.height), 0)
        if self.a == 3:
            self.direction = 1
            self.speed = [1, 0]
            self.sprite = transform.rotate(sprites.subsurface(self.left, self.top, self.width, self.height), 270)
        if self.a == 4:
            self.direction = 2
            self.speed = [0, 1]
            self.sprite = transform.rotate(sprites.subsurface(self.left, self.top, self.width, self.height), 180)
        if self.a == 5:
            self.direction = 3
            self.speed = [-1, 0]
            self.sprite = transform.rotate(sprites.subsurface(self.left, self.top, self.width, self.height), 90)


class Boss(Tank):
    def __init__(self, direction, x, y, left, top, width, height, level):
        Tank.__init__(self, direction, x, y, left, top, width, height)
        self.timer = Timer()
        self.health = 1000
        self.sprite = image.load("img/Boss.png")
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.timer.add(0, self.move, [level], 1)
        self.rect = Rect(self.x, self.y, width, height)
        self.speed = [0, -1]

    def move(self, level):
        # self.speed = [1, 0]
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect = Rect(self.x, self.y, 32, 32)
        if self.rect.collidelist(level.walls) != -1:
            self.x -= self.speed[0]
            self.y -= self.speed[1]
            self.speed[0] = -self.speed[0]
            self.speed[1] = -self.speed[1]
            self.sprite = transform.rotate(self.sprite, 180)
            self.rect = Rect(self.x, self.y, self.width, self.height)
            if self.rect.collidelist(level.walls) != -1:
                self.x -= self.speed[0]
                self.y -= self.speed[1]
                if self.direction == 1:
                    self.direction = 3
                elif self.direction == 0:
                    self.direction = 2
                elif self.direction == 3:
                    self.direction = 1
                elif self.direction == 2:
                    self.direction = 0
                self.speed[0] = -self.speed[0]
                self.speed[1] = -self.speed[1]
                self.sprite = transform.rotate(self.sprite, 180)
                self.rect = Rect(self.x, self.y, self.width, self.height)
        self.a = randint(0, 6)
        if self.a > 4:
            self.shoot(game.level)
        if self.a == 2:
            self.direction = 0
            self.speed = [0, -1]
            self.sprite = transform.rotate(image.load("img/Boss.png"), 0)
        if self.a == 3:
            self.direction = 1
            self.speed = [1, 0]
            self.sprite = transform.rotate(image.load("img/Boss.png"), 270)
        if self.a == 4:
            self.direction = 2
            self.speed = [0, 1]
            self.sprite = transform.rotate(image.load("img/Boss.png"), 180)
        if self.a == 5:
            self.direction = 3
            self.speed = [-1, 0]
            self.sprite = transform.rotate(image.load("img/Boss.png"), 90)

    def shoot(self, level):
        bul_speed = [0, 0]
        bul_position = [self.x, self.y]
        if self.direction == 0:
            bul_speed = [0, -10]
            bul_position = [self.x + 15, self.y - 16]
        elif self.direction == 1:
            bul_speed = [10, 0]
            bul_position = [self.x + 16, self.y + 15]
        elif self.direction == 3:
            bul_speed = [-10, 0]
            bul_position = [self.x - 16, self.y + 15]
        elif self.direction == 2:
            bul_speed = [0, 10]
            bul_position = [self.x + 15, self.y + 16]
        game.bullets.append(BigBullet(bul_speed, bul_position[0], bul_position[1], 6, 6, game.level, 0))


class Bullet:
    def __init__(self, speed, x, y, width, height, level, target):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprite = image.load("img/bul.png").subsurface(0, 0, 6, 6)
        self.rect = Rect(self.x, self.y, width, height)
        self.width = width
        self.damage = 50
        self.height = height
        self.target = 0

    def draw(self):
        global screen
        screen.blit(self.sprite, (self.x, self.y))

    def move(self, level):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect = Rect(self.x, self.y, 13, 13)
        for i in range(len(game.enemies)):
            if self.rect.colliderect(game.enemies[i]):
                game.enemies[i].health -= self.damage
                self.target = 1
                break
        self.rect = Rect(self.x, self.y, self.width, self.height)
        for i in range(len(game.bosses)):
            if self.rect.colliderect(game.bosses[i]):
                game.bosses[i].health -= self.damage
                self.target = 1
                break
            self.rect = Rect(self.x, self.y, self.width, self.height)
        if self.rect.colliderect(game.player):
            self.target = 1
            game.player.health -= self.damage
            self.rect = Rect(self.x, self.y, self.width, self.height)
        if self.rect.collidelist(level.walls) != -1:
            self.target = 1
            self.rect = Rect(self.x, self.y, self.width, self.height)


class BigBullet(Bullet):  # NOT FINISHED!!!!
    def __init__(self, speed, x, y, width, height, level, target):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = 100
        self.sprite = image.load("img/BigBullet.png").subsurface(0, 0, 6, 6)
        self.rect = Rect(self.x, self.y, width, height)
        self.width = width
        self.height = height
        self.damage = 99
        self.target = 0

    def move(self, level):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect = Rect(self.x, self.y, 13, 13)
        if self.rect.collidelist(level.walls) != -1:
            self.target = 1
        if self.rect.collidelist(game.enemies) != -1:
            for i in range(len(game.enemies)):
                if self.rect.colliderect(game.enemies[i]):
                    game.enemies[i].health -= self.damage
                    self.target = 1
                    break
            self.rect = Rect(self.x, self.y, self.width, self.height)
        if self.rect.colliderect(game.player):
            game.player.health -= 100


class MyTank(Tank):
    def move(self, level):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect = Rect(self.x, self.y, 13, 13)
        if self.rect.collidelist(level.walls) != -1 or self.rect.collidelist(game.enemies) != -1:
            for i in range(len(game.enemies)):
                if self.rect.colliderect(game.enemies[i]):
                    game.enemies[i].health -= 50
                    break
            self.x -= self.speed[0]
            self.y -= self.speed[1]
            self.rect = Rect(self.x, self.y, self.width, self.height)
            self.rect = Rect(self.x, self.y, self.width, self.height)


class Scoreboard:  # NOT FINISHED!!!!!
    def __init__(self, level, data, x, y):
        self.x = x
        self.y = y
        self.letters = []
        self.sprites = []
        for ch in data:
            self.letters.append(ch)


class Level:
    def __init__(self, file):
        self.map1 = open(file).read().rstrip().split("\n")
        self.walls = []
        x = 0
        y = 0
        self.sprite = sprites.subsurface(256, 0, CELL_WIDTH, CELL_HEIGHT)
        for line in self.map1:
            for cell in line:
                if cell == '*':
                    self.walls += [Rect(x, y, CELL_WIDTH, CELL_HEIGHT)]
                x += CELL_WIDTH
            y += CELL_HEIGHT
            x = 0

    def draw(self):
        x = 0
        y = 0
        self.sprite = sprites.subsurface(256, 0, 8, 8)
        for line in self.map1:
            for cell in line:
                if cell == '*':
                    screen.blit(self.sprite, (x, y))
                x += CELL_WIDTH
            y += CELL_HEIGHT
            x = 0


class Game:
    def __init__(self):
        global sprites, screen
        init()
        display.set_caption("pipenki")
        screen = display.set_mode((480, 480))
        self.clock = time.Clock()
        self.time = 0
        sprites = image.load("img/sprites1.png")
        self.player = MyTank(0, 100, 100, 1, 2, 13, 13)
        self.level = Level('level01.txt')
        self.enemies = [EnemyTank(0, randint(16, 400), randint(16, 400), 129, 2, 13, 13, self.level) for i in range(10)]
        self.bullets = []
        self.bosses = []
        self.boss = False

    def draw(self):
        global screen
        screen.fill([0, 0, 0])
        self.player.draw()
        self.level.draw()
        for en in self.enemies:
            en.draw()
        for boss in self.bosses:
            boss.draw()
        for bul in self.bullets:
            bul.draw()
        display.flip()

    def start(self):
        while True:
            time_passed = self.clock.tick(40)
            for e in event.get():
                if e.type == QUIT:
                    quit()
                elif e.type == KEYDOWN:
                    if e.key == K_LEFT:
                        self.player.sprite = sprites.subsurface(34, 1, 13, 13)
                        self.player.speed = [-2, 0]
                        self.player.direction = 3
                    if e.key == K_RIGHT:
                        self.player.sprite = sprites.subsurface(97, 1, 13, 13)
                        self.player.speed = [2, 0]
                        self.player.direction = 1
                    if e.key == K_DOWN:
                        self.player.sprite = sprites.subsurface(65, 1, 13, 13)
                        self.player.speed = [0, 2]
                        self.player.direction = 2
                    if e.key == K_UP:
                        self.player.sprite = sprites.subsurface(1, 2, 13, 13)
                        self.player.speed = [0, -2]
                        self.player.direction = 0
                    if e.key == K_SPACE:
                        self.player.shoot(self.level)
                elif e.type == KEYUP:
                    self.player.speed = [0, 0]
                # elif e.key != K_LEFT and e.key != K_RIGHT and e.key != K_DOWN and e.key != K_UP:
                # self.player.speed = [0, 0]
            self.player.move(self.level)
            for i in range(len(self.enemies)):
                self.enemies[i].timer.update(self.time)
            for i in range(len(self.enemies)):
                if self.enemies[i].health <= 0:
                    self.enemies.remove(self.enemies[i])
                    break
            for i in range(len(self.bosses)):
                if (self.bosses[i].health <= 0):
                    self.bosses.remove(self.bosses[i])
                    break
            for i in range(len(self.bullets)):
                self.bullets[i].move(self.level)
                if self.bullets[i].target:
                    self.bullets.remove(self.bullets[i])
                    break
            if len(self.enemies) == 0 and not self.boss:
                self.bosses.append(Boss(0, randint(16, 400), randint(16, 400), 0, 0, 32, 33, self.level))
                self.boss = True
            if len(self.bosses) == 0 and self.boss:
                self.enemies = [EnemyTank(0, randint(16, 400), randint(16, 400), 129, 2, 13, 13, self.level) for i in
                                range(10)]
                self.boss = False
            for boss in self.bosses:
                boss.move(self.level)
            for en in self.enemies:
                en.move(self.level)
            if self.player.health <= 0:
                quit()
            self.draw()


game = Game()
game.start()
