"""Otimização de um filtro ativo passa-baixas Sallen-Key Butterworth de 6a ordem"""
from dataclasses import dataclass
from Python.optimizer import otm_algorithm
import numpy as np


@dataclass
class Config:
    """
        Configuração do problema de otimização
    """
    N_RUNS = 1     # Quantidade de execuções do algoritmo

    N_GEN = 1000    # Número de gerações
    N_POP = 100     # Tamanho da população
    N_VAR = 24      # Número de variáveis por indivíduo
    P_CROSS = 0.5   # Probabilidade de cruzamento
    P_MUT = 0.2     # Probabilidade de mutação

    LOWER_BOUNDS = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])   # Limites inferiores
    UPPER_BOUNDS = np.array([47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47,
                             1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3])   # Limites superiores

    CUTOFF_FREQUENCY = 2 * np.pi * 5000    # Frequência de corte em rad/s
    QUALITY_FACTOR_1 = 0.5176              # Fator de qualidade 1 para o filtro de resposta Butterworth
    QUALITY_FACTOR_2 = 0.7072              # Fator de qualidade 2 para o filtro de resposta Butterworth
    QUALITY_FACTOR_3 = 1.9305              # Fator de qualidade 3 para o filtro de resposta Butterworth

    # Lista de valores de componentes da série E48
    E_SERIES = np.array([1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54,
                         1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49,
                         2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65, 3.83, 4.02,
                         4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49,
                         6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53])


if __name__ == "__main__":
    for i in range(Config.N_RUNS):
        otm_algorithm(output_file="best_result_e48.json", config=Config)
