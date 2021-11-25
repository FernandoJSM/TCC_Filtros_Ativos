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

    r1, r2, r3, r4, c1, c2, c3, c4 = (
            utils.to_si(value=v) for v in component_raw_values
        )

    file_string = \
f"""Version 4
SHEET 1 1320 680
WIRE 112 -160 -64 -160
WIRE 224 -160 176 -160
WIRE 528 -160 352 -160
WIRE 640 -160 592 -160
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
WIRE 816 -32 816 -48
WIRE 816 -32 768 -32
WIRE 128 -16 96 -16
WIRE 640 -16 640 -160
WIRE 640 -16 608 -16
WIRE 672 -16 640 -16
WIRE 768 -16 768 -32
WIRE 816 -16 816 -32
WIRE 544 0 512 0
WIRE -208 16 -208 -48
WIRE 48 16 48 -48
WIRE 464 32 464 -32
WIRE 96 48 96 -16
WIRE 224 48 224 -32
WIRE 224 48 96 48
WIRE 512 64 512 0
WIRE 640 64 640 -16
WIRE 640 64 512 64
WIRE -208 112 -208 96
WIRE 48 112 48 80
WIRE 464 128 464 96
FLAG 48 112 0
FLAG 464 128 0
FLAG -208 -48 vin
FLAG -208 112 0
FLAG 768 -16 0
FLAG 816 -128 vcc
FLAG 576 16 vcc
FLAG 160 0 vcc
FLAG 576 -48 vdd
FLAG 160 -64 vdd
FLAG 816 64 vdd
FLAG 672 -16 vout
SYMBOL res -64 -64 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName R1
SYMATTR Value {r1}
SYMBOL res 48 -64 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName R2
SYMATTR Value {r2}
SYMBOL cap 32 16 R0
SYMATTR InstName C1
SYMATTR Value {c1}
SYMBOL cap 176 -176 R90
WINDOW 0 0 32 VBottom 2
WINDOW 3 32 32 VTop 2
SYMATTR InstName C2
SYMATTR Value {c2}
SYMBOL res 352 -48 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName R3
SYMATTR Value {r3}
SYMBOL res 464 -48 R90
WINDOW 0 0 56 VBottom 2
WINDOW 3 32 56 VTop 2
SYMATTR InstName R4
SYMATTR Value {r4}
SYMBOL cap 448 32 R0
SYMATTR InstName C3
SYMATTR Value {c3}
SYMBOL cap 592 -176 R90
WINDOW 0 0 32 VBottom 2
WINDOW 3 32 32 VTop 2
SYMATTR InstName C4
SYMATTR Value {c4}
SYMBOL voltage -208 0 R0
WINDOW 123 24 124 Left 2
WINDOW 39 0 0 Left 0
SYMATTR Value2 AC 1 0
SYMATTR InstName V1
SYMATTR Value ""
SYMBOL Opamps\\UniversalOpamp 160 -32 M180
SYMATTR InstName U1
SYMBOL Opamps\\UniversalOpamp 576 -16 M180
SYMATTR InstName U2
SYMBOL voltage 816 -144 R0
WINDOW 123 0 0 Left 0
WINDOW 39 0 0 Left 0
SYMATTR InstName V2
SYMATTR Value 15
SYMBOL voltage 816 -32 R0
WINDOW 123 0 0 Left 0
WINDOW 39 0 0 Left 0
SYMATTR InstName V3
SYMATTR Value 15
TEXT -240 152 Left 2 !.ac dec 1e3 1 {MAX_FREQ}"""

    with open(file=output_path, mode="w") as f:
        f.write(file_string)


if __name__ == "__main__":
    data_path = "../data/best_result_e12.json"
    output_path = "../LTspiceSchematics/4th Order Sallen Key Lowpass Filter.asc"
    write_file(data_path=data_path, output_path=output_path)
