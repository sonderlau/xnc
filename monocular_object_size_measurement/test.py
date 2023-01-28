import numpy as np

IMAGE_LENGTH = 4000

IMAGE_WIDTH = 1824

PRECISION = np.double


def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """

    s = np.vstack([a1, a2, b1, b2])  # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])  # get first line
    l2 = np.cross(h[2], h[3])  # get second line
    x, y, z = np.cross(l1, l2)  # point of intersection
    # TODO: 平行线的处理
    # if z == 0:                          # lines are parallel
    #     return (float('inf'), float('inf'))
    return np.array([x / z, y / z], dtype=PRECISION)


def calculate(
    A: list, B: list, C: list, D: list, P_1: list, P_2: list, AC_real_size, BD_real_size
):
    """估计物体的大概长度

    Args:
        A (list): _description_
        B (list): _description_
        C (list): _description_
        D (list): _description_
        P_1 (list): _description_
        P_2 (list): _description_
        AC_real_size (_type_): _description_
        BD_real_size (_type_): _description_

    Returns:
        _type_: _description_
    """

    OA = np.array(A, dtype=PRECISION)
    OB = np.array(B, dtype=PRECISION)
    OC = np.array(C, dtype=PRECISION)
    OD = np.array(D, dtype=PRECISION)

    OM = get_intersect(OA, OC, OB, OD)

    # 灭点
    vp1 = get_intersect(OA, OB, OC, OD)
    vp2 = get_intersect(OA, OD, OB, OC)

    pricipal_point = np.array([IMAGE_LENGTH / 2, IMAGE_LENGTH / 2])

    u = np.sqrt(np.abs(np.dot(vp1 - pricipal_point, vp2 - pricipal_point)))

    OA = np.append(OA, [u])
    OB = np.append(OB, [u])
    OC = np.append(OC, [u])
    OD = np.append(OD, [u])
    OM = np.append(OM, [u])

    P1 = np.array(P_1, dtype=PRECISION)
    P2 = np.array(P_2, dtype=PRECISION)
    OP1 = np.append(P1, [u])
    OP2 = np.append(P2, [u])

    AM = np.linalg.norm(OA - OM)
    CM = np.linalg.norm(OC - OM)
    BM = np.linalg.norm(OB - OM)
    DM = np.linalg.norm(OD - OM)

    # AM \ CM
    lambda_1 = np.divide(AM, CM, dtype=PRECISION)

    # BM \ DM
    lambda_2 = np.divide(BM, DM, dtype=PRECISION)

    # hat lambda 1
    hat_lambda_1 = np.divide(
        AC_real_size, np.linalg.norm(lambda_1 * OC - OA), dtype=PRECISION
    )

    # hat lambda 2
    hat_lambda_2 = np.divide(
        BD_real_size, np.linalg.norm(lambda_2 * OD - OB), dtype=PRECISION
    )

    AC_real = hat_lambda_1 * (lambda_1 * OC - OA)
    BD_real = hat_lambda_2 * (lambda_2 * OD - OB)

    n = np.cross(AC_real, BD_real)

    # OA' = ^lambda_1 * OA
    OA_real = hat_lambda_1 * OA
    OB_real = hat_lambda_2 * OB

    OP1_real = OP1 * np.divide(np.dot(OB_real, n), np.dot(OP1, n))

    OP2_real = OP2 * np.divide(np.dot(OB_real, n), np.dot(OP2, n))

    P1P2 = OP1_real - OP2_real

    size = np.linalg.norm(P1P2)

    return size


d = np.sqrt(2, dtype=PRECISION) * 800


size = calculate(
    A=[1506, 959],
    B=[1302, 382],
    C=[2158, 137],
    D=[2575, 612],
    AC_real_size=d,
    BD_real_size=d,
    P_1=[1987, 345],
    P_2=[2017, 314],
)

print(size)
