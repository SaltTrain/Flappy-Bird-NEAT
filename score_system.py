import pygame

class Scoring_System:
    """Contains everything for keeping track of score, and drawing score
    """    
    
    def __init__(self, screen_size, text_factor_location, text_color, font_size, font_type):
        """Scoring_System constructor

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
        self.text = ''
        self.font = ''
        self.text_container = ''
        
        # keeps track of current score of game
        self.score = 0;
        self.string_score = ''.join(['Score: ', str(self.score)])
        
        # flags for checking when score jumps a tens place
        self.double_flag = False
        self.triple_flag = False
        self.quad_flag = False
        
        # initializes text, font and drawing surface
        self.init_text()
        
    def init_text(self):
        """initializes text, font and drawing surface
        """        
        # create font
        self.font = pygame.font.Font(self.font_type, self.font_size)
        
        # use font to render score and set color
        self.text = self.font.render(self.string_score, True, self.text_color)
        
        # gets the surface of the rendered text
        self.text_container = self.text.get_rect()
        
        # set location of rendered text
        self.text_container.center = (self.screen_size[0]//self.text_factor_location[0], self.screen_size[1]//self.text_factor_location[1])
    
    def draw(self, win):
        """Handles the score drawing on screen

        Args:
            win (pygame.Surface): main window for displaying graphics
        """        
        # updates spacing on screen for new tenths place in score
        if self.score == 10 and not self.double_flag:
            self.text_factor_location[0] += .12
            self.text_container = self.text.get_rect()
            self.text_container.center = (self.screen_size[0] // self.text_factor_location[0], self.screen_size[1] // self.text_factor_location[1])
            self.double_flag = True
        elif self.score == 100 and not self.triple_flag:
            self.text_factor_location[0] += .12
            self.text_container = self.text.get_rect()
            self.text_container.center = (self.screen_size[0] // self.text_factor_location[0], self.screen_size[1] // self.text_factor_location[1])
            self.triple_flag = True
        elif self.score == 1000 and not self.quad_flag:
            self.text_factor_location[0] += .12
            self.text_container = self.text.get_rect()
            self.text_container.center = (self.screen_size[0] // self.text_factor_location[0], self.screen_size[1] // self.text_factor_location[1])
            self.quad_flag = True

        # updates rendered text each frame
        self.text = self.font.render(self.string_score, True, self.text_color)

        # draws text onto screen each frame
        win.blit(self.text ,self.text_container)   
    
    def update_score(self):
        """Increments score and updates string for rendering
        """        
        self.score += 1
        self.string_score = ''.join(['Score: ', str(self.score)])