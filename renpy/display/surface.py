# Function to allocate a surface.
import pygame
from pygame.constants import *

import renpy

# def Surface(width, height):
#     """
#     Allocate a surface. Flags and depth are ignored, for compatibility
#     with pygame.Surface.
#     """

#     return pygame.Surface((width, height), 0,
#                           renpy.game.interface.display.sample_surface)

# class FilledSurface(object):

#     def __init__(self, width, height, color):
#         self.width = width
#         self.height = height
#         self.color = color

#     def blit_to(self, dest, x, y):
#         dest.fill(self.color, [ x, y, self.width, self.height ])

class Surface(object):
    """
    This is our own surface object, which is a node in a tree in which
    all of the leaves are PyGame surfaces. It ensures that things are
    only blit to the screen once, hopefully giving a performance boost.
    """

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.blittables = [ ]

    def blit(self, source, (x, y)):
        """
        Adds the source surface to the list of things that need to be
        blitted to the screen. The source surface is either a
        pygame.Surface, or one of these Ren'Py Surfaces.
        """
        
        self.blittables.append((x, y, source))


    def blit_to(self, dest, x, y):
        """
        This blits the children of this Surface to dest, which must be
        a pygame.Surface. The x and y parameters are the location of
        the upper-left hand corner of this surface, relative to the
        destination surface.
        """

        for xo, yo, source in self.blittables:

            if isinstance(source, pygame.Surface):
                dest.blit(source, (x + xo, y + yo))
            else:
                source.blit_to(dest, x + xo, y + yo)

    def fill(self, color):
        """
        Fake a pygame.Surface.fill()
        """
        
        surf = pygame.Surface((self.width, self.height), 0,
                              renpy.game.interface.display.sample_surface)

        surf.fill(color)

        # surf = FilledSurface(self.width, self.height, color)

        self.blittables.append((0, 0, surf))

    def get_size(self):
        """
        Returns the size of this surface, a mostly ficticious value
        that's taken from the inputs to the constructor. (As in, we
        don't clip to this size.)
        """

        return self.width, self.height
                
    def pygame_surface(self, alpha=True):
        """
        Returns a pygame surface constructed from self.
        """

        if alpha:
            sample = renpy.game.interface.display.sample_surface
        else:
            sample = renpy.game.interface.display.window
        
        rv = pygame.Surface((self.width, self.height), 0, sample)

        self.blit_to(rv, 0, 0)

        return rv
