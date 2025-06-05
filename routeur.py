import pygame, math, random
from time import time
from sys import exit


pygame.init()
screen = pygame.display.set_mode((1024, 720), pygame.RESIZABLE)
pygame.display.set_caption("Routeur")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)


# image
router = pygame.image.load('router.png')
cooper = pygame.image.load('item-copper.png')
crawler = pygame.image.load('crawler.png')
stell_weapon = pygame.image.load('stell-weapon.png')
distributor = pygame.image.load('distributor.png')
drill_laser_center = pygame.image.load('drill-laser-center.png')
background = [pygame.image.load('sand-floor1.png'), pygame.image.load('sand-floor3.png'), pygame.image.load('sand-floor2.png')]
height_background = background[0].get_height()
width_background = background[0].get_width()


# sprite
all_sprites_list = pygame.sprite.LayeredUpdates()
list_waepon = pygame.sprite.Group()
list_player = pygame.sprite.Group()
list_recompence = pygame.sprite.Group()
list_enemy = pygame.sprite.Group()
list_bullet = pygame.sprite.Group()


# global variable
global taille_screen, gameover, score, angle, shoot, menu, temps, nbclone
taille_screen = None
mouse = None
gameover = False
shoot = False
vitesse = 3
totalscore = 0
nbclone = 8
all_backgroud = []
achat = []
skin = distributor


def reset():
    global score, angle, menu, temp2, espacement, conter_espacement, temps
    temps = time()
    espacement = skin.get_width()//4
    conter_espacement = 0
    menu = 'play'
    score, angle = 0, 0
    temp2 = [((200, 200), 0)]

    all_sprites_list.empty()
    list_player.empty()
    list_recompence.empty()
    list_enemy.empty()
    list_waepon.empty

    Waepon()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global skin
        self.image = skin
        self.rect = skin.get_rect()
        list_player.add(self)
        all_sprites_list.add(self)
        self.futurmouvement = []

    def update(self):
        global skin
        self.rect.centerx = pygame.math.clamp(self.futurmouvement[0][0][0], 0, screen.get_width())
        self.rect.centery = pygame.math.clamp(self.futurmouvement[0][0][1], 0, screen.get_height())
        self.image = pygame.transform.rotate(skin, self.futurmouvement[0][1])
        self.futurmouvement.pop(0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = crawler
        self.rect = crawler.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.vitesse = random.uniform(0.8, 1.5)
        list_enemy.add(self)
        all_sprites_list.add(self)

    def update(self):
        global menu, skin
        distancemin = None
        # find the closest player
        for player in list_player.sprites():
            distance = math.hypot((player.rect.centerx-self.rect.centerx), (player.rect.centery-self.rect.centery))
            if distancemin ==  None:
                distancemin = distance
                minplayer = player
            if distancemin>distance:
                distancemin = distance
                minplayer = player
        
        if distancemin<(skin.get_width()+20):
            menu = 'game_over'

        # merci chat gpt j'ai pas apris sa en math 
        # noramliser(en gros c'est rendre la norme du vecteur a un mais garder le meme angle)
        self.rect.centerx += ((minplayer.rect.centerx-self.rect.centerx)/distancemin)*self.vitesse
        self.rect.centery += ((minplayer.rect.centery-self.rect.centery)/distancemin)*self.vitesse


class Waepon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = stell_weapon
        self.rect = stell_weapon.get_rect()
        list_waepon.add(self)
        all_sprites_list.add(self, layer = 2)

    def update(self):
        global shoot, vecteurplayer
        mouse = pygame.mouse.get_pos()
        deltax = mouse[0] - self.rect.centerx
        deltay = mouse[1] - self.rect.centery
        angle_to_mouse = math.atan2(deltay, deltax)
        self.image = pygame.transform.rotate(stell_weapon, math.degrees(-angle_to_mouse)-90)
        if shoot:
            shoot = False
            try:
                vecteur = pygame.math.Vector2.normalize(pygame.math.Vector2(deltax, deltay))
                vecteur.scale_to_length(5)
                vecteur = vecteur+vecteurplayer
                Bullet((self.rect.centerx, self.rect.centery), vecteur)
            except:
                pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, vector):
        super().__init__()
        self.image = drill_laser_center
        self.rect = drill_laser_center.get_rect()
        self.rect.center = pos
        self.vector = vector
        list_bullet.add(self)
        all_sprites_list.add(self)

    def update(self):
        self.rect.center += self.vector
        if not (0<self.rect.centerx<screen.get_width()) or not (0<self.rect.centery<screen.get_height()):
            self.kill()


class Recompence(pygame.sprite.Sprite):
    def __init__(self, xy):
        super().__init__()
        self.image = cooper
        self.rect = cooper.get_rect()
        self.rect.center = xy
        list_recompence.add(self)
        all_sprites_list.add(self)


