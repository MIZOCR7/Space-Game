import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

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
  
  bullets_dy = 20
  if firing:
    bullet = pygame.Rect(player.x + 20,player.y - 10,10,20)
    bullets.append(bullet)
    firing = False
    
  for b in bullets: 
    b.y -= 10
    if b.y <= 0:
      bullets.remove(b)

def enemies():
  pass 
  
  
  
  
run = True
while run:
  clock.tick(FPS)
  screen.fill((0,0,0))
  move()
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
  

