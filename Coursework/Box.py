import pygame

class Box:

    def __init__(self, screen, rect, boxcolour, font, textsize, text, textcolour, border_radius=20):
        # set the variables
        self.screen = screen
        self.rect = pygame.Rect(rect) # make into a Rect object to make drawing and getting centre easier
        self.boxcolour = boxcolour
        self.font = pygame.font.SysFont(font, textsize) # pygame font initialisation
        self.text = text
        self.textcolour = textcolour
        self.border_radius = border_radius

    def draw(self): # condenses drawbox and text into one function to save typing - also makes stockmarketsimulator less cluttered
        self.drawBox()
        self.drawText()

    def drawBox(self):
        # draws a rectangle on the screen, with the correct colour, at the rect position with the correct border radius
        pygame.draw.rect(self.screen, self.boxcolour, self.rect, border_radius=self.border_radius)

    def drawText(self):

        text_render = self.font.render(self.text, True, self.textcolour) # render text
        centre = text_render.get_rect(center=self.rect.center) # get the centre of the box to get a position for the text to sit centred in the box

        self.screen.blit(text_render, centre) # draw the text on top of the box

    def updateText(self, text): # workaround for changing text in the period and interval buttons
        self.text = text