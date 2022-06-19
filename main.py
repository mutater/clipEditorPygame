import math
import os
import pygame
import random
import sys
import tkinter
import tkinter.filedialog
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Mutater's Clip Editor")

TOPLEFT = (0, 0)
TOPMIDDLE = (0.5, 0)
TOPRIGHT = (1, 0)
MIDLEFT = (0, 0.5)
CENTER = (0.5, 0.5)
MIDRIGHT = (1, 0.5)
BOTTOMLEFT = (0, 1)
BOTTOMMIDDLE = (0.5, 1)
BOTTOMRIGHT = (1, 1)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def blue(base):
    modifier = 10 if base < 127 else 20
    return (base, base, base + modifier)


def prompt_file():
    top = tkinter.Tk()
    top.withdraw()
    file_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return file_name


class Screen:
    def __init__(self, background):
        self.width = 1280
        self.height = 720
        
        self.background = background
        
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.variables()
    
    def variables(self):
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.w2 = self.width / 2
        self.h2 = self.height / 2
        self.center = (self.w2, self.h2)
    
    def update(self):
        self.screen.fill(self.background)
        self.variables()

screen = Screen(blue(30))


class Draw:
    def __init__(self, surface):
        self.color = (255, 255, 255)
        self.font = "Verdana"
        self.surface = surface
    
    def get_text(self, text, pos, size, anchor=(0, 0)):
        font = pygame.font.SysFont(self.font, size)
        image = font.render(text, True, self.color)
        
        image_rect = image.get_rect()
        
        image_rect.left = -1 * anchor[0] * image_rect.width + pos[0]
        image_rect.top = -1 * anchor[1] * image_rect.height + pos[1]
        
        return image, image_rect
    
    def text(self, text, pos, size, anchor=(0, 0)):
        image, image_rect = self.get_text(text, pos, size, anchor)
        self.surface.blit(image, image_rect)
    
    def rect(self, pos, size, anchor=(0, 0)):
        n_pos = [pos[0], pos[1]]
        
        n_pos[0] = -1 * anchor[0] * size[0] + pos[0]
        n_pos[1] = -1 * anchor[1] * size[1] + pos[1]
        
        pygame.draw.rect(self.surface, self.color, (n_pos[0], n_pos[1], size[0], size[1]))

draw = Draw(screen.screen)


class Button:
    def __init__(self, pos, size, text, callback):
        self.pos = pos
        self.size = size
        self.text = text
        
        self.color = Blue(60)
        
        self.draw_func = draw.rect(self.pos, self.size)
        self.callback = callback
        
        self.visible = True
    
    def draw(self):
        if self.visible:
            self.draw_func()
    
    def click(pos):
        if not self.visible:
            return False
        
        if (self.pos[0] < pos[0] < self.pos[0] + self.size[0],
            self.pos[1] < pos[1] < self.pos[1] + self.size[1]):
            self.callback()
            return True
        else:
            return False


class Editor:
    def __init__(self):
        self.text = ""
        self.widgets = []
    
    def new_widget(self, widget):
        self.widgets.append(widget)
    
    def draw(self):
        for widget in self.widgets:
            widget.draw()
    
    def click(self, pos):
        for widget in self.widgets:
            widget.click(pos)

editor = Editor()


class Main:
    def __init__(self):
        self.o_millis = 1
        self.millis = 1
        self.delta = 1
        
        editor.new_widget()
    
    def main_update(self):
        for e in pygame.event.get():
            if e.type == QUIT: sys.exit()
            if e.type == KEYDOWN:
                if e.unicode == "q": sys.exit()
            if e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    editor.click(pygame.mouse.get_pos())
        
        screen.update()

    def main_draw(self):
        # TITLE
        title_height = screen.height // 18
        
        draw.color = blue(60)
        draw.rect((0, 0), (screen.width, title_height))
        draw.color = (30, 120, 255)
        draw.text("Mutater's Clip Editor", (10, title_height//2), title_height*3//4, MIDLEFT)
        
        # VIDEO PLAYER
        video_topright = (screen.width - 20, title_height + 20)
        
        draw.color = BLACK
        draw.rect(video_topright, (640, 360), TOPRIGHT)
        draw.color = WHITE
        draw.text(editor.text, (video_topright[0] - 320, video_topright[1] + 180), 40, CENTER)
    
    def main_loop(self):
        while True:
            self.millis = pygame.time.get_ticks()
            self.delta = (self.millis - self.o_millis) / 1000.0
            
            self.main_update()
            self.main_draw()
            
            pygame.display.update()
            self.o_millis = self.millis


if __name__ == "__main__":
    main = Main()
    main.main_loop()