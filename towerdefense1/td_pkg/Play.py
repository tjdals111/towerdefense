import pygame

def choosefont(size):
    font = pygame.font.Font(None, size)
    return font

class Player:
    c_level,r_level,e_level = 1,1,1
    c_cost, r_cost, e_cost = 1000,2000,3000
    
    def __init__(self,hp,money):
        self.hp = hp
        self.initialhp = hp
        self.money = money
        self.score = 0
        self.rangecircle = True

    def hpminus(self,enemy):
        if enemy.isarrive():#적이 도착했을때 hp -1 보스는 -2
            if enemy.tag == 'boss':
                self.hp -= 2
            else:
                self.hp -= 1
            return self.hp

    def usecoin(self,usemoney):#하나 설치할때 돈 소모
        if usemoney<=self.money:
            self.money -= usemoney

    def add_money_score(self,enemy):#적 잡을때 마다 돈 추가
        if enemy.health<=0 and enemy.x<=780 and enemy.health>-10000:
            self.score += enemy.initial_hp//10
            self.money += enemy.coin

        if self.money >= 100000:
            self.money = 100000

    def circle_setting(self):
        self.rangecircle = not self.rangecircle

    def UI(self,tower_type,screen):
        if tower_type == 'common':
            pygame.draw.rect(screen, (255,255,100), (816,5, 126, 194),5)
            pygame.draw.rect(screen, (0,255,0), (1121,230,40,40))
            pygame.draw.rect(screen, (0,0,0), (1121,230,40,40),2)
            leveltext = choosefont(30).render('level '+ str(Player.c_level),True,(0,0,0))
            upgradecost_text = choosefont(25).render(str(Player.c_cost)+'$',True,(0,0,0))
        elif tower_type == 'rare':
            pygame.draw.rect(screen, (255,255,100), (947,5, 126, 194),5)
            pygame.draw.rect(screen, (0,128,128), (1121,230,40,40))
            pygame.draw.rect(screen, (0,0,0), (1121,230,40,40),2)
            leveltext = choosefont(30).render('level '+ str(Player.r_level),True,(0,0,0))
            upgradecost_text = choosefont(25).render(str(Player.r_cost)+'$',True,(0,0,0))
        elif tower_type == 'epic':
            pygame.draw.rect(screen, (255,255,100), (1078,5, 126, 194),5)
            pygame.draw.rect(screen, (0,0,0), (1121,230,40,40))
            pygame.draw.rect(screen, (0,0,0), (1121,230,40,40),2)
            leveltext = choosefont(30).render('level '+ str(Player.e_level),True,(0,0,0))
            upgradecost_text = choosefont(25).render(str(Player.e_cost)+'$',True,(0,0,0))
        elif tower_type == 'slow':
            pygame.draw.rect(screen, (255,255,100), (816,206, 126, 194),5)
        elif tower_type == 'percent':
            pygame.draw.rect(screen, (255,255,100), (947,206, 126, 194),5)

        if tower_type in ('common','rare','epic'):
            typetext = choosefont(30).render(tower_type,True,(0,0,0))
            screen.blit(typetext,((126-typetext.get_width())/2+1078,281))
            screen.blit(leveltext,((126-leveltext.get_width())/2+1078,301))
            screen.blit(upgradecost_text,((126-upgradecost_text.get_width())/2+1078,329))


        pygame.draw.rect(screen, (0,255,0), (859,30, 40, 40))
        pygame.draw.rect(screen, (0,128,128), (990, 30, 40, 40))
        pygame.draw.rect(screen, (0,0,0), (1121, 30, 40, 40))
        pygame.draw.rect(screen, (128,0,0), (859, 230, 40, 40))
        pygame.draw.rect(screen, (0,128,0), (990, 230, 40, 40))

        pygame.draw.rect(screen, (0,0,0), (859,30, 40, 40),2)
        pygame.draw.rect(screen, (0,0,0), (990, 30, 40, 40),2)
        pygame.draw.rect(screen, (0,0,0), (1121, 30, 40, 40),2)
        pygame.draw.rect(screen, (0,0,0), (990, 230, 40, 40),2)
        pygame.draw.rect(screen, (0,0,0), (859, 230, 40, 40),2)

    def levelup(self,tower_type):
        if tower_type == 'common' and self.money >= Player.c_cost:
            Player.c_level += 1
            self.usecoin(Player.c_cost)
            Player.c_cost = int(Player.c_cost*1.5)
        elif tower_type == 'rare' and self.money >= Player.r_cost:
            Player.r_level += 1
            self.usecoin(Player.r_cost)
            Player.r_cost = int(Player.r_cost*1.5)
        elif tower_type == 'epic' and self.money >= Player.e_cost:
            Player.e_level += 1
            self.usecoin(Player.e_cost)
            Player.e_cost = int(Player.e_cost*1.5)