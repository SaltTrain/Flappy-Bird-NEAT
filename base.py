import pygame
import os

# load floor image
BASE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))]

class Base:
    """The Base class handles the floor sprite and its animation. It instance two sprites 
        and swaps position once one base gets fully off the right side of the screen.
    """    
    
    # handled the rate at which the floor moves
    VEL = 5
    
    # gets the width of the image
    WIDTH = BASE_IMG[0].get_width()
    
    # two base sprite
    base_img_1 = BASE_IMG[0]
    base_img_2 = BASE_IMG[0]
    
    def __init__(self, y):
        """Base constructor

        Args:
            y (integer): sets the starting height position of both base sprite
        """     
           
        self.y = y
        
        # positions the first base starting on the left side of the screen, which spans the whole width of the screen.
        #   Than sets the sencond position of the second base sprite 1 whole width apart to the right.
        self.x1 = 0
        self.x2 = self.WIDTH
        
    def move(self):
        """Moves both sprites incrementally to the left. Than checks both sprites to see if their tail end reaches 
            the left off screen area. Than the sprite that reaches the end will get their position pushed to the 
            right of the second sprite.
        """        
        
        # slowly moves both bases to the left
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        
        # checks to see if the first sprite is fully off screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        # checks to see if the second sprite is fully off screen
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
            
    def draw(self, win):
        """Handles the bird animation and adjusts the rotation
            of the bird aswell.

        Args:
            win (pygame window): a pygame window, so the bird knows which window 
                                    to send the updated frame to so it can display
        """
        
        # both sprites are drawn                   
        win.blit(self.base_img_1, (self.x1, self.y))
        win.blit(self.base_img_2, (self.x2, self.y))