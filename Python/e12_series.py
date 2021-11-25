from dataclasses import dataclass
from Python.optimizer import otm_algorithm
import numpy as np


@dataclass
class Config:
    """
        Configuração do problema de otimização
    """
    N_RUNS = 1      # Quantidade de execuções do algoritmo

    N_GEN = 1000    # Número de gerações
    N_POP = 100     # Tamanho da população
    N_VAR = 16      # Número de variáveis por indivíduo
    P_CROSS = 0.5   # Probabilidade de cruzamento
    P_MUT = 0.2     # Probabilidade de mutação

    LOWER_BOUNDS = np.array([0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0])   # Limites inferiores
    UPPER_BOUNDS = np.array([11, 11, 11, 11, 11, 11, 11, 11,
                             1, 1, 1, 1, 3, 3, 3, 3])   # Limites superiores

    CUTOFF_FREQUENCY = 2 * np.pi * 5000    # Frequência de corte em rad/s
    QUALITY_FACTOR_1 = 0.54113             # Fator de qualidade 1 para o filtro de resposta Butterworth de 4a ordem
    QUALITY_FACTOR_2 = 1.30719             # Fator de qualidade 2 para o filtro de resposta Butterworth de 4a ordem

    # Lista de valores de componentes da série E12
    E_SERIES = np.array([1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2])


if __name__ == "__main__":
    for i in range(Config.N_RUNS):
        otm_algorithm(output_file="../data/best_result_e12.json", config=Config)
