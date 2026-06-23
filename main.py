import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60
coold_down = 3000 
last_enemy_time = 0
level = 1
speed = 1
score = 0 

player = pygame.Rect(375,500,50,50)

bullets = []
enemies = []

right = False
left = False

firing = False

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Fighter")
clock = pygame.time.Clock()

def draw():
  pygame.draw.rect(screen,(255,0,0), player) 
  for bullet in bullets:
    pygame.draw.rect(screen, (255,255,255), bullet)
  for enemy in enemies:
    pygame.draw.rect(screen, (0,255,0), enemy)
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
    bullet = pygame.Rect(player.x + 20,player.y - 10,10,20)
    bullets.append(bullet)
    firing = False

  for b in bullets: 
    b.y -= 10
    if b.y <= 0:
      bullets.remove(b)

def enemies_ships():
  global enemies, last_enemy_time, coold_down, speed, score
  current_time = pygame.time.get_ticks()
      
  if current_time >= 5000:
    level = 2
    speed = 5
    coold_down = 2000

  if current_time >= 10000:
    level = 3
    speed = 5
    coold_down = 200
    
  if current_time - last_enemy_time >= coold_down:
    enemy = pygame.Rect(random.randint(50,750), 0, 40,40)
    enemies.append(enemy)
    last_enemy_time = current_time
    return enemy
  
  for enemy in enemies:
    enemy.y += speed
    if enemy.y >= 560:
      enemies.remove(enemy)
      score -= 5 
  
  
def check_collosion():
  global score
  for enemy in enemies[:]:
    for bullet in bullets[:]:
      if bullet.colliderect(enemy):
        enemies.remove(enemy)
        bullets.remove(bullet)
        score += 10
        break 
      
      
run = True
while run:
  clock.tick(FPS)
  screen.fill((0,0,0))
  enemy = enemies_ships()
  move()
  enemies_ships()
  check_collosion()
  draw()
  
  
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        left = True
      if event.key == pygame.K_d:
        right = True 
      if event.key == pygame.K_SPACE:
        firing = True 
      
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        left = False
      if event.key == pygame.K_d:
        right = False 

pygame.quit()

