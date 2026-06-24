import pygame 
import random
from pygame import mixer

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
FPS = 60
coold_down = 3000 
last_enemy_time = 0
level = 1
speed = 2
score = 0 
lives = 3 
font = pygame.font.SysFont('Arial', 32) 
large_font = pygame.font.SysFont("Arial", 64)

player = pygame.Rect(375,500,50,50)

bullets = []
enemies = []

particles = []
powrups = []
powerup_timer = 0
double_shot = False
powerup_end_time = 0 

boss_active = False
boss_rect = pygame.Rect(300, -100, 200, 60)
boss_health = 50
boss_max_health = 50
boss_direction = 1
boss_bullets = []
boss_last_shot = 0
boss_defeated = False

gun_fx = pygame.mixer.Sound('gun.mp3')
gun_fx.set_volume(0.4)

boss_fx = pygame.mixer.Sound('enemy_entry.mp3')
boss_fx.set_volume(0.4) 

dead_fx = pygame.mixer.Sound('game_over.mp3')
dead_fx.set_volume(0.4)

boss_gun = pygame.mixer.Sound("boss_gun.mp3")
boss_gun.set_volume(0.4)

enemy_dead = pygame.mixer.Sound("enemy_dead.mp3")
enemy_dead.set_volume(0.4)

boss_dead = pygame.mixer.Sound("boss_dead.mp3")
boss_dead.set_volume(0.4) 

right = False
left = False

firing = False

game_state = 'menu'

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Fighter")
clock = pygame.time.Clock()

PALETTE = {
    'R': (255, 50, 50),     
    'G': (50, 255, 50),     
    'B': (50, 50, 255),     
    'Y': (255, 255, 50),   
    'W': (255, 255, 255), 
    'C': (50, 255, 255),   
    'M': (255, 50, 255),   
    'O': (255, 150, 50),   
    'D': (100, 100, 100), 
    'L': (200, 200, 200), 
    'P': (180, 50, 255),   
}

def create_pixel_art(art, size):
    rows = len(art)
    cols = max(len(row) for row in art)
    surf = pygame.Surface((cols, rows))
    surf.fill((1, 1, 1))
    surf.set_colorkey((1, 1, 1))
    
    for y, row in enumerate(art):
        for x, char in enumerate(row):
            if char in PALETTE:
                surf.set_at((x, y), PALETTE[char])
                
    return pygame.transform.scale(surf, size)

PLAYER_PIXELS = [
    "    L    ",
    "   LLL   ",
    "  LLCLL  ",
    " LLLLLLL ",
    " RR L RR ",
    " RRRRRRR ",
    "  R   R  ",
    "  Y   Y  ",
    "  O   O  "
]

ENEMY_PIXELS = [
    "  GGGGGGG  ",
    " GGGGGGGGG ",
    "GGRGGGGRGGG",
    "GGGGGGGGGGG",
    "GG  GGG  GG",
    " G       G ",
    " G  G G  G ",
    "  G     G  ",
    "   G   G   "
]

BOSS_PIXELS = [
    "               PPPPPPPPPP               ",
    "           PPPPPPPPPPPPPPPPPP           ",
    "        PPPPPPPPPPPPPPPPPPPPPPPP        ",
    "      PPPPPPPPPPPPPPPPPPPPPPPPPPPP      ",
    "    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP    ",
    "  PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP  ",
    " PPPPPPRRRRPPPPPPPPPPPPPPPPPPRRRRPPPPPP ",
    " PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP ",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPP   PPPPPPPPPPPPPPPPPPPPPP   PPPPPP",
    " PPPP     PPPPPPPPPPPPPPPPPPPP     PPPP ",
    "  PP       PPPPPPPPPPPPPPPPPP       PP  ",
    "  Y         Y      YY      Y         Y  "
]

player_img = create_pixel_art(PLAYER_PIXELS, (50, 50))
enemy_img = create_pixel_art(ENEMY_PIXELS, (40, 40))
boss_img = create_pixel_art(BOSS_PIXELS, (200, 60))

