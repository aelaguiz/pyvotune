import inspyred

from pyvotune.log import logger
log = logger()


def stats_observer(population, num_generations, num_evaluations, args):
    """Print the statistics of the evolutionary computation to the screen.
    
    This function displays the statistics of the evolutionary computation
    to the screen. The output includes the generation number, the current
    number of evaluations, the maximum fitness, the minimum fitness, 
    the average fitness, and the standard deviation.
    
    .. note::
    
       This function makes use of the ``inspyred.ec.analysis.fitness_statistics`` 
       function, so it is subject to the same requirements.
    
    .. Arguments:
       population -- the population of Individuals
       num_generations -- the number of elapsed generations
       num_evaluations -- the number of candidate solution evaluations
       args -- a dictionary of keyword arguments
    
    """
    stats = inspyred.ec.analysis.fitness_statistics(population)
    worst_fit = '{0:>10}'.format(stats['worst'])[:10]
    best_fit = '{0:>10}'.format(stats['best'])[:10]
    avg_fit = '{0:>10}'.format(stats['mean'])[:10]
    med_fit = '{0:>10}'.format(stats['median'])[:10]
    std_fit = '{0:>10}'.format(stats['std'])[:10]
            
    log.info('Generation Evaluation      Worst       Best     Median    Average    Std Dev')
    log.info('---------- ---------- ---------- ---------- ---------- ---------- ----------')
    log.info('{0:>10} {1:>10} {2:>10} {3:>10} {4:>10} {5:>10} {6:>10}\n'.format(num_generations, 
                                                                                num_evaluations, 
                                                                                worst_fit, 
                                                                                best_fit, 
                                                                                med_fit, 
                                                                                avg_fit, 
                                                                                std_fit))
