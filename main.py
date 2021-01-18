import pygame
import os

# not used yet
from pygame.version import PygameVersion

import neat
import time
import random
from pygame.time import get_ticks

# custom import
from bird import Bird
from base import Base
from pipe import Pipe
from score_system import Scoring_System
from neat_model import run_neat_model, replay_genome


# dimensions for the pygame window
WIN_WIDTH = 575
WIN_HEIGHT = 800
SCREEN_SIZE = (WIN_WIDTH, WIN_HEIGHT)

# load background image
BG_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))]
    
    
    
def draw_window(win, birds, pipes, base, scoring_system):
    """Handles the drawing of all sprites

    Args:
        win (Surface): makes a window for displaying and interacting with the graphics
        bird (Bird): custom Bird object
    """    
    # draw background and pins to the top left
    win.blit(BG_IMG[0], (0,0))
    
    # draw pipes
    for pipe in pipes:
        pipe.draw(win)
        
    # draws base floor
    base.draw(win)
    
    # draw scoring system
    scoring_system.draw(win)
    
    # bird draws itself
    for bird in birds:
        bird.draw(win)
    
    # update the display with the new frame
    pygame.display.update()
    
def main(_genomes, config):
    """Main game function call
    """    
    
    pygame.init()
    
    # holds the data needed for each birds neural network
    networks = []
    genomes = []
    birds = []
    
    # creating a seperate network for each bird and append it respectively
    instance_a_NeuralNetwork_foreach_object(_genomes, config, networks, birds, genomes)
    
    # instance objects
    base = Base(730)
    pipes = [Pipe(600)]
    scoring_system = Scoring_System(SCREEN_SIZE, [1.3, 24], (255, 255, 255), 64, 'freesansbold.ttf')
    
    # setup a pygame window
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
     
    # instance a Clocl object for setting the fps
    clock = pygame.time.Clock()
    
    # main game loop
    run = True
    while run:
        
        # set fps
        clock.tick(60)
        
        # user event handling
        for event in pygame.event.get():
            pass
            # check if user quits game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         bird.jump()
                
        # update objects
        
        # checks when the birds passes a pipe and sets the next pipe in pipes as the new target
        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()/2:
                pipe_index = 1
        else: # if we have no birds than we just stop the loop
            run = False
            break
                
        # gives the birds a positive fitness score for surviving each frame
        # 
        for index, bird in enumerate(birds):
            # gives the birds a positive fitness score for surviving each frame
            genomes[index].fitness += 0.002
            # move bird
            bird.move()
            
            # passes the birds y position, top and bottom pipes y position into the input of the network
            output = networks[index].activate( (bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)) )
            
            # adds red line for each bird showing current pipe target
            bird.visualizing_pipe_analysis(win, (pipes[pipe_index].x, pipes[pipe_index].height), (pipes[pipe_index].x, pipes[pipe_index].bottom))
            
            # gets neural network output from the input and jumps if condition is met
            if output[0] > 0.5:
                bird.jump()
                
        # check 
        add_pipe = False
        pipe_removal = []
        for pipe in pipes:
            pipe.move()
            
            # checks each bird if collision with pipe has occured,
            #   than remove bird and its neural network since it died.
            #   Additionally, add a negative fitness score since it died,
            #   which of course is undesired.
            for bird in birds:
                if pipe.collide(bird):
                    if len(birds) == 1:
                        print(scoring_system.score)
                    genomes[birds.index(bird)].fitness -= 0.5
                    networks.pop(birds.index(bird))
                    genomes.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                
                # checks if bird passed the pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            # remove pipe once it reaches the end of screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipe_removal.append(pipe)
                    
                
        # updates score since a pipe has been passed.
        if add_pipe:
            scoring_system.update_score()
            # updates each bird fitness score since it passed a pipe
            for genome in genomes:
                genome.fitness += 0.5
            
            # adds new pipe
            pipes.append(Pipe(600))
            
        # deletes pipe
        for delete_this_pipe in pipe_removal:
            pipes.remove(delete_this_pipe)
        # reset pip removal list
        pipe_removal = []
        
        # bird touches floor or ceiling than kill bird and add a negative fitness score
        for index, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                genomes[birds.index(bird)].fitness -= 0.5
                birds.pop(index)
                networks.pop(index)
                genomes.pop(index)
        
        # update base position
        base.move()
        
        # draws all the sprites on screen
        draw_window(win, birds, pipes, base, scoring_system)


###--helper functions--###
# for instancing network, genome, and bird
def instance_a_NeuralNetwork_foreach_object(_genomes, config, networks, birds, genomes):
    # creating a seperate network for each bird and append it respectively
    for _, genome in _genomes: # returns tuple, 2nd indedx is the genome object
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        
        birds.append(Bird(230, 350))
        
        genome.fitness = 0
        
        genomes.append(genome)

# display neural network information on screen


# main loop
if __name__ == '__main__':
    # get NEAT configuration file location, used to setup the NEAT model
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    
    run_neat_model(config_path, main, 50, 'flappy_bird_NN')