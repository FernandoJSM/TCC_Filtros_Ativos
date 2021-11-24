"""Gera um arquivo para o LTspice de um filtro ativo passa-baixas Sallen-Key Butterworth de 6a ordem"""
from Python import utils
import json

MAX_FREQ = '50k'    # Frequência máxima da simulação em frequências


def write_file(data_path, output_path):
    """
        Gera um arquivo .asc do LTspice de um filtro ativo passa-baixas Sallen-Key Butterworth de 6a ordem
    Arts:
        data_path (str): Caminho do arquivo onde estão salvos os dados da otimização
        output_path (str): Caminho do arquivo onde será salvo o esquemático do LTspice
    """
    with open(file=data_path, mode="r") as f:
        stored_data = json.load(f)

    component_raw_values = stored_data["best_individual"]

    r1_s, r2_s, r3_s, r4_s, r5_s, r6_s, c1_s, c2_s, c3_s, c4_s, c5_s, c6_s = (
            utils.to_si(value=v) for v in component_raw_values
        )

    file_string = \
f"""Version 4
SHEET 1 1320 680
WIRE 112 -160 -64 -160
WIRE 224 -160 176 -160
WIRE 528 -160 352 -160
WIRE 640 -160 592 -160
WIRE 944 -144 768 -144
WIRE 1056 -144 1008 -144
WIRE -160 -48 -208 -48
WIRE -64 -48 -64 -160
WIRE -64 -48 -80 -48
WIRE -48 -48 -64 -48
WIRE 48 -48 32 -48
WIRE 128 -48 48 -48
WIRE 224 -32 224 -160
WIRE 224 -32 192 -32
WIRE 256 -32 224 -32
WIRE 352 -32 352 -160
WIRE 352 -32 336 -32
WIRE 368 -32 352 -32
WIRE 464 -32 448 -32
WIRE 544 -32 464 -32
WIRE 128 -16 96 -16
WIRE 640 -16 640 -160
WIRE 640 -16 608 -16
WIRE 672 -16 640 -16
WIRE 768 -16 768 -144
WIRE 768 -16 752 -16
WIRE 784 -16 768 -16
WIRE 880 -16 864 -16
WIRE 960 -16 880 -16
WIRE 1264 -16 1264 -32
WIRE 1264 -16 1216 -16
WIRE 544 0 512 0
WIRE 1056 0 1056 -144
WIRE 1056 0 1024 0
WIRE 1216 0 1216 -16
WIRE 1264 0 1264 -16
WIRE -208 16 -208 -48
WIRE 48 16 48 -48
WIRE 960 16 928 16
WIRE 464 32 464 -32
WIRE 96 48 96 -16
WIRE 224 48 224 -32
WIRE 224 48 96 48
WIRE 880 48 880 -16
WIRE 512 64 512 0
WIRE 640 64 640 -16
WIRE 640 64 512 64
WIRE 928 80 928 16
WIRE 1056 80 1056 0
WIRE 1056 80 928 80
WIRE -208 112 -208 96
WIRE 48 112 48 80
WIRE 464 128 464 96
WIRE 880 144 880 112
FLAG 48 112 0
FLAG 464 128 0
FLAG -208 -48 vin
FLAG -208 112 0
FLAG 1216 0 0
FLAG 1264 -112 vcc
FLAG 576 16 vcc
FLAG 160 0 vcc
FLAG 576 -48 vdd
FLAG 160 -64 vdd
FLAG 1264 80 vdd
FLAG 880 144 0
FLAG 992 32 vcc
FLAG 992 -32 vdd
FLAG 1056 0 vout
SYMBOL res -64 -64 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName R1
SYMATTR Value {r1_s}
SYMBOL res 48 -64 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName R2
SYMATTR Value {r2_s}
SYMBOL cap 32 16 R0
SYMATTR InstName C1
SYMATTR Value {c1_s}
SYMBOL cap 176 -176 R90
WINDOW 0 0 32 VBottom 2
WINDOW 3 32 32 VTop 2
SYMATTR InstName C2
SYMATTR Value {c2_s}
SYMBOL res 352 -48 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName R3
SYMATTR Value {r3_s}
SYMBOL res 464 -48 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName {r4_s}
SYMATTR Value 4.7k
SYMBOL cap 448 32 R0
SYMATTR InstName C3
SYMATTR Value {c3_s}
SYMBOL cap 592 -176 R90
WINDOW 0 0 32 VBottom 2
WINDOW 3 32 32 VTop 2
SYMATTR InstName C4
SYMATTR Value {c4_s}
SYMBOL voltage -208 0 R0
WINDOW 123 24 124 Left 2
WINDOW 39 0 0 Left 0
SYMATTR InstName V1
SYMATTR Value ""
SYMATTR Value2 AC 1 0
SYMBOL Opamps\\\\UniversalOpamp 160 -32 M180
SYMATTR InstName U1
SYMBOL Opamps\\\\UniversalOpamp 576 -16 M180
SYMATTR InstName U2
SYMBOL voltage 1264 -128 R0
WINDOW 123 0 0 Left 0
WINDOW 39 0 0 Left 0
SYMATTR InstName V2
SYMATTR Value 15
SYMBOL voltage 1264 -16 R0
WINDOW 123 0 0 Left 0
WINDOW 39 0 0 Left 0
SYMATTR InstName V3
SYMATTR Value 15
SYMBOL res 768 -32 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName R5
SYMATTR Value {r5_s}
SYMBOL res 880 -32 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName R6
SYMATTR Value {r6_s}
SYMBOL cap 864 48 R0
SYMATTR InstName C5
SYMATTR Value {c5_s}
SYMBOL cap 1008 -160 R90
WINDOW 0 0 32 VBottom 2
WINDOW 3 32 32 VTop 2
SYMATTR InstName C6
SYMATTR Value {c6_s}
SYMBOL Opamps\\\\UniversalOpamp 992 0 M180
SYMATTR InstName U3
TEXT -242 152 Left 2 !.ac dec 1e3 1 {MAX_FREQ}"""

    with open(file=output_path, mode="w") as f:
        f.write(file_string)


if __name__ == "__main__":
    data_path = "best_result_e24.json"
    output_path = "../LTspiceSchematics/6th Order Sallen Key Lowpass Filter.asc"
    write_file(data_path=data_path, output_path=output_path)
