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

right = False
left = False

firing = False

game_state = 'menu'

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Fighter")
clock = pygame.time.Clock()

def draw():
  if game_state == 'playing':
    pygame.draw.rect(screen,(255,0,0), player) 
    for bullet in bullets:
      pygame.draw.rect(screen, (255,255,255), bullet)
    for enemy in enemies:
      pygame.draw.rect(screen, (0,255,0), enemy)
    
    for p in powrups:
      pygame.draw.rect(screen,(255,255,0),p)
    for part in particles:
      pygame.draw.rect(screen,(255,165,0), (part[0], part[1], 4, 4))
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255)) 
    lives_text = font.render(f"Lives: {lives}", True, (255,50,50))
    level_text = font.render(f"Level: {level}", True, (50,150,255))
    
    if double_shot:
      mode_text = font.render("DOUBLE SHOT ACTIVE!", True, (255,255,0))
    
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
  global enemies, last_enemy_time, coold_down, speed, score, level, lives, game_state, powerup_timer
  
  current_time = pygame.time.get_ticks()
      
  if score < 50:
    level = 1
    speed = 2
    coold_down = 3000
  elif score < 100:
    level = 2
    speed = 3
    coold_down = 2000
  else:
    level = 3
    speed = 5
    coold_down = 1000
    
  if current_time - last_enemy_time >= coold_down:
    enemy = pygame.Rect(random.randint(50,750), 0, 40,40)
    enemies.append(enemy)
    last_enemy_time = current_time
  
  for enemy in enemies[:]:
    enemy.y += speed
    if enemy.colliderect(player):
      create_explosion(enemy.x,enemy.y)
      enemies.remove(enemy)
      lives -= 1
      if lives <= 0: game_state = 'game_over'
    
    
    elif enemy.y >= 560:
      enemies.remove(enemy)
      score -= 5 
      lives -= 1
      if lives <= 0:
        game_state = 'game_over'
  
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
  
  
def check_collosion():
  global score
  for enemy in enemies[:]:
    if enemy not in enemies:
      continue
    for bullet in bullets[:]:
      if bullet.colliderect(enemy):
        create_explosion(enemy.x, enemy.y)
        enemies.remove(enemy)
        if bullet in bullets:
          bullets.remove(bullet)
        score += 10
        break 

def reset_game():
  global score, lives, level, speed, coold_down, enemies, bullets, last_enemy_time
  global left, right, firing
  score = 0
  lives = 3
  level = 1
  speed = 2
  coold_down = 3000
  enemies.clear()
  bullets.clear()
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
