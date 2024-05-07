# main.py

class QRCodeGenerator:
    # Constants
    NUMERIC_CHARSET = set('0123456789')

    ALPHANUMERIC_CHARSET = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:')

    # Code info for each encoding mode
    ENCODING_MODE_INDICATOR = {
        'numeric': '0001',
        'alphanumeric': '0010',
        'byte': '0100',
    }

    # Data capacity for all possible QR Codes
    # L | numeric, alphanumeric, byte, max_bits -> data capacity
    # M | numeric, alphanumeric, byte, max_bits -> data capacity
    # Q | numeric, alphanumeric, byte, max_bits -> data capacity
    # H | numeric, alphanumeric, byte, max_bits -> data capacity
    CAPACITIES_TABLE = {
        1: {
            'L': {'numeric': 41, 'alphanumeric': 25, 'byte': 17, 'max_bits': 152},
            'M': {'numeric': 34, 'alphanumeric': 20, 'byte': 14, 'max_bits': 128},
            'Q': {'numeric': 27, 'alphanumeric': 16, 'byte': 11, 'max_bits': 104},
            'H': {'numeric': 17, 'alphanumeric': 10, 'byte': 7, 'max_bits': 72},
        },
        2: {
            'L': {'numeric': 77, 'alphanumeric': 47, 'byte': 32, 'max_bits': 272},
            'M': {'numeric': 63, 'alphanumeric': 38, 'byte': 26, 'max_bits': 224},
            'Q': {'numeric': 48, 'alphanumeric': 29, 'byte': 20, 'max_bits': 176},
            'H': {'numeric': 34, 'alphanumeric': 20, 'byte': 14, 'max_bits': 128},
        },
        3: {
            'L': {'numeric': 127, 'alphanumeric': 77, 'byte': 53, 'max_bits': 440},
            'M': {'numeric': 101, 'alphanumeric': 61, 'byte': 42, 'max_bits': 352},
            'Q': {'numeric': 77, 'alphanumeric': 47, 'byte': 32, 'max_bits': 272},
            'H': {'numeric': 58, 'alphanumeric': 35, 'byte': 24, 'max_bits': 208},
        },
        4: {
            'L': {'numeric': 187, 'alphanumeric': 114, 'byte': 78, 'max_bits': 640},
            'M': {'numeric': 149, 'alphanumeric': 90, 'byte': 62, 'max_bits': 512},
            'Q': {'numeric': 111, 'alphanumeric': 67, 'byte': 46, 'max_bits': 384},
            'H': {'numeric': 82, 'alphanumeric': 50, 'byte': 34, 'max_bits': 288},
        },
        5: {
            'L': {'numeric': 255, 'alphanumeric': 154, 'byte': 106, 'max_bits': 864},
            'M': {'numeric': 202, 'alphanumeric': 122, 'byte': 84, 'max_bits': 688},
            'Q': {'numeric': 144, 'alphanumeric': 87, 'byte': 60, 'max_bits': 496},
            'H': {'numeric': 106, 'alphanumeric': 64, 'byte': 44, 'max_bits': 368},
        },
        6: {
            'L': {'numeric': 322, 'alphanumeric': 195, 'byte': 134, 'max_bits': 1088},
            'M': {'numeric': 255, 'alphanumeric': 154, 'byte': 106, 'max_bits': 864},
            'Q': {'numeric': 178, 'alphanumeric': 108, 'byte': 74, 'max_bits': 608},
            'H': {'numeric': 139, 'alphanumeric': 84, 'byte': 58, 'max_bits': 480},
        },
        7: {
            'L': {'numeric': 370, 'alphanumeric': 224, 'byte': 154, 'max_bits': 1248},
            'M': {'numeric': 293, 'alphanumeric': 178, 'byte': 122, 'max_bits': 992},
            'Q': {'numeric': 207, 'alphanumeric': 125, 'byte': 86, 'max_bits': 704},
            'H': {'numeric': 154, 'alphanumeric': 93, 'byte': 64, 'max_bits': 528},
        },
        8: {
            'L': {'numeric': 461, 'alphanumeric': 279, 'byte': 192, 'max_bits': 1552},
            'M': {'numeric': 365, 'alphanumeric': 221, 'byte': 152, 'max_bits': 1232},
            'Q': {'numeric': 259, 'alphanumeric': 157, 'byte': 108, 'max_bits': 880},
            'H': {'numeric': 202, 'alphanumeric': 122, 'byte': 84, 'max_bits': 688},
        },
        9: {
            'L': {'numeric': 552, 'alphanumeric': 335, 'byte': 230, 'max_bits': 1856},
            'M': {'numeric': 432, 'alphanumeric': 262, 'byte': 180, 'max_bits': 1456},
            'Q': {'numeric': 312, 'alphanumeric': 189, 'byte': 130, 'max_bits': 1056},
            'H': {'numeric': 235, 'alphanumeric': 143, 'byte': 98, 'max_bits': 800},
        },
        10: {
            'L': {'numeric': 652, 'alphanumeric': 395, 'byte': 271, 'max_bits': 2192},
            'M': {'numeric': 513, 'alphanumeric': 311, 'byte': 213, 'max_bits': 1728},
            'Q': {'numeric': 364, 'alphanumeric': 221, 'byte': 151, 'max_bits': 1232},
            'H': {'numeric': 288, 'alphanumeric': 174, 'byte': 119, 'max_bits': 976},
        },
        11: {
            'L': {'numeric': 772, 'alphanumeric': 468, 'byte': 321, 'max_bits': 2592},
            'M': {'numeric': 604, 'alphanumeric': 366, 'byte': 251, 'max_bits': 2032},
            'Q': {'numeric': 427, 'alphanumeric': 259, 'byte': 177, 'max_bits': 1440},
            'H': {'numeric': 331, 'alphanumeric': 200, 'byte': 137, 'max_bits': 1120},
        },
        12: {
            'L': {'numeric': 883, 'alphanumeric': 535, 'byte': 367, 'max_bits': 2960},
            'M': {'numeric': 691, 'alphanumeric': 419, 'byte': 287, 'max_bits': 2320},
            'Q': {'numeric': 489, 'alphanumeric': 296, 'byte': 203, 'max_bits': 1648},
            'H': {'numeric': 374, 'alphanumeric': 227, 'byte': 155, 'max_bits': 1264},
        },
        13: {
            'L': {'numeric': 1022, 'alphanumeric': 619, 'byte': 425, 'max_bits': 3424},
            'M': {'numeric': 796, 'alphanumeric': 483, 'byte': 331, 'max_bits': 2672},
            'Q': {'numeric': 580, 'alphanumeric': 352, 'byte': 241, 'max_bits': 1952},
            'H': {'numeric': 427, 'alphanumeric': 259, 'byte': 177, 'max_bits': 1440},
        },
        14: {
            'L': {'numeric': 1101, 'alphanumeric': 667, 'byte': 458, 'max_bits': 3688},
            'M': {'numeric': 871, 'alphanumeric': 528, 'byte': 362, 'max_bits': 2920},
            'Q': {'numeric': 621, 'alphanumeric': 376, 'byte': 258, 'max_bits': 2088},
            'H': {'numeric': 468, 'alphanumeric': 283, 'byte': 194, 'max_bits': 1576},
        },
        15: {
            'L': {'numeric': 1250, 'alphanumeric': 758, 'byte': 520, 'max_bits': 4184},
            'M': {'numeric': 991, 'alphanumeric': 600, 'byte': 412, 'max_bits': 3320},
            'Q': {'numeric': 703, 'alphanumeric': 426, 'byte': 292, 'max_bits': 2360},
            'H': {'numeric': 530, 'alphanumeric': 321, 'byte': 220, 'max_bits': 1784},
        },
        16: {
            'L': {'numeric': 1408, 'alphanumeric': 854, 'byte': 586, 'max_bits': 4712},
            'M': {'numeric': 1082, 'alphanumeric': 656, 'byte': 450, 'max_bits': 3624},
            'Q': {'numeric': 775, 'alphanumeric': 470, 'byte': 322, 'max_bits': 2600},
            'H': {'numeric': 602, 'alphanumeric': 365, 'byte': 250, 'max_bits': 2024},
        },
        17: {
            'L': {'numeric': 1548, 'alphanumeric': 938, 'byte': 644, 'max_bits': 5176},
            'M': {'numeric': 1212, 'alphanumeric': 734, 'byte': 504, 'max_bits': 4056},
            'Q': {'numeric': 876, 'alphanumeric': 531, 'byte': 364, 'max_bits': 2936},
            'H': {'numeric': 674, 'alphanumeric': 408, 'byte': 280, 'max_bits': 2264},
        },
        18: {
            'L': {'numeric': 1725, 'alphanumeric': 1046, 'byte': 718, 'max_bits': 5768},
            'M': {'numeric': 1346, 'alphanumeric': 816, 'byte': 560, 'max_bits': 4504},
            'Q': {'numeric': 948, 'alphanumeric': 574, 'byte': 394, 'max_bits': 3176},
            'H': {'numeric': 746, 'alphanumeric': 452, 'byte': 310, 'max_bits': 2504},
        },
        19: {
            'L': {'numeric': 1903, 'alphanumeric': 1153, 'byte': 792, 'max_bits': 6360},
            'M': {'numeric': 1500, 'alphanumeric': 909, 'byte': 624, 'max_bits': 5016},
            'Q': {'numeric': 1063, 'alphanumeric': 644, 'byte': 442, 'max_bits': 3560},
            'H': {'numeric': 813, 'alphanumeric': 493, 'byte': 338, 'max_bits': 2728},
        },
        20: {
            'L': {'numeric': 2061, 'alphanumeric': 1249, 'byte': 858, 'max_bits': 6888},
            'M': {'numeric': 1600, 'alphanumeric': 970, 'byte': 666, 'max_bits': 5352},
            'Q': {'numeric': 1159, 'alphanumeric': 702, 'byte': 482, 'max_bits': 3880},
            'H': {'numeric': 919, 'alphanumeric': 557, 'byte': 382, 'max_bits': 3080},
        },
        21: {
            'L': {'numeric': 2232, 'alphanumeric': 1352, 'byte': 929, 'max_bits': 7456},
            'M': {'numeric': 1708, 'alphanumeric': 1035, 'byte': 711, 'max_bits': 5712},
            'Q': {'numeric': 1224, 'alphanumeric': 742, 'byte': 509, 'max_bits': 4096},
            'H': {'numeric': 969, 'alphanumeric': 587, 'byte': 403, 'max_bits': 3248},
        },
        22: {
            'L': {'numeric': 2409, 'alphanumeric': 1460, 'byte': 1003, 'max_bits': 8048},
            'M': {'numeric': 1872, 'alphanumeric': 1134, 'byte': 779, 'max_bits': 6256},
            'Q': {'numeric': 1358, 'alphanumeric': 823, 'byte': 565, 'max_bits': 4544},
            'H': {'numeric': 1056, 'alphanumeric': 640, 'byte': 439, 'max_bits': 3536},
        },
        23: {
            'L': {'numeric': 2620, 'alphanumeric': 1588, 'byte': 1091, 'max_bits': 8752},
            'M': {'numeric': 2059, 'alphanumeric': 1248, 'byte': 857, 'max_bits': 6880},
            'Q': {'numeric': 1468, 'alphanumeric': 890, 'byte': 611, 'max_bits': 4912},
            'H': {'numeric': 1108, 'alphanumeric': 672, 'byte': 461, 'max_bits': 3712},
        },
        24: {
            'L': {'numeric': 2812, 'alphanumeric': 1704, 'byte': 1171, 'max_bits': 9392},
            'M': {'numeric': 2188, 'alphanumeric': 1326, 'byte': 911, 'max_bits': 7312},
            'Q': {'numeric': 1588, 'alphanumeric': 963, 'byte': 661, 'max_bits': 5312},
            'H': {'numeric': 1228, 'alphanumeric': 744, 'byte': 511, 'max_bits': 4112},
        },
        25: {
            'L': {'numeric': 3057, 'alphanumeric': 1853, 'byte': 1273, 'max_bits': 10208},
            'M': {'numeric': 2395, 'alphanumeric': 1451, 'byte': 997, 'max_bits': 8000},
            'Q': {'numeric': 1718, 'alphanumeric': 1041, 'byte': 715, 'max_bits': 5744},
            'H': {'numeric': 1286, 'alphanumeric': 779, 'byte': 535, 'max_bits': 4304},
        },
        26: {
            'L': {'numeric': 3283, 'alphanumeric': 1990, 'byte': 1367, 'max_bits': 10960},
            'M': {'numeric': 2544, 'alphanumeric': 1542, 'byte': 1059, 'max_bits': 8496},
            'Q': {'numeric': 1804, 'alphanumeric': 1094, 'byte': 751, 'max_bits': 6032},
            'H': {'numeric': 1425, 'alphanumeric': 864, 'byte': 593, 'max_bits': 4768},
        },
        27: {
            'L': {'numeric': 3514, 'alphanumeric': 2132, 'byte': 1465, 'max_bits': 11744},
            'M': {'numeric': 2701, 'alphanumeric': 1637, 'byte': 1125, 'max_bits': 9024},
            'Q': {'numeric': 1933, 'alphanumeric': 1172, 'byte': 805, 'max_bits': 6464},
            'H': {'numeric': 1501, 'alphanumeric': 910, 'byte': 625, 'max_bits': 5024},
        },
        28: {
            'L': {'numeric': 3669, 'alphanumeric': 2223, 'byte': 1528, 'max_bits': 12248},
            'M': {'numeric': 2857, 'alphanumeric': 1732, 'byte': 1190, 'max_bits': 9544},
            'Q': {'numeric': 2085, 'alphanumeric': 1263, 'byte': 868, 'max_bits': 6968},
            'H': {'numeric': 1581, 'alphanumeric': 958, 'byte': 658, 'max_bits': 5288},
        },
        29: {
            'L': {'numeric': 3909, 'alphanumeric': 2369, 'byte': 1628, 'max_bits': 13048},
            'M': {'numeric': 3035, 'alphanumeric': 1839, 'byte': 1264, 'max_bits': 10136},
            'Q': {'numeric': 2181, 'alphanumeric': 1322, 'byte': 908, 'max_bits': 7288},
            'H': {'numeric': 1677, 'alphanumeric': 1016, 'byte': 698, 'max_bits': 5608},
        },
        30: {
            'L': {'numeric': 4158, 'alphanumeric': 2520, 'byte': 1732, 'max_bits': 13880},
            'M': {'numeric': 3289, 'alphanumeric': 1994, 'byte': 1370, 'max_bits': 10984},
            'Q': {'numeric': 2358, 'alphanumeric': 1429, 'byte': 982, 'max_bits': 7880},
            'H': {'numeric': 1782, 'alphanumeric': 1080, 'byte': 742, 'max_bits': 5960},
        },
        31: {
            'L': {'numeric': 4417, 'alphanumeric': 2677, 'byte': 1840, 'max_bits': 14744},
            'M': {'numeric': 3486, 'alphanumeric': 2113, 'byte': 1452, 'max_bits': 11640},
            'Q': {'numeric': 2473, 'alphanumeric': 1499, 'byte': 1030, 'max_bits': 8264},
            'H': {'numeric': 1897, 'alphanumeric': 1150, 'byte': 790, 'max_bits': 6344},
        },
        32: {
            'L': {'numeric': 4686, 'alphanumeric': 2840, 'byte': 1952, 'max_bits': 15640},
            'M': {'numeric': 3693, 'alphanumeric': 2238, 'byte': 1538, 'max_bits': 12328},
            'Q': {'numeric': 2670, 'alphanumeric': 1618, 'byte': 1112, 'max_bits': 8920},
            'H': {'numeric': 2022, 'alphanumeric': 1226, 'byte': 842, 'max_bits': 6760},
        },
        33: {
            'L': {'numeric': 4965, 'alphanumeric': 3009, 'byte': 2068, 'max_bits': 16568},
            'M': {'numeric': 3909, 'alphanumeric': 2369, 'byte': 1628, 'max_bits': 13048},
            'Q': {'numeric': 2805, 'alphanumeric': 1700, 'byte': 1168, 'max_bits': 9368},
            'H': {'numeric': 2157, 'alphanumeric': 1307, 'byte': 898, 'max_bits': 7208},
        },
        34: {
            'L': {'numeric': 5253, 'alphanumeric': 3183, 'byte': 2188, 'max_bits': 17528},
            'M': {'numeric': 4134, 'alphanumeric': 2506, 'byte': 1722, 'max_bits': 13800},
            'Q': {'numeric': 2949, 'alphanumeric': 1787, 'byte': 1228, 'max_bits': 9848},
            'H': {'numeric': 2301, 'alphanumeric': 1394, 'byte': 958, 'max_bits': 7688},
        },
        35: {
            'L': {'numeric': 5529, 'alphanumeric': 3351, 'byte': 2303, 'max_bits': 18448},
            'M': {'numeric': 4343, 'alphanumeric': 2632, 'byte': 1809, 'max_bits': 14496},
            'Q': {'numeric': 3081, 'alphanumeric': 1867, 'byte': 1283, 'max_bits': 10288},
            'H': {'numeric': 2361, 'alphanumeric': 1431, 'byte': 983, 'max_bits': 7888},
        },
        36: {
            'L': {'numeric': 5836, 'alphanumeric': 3537, 'byte': 2431, 'max_bits': 19472},
            'M': {'numeric': 4588, 'alphanumeric': 2780, 'byte': 1911, 'max_bits': 15312},
            'Q': {'numeric': 3244, 'alphanumeric': 1966, 'byte': 1351, 'max_bits': 10832},
            'H': {'numeric': 2524, 'alphanumeric': 1530, 'byte': 1051, 'max_bits': 8432},
        },
        37: {
            'L': {'numeric': 6153, 'alphanumeric': 3729, 'byte': 2563, 'max_bits': 20528},
            'M': {'numeric': 4775, 'alphanumeric': 2894, 'byte': 1989, 'max_bits': 15936},
            'Q': {'numeric': 3417, 'alphanumeric': 2071, 'byte': 1423, 'max_bits': 11408},
            'H': {'numeric': 2625, 'alphanumeric': 1591, 'byte': 1093, 'max_bits': 8768},
        },
        38: {
            'L': {'numeric': 6479, 'alphanumeric': 3927, 'byte': 2699, 'max_bits': 21616},
            'M': {'numeric': 5039, 'alphanumeric': 3054, 'byte': 2099, 'max_bits': 16816},
            'Q': {'numeric': 3599, 'alphanumeric': 2181, 'byte': 1499, 'max_bits': 12016},
            'H': {'numeric': 2735, 'alphanumeric': 1658, 'byte': 1139, 'max_bits': 9136},
        },
        39: {
            'L': {'numeric': 6743, 'alphanumeric': 4087, 'byte': 2809, 'max_bits': 22496},
            'M': {'numeric': 5313, 'alphanumeric': 3220, 'byte': 2213, 'max_bits': 17728},
            'Q': {'numeric': 3791, 'alphanumeric': 2298, 'byte': 1579, 'max_bits': 12656},
            'H': {'numeric': 2927, 'alphanumeric': 1774, 'byte': 1219, 'max_bits': 9776},
        },
        40: {
            'L': {'numeric': 7089, 'alphanumeric': 4296, 'byte': 2953, 'max_bits': 23648},
            'M': {'numeric': 5596, 'alphanumeric': 3391, 'byte': 2331, 'max_bits': 18672},
            'Q': {'numeric': 3993, 'alphanumeric': 2420, 'byte': 1663, 'max_bits': 13328},
            'H': {'numeric': 3057, 'alphanumeric': 1852, 'byte': 1273, 'max_bits': 10208},
        },
    }

    # Error Correction Code Words and Block Information
    # 0 | EC Code Words Per Block
    # 1 | Block 1 Count
    # 2 | Block 1 Data Code Words
    # 3 | Block 2 Count
    # 4 | Block 2 Data Code Words
    ECCWBI = {
        1: {
            'L': [7, 1, 19, 0, 0],
            'M': [10, 1, 16, 0, 0],
            'Q': [13, 1, 13, 0, 0],
            'H': [17, 1, 9, 0, 0],
        },
        2: {
            'L': [10, 1, 34, 0, 0],
            'M': [16, 1, 28, 0, 0],
            'Q': [22, 1, 22, 0, 0],
            'H': [28, 1, 16, 0, 0],
        },
        3: {
            'L': [15, 1, 55, 0, 0],
            'M': [26, 1, 44, 0, 0],
            'Q': [18, 2, 17, 0, 0],
            'H': [22, 2, 13, 0, 0],
        },
        4: {
            'L': [20, 1, 80, 0, 0],
            'M': [18, 2, 32, 0, 0],
            'Q': [26, 2, 24, 0, 0],
            'H': [16, 4, 9, 0, 0],
        },
        5: {
            'L': [26, 1, 108, 0, 0],
            'M': [24, 2, 43, 0, 0],
            'Q': [18, 2, 15, 2, 16],
            'H': [22, 2, 11, 2, 12],
        },
        6: {
            'L': [18, 2, 68, 0, 0],
            'M': [16, 4, 27, 0, 0],
            'Q': [24, 4, 19, 0, 0],
            'H': [28, 4, 15, 0, 0],
        },
        7: {
            'L': [20, 2, 78, 0, 0],
            'M': [18, 4, 31, 0, 0],
            'Q': [18, 2, 14, 4, 15],
            'H': [26, 4, 13, 1, 14],
        },
        8: {
            'L': [24, 2, 97, 0, 0],
            'M': [22, 2, 38, 2, 39],
            'Q': [22, 4, 18, 2, 19],
            'H': [26, 4, 14, 2, 15],
        },
        9: {
            'L': [30, 2, 116, 0, 0],
            'M': [22, 3, 36, 2, 37],
            'Q': [20, 4, 16, 4, 17],
            'H': [24, 4, 12, 4, 13],
        },
        10: {
            'L': [18, 2, 68, 2, 69],
            'M': [26, 4, 43, 1, 44],
            'Q': [24, 6, 19, 2, 20],
            'H': [28, 6, 15, 2, 16],
        },
        11: {
            'L': [20, 4, 81, 0, 0],
            'M': [30, 1, 50, 4, 51],
            'Q': [28, 4, 22, 4, 23],
            'H': [24, 3, 12, 8, 13],
        },
        12: {
            'L': [24, 2, 92, 2, 93],
            'M': [22, 6, 36, 2, 37],
            'Q': [26, 4, 20, 6, 21],
            'H': [28, 7, 14, 4, 15],
        },
        13: {
            'L': [26, 4, 107, 0, 0],
            'M': [22, 8, 37, 1, 38],
            'Q': [24, 8, 20, 4, 21],
            'H': [22, 12, 11, 4, 12],
        },
        14: {
            'L': [30, 3, 115, 1, 116],
            'M': [24, 4, 40, 5, 41],
            'Q': [20, 11, 16, 5, 17],
            'H': [24, 11, 12, 5, 13],
        },
        15: {
            'L': [22, 5, 87, 1, 88],
            'M': [24, 5, 41, 5, 42],
            'Q': [30, 5, 24, 7, 25],
            'H': [24, 11, 12, 7, 13],
        },
        16: {
            'L': [24, 5, 98, 1, 99],
            'M': [28, 7, 45, 3, 46],
            'Q': [24, 15, 19, 2, 20],
            'H': [30, 3, 15, 13, 16],
        },
        17: {
            'L': [28, 1, 107, 5, 108],
            'M': [28, 10, 46, 1, 47],
            'Q': [28, 1, 22, 15, 23],
            'H': [28, 2, 14, 17, 15],
        },
        18: {
            'L': [30, 5, 120, 1, 121],
            'M': [26, 9, 43, 4, 44],
            'Q': [28, 17, 22, 1, 23],
            'H': [28, 2, 14, 19, 15],
        },
        19: {
            'L': [28, 3, 113, 4, 114],
            'M': [26, 3, 44, 11, 45],
            'Q': [26, 17, 21, 4, 22],
            'H': [26, 9, 13, 16, 14],
        },
        20: {
            'L': [28, 3, 107, 5, 108],
            'M': [26, 3, 41, 13, 42],
            'Q': [30, 15, 24, 5, 25],
            'H': [28, 15, 15, 10, 16],
        },
        21: {
            'L': [28, 4, 116, 4, 117],
            'M': [26, 17, 42, 0, 0],
            'Q': [28, 17, 22, 6, 23],
            'H': [30, 19, 16, 6, 17],
        },
        22: {
            'L': [28, 2, 111, 7, 112],
            'M': [28, 17, 46, 0, 0],
            'Q': [30, 7, 24, 16, 25],
            'H': [24, 34, 13, 0, 0],
        },
        23: {
            'L': [30, 4, 121, 5, 122],
            'M': [28, 4, 47, 14, 48],
            'Q': [30, 11, 24, 14, 25],
            'H': [30, 16, 15, 14, 16],
        },
        24: {
            'L': [30, 6, 117, 4, 118],
            'M': [28, 6, 45, 14, 46],
            'Q': [30, 11, 24, 16, 25],
            'H': [30, 30, 16, 2, 17],
        },
        25: {
            'L': [26, 8, 106, 4, 107],
            'M': [28, 8, 47, 13, 48],
            'Q': [30, 7, 24, 22, 25],
            'H': [30, 22, 15, 13, 16],
        },
        26: {
            'L': [28, 10, 114, 2, 115],
            'M': [28, 19, 46, 4, 47],
            'Q': [28, 28, 22, 6, 23],
            'H': [30, 33, 16, 4, 17],
        },
        27: {
            'L': [30, 8, 122, 4, 123],
            'M': [28, 22, 45, 3, 46],
            'Q': [30, 8, 23, 26, 24],
            'H': [30, 12, 15, 28, 16],
        },
        28: {
            'L': [30, 3, 117, 10, 118],
            'M': [28, 3, 45, 23, 46],
            'Q': [30, 4, 24, 31, 25],
            'H': [30, 11, 15, 31, 16],
        },
        29: {
            'L': [30, 7, 116, 7, 117],
            'M': [28, 21, 45, 7, 46],
            'Q': [30, 1, 23, 37, 24],
            'H': [30, 19, 15, 26, 16],
        },
        30: {
            'L': [30, 5, 115, 10, 116],
            'M': [28, 19, 47, 10, 48],
            'Q': [30, 15, 24, 25, 25],
            'H': [30, 23, 15, 25, 16],
        },
        31: {
            'L': [30, 13, 115, 3, 116],
            'M': [28, 2, 46, 29, 47],
            'Q': [30, 42, 24, 1, 25],
            'H': [30, 23, 15, 28, 16],
        },
        32: {
            'L': [30, 17, 115, 0, 0],
            'M': [28, 10, 46, 23, 47],
            'Q': [30, 10, 24, 35, 25],
            'H': [30, 19, 15, 35, 16],
        },
        33: {
            'L': [30, 17, 115, 1, 116],
            'M': [28, 14, 46, 21, 47],
            'Q': [30, 29, 24, 19, 25],
            'H': [30, 11, 15, 46, 16],
        },
        34: {
            'L': [30, 13, 115, 6, 116],
            'M': [28, 14, 46, 23, 47],
            'Q': [30, 44, 24, 7, 25],
            'H': [30, 59, 16, 1, 17],
        },
        35: {
            'L': [30, 12, 121, 7, 122],
            'M': [28, 12, 47, 26, 48],
            'Q': [30, 39, 24, 14, 25],
            'H': [30, 22, 15, 41, 16],
        },
        36: {
            'L': [30, 6, 121, 14, 122],
            'M': [28, 6, 47, 34, 48],
            'Q': [30, 46, 24, 10, 25],
            'H': [30, 2, 15, 64, 16],
        },
        37: {
            'L': [30, 17, 122, 4, 123],
            'M': [28, 29, 46, 14, 47],
            'Q': [30, 49, 24, 10, 25],
            'H': [30, 24, 15, 46, 16],
        },
        38: {
            'L': [30, 4, 122, 18, 123],
            'M': [28, 13, 46, 32, 47],
            'Q': [30, 48, 24, 14, 25],
            'H': [30, 42, 15, 32, 16],
        },
        39: {
            'L': [30, 20, 117, 4, 118],
            'M': [28, 40, 47, 7, 48],
            'Q': [30, 43, 24, 22, 25],
            'H': [30, 10, 15, 67, 16],
        },
        40: {
            'L': [30, 19, 118, 6, 119],
            'M': [28, 18, 47, 31, 48],
            'Q': [30, 34, 24, 34, 25],
            'H': [30, 20, 15, 61, 16],
        },
    }

    # AntiLog and values used in GF(256) arithmetic
    GALOIS_ANTILOG = [
        1,
        2,
        4,
        8,
        16,
        32,
        64,
        128,
        29,
        58,
        116,
        232,
        205,
        135,
        19,
        38,
        76,
        152,
        45,
        90,
        180,
        117,
        234,
        201,
        143,
        3,
        6,
        12,
        24,
        48,
        96,
        192,
        157,
        39,
        78,
        156,
        37,
        74,
        148,
        53,
        106,
        212,
        181,
        119,
        238,
        193,
        159,
        35,
        70,
        140,
        5,
        10,
        20,
        40,
        80,
        160,
        93,
        186,
        105,
        210,
        185,
        111,
        222,
        161,
        95,
        190,
        97,
        194,
        153,
        47,
        94,
        188,
        101,
        202,
        137,
        15,
        30,
        60,
        120,
        240,
        253,
        231,
        211,
        187,
        107,
        214,
        177,
        127,
        254,
        225,
        223,
        163,
        91,
        182,
        113,
        226,
        217,
        175,
        67,
        134,
        17,
        34,
        68,
        136,
        13,
        26,
        52,
        104,
        208,
        189,
        103,
        206,
        129,
        31,
        62,
        124,
        248,
        237,
        199,
        147,
        59,
        118,
        236,
        197,
        151,
        51,
        102,
        204,
        133,
        23,
        46,
        92,
        184,
        109,
        218,
        169,
        79,
        158,
        33,
        66,
        132,
        21,
        42,
        84,
        168,
        77,
        154,
        41,
        82,
        164,
        85,
        170,
        73,
        146,
        57,
        114,
        228,
        213,
        183,
        115,
        230,
        209,
        191,
        99,
        198,
        145,
        63,
        126,
        252,
        229,
        215,
        179,
        123,
        246,
        241,
        255,
        227,
        219,
        171,
        75,
        150,
        49,
        98,
        196,
        149,
        55,
        110,
        220,
        165,
        87,
        174,
        65,
        130,
        25,
        50,
        100,
        200,
        141,
        7,
        14,
        28,
        56,
        112,
        224,
        221,
        167,
        83,
        166,
        81,
        162,
        89,
        178,
        121,
        242,
        249,
        239,
        195,
        155,
        43,
        86,
        172,
        69,
        138,
        9,
        18,
        36,
        72,
        144,
        61,
        122,
        244,
        245,
        247,
        243,
        251,
        235,
        203,
        139,
        11,
        22,
        44,
        88,
        176,
        125,
        250,
        233,
        207,
        131,
        27,
        54,
        108,
        216,
        173,
        71,
        142,
        1,
        2,
        4,
        8,
        16,
        32,
        64,
        128,
        29,
        58,
        116,
        232,
        205,
        135,
        19,
        38,
        76,
        152,
        45,
        90,
        180,
        117,
        234,
        201,
        143,
        3,
        6,
        12,
        24,
        48,
        96,
        192,
        157,
        39,
        78,
        156,
        37,
        74,
        148,
        53,
        106,
        212,
        181,
        119,
        238,
        193,
        159,
        35,
        70,
        140,
        5,
        10,
        20,
        40,
        80,
        160,
        93,
        186,
        105,
        210,
        185,
        111,
        222,
        161,
        95,
        190,
        97,
        194,
        153,
        47,
        94,
        188,
        101,
        202,
        137,
        15,
        30,
        60,
        120,
        240,
        253,
        231,
        211,
        187,
        107,
        214,
        177,
        127,
        254,
        225,
        223,
        163,
        91,
        182,
        113,
        226,
        217,
        175,
        67,
        134,
        17,
        34,
        68,
        136,
        13,
        26,
        52,
        104,
        208,
        189,
        103,
        206,
        129,
        31,
        62,
        124,
        248,
        237,
        199,
        147,
        59,
        118,
        236,
        197,
        151,
        51,
        102,
        204,
        133,
        23,
        46,
        92,
        184,
        109,
        218,
        169,
        79,
        158,
        33,
        66,
        132,
        21,
        42,
        84,
        168,
        77,
        154,
        41,
        82,
        164,
        85,
        170,
        73,
        146,
        57,
        114,
        228,
        213,
        183,
        115,
        230,
        209,
        191,
        99,
        198,
        145,
        63,
        126,
        252,
        229,
        215,
        179,
        123,
        246,
        241,
        255,
        227,
        219,
        171,
        75,
        150,
        49,
        98,
        196,
        149,
        55,
        110,
        220,
        165,
        87,
        174,
        65,
        130,
        25,
        50,
        100,
        200,
        141,
        7,
        14,
        28,
        56,
        112,
        224,
        221,
        167,
        83,
        166,
        81,
        162,
        89,
        178,
        121,
        242,
        249,
        239,
        195,
        155,
        43,
        86,
        172,
        69,
        138,
        9,
        18,
        36,
        72,
        144,
        61,
        122,
        244,
        245,
        247,
        243,
        251,
        235,
        203,
        139,
        11,
        22,
        44,
        88,
        176,
        125,
        250,
        233,
        207,
        131,
        27,
        54,
        108,
        216,
        173,
        71,
        142
    ]

    # Log and values used in GF(256) arithmetic
    GALOIS_LOG = [
        0,
        0,
        1,
        25,
        2,
        50,
        26,
        198,
        3,
        223,
        51,
        238,
        27,
        104,
        199,
        75,
        4,
        100,
        224,
        14,
        52,
        141,
        239,
        129,
        28,
        193,
        105,
        248,
        200,
        8,
        76,
        113,
        5,
        138,
        101,
        47,
        225,
        36,
        15,
        33,
        53,
        147,
        142,
        218,
        240,
        18,
        130,
        69,
        29,
        181,
        194,
        125,
        106,
        39,
        249,
        185,
        201,
        154,
        9,
        120,
        77,
        228,
        114,
        166,
        6,
        191,
        139,
        98,
        102,
        221,
        48,
        253,
        226,
        152,
        37,
        179,
        16,
        145,
        34,
        136,
        54,
        208,
        148,
        206,
        143,
        150,
        219,
        189,
        241,
        210,
        19,
        92,
        131,
        56,
        70,
        64,
        30,
        66,
        182,
        163,
        195,
        72,
        126,
        110,
        107,
        58,
        40,
        84,
        250,
        133,
        186,
        61,
        202,
        94,
        155,
        159,
        10,
        21,
        121,
        43,
        78,
        212,
        229,
        172,
        115,
        243,
        167,
        87,
        7,
        112,
        192,
        247,
        140,
        128,
        99,
        13,
        103,
        74,
        222,
        237,
        49,
        197,
        254,
        24,
        227,
        165,
        153,
        119,
        38,
        184,
        180,
        124,
        17,
        68,
        146,
        217,
        35,
        32,
        137,
        46,
        55,
        63,
        209,
        91,
        149,
        188,
        207,
        205,
        144,
        135,
        151,
        178,
        220,
        252,
        190,
        97,
        242,
        86,
        211,
        171,
        20,
        42,
        93,
        158,
        132,
        60,
        57,
        83,
        71,
        109,
        65,
        162,
        31,
        45,
        67,
        216,
        183,
        123,
        164,
        118,
        196,
        23,
        73,
        236,
        127,
        12,
        111,
        246,
        108,
        161,
        59,
        82,
        41,
        157,
        85,
        170,
        251,
        96,
        134,
        177,
        187,
        204,
        62,
        90,
        203,
        89,
        95,
        176,
        156,
        169,
        160,
        81,
        11,
        245,
        22,
        235,
        122,
        117,
        44,
        215,
        79,
        174,
        213,
        233,
        230,
        231,
        173,
        232,
        116,
        214,
        244,
        234,
        168,
        80,
        88,
        175
    ]

    # Table of all of the generator polynomials
    # Indexed by the number of ECC Code Words
    GENERATOR_POLYNOMIALS = {
        7: [1, 127, 122, 154, 164, 11, 68, 117],
        10: [1, 216, 194, 159, 111, 199, 94, 95, 113, 157, 193],
        13: [1, 137, 73, 227, 17, 177, 17, 52, 13, 46, 43, 83, 132, 120],
        15: [1, 29, 196, 111, 163, 112, 74, 10, 105, 105, 139, 132, 151, 32, 134, 26],
        16: [1, 59, 13, 104, 189, 68, 209, 30, 8, 163, 65, 41, 229, 98, 50, 36, 59],
        17: [1, 119, 66, 83, 120, 119, 22, 197, 83, 249, 41, 143, 134, 85, 53, 125, 99, 79],
        18: [1, 239, 251, 183, 113, 149, 175, 199, 215, 240, 220, 73, 82, 173, 75, 32, 67, 217, 146],
        20: [1, 152, 185, 240, 5, 111, 99, 6, 220, 112, 150, 69, 36, 187, 22, 228, 198, 121, 121, 165, 174],
        22: [1, 89, 179, 131, 176, 182, 244, 19, 189, 69, 40, 28, 137, 29, 123, 67, 253, 86, 218, 230, 26, 145, 245],
        24: [1, 122, 118, 169, 70, 178, 237, 216, 102, 115, 150, 229, 73, 130, 72, 61, 43, 206, 1, 237, 247, 127, 217, 144, 117],
        26: [1, 246, 51, 183, 4, 136, 98, 199, 152, 77, 56, 206, 24, 145, 40, 209, 117, 233, 42, 135, 68, 70, 144, 146, 77, 43, 94],
        28: [1, 252, 9, 28, 13, 18, 251, 208, 150, 103, 174, 100, 41, 167, 12, 247, 56, 117, 119, 233, 127, 181, 100, 121, 147, 176, 74, 58, 197],
        30: [1, 212, 246, 77, 73, 195, 192, 75, 98, 5, 70, 103, 177, 22, 217, 138, 51, 181, 246, 72, 25, 18, 46, 228, 74, 216, 195, 11, 106, 130, 150]
    }

    def __init__(self, data, error_correction='H'):
        self.data = data
        self.version = None
        self.encoding_mode = None
        self.error_correction = error_correction
        self.module_size = None
        self.quiet_zone_size = None
        self.mask_pattern = None
        self.image_factory = None

    def determine_best_encoding_mode(self):
        # Check if input string consists of only decimal digits
        if all(char in self.NUMERIC_CHARSET for char in self.data):
            self.encoding_mode = 'numeric'
            return

        # Check if input string can be encoded in alphanumeric mode
        if all(char in self.ALPHANUMERIC_CHARSET for char in self.data):
            self.encoding_mode = 'alphanumeric'
            return

        # Check if input string can be encoded in UTF-8
        try:
            self.data.encode('utf-8')
            self.encoding_mode = 'byte'
            return
        except UnicodeEncodeError:
            pass

        # If none of the above conditions are met, raise an error
        raise ValueError('Unable to determine the best encoding mode for the input string.')

    def get_encoding_mode_indicator(self):
        return self.ENCODING_MODE_INDICATOR[self.encoding_mode]

    def determine_smallest_version(self):
        # Calculate data length
        data = self.data
        data_length = len(data)

        # Get the maximum capacity for the chosen encoding mode and error correction level
        max_capacity = self.CAPACITIES_TABLE[40][self.error_correction][self.encoding_mode]

         # Check if the data length exceeds the maximum capacity
        if data_length > max_capacity:
            raise ValueError(f'Input data exceeds the maximum capacity for {self.encoding_mode} encoding mode and error correction level {self.error_correction}.')

        # Iterate through QR code versions to find the smallest version that can accommodate the data
        for version, capacities in self.CAPACITIES_TABLE.items():
            # Check if the data length fits within the capacity for the chosen error correction level and encoding mode
            capacity = capacities[self.error_correction][self.encoding_mode]
            if data_length <= capacity:
                self.version = version
                return


    def determine_character_count_indicator_bits(self):
        # Determine CCI bits count according to the QR Code version
        match self.encoding_mode:
            case 'numeric':
                if self.version in range(1, 10):
                    return 10
                elif self.version in range(10, 27):
                    return 12
                elif self.version in range(27, 41):
                    return 14
            case 'alphanumeric':
                if self.version in range(1, 10):
                    return 9
                elif self.version in range(10, 27):
                    return 11
                elif self.version in range(27, 41):
                    return 13
            case 'byte':
                if self.version in range(1, 10):
                    return 8
                elif self.version in range(10, 41):
                    return 16
            case _:
                raise ValueError(f'Invalid encoding mode: {self.encoding_mode}')

    def get_character_count_indicator(self):
        # Convert data length to binary - get CCI
        character_count_indicator = format(len(self.data), f'0{self.determine_character_count_indicator_bits()}b')

        return character_count_indicator

    def encode_numeric(self,):
        # Check if input data contains only numeric characters
        if not self.data.isdigit():
            raise ValueError('Invalid input data. Numeric encoding mode requires numeric characters only.')

        # Implement numeric data encoding logic
        encoded_data = ''

        # Split digit data into groups of three or less
        groups = [self.data[i:i+3] for i in range(0, len(self.data), 3)]

        # Convert each group to binary
        for group in groups:
            # Convert group to 10-bit, 7-bit or 4-bit binary
            # depending on len(group) - count of digits
            match len(group):
                case 3:
                    encoded_group = format(int(group), '010b')
                case 2:
                    encoded_group = format(int(group), '07b')
                case 1:
                    encoded_group = format(int(group), '04b')
                case _:
                    raise ValueError(f'Invalid data group size: {len(group)}')

            encoded_data += encoded_group

        return encoded_data

    def encode_alphanumeric(self):
        # Implement alphanumeric data encoding logic
        alphanumeric_charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'

        # Check if input data contains only alphanumeric characters
        if any(char not in alphanumeric_charset for char in self.data):
            raise ValueError('Invalid input data. Alphanumeric encoding mode requires alphanumeric characters only.')

        # Initialize encoded data string
        encoded_data = ''

        # Divide data into groups of two characters
        groups = [self.data[i:i+2] for i in range(0, len(self.data), 2)]

        for group in groups:
            # Convert group to 11-bit or 6-bit binary
            # depending on len(group) - count of digits
            match len(group):
                case 2:
                    index1 = alphanumeric_charset.index(group[0])
                    index2 = alphanumeric_charset.index(group[1])

                    encoded_group = format(index1 * 45 + index2, '011b')
                case 1:
                    encoded_group = format(alphanumeric_charset.index(group[0]), '06b')
                case _:
                    raise ValueError(f'Invalid data group size: {len(group)}')

            encoded_data += encoded_group

        return encoded_data

    def encode_byte(self):
        # Implement binary data encoding logic
        # Encode data in UTF-8 byte mode
        utf8_encoded_data = self.data.encode('utf-8')

        # Convert each byte into binary and pad to 8 bits
        encoded_data = ''.join(format(byte, '08b') for byte in utf8_encoded_data)

        return encoded_data

    def encode_data(self):
        # Determine encoding mode based on chosen option
        match self.encoding_mode:
            case 'numeric':
                return self.encode_numeric()
            case 'alphanumeric':
                return self.encode_alphanumeric()
            case 'byte':
                return self.encode_byte()
            case _:
                raise ValueError(f'Invalid encoding mode: {self.encoding_mode}')


    def pad_encoded_data(self, pad_emi_cci_data_sequence, required_bits):
        # Add terminator of up to four 0s if necessary
        if len(pad_emi_cci_data_sequence) < required_bits:
            terminator_length = min(4, required_bits - len(pad_emi_cci_data_sequence))
            pad_emi_cci_data_sequence += '0' * terminator_length

        # Add more 0s to make the length a multiple of 8
        if len(pad_emi_cci_data_sequence) % 8 != 0:
            padding_length = 8 - (len(pad_emi_cci_data_sequence) % 8)
            pad_emi_cci_data_sequence += '0' * padding_length

        # Add pad bytes if the string is still too short
        while len(pad_emi_cci_data_sequence) < required_bits:
            pad_emi_cci_data_sequence += '11101100'  # Pad byte 1
            if len(pad_emi_cci_data_sequence) < required_bits:
                pad_emi_cci_data_sequence += '00010001'  # Pad byte 2

        return pad_emi_cci_data_sequence

    def get_emi_cci_data_sequence(self):
        # Obtaining a string of bits that consists of the EMI, the character count indicator, and the data bits
        emi_cci_data_sequence = self.get_encoding_mode_indicator() + self.get_character_count_indicator() + self.encode_data()

        # Determine the required number of bits for this QR code
        required_bits = self.CAPACITIES_TABLE[self.version][self.error_correction]['max_bits']

        # Pad encoded data if necessary
        padded_encoded_data = self.pad_encoded_data(emi_cci_data_sequence, required_bits)

        # Convert to bytearray
        splitted_padded_encoded_data = [padded_encoded_data[i:i+8] for i in range(0, len(padded_encoded_data), 8)]
        int_padded_encoded_data = [int(i, 2) for i in splitted_padded_encoded_data]
        final_data_sequence = bytearray(int_padded_encoded_data)

        return final_data_sequence

    def rs_encode_data(self):
        '''Reed-Solomon main encoding function, using polynomial division (algorithm Extended Synthetic Division)'''
        # Original message
        msg_in = self.get_emi_cci_data_sequence()

        # Given number of error correction symbols
        nsym = self.ECCWBI[self.version][self.error_correction][0]

        # Generator polynomial
        gen = self.GENERATOR_POLYNOMIALS[nsym]

        # Cache lengths for faster access inside loops
        msg_in_len = len(msg_in)
        gen_len = len(gen)

        if (msg_in_len + nsym) > 255: 
            raise ValueError(f'Message is too long ({msg_in_len + nsym} when max is 255)')

        # Init msg_out with the values inside msg_in and pad with len(gen)-1 bytes (which is the number of ecc symbols).
        msg_out = bytearray(msg_in) + bytearray(gen_len-1)

        # Precompute the logarithm of every items in the generator
        lgen = bytearray([self.GALOIS_LOG[gen[j]] for j in range(len(gen))])

        # Synthetic division main loop
        for i in range(msg_in_len):
            coef = msg_out[i] # Note that it's msg_out here, not msg_in. Thus, we reuse the updated value at each iteration (this is how Synthetic Division works: instead of storing in a temporary register the intermediate values, we directly commit them to the output).
            if coef != 0: # log(0) is undefined, so we need to manually check for this case. There's no need to check the divisor here because we know it can't be 0 since we generated it.
                lcoef = self.GALOIS_LOG[coef] # Precaching
                # In synthetic division, we always skip the first coefficient of the divisior, because it's only used to normalize the dividend coefficient (which is here useless since the divisor, the generator polynomial, is always monic)
                # If gen[j] != 0: # log(0) is undefined so we need to check that, but it slow things down in fact and it's useless in our case (reed-solomon encoding) since we know that all coefficients in the generator are not 0
                for j in range(1, gen_len):
                    msg_out[i + j] ^= self.GALOIS_ANTILOG[lcoef + lgen[j]] # It's equivalent to an addition and to an XOR). In other words, this is simply a "multiply-accumulate operation"

        # Recopy the original message bytes (overwrites the part where the quotient was computed)
        msg_out[:msg_in_len] = msg_in # Bytarray format

        return msg_out

    def divide_data_into_blocks(self, encoded_data):
        # Determine the number of blocks and error correction codewords for each block
        # depending on version and error correction
        ecc_info = self.ECCWBI[self.version][self.error_correction]

        # Number of error correction codes per block
        ec_codewords_per_block = ecc_info[0]
        
        # Info abount block count and number of data code words per block
        # [(block1_count, block1_data_code_words),(block2_count, block2_data_code_words)]
        block_info = [(ecc_info[i], ecc_info[i + 1]) for i in range(1, len(ecc_info), 2)]

        # Divide the encoded data into blocks
        blocks = []
        start_index = 0
        for ec_count, data_count in block_info:
            block = encoded_data[start_index:start_index + data_count]
            blocks.append((block, ec_count))
            start_index += data_count

        return blocks


    def generate_matrix(self, encoded_data):
        # Generate QR code matrix based on encoded data
        # Determine QR code size based on version and encoding mode
        qr_size = 21 + (self.version - 1) * 4

        # Initialize QR code matrix with white modules
        qr_matrix = [[0] * qr_size for _ in range(qr_size)]

        # Add encoded data to QR code matrix
        # This is just a placeholder, actual implementation depends on the QR code structure

        return qr_matrix

    def add_quiet_zone(self):
        # Add quiet zone around the QR code matrix
        pass

    def add_timing_patterns(self):
        # Add timing patterns to the QR code matrix
        pass

    def apply_error_correction(self):
        # Apply error correction coding to the QR code data
        pass

    def render_qr_code(self):
        # Render the QR code matrix as a visual representation
        pass

    def generate_qr_code(self):
        pass


if __name__ == '__main__':
    generator = QRCodeGenerator('HELLO WORLD', error_correction='M')
    generator.determine_best_encoding_mode()
    generator.determine_smallest_version()
    print(generator.rs_encode_data())
