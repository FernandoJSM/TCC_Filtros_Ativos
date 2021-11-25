import re
import matplotlib.pyplot as plt


def extract_datapoints(file_path):
    """
        Extrai os pontos de amplitude do plot de frequência do LTSpice
    Args:
        file_path (str): Caminho do arquivo
    """
    freq_list = list()
    amplitude_list = list()

    with open(file=file_path, mode="r") as f:
        data = f.readlines()

    data.pop(0)
    for line in data:
        values = re.findall(pattern=r"(-?[0-9]\.[0-9]+e[+-][0-9]{3})+", string=line)
        freq = float(values[0])
        amplitude = float(values[1])
        # phase = float(values[2])

        freq_list.append(freq)
        amplitude_list.append(amplitude)

    return freq_list, amplitude_list


if __name__ == "__main__":
    f_e12, a_e12 = extract_datapoints(file_path="../LTspiceSchematics/frequency_response_e12.txt")
    f_e24, a_e24 = extract_datapoints(file_path="../LTspiceSchematics/frequency_response_e24.txt")
    f_e48, a_e48 = extract_datapoints(file_path="../LTspiceSchematics/frequency_response_e48.txt")

    plt.semilogx(f_e12, a_e12, color="r", label="Série E12")
    plt.semilogx(f_e24, a_e24, color="g", label="Série E24")
    plt.semilogx(f_e48, a_e48, color="b", label="Série E48")
    plt.semilogx([5e3, 5e3], [-10e3, 10e3], color='k')

    plt.axis([1, 100e3, -80, 1])
    plt.grid(color='k', linestyle='-', linewidth=0.5)

    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Ganho (dB)")
    plt.title("Resposta em frequência do filtro obtido com a otimização")
    plt.legend()
    plt.show()
