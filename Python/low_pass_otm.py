"""Otimização de um filtro ativo passa-baixas Sallen-Key Butterworth de 6a ordem"""

from deap import base, creator, tools, algorithms
import numpy as np
import random


# Configuração do problema de otimização
from Python import utils

N_RUNS = 10     # Quantidade de execuções do algoritmo

N_GEN = 1000    # Número de gerações
N_POP = 100     # Tamanho da população
N_VAR = 24      # Número de variáveis por indivíduo
P_CROSS = 0.5   # Probabilidade de cruzamento
P_MUT = 0.2     # Probabilidade de mutação

LOWER_BOUNDS = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])   # Limites inferiores
UPPER_BOUNDS = np.array([23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,
                         1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3])   # Limites superiores

CUTOFF_FREQUENCY = 2 * np.pi * 300    # Frequência de corte em rad/s
QUALITY_FACTOR_1 = 0.5176              # Fator de qualidade 1 para o filtro de resposta Butterworth
QUALITY_FACTOR_2 = 0.7072              # Fator de qualidade 2 para o filtro de resposta Butterworth
QUALITY_FACTOR_2 = 1.9305              # Fator de qualidade 3 para o filtro de resposta Butterworth

# Lista de valores de componentes da série E12
E24_SERIES = np.array([1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                       3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1])


class Optimizer:
    """
        Funções utilizadas pelo otimizador
    """

    @staticmethod
    def generate_individual(individual_class):
        """
            Gera os indivíduos conforme os limites inferiores e superiores
        Args:
            individual_class (DEAP Class): Classe do DEAP utilizada para definir o indivíduo
        """
        individual_vars = [random.randint(LOWER_BOUNDS[i], UPPER_BOUNDS[i]) for i in range(N_VAR)]
        individual = individual_class(individual_vars)

        return individual

    @staticmethod
    def distance(feasible_ind, original_ind):
        """
            Função de distância cartesiana entre dois indivíduos
        """
        return sum((f - o) ** 2 for f, o in zip(feasible_ind, original_ind))

    @staticmethod
    def closest_feasible(individual):
        """
            Função que retorna um indivíduo válido em relação ao indivíduo inválido
        """
        feasible_ind = individual
        feasible_ind = np.maximum(LOWER_BOUNDS, feasible_ind)
        feasible_ind = np.minimum(UPPER_BOUNDS, feasible_ind)
        return feasible_ind

    @staticmethod
    def valid(individual):
        """
            Determines se o indivíduo é factível ou não
        """
        if any(individual < LOWER_BOUNDS) or any(individual > UPPER_BOUNDS):
            return False
        return True

    @staticmethod
    def calculate_values(individual):
        """
            Calcula os valores dos componentes a partir do indivíduo
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        r1 = E24_SERIES[individual[0]] * 1e3 * (10 ** individual[12])
        r2 = E24_SERIES[individual[1]] * 1e3 * (10 ** individual[13])
        r3 = E24_SERIES[individual[2]] * 1e3 * (10 ** individual[14])
        r4 = E24_SERIES[individual[3]] * 1e3 * (10 ** individual[15])
        r5 = E24_SERIES[individual[4]] * 1e3 * (10 ** individual[16])
        r6 = E24_SERIES[individual[5]] * 1e3 * (10 ** individual[17])

        c1 = E24_SERIES[individual[6]] * 1e-9 * (10 ** individual[18])
        c2 = E24_SERIES[individual[7]] * 1e-9 * (10 ** individual[19])
        c3 = E24_SERIES[individual[8]] * 1e-9 * (10 ** individual[20])
        c4 = E24_SERIES[individual[9]] * 1e-9 * (10 ** individual[21])
        c5 = E24_SERIES[individual[10]] * 1e-9 * (10 ** individual[22])
        c6 = E24_SERIES[individual[11]] * 1e-9 * (10 ** individual[23])

        return r1, r2, r3, r4, r5, r6, c1, c2, c3, c4, c5, c6

    @staticmethod
    def low_pass_calc(individual):
        """
            Calcula os valores para o filtro passa-baixas com resposta Butterworth
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        r1, r2, r3, r4, r5, r6, c1, c2, c3, c4, c5, c6 = Optimizer.calculate_values(individual)

        wc1 = 1 / np.sqrt(r1 * r2 * c1 * c2)
        wc2 = 1 / np.sqrt(r3 * r4 * c3 * c4)
        wc3 = 1 / np.sqrt(r5 * r6 * c5 * c6)

        q1 = np.sqrt(r1 * r2 * c1 * c2) / (r1 * c1 + r2 * c1)
        q2 = np.sqrt(r3 * r4 * c3 * c4) / (r3 * c3 + r4 * c3)
        q3 = np.sqrt(r5 * r6 * c5 * c6) / (r5 * c5 + r6 * c5)

        return wc1, wc2, wc3, q1, q2, q3

    @staticmethod
    def objective_function(individual):
        """
            Função objetivo do problema, que é o cálculo do erro de frequência e fator de
            qualidade para o filtro passa-baixas com resposta Butterworth
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        wc1, wc2, wc3, q1, q2, q3 = Optimizer.low_pass_calc(individual)

        deviation_wc = (np.abs(wc1 - CUTOFF_FREQUENCY) +
                        np.abs(wc2 - CUTOFF_FREQUENCY) +
                        np.abs(wc3 - CUTOFF_FREQUENCY)) / CUTOFF_FREQUENCY
        deviation_q = np.abs(q1 - QUALITY_FACTOR_1) + np.abs(q2 - QUALITY_FACTOR_2) + np.abs(q3 - QUALITY_FACTOR_2)

        f_obj = 0.5*deviation_wc + 0.5*deviation_q

        return f_obj,   # OBS: A vírgula é importante para que seja retornado como tuple

    @staticmethod
    def print_ind(individual):
        """
            Imprime os parâmetros de um indivíduo
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        component_raw_values = Optimizer.calculate_values(individual)
        r1, r2, r3, r4, r5, r6, c1, c2, c3, c4, c5, c6 = (
            utils.to_si(value=v) for v in component_raw_values
        )

        wc1, wc2, wc3, _, _, _ = Optimizer.low_pass_calc(individual)

        print("\nDados do indivíduo:")
        print(f"R1 = {r1} ohms")
        print(f"R2 = {r2} ohms")
        print(f"C1 = {c1} farads")
        print(f"C2 = {c2} farads")

        print(f"R3 = {r3} ohms")
        print(f"R4 = {r4} ohms")
        print(f"C3 = {c3} farads")
        print(f"C4 = {c4} farads")

        print(f"R5 = {r5} ohms")
        print(f"R6 = {r6} ohms")
        print(f"C5 = {c5} farads")
        print(f"C6 = {c6} farads")

        print("fc1 = " + "{:.3f}".format(wc1/(2 * np.pi)) + " Hz")
        print("fc2 = " + "{:.3f}".format(wc2/(2 * np.pi)) + " Hz")
        print("fc3 = " + "{:.3f}".format(wc2 / (2 * np.pi)) + " Hz")


