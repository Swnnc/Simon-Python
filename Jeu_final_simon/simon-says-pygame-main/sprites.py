import pygame
from settings import *
import math
import numpy
pygame.mixer.init()


class Button:
    def __init__(self, x, y, colour,image_path):
        self.x, self.y = x, y
        self.colour = colour
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (BUTTON_SIZE, BUTTON_SIZE))

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, BUTTON_SIZE, BUTTON_SIZE))
        screen.blit(self.scaled_image, (self.x, self.y))

    def clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + BUTTON_SIZE and self.y <= mouse_y <= self.y + BUTTON_SIZE
    
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


class Audio:
    def __init__(self, frequency: int):
        duration = 0.5  # The duration of that the sound will play
        bits = 16  # number of bits of data each sample will use
        sample_rate = 44100  # number of sample rate will generate on a second of audio
        total_samples = int(round(duration * sample_rate))  # total number of samples required by the samples rates in the duration of the audio in seconds
        data = numpy.zeros((total_samples, 2), dtype=numpy.int16)  # data will contain all the samples for the synth wave
        max_sample = 2 ** (bits - 1) - 1  # largest possible value a single sample can use
        for sample in range(total_samples):  # generate a sample for each period of time in the sine wave
            sample_time = float(sample) / sample_rate  # calculate the current time for the current sample
            for channel in range(2):  # generate data for left and right side of the audio
                data[sample][channel] = int(round(max_sample * math.sin(2 * math.pi * frequency * sample_time)))
        self.sound = pygame.sndarray.make_sound(data)  # use sound array to generate the sound from this data
        self.current_channel = None

    def play(self):
        self.current_channel = pygame.mixer.find_channel(True)
        self.current_channel.play(self.sound)


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
    # chargement de la police pour le score et les ecritures
        font = pygame.font.Font("police\policepixel2.ttf", 35)
        text = font.render(self.text, True, ROUGE)

        screen.blit(text, (self.x, self.y))

