import pygame
import math

class Timer:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def current_time(self):
        current_time = pygame.time.get_ticks()
        return truncate((current_time - self.start_time)/1000, 3)
    
    def draw(self, x, y, font, screen):
        current_time = self.current_time()
        text = font.render(str(current_time), True, 'black')
        text_rect = text.get_rect(center=(x, y))
        text_rect.inflate_ip(10, 10)
        screen.blit(text, text_rect)

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))