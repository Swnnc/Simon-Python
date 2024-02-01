import pygame
import sys
from main import Game


# Initialisation de Pygame
pygame.init()
#charger le son ici 
pygame.mixer.init()
pygame.mixer.music.load('son/intro.mp3')
pygame.mixer.music.play(-1)
# Paramètres de l'écran
largeur, hauteur = 800, 800
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Menu d'accueil")

# Couleurs
blanc = (255, 255, 255)

# Charger le fond d'écran
fond_image = pygame.image.load("images/city.png")
fond_image = pygame.transform.scale(fond_image, (largeur, hauteur))

# Charger et redimensionner l'image du bouton Jouer
jouer_image = pygame.image.load("images/buton-play.png")
nouvelle_largeur_jouer = largeur // 3
nouvelle_hauteur_jouer = int(nouvelle_largeur_jouer / jouer_image.get_width() * jouer_image.get_height())
jouer_image = pygame.transform.scale(jouer_image, (nouvelle_largeur_jouer, nouvelle_hauteur_jouer))
jouer_rect = jouer_image.get_rect(center=(largeur // 2, hauteur // 1.5 - 50))

# Charger et redimensionner l'image du bouton Quitter
quitter_image = pygame.image.load("images/buton-exit.png")
nouvelle_largeur_quitter = largeur // 3
nouvelle_hauteur_quitter = int(nouvelle_largeur_quitter / quitter_image.get_width() * quitter_image.get_height())
quitter_image = pygame.transform.scale(quitter_image, (nouvelle_largeur_quitter, nouvelle_hauteur_quitter))
quitter_rect = quitter_image.get_rect(center=(largeur // 2, hauteur // 1.5 + 100))

def lancer_jeu():
    game = Game()
    game.new()
    game.run()

# Boucle principale du menu
while True:
    ecran.blit(fond_image, (0, 0))  # Afficher le fond d'écran

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if jouer_rect.collidepoint(mouse_x, mouse_y):
                lancer_jeu()  # Appel de la fonction pour lancer le jeu
            elif quitter_rect.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                sys.exit()

    # Afficher le bouton Jouer
    ecran.blit(jouer_image, jouer_rect)

    # Afficher le bouton Quitter
    ecran.blit(quitter_image, quitter_rect)

    pygame.display.flip()
