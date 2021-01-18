import neat
import pickle

def run_neat_model(config_path, function_name, max_generations, file_name):
    """Creates a NEAT model based on parameters passed. If further modification is required for model
        than tweak the init_neat_model() function.

    Args:
        config_path (string): path location to the required text file
        function_name (string): main looping function, must contain the fitness evaluation
        max_generations (integer): max number of generation before stopping
        file_name (string): file name used to save the 'winner' of the neat model
    """    
    # initializes the NEAT model
    config = init_neat_model(config_path)
    
    # uses configured neat model for configuring Population parameters
    population = neat.Population(config)
    
    # --not required-- however useful information is generated on the command prompt on each generation
    show_neat_generations_statistics(population)
    
    # runs the neat model until fitness requirements are met, returns best model
    winner_neat_model = population.run(function_name, max_generations)
    
    # saves the model for future use
    save_neat_model(file_name, winner_neat_model)







def init_neat_model(config_path):
    """Initializes a NEAT model based on the configuration file.

    Args:
        config_path (string): path location to the required text file

    Returns:
        neat.config.Config: used to configure the Population object
    """
    # create NEAT model
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path)
    
    # return model
    return config              

def show_neat_generations_statistics(population):
    """Helps user monitor each generation. Information is displayed on the command prompt

    Args:
        population (neat.Population): Population object created with NEAT model configurations
    """    
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
        
def save_neat_model(file_name, neat_model):
    """Saves NEAT model in pickle format for use later.

    Args:
        file_name (string): name of model 
        neat_model (neat.genome.DefaultGenome): the neural network that performed the best 
    """    
    with open(''.join([file_name,'.pickle']), 'wb') as f:
        pickle.dump(neat_model, f)

def replay_genome(config_path, genome_file_name='winner.pickle'):
    """Loads Genome model

    Args:
        config_path (string): path location to the required text file
        genome_file_name (string, optional): genome file name, used for loading file. Defaults to 'winner.pickle' as EX.

    Returns:
        [type]: [description]
    """    
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_file_name, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    return genomes, config

