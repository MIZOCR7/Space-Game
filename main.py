import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

player = pygame.Rect(200,200,50,50)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Fighter")


def draw():
  pygame.draw.rect(screen,(255,255,255), player)


run = True
while run:
  screen.fill((255,255,255))
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    
  draw()
      
pygame.quit()
  

