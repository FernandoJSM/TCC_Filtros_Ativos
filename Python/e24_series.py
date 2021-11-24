"""Otimização de um filtro ativo passa-baixas Sallen-Key Butterworth de 6a ordem"""
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
    N_VAR = 24      # Número de variáveis por indivíduo
    P_CROSS = 0.5   # Probabilidade de cruzamento
    P_MUT = 0.2     # Probabilidade de mutação

    LOWER_BOUNDS = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])   # Limites inferiores
    UPPER_BOUNDS = np.array([23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,
                             1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3])   # Limites superiores

    CUTOFF_FREQUENCY = 2 * np.pi * 5000    # Frequência de corte em rad/s
    QUALITY_FACTOR_1 = 0.5176              # Fator de qualidade 1 para o filtro de resposta Butterworth
    QUALITY_FACTOR_2 = 0.7072              # Fator de qualidade 2 para o filtro de resposta Butterworth
    QUALITY_FACTOR_3 = 1.9305              # Fator de qualidade 3 para o filtro de resposta Butterworth

    # Lista de valores de componentes da série E24
    E_SERIES = np.array([1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                         3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1])


if __name__ == "__main__":
    for i in range(Config.N_RUNS):
        otm_algorithm(output_file="../data/best_result_e24.json", config=Config)
