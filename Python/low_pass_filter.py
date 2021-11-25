from Python import utils
import random
import numpy as np


class LowPassFilter:
    """
        Funções utilizadas pelo otimizador
    """

    def __init__(self, config):
        """
            Inicializa os atributos da classe
        Args:
            config (dataclass): Classe contendo as constantes para a execução do algoritmo
        """
        self.config = config

    def generate_individual(self, individual_class):
        """
            Gera os indivíduos conforme os limites inferiores e superiores
        Args:
            individual_class (DEAP Class): Classe do DEAP utilizada para definir o indivíduo
        """
        individual_vars = [random.randint(self.config.LOWER_BOUNDS[i], self.config.UPPER_BOUNDS[i]) for i in range(self.config.N_VAR)]
        individual = individual_class(individual_vars)

        return individual

    @staticmethod
    def distance(feasible_ind, original_ind):
        """
            Função de distância cartesiana entre dois indivíduos
        """
        return sum((f - o) ** 2 for f, o in zip(feasible_ind, original_ind))

    def closest_feasible(self, individual):
        """
            Função que retorna um indivíduo válido em relação ao indivíduo inválido
        """
        feasible_ind = individual
        feasible_ind = np.maximum(self.config.LOWER_BOUNDS, feasible_ind)
        feasible_ind = np.minimum(self.config.UPPER_BOUNDS, feasible_ind)
        return feasible_ind

    def valid(self, individual):
        """
            Determines se o indivíduo é factível ou não
        """
        if any(individual < self.config.LOWER_BOUNDS) or any(individual > self.config.UPPER_BOUNDS):
            return False
        return True

    def calculate_values(self, individual):
        """
            Calcula os valores dos componentes a partir do indivíduo
        Args:
            individual (list): Indivíduo com as variáveis de projeto

        """
        r1 = self.config.E_SERIES[individual[0]] * 1e3 * (10 ** individual[8])
        r2 = self.config.E_SERIES[individual[1]] * 1e3 * (10 ** individual[9])
        r3 = self.config.E_SERIES[individual[2]] * 1e3 * (10 ** individual[10])
        r4 = self.config.E_SERIES[individual[3]] * 1e3 * (10 ** individual[11])

        c1 = self.config.E_SERIES[individual[4]] * 1e-9 * (10 ** individual[12])
        c2 = self.config.E_SERIES[individual[5]] * 1e-9 * (10 ** individual[13])
        c3 = self.config.E_SERIES[individual[6]] * 1e-9 * (10 ** individual[14])
        c4 = self.config.E_SERIES[individual[7]] * 1e-9 * (10 ** individual[15])

        return r1, r2, r3, r4, c1, c2, c3, c4

    def low_pass_calc(self, individual):
        """
            Calcula os valores para o filtro passa-baixas com resposta Butterworth
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        r1, r2, r3, r4, c1, c2, c3, c4 = self.calculate_values(individual=individual)

        wc1 = 1 / np.sqrt(r1 * r2 * c1 * c2)
        wc2 = 1 / np.sqrt(r3 * r4 * c3 * c4)

        q1 = np.sqrt(r1 * r2 * c1 * c2) / (r1 * c1 + r2 * c1)
        q2 = np.sqrt(r3 * r4 * c3 * c4) / (r3 * c3 + r4 * c3)

        return wc1, wc2, q1, q2

    def objective_function_output(self, individual):
        """
            Função objetivo do problema, com os valores de saída separados
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        wc1, wc2, q1, q2 = self.low_pass_calc(individual=individual)

        deviation_wc = (np.abs(wc1 - self.config.CUTOFF_FREQUENCY) +
                        np.abs(wc2 - self.config.CUTOFF_FREQUENCY)) / self.config.CUTOFF_FREQUENCY
        deviation_q = np.abs(q1 - self.config.QUALITY_FACTOR_1) + \
                      np.abs(q2 - self.config.QUALITY_FACTOR_2)

        f_obj = 0.5 * deviation_wc + 0.5 * deviation_q

        return f_obj, deviation_wc, deviation_q

    def objective_function(self, individual):
        """
            Função objetivo do problema, que é o cálculo do erro de frequência e fator de
            qualidade para o filtro passa-baixas com resposta Butterworth
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        f_obj, _, _ = self.objective_function_output(individual=individual)

        return f_obj,   # OBS: A vírgula é importante para que seja retornado como tuple

    def print_ind(self, individual):
        """
            Imprime os parâmetros de um indivíduo
        Args:
            individual (list): Indivíduo com as variáveis de projeto
        """
        component_raw_values = self.calculate_values(individual=individual)
        r1, r2, r3, r4, c1, c2, c3, c4 = (
            utils.to_si(value=v) for v in component_raw_values
        )

        print("\nDados do indivíduo:")
        print(f"R1 = {r1} ohms")
        print(f"R2 = {r2} ohms")
        print(f"C1 = {c1} farads")
        print(f"C2 = {c2} farads")

        print(f"R3 = {r3} ohms")
        print(f"R4 = {r4} ohms")
        print(f"C3 = {c3} farads")
        print(f"C4 = {c4} farads")

        f_obj, deviation_wc, deviation_q = self.objective_function_output(individual=individual)

        print(f"{f_obj=}\t{deviation_wc=}\t{deviation_q=}")
