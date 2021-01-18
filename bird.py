import pygame
import os

# load all of the bird animation images
BIRD_IMG = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))]


class Bird:
    """The Bird class represents a flappy bird sprite. The main feature of this model is the jump() function. It allows the Bird to perform a jump animation. The rest of the functions are standard pygame requirements. move() is used to calculate movement. While draw() handles the graphics handling on screen. Finally get_mask() provides a collision mask, useful for well collision detection.
    """    
    
    IMGS = BIRD_IMG
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        """Bird's constructor

        Args:
            x (float): the current instance Bird x position on screen
            y (float): the current instance Bird y position on screen
        """        
        
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        
        self.top_pipe_position = (0,0)
        self.bottom_pipe_position = (0,0)
        
        # holds the current default image
        self.img = self.IMGS[0]
        
    def jump(self):
        """Action used by the user. If the users uses jump() than the self.vel is set to -10.5 so that when move() 
            is running per frame. Than it will appropriatly move the charchter in a upwards realisitic jump trajectory.
        """        
        
        # scales the jump trajectory
        self.vel = -11.5
        
        # hold the original height as a reference
        self.height = self.y
        
        self.tick_count = 0
        
    def move(self):
        """Calculates the birds movement and sets its rotation 
            based off of upwards or downwards trajectory
        """        
        self.tick_count += .6
        
        # if the birds jumps, than it will update self.vel to -10.5 
        #    so the bird moves up while holding a proper rotation
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2
        
        # set max speed, bird can't move faster than 16 pixles per frame
        if displacement >= 16:
                displacement = 16
        # downward movement
        if displacement < 0:
            displacement -= 2
            
            
        # birds height is changed by the displacement per frame
        self.y +=  displacement/2.5
        
        # keep bird rotated upwards while is traveling up
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        # else rotate the bird downwards since it traveling downwards
        else:
            # while the bird is falling down, rotate it downwards to a max of -90:
            if self.tilt > -35:
                # slowly rotate the bird downwards
                self.tilt  -= self.ROTATION_VELOCITY
          
    def draw(self, win):
        """Handles the bird animation and adjusts the rotation
            of the bird aswell.

        Args:
            win (pygame window): a pygame window, so the bird knows which window 
                                    to send the updated frame to so it can display
        """            
        # increments per frame
        self.img_count += 1
        
        # self.ANIMATION_TIME dictates the length it takes the bird 
        #   to complete a flap from start to finish. In this case each 
        #   image will last 5 frames, before updating. The total animation 
        #   take 25 frames to finish.
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 +1:
            self.img = self.IMGS[0]
            self.img_count = 0;
    
        # self.tilt is handled by self.move() each frame. As the bird falls, self.move() will slowly rotate the bird downwards to a max of -90.
        #   the bird will stop flapping and just glide if it meets or exceeds the downward rotation threshhold  
        if self.tilt <= -20:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        # rotates the bird and changes the transofrm pivot from the top left to the center of the bird
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        
        pygame.draw.line(win, (255, 0, 0), (self.x + (self.img.get_width()/2), self.y + (self.img.get_height()/2)), self.top_pipe_position, width=2)
        pygame.draw.line(win, (255, 0, 0), (self.x + (self.img.get_width()/2), self.y + (self.img.get_height()/2)), self.bottom_pipe_position, width=2)
        
    def get_mask(self):
        """pygame.mask: -> Useful for fast pixel perfect collision detection. A Mask uses 1bit per pixel to store which parts collide.

        Returns:
            Mask: gets collision mask for the bird in its current image of animation 
        """        
        return pygame.mask.from_surface(self.img)
    
    def visualizing_pipe_analysis(self, win, top_pipe_position, bottom_pipe_position):
        self.top_pipe_position = top_pipe_position
        self.bottom_pipe_position = bottom_pipe_position
        
    