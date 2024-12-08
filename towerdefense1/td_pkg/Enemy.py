import pygame


class Enemy:
    num = 0
    bosscount = 0
    def __init__(self, x, y, health,speed ,coin,tag):
        self.x = x
        self.y = y
        self.health = health
        self.color = (255,0,0)
        self.speed = speed
        self.initial_speed = speed
        self.coin = coin
        self.arrive = False
        self.initial_hp = health
        self.tag = tag
        self.slow_tower = []

    def move(self):#몹이 움직이는 거 설정
        if (self.x % 200) <= 5 and self.x >= 150:
            if (self.x//200)%2 ==1:
                self.y += self.speed
                if self.y >= 500:
                    self.x +=self.speed
            else:
                self.y -= self.speed
                if self.y <= 100:
                    self.x +=self.speed
        else:
            self.x += self.speed
    def draw(self,screen):#적 생성

        if self.health <= 0.4*self.initial_hp:
            self.color = (255,255,0)
        elif self.health <= 0.7*self.initial_hp:
            self.color = (255,165,0)

        if self.tag == 'common':
            pygame.draw.rect(screen, self.color, (self.x, self.y, 20, 20))
            pygame.draw.rect(screen, (0,0,0), (self.x, self.y, 20, 20),1)
        elif self.tag == 'boss':
            pygame.draw.rect(screen, self.color, (self.x, self.y, 25, 25))
            pygame.draw.rect(screen, (0,0,0), (self.x, self.y, 26, 26),5)

        hplength = 20*self.health/self.initial_hp
        pygame.draw.rect(screen, (0,0,0), (self.x-1, self.y+15, 22, 7))
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y+16, hplength, 5))

    def isarrive(self):#적이 오른쪽 끝에 도착했는지 확인
        if self.x > 780:#창이 800*800이라 x가 800이 넘으면 도착으로 판정
            self.health = -10000#창 넘어간 적 삭제 위해 체력 0으로 설정
            self.arrive = True
        return self.x>780
    
    @classmethod
    def numplus(cls):#적이 소환된 횟수 계산
        cls.num += 1