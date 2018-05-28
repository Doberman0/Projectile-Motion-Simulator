import pygame, math, sys, random, copy
from pygame.locals import *

class RandomButton(Button): #Use of inheritence
                            #Makes  a random button in pygame
    def __init__(self,Label, PosXStart, PosYStart, Width, Length, Surface, Range):
        super().__init__(Label, PosXStart, PosYStart, Width, Length, Surface) #Inhereits all fields and methods from button class
        self._Range = Range #Range must be given as a tuple

    def GetNumInRange(self): #Gets a random real number in a given range to 1dp
        return str(round(random.uniform(self._Range[0], self._Range[1]),1))
