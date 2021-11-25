import numpy as np


def resistors(ai, bi, ca, cb):
    fc = 5000
    den = 4*np.pi*fc*ca*cb
    sq_root = np.sqrt((ai**2)*(cb**2)-4*bi*ca*cb)
    ra = ((ai*cb) + sq_root) / den
    rb = ((ai * cb) - sq_root) / den

    return ra, rb

# Primeiro estágio
a1 = 1.8478
b1 = 1

# O primeiro ponto é que c2 >= 4 c1 / a1^2
c1 = 12e-9   # 12nF
c2 = 82e-9   # 56nF

print("c2 >= 4 c1 / a1^2: " + str(c2 >= 4*c1 / (a1 ** 2)))

r1, r2 = resistors(a1, b1, c1, c2)

print(f"{r1=}\t{r2=}\t{c1=}\t{c2=}")

fc1 = (1/np.sqrt(r1*r2*c1*c2))/(2*np.pi)
print(f"{fc1=}Hz")

# Segundo estágio
a2 = 0.7654
b2 = 1

c3 = 5.6e-9   # 5.6nF
c4 = 100e-9   # 100nF

print("c4 >= 4 c3 / a2^2: " + str(c4 >= 4*c3 / (a2 ** 2)))

r3, r4 = resistors(a2, b2, c3, c4)

print(f"{r3=}\t{r4=}\t{c3=}\t{c4=}")

fc2 = (1/np.sqrt(r3*r4*c3*c4))/(2*np.pi)
print(f"{fc2=}")

print("Com componentes comerciais:")

fc1 = (1/np.sqrt(4700*220*c1*c2))/(2*np.pi)
fc2 = (1/np.sqrt(3900*470*c3*c4))/(2*np.pi)
print(f"{fc1=}\t{fc2=}")
