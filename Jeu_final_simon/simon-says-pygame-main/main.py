import pygame
from settings import *
from sprites import *
import random
import sys
import pygame_menu

class Game:
    def __init__(self):
        pygame.init()
        #ajout du son 
        pygame.mixer.init()
        pygame.mixer.music.load('son/testson.mp3')
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
      
        self.flash_colours = [YELLOW, BLUE, RED, GREEN]
        self.colours = [ELEC, EAU, FEU, PLANTE]
        self.correct_rounds = 0
        self.health_bar = Healthbar(165,210,175,20,100) #Création de l'instance barre de vie joueur
        self.health_bar1 = Healthbar(615,200,175,20,100) #Création de l'instance barre de vie boss
        self.buttons = [
            Button(375, 220, ELEC, "images/types_pixel_ELEC.png"),
            Button(475, 220, EAU, "images/types_pixel_eau.png"),
            Button(375, 320, FEU, "images/types_pixel_feu.png"),
            Button(475, 320, PLANTE, "images/types_pixel_plante.png"),
        ]
        self.background2 = pygame.image.load("niv2.png").convert()
        self.background3 = pygame.image.load("niv3.png").convert()
        self.background1 = pygame.image.load("niv1.png").convert()
        self.background = pygame.transform.scale(self.background1, (WIDTH, HEIGHT))
        

    def get_high_score(self):
        with open("high_score.txt", "r") as file:
            score = file.read()
        return int(score)

    def save_score(self):
        with open("high_score.txt", "w") as file:
            if self.score > self.high_score:
                file.write(str(self.score))
            else:
                file.write(str(self.high_score))

    def new(self):
        self.waiting_input = False
        self.pattern = []
        self.current_step = 0
        self.score = 0
        self.high_score = self.get_high_score()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.clicked_button = None
            self.events()
            self.draw()
            self.update()
            self.vie() #Appel de la fonction vie 
            self.lvl3()

    def update(self):
        if not self.waiting_input:
            pygame.time.wait(1000)
            self.pattern.append(random.choice(self.colours))
            for button in self.pattern:
                self.button_animation(button)
                pygame.time.wait(200)
            self.waiting_input = True

        else:
            # Appuie sur le bon bouton
            if self.clicked_button and self.clicked_button == self.pattern[self.current_step]:
                self.button_animation(self.clicked_button)
                self.current_step += 1

                # Appuie sur le dernier bouton
                if self.current_step == len(self.pattern):
                    self.score += 1
                    self.waiting_input = False
                    self.current_step = 0
                    self.health_bar1.hp -= 20 # PV du boss -20 si le score augmente
                
                if self.score >= 10 : #A partir du score 10, le boss pert plus de vie
                    self.health_bar1.hp = 100 
                    
                if self.score % 5 == 0:
                    self.correct_rounds += 5
            
                #ajout d'une condition permettant de verifier le nombre de point et de passer au niveau suivant
                if self.correct_rounds >4:
                    self.correct_rounds = 0
                    self.lvl2()
            # Appuie sur le mauvais bouton
            elif self.clicked_button and self.clicked_button != self.pattern[self.current_step]:
                self.health_bar.hp -= 35 # Si le joueur se trompe il perd 35 hp
                if self.health_bar.hp <= 0 : # Si le joueur n'a plus de vie, le jeu se relance

                    self.game_over()
                    self.save_score()
                    self.playing = False
                    self.health_bar.hp = 100
                    self.health_bar1.hp = 100
                    game.new()
                    game.run()
    def button_animation(self, colour):
        for i in range(len(self.colours)):
            if self.colours[i] == colour:
            
                flash_colour = self.flash_colours[i]
                button = self.buttons[i]

        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE))
        flash_surface = flash_surface.convert_alpha()
        r, g, b = flash_colour

        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, ANIMATION_SPEED * step):
                self.screen.blit(original_surface, (0, 0))
                flash_surface.fill((r, g, b, alpha))
                self.screen.blit(flash_surface, (button.x, button.y))
                pygame.display.update()
                self.clock.tick(FPS)
        self.screen.blit(original_surface, (0, 0))

    def game_over(self):
        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((self.screen.get_size()))
        flash_surface = flash_surface.convert_alpha()
  
        r, g, b = WHITE
        for _ in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    self.screen.blit(original_surface, (0, 0))
                    flash_surface.fill((r, g, b, alpha))
                    self.screen.blit(flash_surface, (0, 0))
                    pygame.display.update()
                    self.clock.tick(FPS)

        # Une fois terminée l'animation, affichez l'écran de Game Over
        game_over_screen = GameOverScreen(self.screen)  # Passez la surface actuelle à l'écran de Game Over
        game_over_screen.run()


    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.screen.blit(self.background, (0, 0))
        UIElement(100, 20, f"Score: {str(self.score)}").draw(self.screen)
        UIElement(400, 20, f"High score: {str(self.high_score)}").draw(self.screen)
        self.health_bar.draw(self.screen)
        self.health_bar1.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.clicked(mouse_x, mouse_y):
                        self.clicked_button = button.colour

    def vie(self): # Pour le passage de niveau
        if self.health_bar1.hp == 0 :
            self.health_bar1.hp = 100

    
    def lvl2(self) :

        # Lancer la transition entre les niveaux
        self.background = pygame.transform.scale(self.background2, (WIDTH, HEIGHT))
        # Lancement du son 
        pygame.mixer.init()
        pygame.mixer.music.load('son/niveau3.mp3')
        pygame.mixer.music.play(-1)

        # Remplacement des barres de vie et des cases
        self.health_bar.x = 150
        self.health_bar.y = 270
        self.health_bar.w = 175
        self.health_bar.h = 20
        self.health_bar1.x = 655
        self.health_bar1.y = 250
        self.health_bar1.w = 175
        self.health_bar1.h = 20
        self.buttons[0].x,self.buttons[0].y = 350, 200
        self.buttons[1].x,self.buttons[1].y = 450, 200
        self.buttons[2].x,self.buttons[2].y = 350, 300
        self.buttons[3].x,self.buttons[3].y = 450, 300
        

        ANIMATION_SPEED=60
        self.ajouterbouton(550, 200, DRAGON, "images/types_pixel_dragon.png")
        self.ajouterbouton(550, 300, SPECTRE, "images/types_pixel_spectre.png")
     

        #Ajout de deux nouvelles couleurs
        self.colours.append(DRAGON)
        self.colours.append(SPECTRE)

        #Ajout de deux nouveaux flashs
        self.flash_colours.append(ORANGE)
        self.flash_colours.append(DARKBLUE)


    def ajouterbouton(self, x, y, color, image_path):
        nouveau_bouton = Button(x, y, color, image_path)
        self.buttons.append(nouveau_bouton)

    def lvl3(self):
        if self.score >= 10  :
            # Remplacement des barres de vie et des cases 
            self.health_bar.x = 125
            self.health_bar.y = 200
            self.health_bar.w = 175
            self.health_bar.h = 20
            self.health_bar1.x = 675
            self.health_bar1.y = 175
            self.health_bar1.w = 175
            self.health_bar1.h = 20
            self.buttons[0].x,self.buttons[0].y = 350, 200
            self.buttons[1].x,self.buttons[1].y = 450, 200
            self.buttons[2].x,self.buttons[2].y = 350, 300
            self.buttons[3].x,self.buttons[3].y = 450, 300
            self.background = pygame.transform.scale(self.background3, (WIDTH, HEIGHT))


class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.largeur, self.hauteur = 950, 550
        self.ecran = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Game Over")
        self.fond_image = pygame.image.load("images/GameOver.png")
        self.fond_image = pygame.transform.scale(self.fond_image, (self.largeur, self.hauteur))

    def run(self):
        while True:
            self.screen.blit(self.fond_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()


# Exécution du jeu
if __name__ == "__main__":
    game = Game()
    while True:
        game.new()
        game.run()