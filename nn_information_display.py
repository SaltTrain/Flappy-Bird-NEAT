import pygame

class NN_Information_Display():
    """Displays neural network information on screen
    """    
    
    def __init__(self, screen_size, text_factor_location, text_color, font_size, font_type):
        """NN_Information_Dispay constructor

        Args:
            screen_size ((integer)tuple): should contain width and height of screen
            text_factor_location ((float)list): gets divided by screen_size to determine score drawing location EX: for center location [2,2]
            text_color ((integer)tuple): should contain r, g, b values, each ranges from 0-255
            font_size (integer): font size
            font_type (string): string of supported pygame fonts, EX: freesansbold.ttf
        """        
        
        self.screen_size = screen_size
        self.text_factor_location = text_factor_location
        self.text_color = text_color
        self.font_size = font_size
        self.font_type = font_type
        
        # these initialized variables are used to store required pygame objects for creating text
        self.text_1 = ''
        self.text_2 = ''
        self.text_3 = ''
        
        self.font = ''
        
        self.text_container_1 = ''
        self.text_container_2 = ''
        self.text_container_3 = ''
        
        # required text information
        self.generations = 0
        self.birds_remaining = 0
        self.best_fitness = 0
        
        self.first_line = ''.join(['Gen: ',str(self.generations)])
        self.second_line = ''.join(['Birds: ', str(self.birds_remaining)])
        self.third_line = ''.join(['Fit: ', '{0:.2f}'.format(self.best_fitness)])
        
         # initializes text, font and drawing surface
        self.init_text()
    
    def init_text(self):
        """initializes text, font and drawing surface
        """        
        # create font
        self.font = pygame.font.Font(self.font_type, self.font_size)
        
        # use font to render score and set color
        self.text_1 = self.font.render(self.first_line, True, self.text_color)
        self.text_2 = self.font.render(self.second_line, True, self.text_color)
        self.text_3 = self.font.render(self.third_line, True, self.text_color)
        
        # gets the surface of the rendered text
        self.text_container_1 = self.text_1.get_rect()
        self.text_container_2 = self.text_2.get_rect()
        self.text_container_3 = self.text_3.get_rect()
        
        # set location of rendered text
        self.text_container_1.center = (self.screen_size[0]//self.text_factor_location[0], self.screen_size[1]//self.text_factor_location[1])
        self.text_container_2.center = (self.screen_size[0]//self.text_factor_location[0], self.screen_size[1]//self.text_factor_location[1]+self.font_size)
        self.text_container_3.center = (self.screen_size[0]//self.text_factor_location[0], self.screen_size[1]//self.text_factor_location[1]+self.font_size+self.font_size)
    
    def draw(self, win):
        """Handles the score drawing on screen

        Args:
            win (pygame.Surface): main window for displaying graphics
        """       
        # updates rendered text each frame
        self.text_1 = self.font.render(self.first_line, True, self.text_color)
        self.text_2 = self.font.render(self.second_line, True, self.text_color)
        self.text_3 = self.font.render(self.third_line, True, self.text_color)

        # draws text onto screen each frame
        win.blit(self.text_1 ,self.text_container_1)
        win.blit(self.text_2 ,self.text_container_2)
        win.blit(self.text_3 ,self.text_container_3)
        
    def update_information(self, bird_count, generation):
        """Gets information on bird count and current generation for keeping 
            text display updated

        Args:
            bird_count (integer): how many birds are currently left
            generation (integer): current generation count
        """        
        self.birds_remaining = bird_count
        self.generations = generation
        
        self.first_line = ''.join(['Gen: ',str(self.generations)])
        self.second_line = ''.join(['Birds: ', str(self.birds_remaining)])
        
    def update_fitness_score(self, best_fitness):
        """Gets information on the last bird left in the current generation

        Args:
            best_fitness (integer): best genome fitness score so far
        """        
        self.best_fitness = best_fitness
        
        self.third_line = ''.join(['Fit: ', '{0:.2f}'.format(self.best_fitness)])