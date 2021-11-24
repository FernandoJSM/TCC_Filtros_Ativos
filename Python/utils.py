"""Métodos úteis utilizados no código"""
import json
import os
import numpy as np


def save_file(output_file, logbook, best_ind):
    """
        Salva os dados da otimização se o resultado for melhor do que já está salvo
    Args:
        output_file (str): Caminho do arquivo json de saída
        logbook (DEAP logbook): Objeto logbook do DEAP
        best_ind (list): Lista com os valores de componentes obtidos, de r1-r6 e c1-c6
    """
    hist = logbook.select("min")

    new_data = {
        "hist": hist,
        "best_fitness": hist[-1],
        "best_individual": best_ind
    }

    if os.path.exists(output_file):
        with open(file=output_file, mode="r") as f:
            stored_data = json.load(f)

        if hist[-1] < stored_data.get("best_fitness", np.inf):
            print("Novo ótimo encontrado!")
        else:
            return

    with open(file=output_file, mode="w") as f:
        json.dump(new_data, f, indent=4)


def to_si(value):
    """
        Converte o valor para uma string com o respectivo prefixo conforme a linguagem SPICE
    """
    dec_suffixes = ['m', 'u', 'n', 'p']
    inc_suffixes = ['K', 'MEG', 'G', 'T']

    if value == 0:
        return str(0)

    degree = int(np.floor(np.log10(np.abs(value)) / 3))

    suffix = ""

    if degree != 0:
        if degree > 0:
            suffix = inc_suffixes[degree - 1]
        elif degree < 0:
            suffix = dec_suffixes[-degree - 1]
        scale = 10 ** (degree * 3)

        scaled = np.round(value / scale, 3)

        s = f"{scaled}{suffix}"

    else:
        s = f"{value}"

    return s
