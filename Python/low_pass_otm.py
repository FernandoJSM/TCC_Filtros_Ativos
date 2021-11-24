from deap import base, creator, tools, algorithms
import random
import numpy as np
from decimal import Decimal


class Optimizer:
    """
        Funções utilizadas pelo otimizador
    """

    @staticmethod
    def generate_individual(individual_class, n_var, lower_bounds, upper_bounds):
        """
            Gera os indivíduos conforme os limites inferiores e superiores
        Args:
            individual_class (DEAP Class): Classe do DEAP utilizada para definir o indivíduo
            n_var (int): Tamanho do indivíduo
            lower_bounds (list): Lista contendo os limites inferiores
            upper_bounds (list): Lista contendo os limites superiores
        """
        individual_vars = [random.randint(lower_bounds[i], upper_bounds[i]) for i in range(n_var)]
        individual = individual_class(individual_vars)

        return individual

    @staticmethod
    def low_pass_calc(individual):
        """
            Calcula os valores para o filtro passa-baixas com resposta Butterworth
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        E12_series = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

        r1 = E12_series[individual[0]] * 1e3 * (10 ** individual[8])
        r2 = E12_series[individual[1]] * 1e3 * (10 ** individual[9])
        r3 = E12_series[individual[2]] * 1e3 * (10 ** individual[10])
        r4 = E12_series[individual[3]] * 1e3 * (10 ** individual[11])
        c1 = E12_series[individual[4]] * 1e-9 * (10 ** individual[12])
        c2 = E12_series[individual[5]] * 1e-9 * (10 ** individual[13])
        c3 = E12_series[individual[6]] * 1e-9 * (10 ** individual[14])
        c4 = E12_series[individual[7]] * 1e-9 * (10 ** individual[15])

        wc1 = 1 / np.sqrt(r1 * r2 * c1 * c2)
        wc2 = 1 / np.sqrt(r3 * r4 * c3 * c4)

        q1 = np.sqrt(r1 * r2 * c1 * c2) / (r1 * c1 + r2 * c1)
        q2 = np.sqrt(r3 * r4 * c3 * c4) / (r3 * c3 + r4 * c3)

        return wc1, wc2, q1, q2

    @staticmethod
    def objective_function(individual, cutoff_frequency, quality_factor_1, quality_factor_2):
        """
            Função objetivo do problema, que é o cálculo do erro de frequência e fator de
            qualidade para o filtro passa-baixas com resposta Butterworth
        Args:
            individual (list): Indivíduo com as variáveis de projeto
            cutoff_frequency (float): Frequência de corte em rad/s
            quality_factor_1 (float): Fator de qualidade 1 para o filtro de resposta Butterworth
            quality_factor_2 (float): Fator de qualidade 2 para o filtro de resposta Butterworth
        """
        wc1, wc2, q1, q2 = Optimizer.low_pass_calc(individual)

        deviation_wc = (np.abs(wc1 - cutoff_frequency) + np.abs(wc2 - cutoff_frequency)) / cutoff_frequency
        deviation_q = np.abs(q1 - quality_factor_1) + np.abs(q2 - quality_factor_2)

        f_obj = 0.5*deviation_wc + 0.5*deviation_q

        return f_obj,   # OBS: A vírgula é importante para que seja retornado como tuple


    @staticmethod
    def print_ind(individual):
        """
            Imprime os parâmetros de um indivíduo
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        E12_series = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

        r1 = E12_series[individual[0]] * 1e3 * (10 ** individual[8])
        r2 = E12_series[individual[1]] * 1e3 * (10 ** individual[9])
        r3 = E12_series[individual[2]] * 1e3 * (10 ** individual[10])
        r4 = E12_series[individual[3]] * 1e3 * (10 ** individual[11])
        c1 = E12_series[individual[4]] * 1e-9 * (10 ** individual[12])
        c2 = E12_series[individual[5]] * 1e-9 * (10 ** individual[13])
        c3 = E12_series[individual[6]] * 1e-9 * (10 ** individual[14])
        c4 = E12_series[individual[7]] * 1e-9 * (10 ** individual[15])

        wc1, wc2, _, _ = Optimizer.low_pass_calc(individual)

        print("\nDados do indivíduo:")
        print("R1 = " + Decimal(r1).normalize().to_eng_string() + " ohms")
        print("R2 = " + Decimal(r2).normalize().to_eng_string() + " ohms")
        print("C1 = " + Decimal(c1).normalize().to_eng_string() + " farads")
        print("C2 = " + Decimal(c1).normalize().to_eng_string() + " farads")
        print("R3 = " + Decimal(r3).normalize().to_eng_string() + " ohms")
        print("R4 = " + Decimal(r4).normalize().to_eng_string() + " ohms")
        print("C3 = " + Decimal(c3).normalize().to_eng_string() + " farads")
        print("C4 = " + Decimal(c4).normalize().to_eng_string() + " farads")

        print("fc1 = " + str(wc1/(2 * np.pi)) + " Hz")
        print("fc2 = " + str(wc2/(2 * np.pi)) + " Hz")


def main():
    # Configuração do problema de otimização
    n_gen = 1000    # Número de gerações
    n_pop = 100     # Tamanho da população
    n_var = 16      # Número de variáveis por indivíduo
    p_cross = 0.5   # Probabilidade de cruzamento
    p_mut = 0.3     # Probabilidade de mutação

    lower_bounds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    upper_bounds = [11, 11, 11, 11, 11, 11, 11, 11, 1, 1, 1, 1, 3, 3, 3, 3]

    cutoff_frequency = 2 * np.pi * 5000     # Frequência de corte em rad/s
    quality_factor_1 = 0.54118              # Fator de qualidade 1 para o filtro de resposta Butterworth
    quality_factor_2 = 1.30651              # Fator de qualidade 2 para o filtro de resposta Butterworth

    # ---

    creator.create(name="FitnessMin", base=base.Fitness, weights=(-1.0,))
    creator.create(name="Individual", base=list, fitness=creator.FitnessMin)

    # Inicializando estruturas:
    toolbox = base.Toolbox()
    toolbox.register(alias="individual", function=Optimizer.generate_individual,
                     individual_class=creator.Individual, n_var=n_var, lower_bounds=lower_bounds,
                     upper_bounds=upper_bounds)
    toolbox.register(alias="population", function=tools.initRepeat, container=list, func=toolbox.individual)

    toolbox.register(alias="evaluate", function=Optimizer.objective_function, cutoff_frequency=cutoff_frequency,
                     quality_factor_1=quality_factor_1, quality_factor_2=quality_factor_2)

    # Definição dos operadores
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=n_pop)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)

    algorithms.eaSimple(population=pop, toolbox=toolbox, cxpb=p_cross,
                        mutpb=p_mut, ngen=n_gen, stats=stats,
                        halloffame=hof)
    print(hof[0])
    Optimizer.print_ind(hof[0])


if __name__ == "__main__":
    main()