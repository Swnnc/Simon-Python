import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT  = 450

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Test")

class Healthbar():
    def __init__(self,x,y,w,h,max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x,self.y,self.w,self.h))
        pygame.draw.rect(surface, "green", (self.x,self.y,self.w * ratio,self.h))

health_bar = Healthbar(250,400,300,40,100)
health_bar1 = Healthbar(250,200,300,40,100)

run = True
while run:
    screen.fill("indigo")
    health_bar.draw(screen)
    health_bar1.draw(screen)

  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            health_bar.hp -= 35
            if health_bar.hp <=0 :
                run = False 
    
    pygame.display.flip()

pygame.quit()  