def draw():
  if game_state == 'playing':
    if boss_active:
      screen.fill((20,0,0)) 
      
    screen.blit(player_img, (player.x, player.y)) 
    for bullet in bullets:
      pygame.draw.rect(screen, (255,255,255), bullet)
    for enemy in enemies:
      screen.blit(enemy_img, (enemy.x, enemy.y))
    
    for p in powrups:
      pygame.draw.rect(screen,(255,255,0),p)
    for part in particles:
      pygame.draw.rect(screen,(255,165,0), (part[0], part[1], 4, 4))
    
    if boss_active:
      screen.blit(boss_img, (boss_rect.x, boss_rect.y))
      for bb in boss_bullets:
        pygame.draw.rect(screen, (255,0,255), bb)
      
      pygame.draw.rect(screen, (255,0,0), (WIDTH//2 - 150, 20, 300, 15))
      health_width = int((boss_health / boss_max_health) * 300)
      if health_width > 0:
        pygame.draw.rect(screen, (0,255,0), (WIDTH//2 - 150, 20, health_width, 15))
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255)) 
    lives_text = font.render(f"Lives: {lives}", True, (255,50,50))
    
    if boss_active:
      level_text = font.render("BOSS FIGHT!", True, (255,0,255))
    else:
      level_text = font.render(f"Level: {level}", True, (50,150,255))
    
    if double_shot:
      mode_text = font.render("DOUBLE SHOT ACTIVE!", True, (255,255,0))
      screen.blit(mode_text, (WIDTH//2 - mode_text.get_width()//2, 50))
    
    screen.blit(score_text,(10,10))
    screen.blit(lives_text,(10,50)) 
    screen.blit(level_text, (680,10))
  
  elif game_state == 'menu':
    title = large_font.render('SPACE FIGHTER', True, (0,255,0))
    instructions = font.render("Press SPACEBAR to Start", True, (255,255,255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
    screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 350))
    
  elif game_state == 'game_over':
    go_title = large_font.render("GAME OVER", True, (255,0,0))
    final_score = font.render(f"Final Score: {score}", True, (255,255,255))
    restart_text = font.render("Press SPACEBAR to Try Again", True, (255,255,255)) 
    screen.blit(go_title, (WIDTH//2 - go_title.get_width()//2, 150))
    screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2,280))
    screen.blit(restart_text, (WIDTH//2-restart_text.get_width()//2, 380))

  pygame.display.update()

def move():
  global firing
  dx = 0
  
  if right == True:
    dx += 10
  if left == True:
    dx -= 10
    
  player.x += dx
  
  if player.x <= 0:
    player.x = 0
  if player.x >= 750:
    player.x = 750
  
  if firing:
    if double_shot:
      b1 = pygame.Rect(player.x, player.y-10,10,20)
      b2 = pygame.Rect(player.x+40,player.y-10,10,20)
      bullets.append(b1)
      bullets.append(b2)
    else:
      bullet = pygame.Rect(player.x + 20,player.y - 10,10,20)
      bullets.append(bullet)
    firing = False

  for b in bullets[:]: 
    b.y -= 10
    if b.y <= 0:
      bullets.remove(b)

def create_explosion(x,y):
  for _ in range(15):
    p_dx = random.randint(-4,4)
    p_dy = random.randint(-4,4)
    
    if p_dx == 0 and p_dy ==0: p_dy=2
    particles.append([x+20, y+20, p_dx, p_dy,20])
    
def update_particles():
  for p in particles[:]:
    p[0] += p[2]
    p[1] += p[3]
    p[4] -= 1
    if p[4] <= 0:
      particles.remove(p)



def enemies_ships():
  global enemies, last_enemy_time, coold_down, speed, score, level, lives, game_state, powerup_timer, boss_active, boss_defeated
  
  if boss_active:
    return
  
  current_time = pygame.time.get_ticks()
      
  if score < 50:
    level = 1
    speed = 2
    coold_down = 3000
  elif score < 100:
    level = 2
    speed = 3
    coold_down = 2000
  elif score < 150:
    level = 3
    speed = 5
    coold_down = 1000
  else:
    if not boss_defeated:
      boss_active = True 
      boss_fx.play()
      return 
    else:
      level = 4
      speed = 6
      coold_down = 800
  
  if current_time - last_enemy_time >= coold_down:
    enemy = pygame.Rect(random.randint(50,750), 0, 40,40)
    enemies.append(enemy)
    last_enemy_time = current_time
  
  for enemy in enemies[:]:
    enemy.y += speed
    if enemy.colliderect(player):
      create_explosion(enemy.x,enemy.y)
      enemy_dead.play()
      enemies.remove(enemy)
      lives -= 1
      if lives <= 0:
        game_state = 'game_over'
        dead_fx.play()
    
    
    elif enemy.y >= 560:
      enemies.remove(enemy)
      score -= 5 
      lives -= 1
      if lives <= 0:
        game_state = 'game_over'
        dead_fx.play()
  
  powerup_timer += 1
  if powerup_timer > 720:
    powrups.append(pygame.Rect(random.randint(50,750), 0, 25,25))
    powerup_timer = 0
    
  for p in powrups[:]:
    p.y += 3
    if p.colliderect(player):
      global double_shot, powerup_end_time
      double_shot = True
      powerup_end_time = pygame.time.get_ticks() + 7000
      powrups.remove(p)


def boss_battle():
  global boss_active, boss_direction, boss_health, boss_last_shot, lives, game_state, score, boss_defeated
  
  if not boss_active:
    return
  
  current_time = pygame.time.get_ticks()
  
  if boss_rect.y < 60:
    boss_rect.y += 2
  else:
    boss_rect.x += 4 * boss_direction
    if boss_rect.right >= WIDTH or boss_rect.left <= 0:
      boss_direction *= -1
  
  if current_time - boss_last_shot >= 1200:
    left_laser = pygame.Rect(boss_rect.left + 20, boss_rect.bottom, 12, 24)
    right_laser = pygame.Rect(boss_rect.right - 32, boss_rect.bottom,12, 24)
    boss_bullets.append(left_laser)
    boss_bullets.append(right_laser)
    boss_last_shot = current_time
    boss_gun.play()
    
  for bb in boss_bullets[:]:
    bb.y += 7
    if bb.colliderect(player):
      boss_bullets.remove(bb)
      lives -= 1
      if lives <= 0:
        game_state = 'game_over'
        dead_fx.play()
    elif bb.y > HEIGHT:
      boss_bullets.remove(bb)
    
  for bullet in bullets[:]:
    if bullet.colliderect(boss_rect) and boss_rect.y >= 60:
      bullets.remove(bullet)
      boss_health -= 1
      create_explosion(bullet.x - 20, bullet.y)
      
      if boss_health <= 0:
        for _ in range(5):
          create_explosion(boss_rect.x + random.randint(0,160), boss_rect.y + random.randint(0,40))
          
        score += 200
        boss_active = False
        boss_defeated = True
        boss_dead.play()

def check_collosion():
  global score
  for enemy in enemies[:]:
    if enemy not in enemies:
      continue
    for bullet in bullets[:]:
      if bullet.colliderect(enemy):
        create_explosion(enemy.x, enemy.y)
        enemy_dead.play()
        enemies.remove(enemy)
        if bullet in bullets:
          bullets.remove(bullet)
        score += 10
        break 

def reset_game():
  global score, lives, level, speed, coold_down, enemies, bullets, last_enemy_time
  global left, right, firing, boss_active, boss_health, boss_bullets, boss_defeated
  score = 0
  lives = 3
  level = 1
  speed = 2
  coold_down = 3000
  enemies.clear()
  bullets.clear()
  
  boss_active = False
  boss_health = 50
  boss_bullets.clear()
  boss_rect.x = 300
  boss_rect.y = -100
  boss_defeated = False
  
  last_enemy_time = pygame.time.get_ticks()    
  left = False
  right = False
  firing = False
  player.x = 375
  player.y = 500
        
def main():
  global left, right, firing, game_state
  run = True
  while run:
    clock.tick(FPS)
    screen.fill((0,0,0))
    
    if game_state == 'playing':
      move()
      enemies_ships()
      boss_battle()
      check_collosion()
      update_particles()
      
    draw()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False 
    
      if event.type == pygame.KEYDOWN:
        if game_state == 'playing':
          if event.key == pygame.K_a:
            left = True
          if event.key == pygame.K_d:
            right = True    
          if event.key == pygame.K_SPACE:
            gun_fx.play()
            firing = True 
        else:
          if event.key == pygame.K_SPACE:
            reset_game()
            game_state = 'playing'
            
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
          left = False
        if event.key == pygame.K_d:
          right = False 

  pygame.quit()

if __name__ == '__main__':
  main()
