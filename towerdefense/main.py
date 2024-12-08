import pygame
import random
from td_pkg.Tower import *
from td_pkg.Enemy import *
from td_pkg.Play import *
from pygame.locals import *

# Pygame 초기화
pygame.init()

# 사운드 초기화
pygame.mixer.init()

#사운드 로드
sound = pygame.mixer.Sound("towerdefense/Blippy Trance.mp3")

# 화면 크기 설정
screen_width = 1210#게임 화면 (0<x<800) , ui (800<x<1200)
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('tower_defense')
background = pygame.image.load('towerdefense/td_image/background.png')
ganghwa = pygame.image.load('towerdefense/td_image/ganghwa.png')
buildtower = pygame.image.load('towerdefense/td_image/tower.png')
setting = pygame.image.load('towerdefense/td_image/setting.png')
start_background = pygame.image.load('towerdefense/td_image/start.png')
manual_button = pygame.image.load('towerdefense/td_image/manual_click.png')
game_manual = pygame.image.load('towerdefense/td_image/manual.png')
game_manual_out = pygame.image.load('towerdefense/td_image/manual_x.png')

class NoMoney(Exception):
    def __init__(self):
        super().__init__('not enough money')
class SpTowerUpgrade(Exception):
    def __init__(self):
        super().__init__('This tower cannot be upgraded')

