import pygame
import random
import os

# load pipe image
PIPE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))]

class Pipe:
    """Handles the top and bottom pipe spawing, animation, and collision. The most important function would probably be the collide(). 
        It checks the bird's mask and compares it with both the top and bottom pipe masks; than checks if any collision occures. 
        move() moves both pipes, while draw(), well draws it on screen. The set_height() function randomizes the top and bottom respective 
        heights relative towards the flappy bird in the center. This as you imagine adds variety and gameplay
    """    
    
    # max distance threshold for the top and bottom pipe
    GAP = 200
    
    # screen travel speed
    VEL = 5
    
    def __init__(self, x):
        """Pipe's constructor

        Args:
            x (integer): top and bottom pipes starting x position
        """        
        self.x = x
        self.height = 0
        
        # top and bottom pipes current height, get randomly set later
        self.top = 0
        self.bottom = 0
        
        # top and bottom pip sprite, both pipes are the same sprite, I just flipped the top pipe as to keep it oriented
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG[0], False, True)
        self.PIPE_BOTTOM = PIPE_IMG[0]
        
        # flag is set off when the pipes pass the flappy bird 
        self.passed = False
        
        # sets the pipes gap distance randomly
        self.set_height()
        
    def set_height(self):
        """Sets the pipes gap distance randomly
        """        
        
        # determines the random gap size
        self.height = random.randrange(100,400)
        
        # than subtract the top and bottom pipe heights with the determined gap size
        self.top = self.height  - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    def move(self):
        """Moves the top and bottom pip along the screen.
        """        
        self.x -= self.VEL
        
    def draw(self, win):
        """Handles the bird animation and adjusts the rotation
            of the bird aswell.

        Args:
            win (pygame window): a pygame window, so the bird knows which window 
                                    to send the updated frame to so it can display
        """
        
        # both sprites are drawn     
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
    def collide(self, bird):
        """Checks to see if the flappy bird has collided with either the top or bottom pipe. This collision is using pygame.Mask object. 
            Which makes it easier and provides better collision detection.

        Args:
            bird (Bird): custom Bird object

        Returns:
            bool: True if the bird collides with either pipe
        """        
        
        # gets the birds, top pipe, bottom pipes mask
        bird_mask = bird.get_mask()
        top_mask =  pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask =  pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        # distance of the bird from the top and bottom pipe
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        # Mask object checks and finds any pixel overlap from either pipe and bird
        bottom_collider_flag = bird_mask.overlap(bottom_mask, bottom_offset)
        top_collider_flag = bird_mask.overlap(top_mask, top_offset)
        
        # if any collision happens with the top or bottom pipe than return True, indicating collision
        if bottom_collider_flag or top_collider_flag:
            return True
        
        return False
