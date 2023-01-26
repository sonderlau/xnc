import numpy as np

# 焦距
f = 4.76

ratio = np.divide(1365.18, 297, dtype= np.float64)

u = f * ratio

# AM \ CM
lambda_1 = np.divide(659.49, 949.82, dtype=np.float64)

# BM \ DM
lambda_2 = np.divide(1094.97, 897.61, dtype=np.float64)

OA = np.array([1081, 855, u], dtype=np.float64)
OB = np.array([607, 1661, u], dtype=np.float64)
OC = np.array([2397, 1771, u], dtype=np.float64)
OD = np.array([2439, 871, u], dtype=np.float64)
OP1 = np.array([901, 805, u], dtype=np.float64)
OP2 = np.array([2919, 787, u], dtype=np.float64)

# hat lambda 1
hat_lambda_1 = np.divide(
    363.74304117055,
    np.linalg.norm(lambda_1 * OC - OA),
    dtype= np.float64
)

# hat lambda 2
hat_lambda_2 = np.divide(
    363.74304117055,
    np.linalg.norm(lambda_2 * OD - OB),
    dtype= np.float64
)



AC_real = hat_lambda_1 * (lambda_1 * OC - OA)
BD_real = hat_lambda_2 * (lambda_2 * OD - OB) 

n = np.cross(AC_real, BD_real)



OP1_real = OP1 * np.divide(
    np.dot(hat_lambda_1 * OA, n),
    np.dot(OP1, n),
    dtype= np.float64
)

OP2_real = OP2 * np.divide(
    np.dot(hat_lambda_1 * OA, n),
    np.dot(OP2, n),
    dtype= np.float64
)

P1P2 = OP1_real - OP2_real

size = np.linalg.norm(P1P2)

## Actual 440
print(size)