def bouger(angle):
    global vecteurplayer, temp2, conter_espacement, nbclone
    listejoueur = list_player.sprites()
    if conter_espacement ==  0:
        if len(listejoueur)<nbclone: 
            player = Player()
            for element in temp2:
                player.futurmouvement.append(element)
    conter_espacement += 1
    if conter_espacement ==  espacement:
        conter_espacement = 0
    listejoueur = list_player.sprites()
    vecteurplayer = pygame.math.Vector2(vitesse*math.cos(angle), vitesse*math.sin(angle))
    x = pygame.math.clamp(temp2[-1][0][0]+vecteurplayer[0], 0, screen.get_width())
    y = pygame.math.clamp(temp2[-1][0][1]+vecteurplayer[1], 0, screen.get_height())
    angle = -math.degrees(angle)
    temp2.append(((x, y), angle))
    if len(temp2) >= nbclone*espacement:
        temp2.pop(0)
    
    for player in listejoueur:
        player.futurmouvement.append(((x, y), angle))

    listwaepon = list_waepon.sprites()
    for weapon in listwaepon:
        weapon.rect.centerx = x
        weapon.rect.centery = y


def afficher_fond():
    global taille_screen, temp1
    if taille_screen != screen.get_size():
        taille_screen = screen.get_size()
        all_backgroud.clear()
        for y in range(0, screen.get_height(), height_background):
            for x in range(0, screen.get_width(), width_background):
                a = random.randint(0, len(background)-1)
                all_backgroud.append((background[a], (x, y)))
        screen.blits(all_backgroud)
        temp1 = screen.copy()
    screen.blit(temp1, (0, 0))


def spawn_enemy():
    global taille_screen, temps
    tempsref = time()-temps
    if tempsref<218:
        chanced_aparition = int(-2*tempsref+100+(0.5*tempsref)**1.24)
    else:
        chanced_aparition = 0

    if len(list_enemy.sprites()) < 30 and random.randint(0, chanced_aparition) ==  0:
        side = random.randint(0, 3)
        width = taille_screen[0]
        height = taille_screen[1]
        if side ==  0:
            x, y = random.randint(0, width), height+30
        elif side ==  1: 
            x, y = random.randint(0, width), -30
        elif side ==  2: 
            x, y = width+30, random.randint(0, height)
        else: 
            x, y = -0, random.randint(0, height)
        Enemy(x, y)


reset()
while True:
    screen.fill((255, 255, 255))
    afficher_fond()
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            pygame.quit()
            exit()
            pygame.key.get_pressed
        if event.type ==  pygame.KEYDOWN:
            if menu ==  'game_over':
                if event.key ==  pygame.K_r :
                    reset()
                elif event.key ==  pygame.K_q :
                    pygame.quit()
                    exit()
                elif event.key ==  pygame.K_s :
                    menu = 'shop'
            
            elif menu ==  'shop':
                if event.key ==  pygame.K_r :
                    reset()
                elif event.key ==  pygame.K_q :
                    pygame.quit()
                    exit()
                elif event.key ==  pygame.K_b :
                    if not 'routeur' in achat:
                        if totalscore>= 100:
                            totalscore-100
                            achat.append('routeur')
                    else:
                        skin = router
        
        if event.type ==  pygame.MOUSEBUTTONDOWN:
            if menu ==  'play':
                shoot = True


    if menu ==  'play':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angle -= 0.1
        if keys[pygame.K_RIGHT]:
            angle += 0.1
        
        for i in pygame.sprite.groupcollide(list_recompence, list_player, True, False):
            score += 1
            totalscore += 1
        
        for enemy in pygame.sprite.groupcollide(list_enemy, list_bullet, False, True):
            Recompence(enemy.rect.center)
            enemy.kill()

        spawn_enemy()
        bouger(angle)
        all_sprites_list.update()
        all_sprites_list.draw(screen)
        texte = font.render(f"Score : {score}", True, (255, 255, 255))
        screen.blit(texte, (10, 10))


    elif menu ==  'game_over':
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Score Final: {score}", True, (255, 255, 255))
        restart_text = font.render("Appuyez sur R pour recommencer ou Q pour quitter ou S pour Shop", True, (255, 255, 255))
        
        screen_rect = screen.get_rect()
        
        game_over_rect = game_over_text.get_rect(center = (screen_rect.centerx, screen_rect.centery - 50))
        score_rect = score_text.get_rect(center = (screen_rect.centerx, screen_rect.centery))
        restart_rect = restart_text.get_rect(center = (screen_rect.centerx, screen_rect.centery + 50))
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)

        
    elif menu ==  'shop':
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        score_text = font.render(f"Score Final: {totalscore}", True, (255, 255, 255))
        restart_text = font.render("Appuyez sur R pour recommencer ou Q pour quitter", True, (255, 255, 255))
        if not'routeur'in achat:
            text = font.render("B pour acheter le skin routeur pour 100 point", True, (255, 255, 255))
        else:
            text = font.render("B pour equiper le skin routeur", True, (255, 255, 255))
        score_rect = score_text.get_rect(center = (screen_rect.centerx, screen_rect.centery))
        screen_rect = screen.get_rect()
        rect = text.get_rect(center = (screen_rect.centerx, screen_rect.centery))
        restart_rect = restart_text.get_rect(center = (screen_rect.centerx, screen_rect.centery + 50))
        score_rect = score_text.get_rect(center = (screen_rect.centerx, screen_rect.centery-50))

        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(text, rect)

    pygame.display.update()
    clock.tick(60)
