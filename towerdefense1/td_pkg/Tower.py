import pygame

class Tower:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

        if type == 'common':
            self.damage = 80
            self.initial_damage = 80
            self.range = 110
            self.speed = 300
            self.color = (0,255,0)
            self.cost = 500
        
        elif type == 'rare':
            self.damage = 240
            self.initial_damage = 240
            self.range = 170
            self.speed = 400
            self.color = (0,128,128)
            self.cost = 2000

        elif type == 'epic':
            self.damage = 55
            self.initial_damage = 55
            self.range = 230
            self.speed = 100
            self.color = (0,0,0)
            self.cost = 4000

        #---------------------------------위쪽이 기본타워,아래쪽이 특수타워
        elif type == 'slow':#슬로우(데미지 0)
            self.range = 200
            self.color = (128,0,0)
            self.cost = 5000
            self.slownum = 0.6
            self.speed = 0
            self.damage = 0
        elif type == 'percent':#적 현재 체력의 40퍼센트 데미지, 범위에 있는 적 중 가장 hp가 많은적 공격, 최소 공격력 150
            self.perdamage = 0.8
            self.range = 150
            self.speed = 500
            self.color = (0,128,0)
            self.mindamage = 50
            self.maxdamage = 7000
            self.cost = 7000

        self.lastattack = pygame.time.get_ticks()
        
    def draw(self,player,screen):#타워 생성
        if player.rangecircle:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.range, 1)
        pygame.draw.rect(screen, self.color, (self.x-10, self.y-10, 20, 20))
        pygame.draw.rect(screen, (0,0,0), (self.x-10, self.y-10, 20, 20),1)
    def attack(self, enemies,screen):#attack_speed에 맞춰서 공격
        if self.type == 'slow':
            for enemy in enemies:
                if self.is_in_range(enemy):
                    pygame.draw.line(screen, self.color, (self.x,self.y), (enemy.x+10,enemy.y+10), 4)
                    if self not in enemy.slow_tower:
                        enemy.slow_tower.append(self)
                else:
                    if self in enemy.slow_tower:
                        enemy.slow_tower.remove(self)
                    
                if enemy.slow_tower:
                    enemy.speed = enemy.initial_speed*self.slownum
                else:
                    enemy.speed = enemy.initial_speed
        elif self.type == 'percent':
            target = False
            target_hp = 0
            for enemy in enemies:
                if enemy.health > target_hp and self.is_in_range(enemy):
                    target = enemy
                    target_hp = enemy.health
            if target and pygame.time.get_ticks()-self.lastattack >= self.speed:
                if target.health <= self.mindamage:
                    target.health -= self.mindamage
                elif target.health*(1-self.perdamage) >= self.maxdamage:
                    target.health -= self.maxdamage
                else:
                    target.health *= self.perdamage
                pygame.draw.line(screen, self.color, (self.x,self.y), (target.x+10,target.y+10), 4)
                self.lastattack = pygame.time.get_ticks()
        
        else:
            for enemy in enemies:
                if pygame.time.get_ticks()-self.lastattack >= self.speed and self.is_in_range(enemy):
                    enemy.health -= self.damage
                    pygame.draw.line(screen, self.color, (self.x,self.y), (enemy.x+10,enemy.y+10), 4)
                    self.lastattack = pygame.time.get_ticks()

    def is_in_range(self, enemy):#공격 범위에 적이 들어왔는가?
        distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
        return distance <= self.range

    def is_same_coord(self,towers):
        for tower in towers:
            if self.x == tower.x and self.y == tower.y:
                return False
        return True