def otm_algorithm(output_file):
    """
        Rotina principal do algoritmo de otimização
    Args:
        output_file (str): Caminho do arquivo LTspice de saída
    """
    creator.create(name="FitnessMin", base=base.Fitness, weights=(-1.0,))
    creator.create(name="Individual", base=np.ndarray, fitness=creator.FitnessMin)

    # Inicializando estruturas:
    toolbox = base.Toolbox()
    toolbox.register(alias="individual", function=Optimizer.generate_individual,
                     individual_class=creator.Individual)
    toolbox.register(alias="population", function=tools.initRepeat, container=list, func=toolbox.individual)

    toolbox.register(alias="evaluate", function=Optimizer.objective_function)
    toolbox.decorate("evaluate", tools.ClosestValidPenalty(feasibility=Optimizer.valid,
                                                           feasible=Optimizer.closest_feasible,
                                                           alpha=1.0e3,
                                                           distance=Optimizer.distance))

    # Definição dos operadores
    toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0.5)
    toolbox.register("mutate", tools.mutUniformInt, low=list(LOWER_BOUNDS), up=list(UPPER_BOUNDS), indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=2)

    pop = toolbox.population(n=N_POP)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    hof = tools.HallOfFame(maxsize=1, similar=np.array_equal)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)

    _, logbook = algorithms.eaSimple(population=pop, toolbox=toolbox, cxpb=P_CROSS,
                                     mutpb=P_MUT, ngen=N_GEN, stats=stats,
                                     halloffame=hof, verbose=True)

    best_components = Optimizer.calculate_values(individual=hof[0])

    utils.save_file(output_file=output_file,
                    logbook=logbook,
                    best_ind=best_components)

    print("\nFitness:")
    print(Optimizer.objective_function(hof[0])[0])
    Optimizer.print_ind(hof[0])


if __name__ == "__main__":
    for i in range(1):
        otm_algorithm(output_file="best_result.json")