# 게임 루프
def game_loop():
    clock = pygame.time.Clock()

    running = True
    game_over = False
    start = True
    manual = False

    infotowers = [Tower(2000,0,'common'),Tower(2000,0,'rare'),Tower(2000,0,'epic'),Tower(2000,0,'slow'),Tower(2000,0,'percent')]#타워 리스트(타워 정보띄우기용 타워)]
    towers = []#타워 리스트
    enemies = []#적 리스트
    buttons = []

    Enemy.bosscount = 0
    Enemy.num = 0

    player = Player(5, 4000)
    best_score = 0

    NoMoneytext = ''
    spupgradetext = ''
    spupgradetime = 0
    lastenhancetime = 0
    NoMoneytime = 0

    ganghwa_rect = pygame.Rect(ganghwa.get_rect(topleft=(1091, 355)))
    setting_rect = pygame.Rect(setting.get_rect(topleft=(740, 740)))
    manual_rect = pygame.Rect(manual_button.get_rect(topleft=((1210-manual_button.get_width())/2,(800-manual_button.get_height())/2+70)))
    manualx_rect = pygame.Rect(game_manual_out.get_rect(topleft=((1210-game_manual.get_width())/2+967,(800-game_manual.get_height())/2)))

    for i in range(1,4):
        buttons.append((125,150*i-5))
        buttons.append((265,150*i-5))
        buttons.append((325,150*i-5))
        buttons.append((465,150*i-5))
        buttons.append((525,150*i-5))
        buttons.append((665,150*i-5))

    tower_type = 'common'#타워의 기본 타입 = common

    while running:
        while start:
            screen.blit(start_background,(0,0))
            screen.blit(manual_button,((1210-manual_button.get_width())/2,(800-manual_button.get_height())/2+70))
            
            gamestart_text = choosefont(40).render('Press Any Key to Start',True,(0,0,0))
            screen.blit(gamestart_text, ((1210-gamestart_text.get_width())/2,(800-gamestart_text.get_height())/2+20))
            
            if manual:
                screen.blit(game_manual,((1210-game_manual.get_width())/2,(800-game_manual.get_height())/2))
                screen.blit(game_manual_out,((1210-game_manual.get_width())/2+967,(800-game_manual.get_height())/2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    start = False
                    sound.play(loops=-1)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and manual_rect.collidepoint(event.pos):
                    manual = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and manualx_rect.collidepoint(event.pos):
                    manual = False

            pygame.display.update()
        screen.blit(background,(0,0))
        screen.blit(ganghwa,(1088,355))
        screen.blit(setting,(740,740))
        ganghwatext = choosefont(30).render('upgrade',True,(0,0,0))
        screen.blit(ganghwatext,((126-ganghwatext.get_width())/2+1078,362))
        for button in buttons:
            screen.blit(buildtower,(button))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    button_rect = pygame.Rect(button[0], button[1], buildtower.get_width(), buildtower.get_height())
                    if button_rect.collidepoint(event.pos):
                        new_tower = Tower(button[0]+15, button[1]+15, tower_type)
                        if new_tower.is_same_coord(towers):
                            try:
                                if new_tower.cost > player.money:
                                    raise NoMoney
                            except NoMoney as e:
                                NoMoneytime = pygame.time.get_ticks()
                                NoMoneytext = e
                            else:
                                player.usecoin(new_tower.cost)
                                towers.append(new_tower)

                if setting_rect.collidepoint(event.pos):
                    player.circle_setting()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for button in buttons:
                    button_rect = pygame.Rect(button[0], button[1], buildtower.get_width(), buildtower.get_height())
                    for tower in towers:
                        if tower.x == button[0]+15 and tower.y == button[1]+15 and button_rect.collidepoint(event.pos):
                            towers.remove(tower)
        


        if pygame.time.get_ticks() - NoMoneytime < 2000:
            screen.blit(choosefont(30).render(f'{NoMoneytext}',True,(255,0,0)),(20,700))

        if player.hp <= 0:
            player.hp = 0
            game_over = True

        if player.score >= best_score:
            best_score = player.score

        hptext = choosefont(40).render('HP : '+str(player.hp),True,(0,0,0))
        screen.blit(hptext,(830,420))

        moneytext = choosefont(35).render('COIN : '+str(player.money)+'$',True,(0,0,0))
        screen.blit(moneytext,(830,590))

        scoretext = choosefont(35).render('SCORE : ' +str(player.score),True,(0,0,0))
        screen.blit(scoretext,(830,470))

        bestscoretext = choosefont(35).render('BEST SCORE : ' +str(best_score),True,(0,0,0))
        screen.blit(bestscoretext,(830,510))

        if player.rangecircle:
            settingtext = choosefont(25).render('ON',True,(0,0,0))
        else:
            settingtext = choosefont(25).render('OFF',True,(0,0,0))
        screen.blit(settingtext,(740+(50-settingtext.get_width())/2,740+(50-settingtext.get_height())/2))


        for tower in towers:
            if tower.type == 'common':
                tower.damage = tower.initial_damage*1.2**(Player.c_level-1)
            elif tower.type == 'rare':
                tower.damage = tower.initial_damage*1.2**(Player.r_level-1)
            elif tower.type == 'epic':
                tower.damage = tower.initial_damage*1.2**(Player.e_level-1)

        for tower in infotowers:
            if tower.type == 'common':
                tower.damage = tower.initial_damage*1.2**(Player.c_level-1)
            elif tower.type == 'rare':
                tower.damage = tower.initial_damage*1.2**(Player.r_level-1)
            elif tower.type == 'epic':
                tower.damage = tower.initial_damage*1.2**(Player.e_level-1)

        if pygame.time.get_ticks() - spupgradetime < 2000:
            screen.blit(choosefont(30).render(f'{spupgradetext}',True,(255,0,0)),(20,730))

        if event.type == pygame.MOUSEBUTTONDOWN and ganghwa_rect.collidepoint(event.pos) and pygame.time.get_ticks()-lastenhancetime>500:
            try:
                upgradecost = 0
                if tower_type == 'common':
                    upgradecost = Player.c_cost
                elif tower_type == 'rare':
                    upgradecost = Player.r_cost
                elif tower_type == 'epic':
                    upgradecost = Player.e_cost
                
                if upgradecost > player.money:
                    raise NoMoney
                
                if tower_type in ['slow','percent']:
                    raise SpTowerUpgrade
            except NoMoney as e:
                NoMoneytime = pygame.time.get_ticks()
                NoMoneytext = e
            except SpTowerUpgrade as e:
                spupgradetime = pygame.time.get_ticks()
                spupgradetext = e
            else:
                player.levelup(tower_type)
            lastenhancetime = pygame.time.get_ticks()

        key = pygame.key.get_pressed()#key = 누른 키 저장
        if key[pygame.K_1]:#1,2,3,4,5 구분하여 설치할 타워의 type 변환
            tower_type = 'common'
        elif key[pygame.K_2]:
            tower_type = 'rare'
        elif key[pygame.K_3]:
            tower_type = 'epic'
        elif key[pygame.K_4]:
            tower_type = 'slow'
        elif key[pygame.K_5]:
            tower_type = 'percent'
        
        player.UI(tower_type,screen)

        for tower in infotowers:
            if tower.type == 'common':
                x,y = 816,80
                damagetext = choosefont(25).render('{:.1f} damage'.format(tower.damage),True,(0,0,0))
                speedtext = choosefont(25).render('{}s'.format(tower.speed/1000),True,(0,0,0))
                costtext = choosefont(25).render('{}$'.format(tower.cost),True,(0,0,0))
            elif tower.type == 'rare':
                x,y = 947,80
                damagetext = choosefont(25).render('{:.1f} damage'.format(tower.damage),True,(0,0,0))
                speedtext = choosefont(25).render('{}s'.format(tower.speed/1000),True,(0,0,0))
                costtext = choosefont(25).render('{}$'.format(tower.cost),True,(0,0,0))
            elif tower.type == 'epic':
                x,y = 1078,80
                damagetext = choosefont(25).render('{:.1f} damage'.format(tower.damage),True,(0,0,0))
                speedtext = choosefont(25).render('{}s'.format(tower.speed/1000),True,(0,0,0))
                costtext = choosefont(25).render('{}$'.format(tower.cost),True,(0,0,0))
            elif tower.type == 'slow':
                x,y = 816,281
                damagetext = choosefont(25).render(r'{}% slow'.format((10-tower.slownum*10)*10),True,(0,0,0))
                costtext = choosefont(25).render('{}$'.format(tower.cost),True,(0,0,0))
                speedtext = choosefont(25).render('',True,(0,0,0))
            elif tower.type == 'percent':
                x,y = 947,281
                damagetext = choosefont(25).render(r'{}% damage'.format((10-tower.perdamage*10)*10),True,(0,0,0))
                speedtext = choosefont(25).render('{}s'.format(tower.speed/1000),True,(0,0,0))
                costtext = choosefont(25).render('{}$'.format(tower.cost),True,(0,0,0))
                maxmin = choosefont(20).render('max:{}  min:{}'.format(tower.maxdamage,tower.mindamage),True,(0,0,0))
                screen.blit(maxmin,((126-maxmin.get_width())/2+x,y+90))

            typetext = choosefont(30).render(tower.type,True,(0,0,0))
            screen.blit(typetext,((126-typetext.get_width())/2+x,y))
            screen.blit(damagetext,((126-damagetext.get_width())/2+x,y+50))
            screen.blit(speedtext,((126-speedtext.get_width())/2+x,y+70))
            screen.blit(costtext,((126-costtext.get_width())/2+x,y+30))
        
        for tower in towers:
            tower.draw(player,screen)
            tower.attack(enemies,screen)
            

        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)

            enemy.isarrive()
            player.hpminus(enemy)

            if enemy.health<=0 and enemy.x<=780 and enemy.health>-10000:
                player.add_money_score(enemy)


        enemyspawn = min(0.06,((Enemy.num)**0.3)/500+0.03)

        if random.random() < enemyspawn:  # 랜덤 모듈로 생성한 난수가 enemyspawn보다 작을때 적 생성
            Enemy.numplus()
            if Enemy.num %50 == 0:# 적 50마리 생성될때 마다 보스 몹 소환
                enemies.append(Enemy(0,100,min(1300000,1500+50*(2**Enemy.bosscount)),2,min(6000,Enemy.bosscount*330),'boss'))#적이 생성된 횟수가 많을 수록 체력이 많아짐 --> 점점 난이도 상승
                Enemy.bosscount += 1
            else:#평상시엔 평범한 몹
                enemies.append(Enemy(0, 100,int(500+10*((Enemy.num*10)**0.6)) ,4, min(2000,150+20*(Enemy.num//50)),'common'))#적이 생성된 횟수가 많을 수록 체력이 많아짐 --> 점점 난이도 상승

        # 적이 죽으면 리스트에서 제거
        enemies = [enemy for enemy in enemies if enemy.health > 0]

        spawnp = choosefont(30).render('spawn probability : ' +f'{enemyspawn*100:.3f}%',True,(0,0,0))
        screen.blit(spawnp,(830,690))
        enemyhp = choosefont(30).render(f'common hp : {int(500+10*((Enemy.num*10)**0.6))}',True,(0,0,0))
        screen.blit(enemyhp,(830,715))
        bossenemyhp = choosefont(30).render(f'next boss hp : {min(1300000,1500+50*(2**Enemy.bosscount))}',True,(0,0,0))
        screen.blit(bossenemyhp,(830,740))


        if game_over:
            gameover_screen = pygame.Surface((1210, 800), pygame.SRCALPHA)#반투명한 회색으로 화면 채우기
            gameover_screen.fill((128, 128, 128, 200))
            screen.blit(gameover_screen, (0, 0))
            
            gameover_text = choosefont(80).render("Game Over", True, (255, 0, 0))#게임 오버 텍스트
            screen.blit(gameover_text, ((1210-gameover_text.get_width())/2,(800-gameover_text.get_height())/2-90))
            
            score_text = choosefont(50).render(f"SCORE : {player.score}      BESTSCORE : {best_score}", True, (255, 255, 255))#점수 띄우기
            screen.blit(score_text, ((1210-score_text.get_width())/2,(800-score_text.get_height())/2-30))

            restart_text = choosefont(30).render("Press R to restart", True, (255, 255, 255))#다시시작 텍스트
            screen.blit(restart_text, ((1210-restart_text.get_width())/2,(800-restart_text.get_height())/2+10))
            
            pygame.display.update()#이 조건문 이후에 while문에 갇히므로 디스플레이 업데이트 한번하기
            
            while game_over:#게임 정지
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game_over = False

                    key = pygame.key.get_pressed()
                    if key[pygame.K_r]:#r 누르면 전부 초기화 최고 기록 빼고
                        Player.c_level,Player.r_level,Player.e_level = 1,1,1
                        Player.c_cost, player.r_cost, Player.e_cost = 1000,2000,3000
                        game_over = False
                        infotowers = [Tower(2000,0,'common'),Tower(2000,0,'rare'),Tower(2000,0,'epic'),Tower(2000,0,'slow'),Tower(2000,0,'percent')]
                        towers = []
                        enemies = []

                        player = Player(5, 4000)
                        tower_type = 'common'
                        Enemy.num = 0
                        Enemy.bosscount = 0

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# 게임 시작
game_loop()
