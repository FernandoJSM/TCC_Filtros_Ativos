from deap import creator, base, tools, algorithms
from Python import utils
from Python.low_pass_filter import LowPassFilter
import numpy as np


def otm_algorithm(output_file, config):
    """
        Rotina principal do algoritmo de otimização
    Args:
        output_file (str): Caminho do arquivo LTspice de saída
        config (dataclass): Classe contendo as constantes para a execução do algoritmo
    """
    creator.create(name="FitnessMin", base=base.Fitness, weights=(-1.0,))
    creator.create(name="Individual", base=np.ndarray, fitness=creator.FitnessMin)

    otm_base = LowPassFilter(config=config)

    # Inicializando estruturas:
    toolbox = base.Toolbox()
    toolbox.register(alias="individual", function=otm_base.generate_individual,
                     individual_class=creator.Individual)
    toolbox.register(alias="population", function=tools.initRepeat, container=list, func=toolbox.individual)

    toolbox.register(alias="evaluate", function=otm_base.objective_function)
    toolbox.decorate("evaluate", tools.ClosestValidPenalty(feasibility=otm_base.valid,
                                                           feasible=otm_base.closest_feasible,
                                                           alpha=1.0e3,
                                                           distance=otm_base.distance))

    # Definição dos operadores
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", tools.mutUniformInt, low=list(config.LOWER_BOUNDS),
                     up=list(config.UPPER_BOUNDS), indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=config.N_POP)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    hof = tools.HallOfFame(maxsize=1, similar=np.array_equal)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)

    _, logbook = algorithms.eaSimple(population=pop, toolbox=toolbox, cxpb=config.P_CROSS,
                                     mutpb=config.P_MUT, ngen=config.N_GEN, stats=stats,
                                     halloffame=hof, verbose=True)

    best_components = otm_base.calculate_values(individual=hof[0])

    utils.save_file(output_file=output_file,
                    logbook=logbook,
                    best_ind=best_components)

    otm_base.print_ind(individual=hof[0])
