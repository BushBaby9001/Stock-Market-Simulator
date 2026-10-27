import pygame
from Box import Box

class Button(Box):

    def __init__(self, screen, rect, boxcolour, font, textsize, text, textcolour, hovercolour, clickcolour, border_radius=20):
        super().__init__(screen, rect, boxcolour, font, textsize, text, textcolour, border_radius)
        self.hovercolour = hovercolour
        self.clickcolour = clickcolour
        self.originalboxcolour = boxcolour
        self.originaltext = text
        self.active = False # added to check if the box is currently being hovered over/ clicked (for text input later)


    def interaction(self, mousepos, event, function):
        if self.rect.collidepoint(mousepos): # if the mouse hovers over the button
            self.boxcolour = self.hovercolour # change colour
            if event.type == pygame.MOUSEBUTTONDOWN: # if theres a click
                self.boxcolour = self.clickcolour # change colour again
                try:
                    self.active = True # then activate and run function()
                    function()
                except TypeError: # stops from trying to call NoneType
                    pass

        else:
            self.boxcolour = self.originalboxcolour

            self.active = False
