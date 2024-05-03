# main.py

class QRCodeGenerator:
    # Constants
    NUMERIC_CHARSET = set('0123456789')

    ALPHANUMERIC_CHARSET = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:')

    ENCODING_MODE_INDICATOR = {
        'numeric': '0001',
        'alpanumeric': '0010',
        'byte': '0011',
    }

    # Version -> Error Correction Level -> Encoding Mode -> Allowed Data chars count
    CAPACITIES_TABLE = {
        1: {
            'L': {'numeric': 41, 'alphanumeric': 25, 'byte': 17},
            'M': {'numeric': 34, 'alphanumeric': 20, 'byte': 14},
            'Q': {'numeric': 27, 'alphanumeric': 16, 'byte': 11},
            'H': {'numeric': 17, 'alphanumeric': 10, 'byte': 7},
        },
        2: {
            'L': {'numeric': 77, 'alphanumeric': 47, 'byte': 32},
            'M': {'numeric': 63, 'alphanumeric': 38, 'byte': 26},
            'Q': {'numeric': 48, 'alphanumeric': 29, 'byte': 20},
            'H': {'numeric': 34, 'alphanumeric': 20, 'byte': 14},
        },
        3: {
            'L': {'numeric': 127, 'alphanumeric': 77, 'byte': 53},
            'M': {'numeric': 101, 'alphanumeric': 61, 'byte': 42},
            'Q': {'numeric': 77, 'alphanumeric': 47, 'byte': 32},
            'H': {'numeric': 58, 'alphanumeric': 35, 'byte': 24},
        },
        4: {
            'L': {'numeric': 187, 'alphanumeric': 114, 'byte': 78},
            'M': {'numeric': 149, 'alphanumeric': 90, 'byte': 62},
            'Q': {'numeric': 111, 'alphanumeric': 67, 'byte': 46},
            'H': {'numeric': 82, 'alphanumeric': 50, 'byte': 34},
        },
        5: {
            'L': {'numeric': 255, 'alphanumeric': 154, 'byte': 106},
            'M': {'numeric': 202, 'alphanumeric': 122, 'byte': 84},
            'Q': {'numeric': 144, 'alphanumeric': 87, 'byte': 60},
            'H': {'numeric': 106, 'alphanumeric': 64, 'byte': 44},
        },
        6: {
            'L': {'numeric': 322, 'alphanumeric': 195, 'byte': 134},
            'M': {'numeric': 255, 'alphanumeric': 154, 'byte': 106},
            'Q': {'numeric': 178, 'alphanumeric': 108, 'byte': 74},
            'H': {'numeric': 139, 'alphanumeric': 84, 'byte': 58},
        },
        7: {
            'L': {'numeric': 370, 'alphanumeric': 224, 'byte': 154},
            'M': {'numeric': 293, 'alphanumeric': 178, 'byte': 122},
            'Q': {'numeric': 207, 'alphanumeric': 125, 'byte': 86},
            'H': {'numeric': 154, 'alphanumeric': 93, 'byte': 64},
        },
        8: {
            'L': {'numeric': 461, 'alphanumeric': 279, 'byte': 192},
            'M': {'numeric': 365, 'alphanumeric': 221, 'byte': 152},
            'Q': {'numeric': 259, 'alphanumeric': 157, 'byte': 108},
            'H': {'numeric': 202, 'alphanumeric': 122, 'byte': 84},
        },
        9: {
            'L': {'numeric': 552, 'alphanumeric': 335, 'byte': 230},
            'M': {'numeric': 432, 'alphanumeric': 262, 'byte': 180},
            'Q': {'numeric': 312, 'alphanumeric': 189, 'byte': 130},
            'H': {'numeric': 235, 'alphanumeric': 143, 'byte': 98},
        },
        10: {
            'L': {'numeric': 652, 'alphanumeric': 395, 'byte': 271},
            'M': {'numeric': 513, 'alphanumeric': 311, 'byte': 213},
            'Q': {'numeric': 364, 'alphanumeric': 221, 'byte': 151},
            'H': {'numeric': 288, 'alphanumeric': 174, 'byte': 119},
        },
        11: {
            'L': {'numeric': 772, 'alphanumeric': 468, 'byte': 321},
            'M': {'numeric': 604, 'alphanumeric': 366, 'byte': 251},
            'Q': {'numeric': 427, 'alphanumeric': 259, 'byte': 177},
            'H': {'numeric': 331, 'alphanumeric': 200, 'byte': 137},
        },
        12: {
            'L': {'numeric': 883, 'alphanumeric': 535, 'byte': 367},
            'M': {'numeric': 691, 'alphanumeric': 419, 'byte': 287},
            'Q': {'numeric': 489, 'alphanumeric': 296, 'byte': 203},
            'H': {'numeric': 374, 'alphanumeric': 227, 'byte': 155},
        },
        13: {
            'L': {'numeric': 1022, 'alphanumeric': 619, 'byte': 425},
            'M': {'numeric': 796, 'alphanumeric': 483, 'byte': 331},
            'Q': {'numeric': 580, 'alphanumeric': 352, 'byte': 241},
            'H': {'numeric': 427, 'alphanumeric': 259, 'byte': 177},
        },
        14: {
            'L': {'numeric': 1101, 'alphanumeric': 667, 'byte': 458},
            'M': {'numeric': 871, 'alphanumeric': 528, 'byte': 362},
            'Q': {'numeric': 621, 'alphanumeric': 376, 'byte': 258},
            'H': {'numeric': 468, 'alphanumeric': 283, 'byte': 194},
        },
        15: {
            'L': {'numeric': 1250, 'alphanumeric': 758, 'byte': 520},
            'M': {'numeric': 991, 'alphanumeric': 600, 'byte': 412},
            'Q': {'numeric': 703, 'alphanumeric': 426, 'byte': 292},
            'H': {'numeric': 530, 'alphanumeric': 321, 'byte': 220},
        },
        16: {
            'L': {'numeric': 1408, 'alphanumeric': 854, 'byte': 586},
            'M': {'numeric': 1082, 'alphanumeric': 656, 'byte': 450},
            'Q': {'numeric': 775, 'alphanumeric': 470, 'byte': 322},
            'H': {'numeric': 602, 'alphanumeric': 365, 'byte': 250},
        },
        17: {
            'L': {'numeric': 1548, 'alphanumeric': 938, 'byte': 644},
            'M': {'numeric': 1212, 'alphanumeric': 734, 'byte': 504},
            'Q': {'numeric': 876, 'alphanumeric': 531, 'byte': 364},
            'H': {'numeric': 674, 'alphanumeric': 408, 'byte': 280},
        },
        18: {
            'L': {'numeric': 1725, 'alphanumeric': 1046, 'byte': 718},
            'M': {'numeric': 1346, 'alphanumeric': 816, 'byte': 560},
            'Q': {'numeric': 948, 'alphanumeric': 574, 'byte': 394},
            'H': {'numeric': 746, 'alphanumeric': 452, 'byte': 310},
        },
        19: {
            'L': {'numeric': 1903, 'alphanumeric': 1153, 'byte': 792},
            'M': {'numeric': 1500, 'alphanumeric': 909, 'byte': 624},
            'Q': {'numeric': 1063, 'alphanumeric': 644, 'byte': 442},
            'H': {'numeric': 813, 'alphanumeric': 493, 'byte': 338},
        },
        20: {
            'L': {'numeric': 2061, 'alphanumeric': 1249, 'byte': 858},
            'M': {'numeric': 1600, 'alphanumeric': 970, 'byte': 666},
            'Q': {'numeric': 1159, 'alphanumeric': 702, 'byte': 482},
            'H': {'numeric': 919, 'alphanumeric': 557, 'byte': 382},
        },
        21: {
            'L': {'numeric': 2232, 'alphanumeric': 1352, 'byte': 929},
            'M': {'numeric': 1708, 'alphanumeric': 1035, 'byte': 711},
            'Q': {'numeric': 1224, 'alphanumeric': 742, 'byte': 509},
            'H': {'numeric': 969, 'alphanumeric': 587, 'byte': 403},
        },
        22: {
            'L': {'numeric': 2409, 'alphanumeric': 1460, 'byte': 1003},
            'M': {'numeric': 1872, 'alphanumeric': 1134, 'byte': 779},
            'Q': {'numeric': 1358, 'alphanumeric': 823, 'byte': 565},
            'H': {'numeric': 1056, 'alphanumeric': 640, 'byte': 439},
        },
        23: {
            'L': {'numeric': 2620, 'alphanumeric': 1588, 'byte': 1091},
            'M': {'numeric': 2059, 'alphanumeric': 1248, 'byte': 857},
            'Q': {'numeric': 1468, 'alphanumeric': 890, 'byte': 611},
            'H': {'numeric': 1108, 'alphanumeric': 672, 'byte': 461},
        },
        24: {
            'L': {'numeric': 2812, 'alphanumeric': 1704, 'byte': 1171},
            'M': {'numeric': 2188, 'alphanumeric': 1326, 'byte': 911},
            'Q': {'numeric': 1588, 'alphanumeric': 963, 'byte': 661},
            'H': {'numeric': 1228, 'alphanumeric': 744, 'byte': 511},
        },
        25: {
            'L': {'numeric': 3057, 'alphanumeric': 1853, 'byte': 1273},
            'M': {'numeric': 2395, 'alphanumeric': 1451, 'byte': 997},
            'Q': {'numeric': 1718, 'alphanumeric': 1041, 'byte': 715},
            'H': {'numeric': 1286, 'alphanumeric': 779, 'byte': 535},
        },
        26: {
            'L': {'numeric': 3283, 'alphanumeric': 1990, 'byte': 1367},
            'M': {'numeric': 2544, 'alphanumeric': 1542, 'byte': 1059},
            'Q': {'numeric': 1804, 'alphanumeric': 1094, 'byte': 751},
            'H': {'numeric': 1425, 'alphanumeric': 864, 'byte': 593},
        },
        27: {
            'L': {'numeric': 3514, 'alphanumeric': 2132, 'byte': 1465},
            'M': {'numeric': 2701, 'alphanumeric': 1637, 'byte': 1125},
            'Q': {'numeric': 1933, 'alphanumeric': 1172, 'byte': 805},
            'H': {'numeric': 1501, 'alphanumeric': 910, 'byte': 625},
        },
        28: {
            'L': {'numeric': 3669, 'alphanumeric': 2223, 'byte': 1528},
            'M': {'numeric': 2857, 'alphanumeric': 1732, 'byte': 1190},
            'Q': {'numeric': 2085, 'alphanumeric': 1263, 'byte': 868},
            'H': {'numeric': 1581, 'alphanumeric': 958, 'byte': 658},
        },
        29: {
            'L': {'numeric': 3909, 'alphanumeric': 2369, 'byte': 1628},
            'M': {'numeric': 3035, 'alphanumeric': 1839, 'byte': 1264},
            'Q': {'numeric': 2181, 'alphanumeric': 1322, 'byte': 908},
            'H': {'numeric': 1677, 'alphanumeric': 1016, 'byte': 698},
        },
        30: {
            'L': {'numeric': 4158, 'alphanumeric': 2520, 'byte': 1732},
            'M': {'numeric': 3289, 'alphanumeric': 1994, 'byte': 1370},
            'Q': {'numeric': 2358, 'alphanumeric': 1429, 'byte': 982},
            'H': {'numeric': 1782, 'alphanumeric': 1080, 'byte': 742},
        },
        31: {
            'L': {'numeric': 4417, 'alphanumeric': 2677, 'byte': 1840},
            'M': {'numeric': 3486, 'alphanumeric': 2113, 'byte': 1452},
            'Q': {'numeric': 2473, 'alphanumeric': 1499, 'byte': 1030},
            'H': {'numeric': 1897, 'alphanumeric': 1150, 'byte': 790},
        },
        32: {
            'L': {'numeric': 4686, 'alphanumeric': 2840, 'byte': 1952},
            'M': {'numeric': 3693, 'alphanumeric': 2238, 'byte': 1538},
            'Q': {'numeric': 2670, 'alphanumeric': 1618, 'byte': 1112},
            'H': {'numeric': 2022, 'alphanumeric': 1226, 'byte': 842},
        },
        33: {
            'L': {'numeric': 4965, 'alphanumeric': 3009, 'byte': 2068},
            'M': {'numeric': 3909, 'alphanumeric': 2369, 'byte': 1628},
            'Q': {'numeric': 2805, 'alphanumeric': 1700, 'byte': 1168},
            'H': {'numeric': 2157, 'alphanumeric': 1307, 'byte': 898},
        },
        34: {
            'L': {'numeric': 5253, 'alphanumeric': 3183, 'byte': 2188},
            'M': {'numeric': 4134, 'alphanumeric': 2506, 'byte': 1722},
            'Q': {'numeric': 2949, 'alphanumeric': 1787, 'byte': 1228},
            'H': {'numeric': 2301, 'alphanumeric': 1394, 'byte': 958},
        },
        35: {
            'L': {'numeric': 5529, 'alphanumeric': 3351, 'byte': 2303},
            'M': {'numeric': 4343, 'alphanumeric': 2632, 'byte': 1809},
            'Q': {'numeric': 3081, 'alphanumeric': 1867, 'byte': 1283},
            'H': {'numeric': 2361, 'alphanumeric': 1431, 'byte': 983},
        },
        36: {
            'L': {'numeric': 5836, 'alphanumeric': 3537, 'byte': 2431},
            'M': {'numeric': 4588, 'alphanumeric': 2780, 'byte': 1911},
            'Q': {'numeric': 3244, 'alphanumeric': 1966, 'byte': 1351},
            'H': {'numeric': 2524, 'alphanumeric': 1530, 'byte': 1051},
        },
        37: {
            'L': {'numeric': 6153, 'alphanumeric': 3729, 'byte': 2563},
            'M': {'numeric': 4775, 'alphanumeric': 2894, 'byte': 1989},
            'Q': {'numeric': 3417, 'alphanumeric': 2071, 'byte': 1423},
            'H': {'numeric': 2625, 'alphanumeric': 1591, 'byte': 1093},
        },
        38: {
            'L': {'numeric': 6479, 'alphanumeric': 3927, 'byte': 2699},
            'M': {'numeric': 5039, 'alphanumeric': 3054, 'byte': 2099},
            'Q': {'numeric': 3599, 'alphanumeric': 2181, 'byte': 1499},
            'H': {'numeric': 2735, 'alphanumeric': 1658, 'byte': 1139},
        },
        39: {
            'L': {'numeric': 6743, 'alphanumeric': 4087, 'byte': 2809},
            'M': {'numeric': 5313, 'alphanumeric': 3220, 'byte': 2213},
            'Q': {'numeric': 3791, 'alphanumeric': 2298, 'byte': 1579},
            'H': {'numeric': 2927, 'alphanumeric': 1774, 'byte': 1219},
        },
        40: {
            'L': {'numeric': 7089, 'alphanumeric': 4296, 'byte': 2953},
            'M': {'numeric': 5596, 'alphanumeric': 3391, 'byte': 2331},
            'Q': {'numeric': 3993, 'alphanumeric': 2420, 'byte': 1663},
            'H': {'numeric': 3057, 'alphanumeric': 1852, 'byte': 1273},
        },
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
        if all(char in self.ALPHANUMERIC_CHARSET for char in self.data.upper()):
            self.encoding_mode = 'alphanumeric'
            return

        # Check if input string can be encoded in ISO 8859-1 (Latin-1)
        try:
            self.data.encode('latin-1')
            self.encoding_mode = 'byte'
            return
        except UnicodeEncodeError:
            pass

        # If none of the above conditions are met, raise an error
        raise ValueError('Unable to determine the best encoding mode for the input string.')

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
        character_count_indicator = format(len(self.data), f'0{determine_character_count_indicator_bits()}b')

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
        aplhanumeric_charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'

        # Initialize encoded data string
        encoded_data = ''

        # Divide data into groups of two characters
        groups = [self.data[i:i+2] for i in range(0, len(self.data), 2)]

        for group in groups:
            # Convert group to 11-bit or 6-bit binary
            # depending on len(group) - count of digits
            match len(group):
                case 2:
                    index1 = aplhanumeric_charset.index(group[0])
                    index2 = aplhanumeric_charset.index(group[1])

                    encoded_group = format(index1 * 45 + index2, '011b')
                case 1:
                    encoded_group = format(aplhanumeric_charset.index(group[0]), '06b')
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
    generator = QRCodeGenerator('test?test?test?test?test?test?', error_correction='L')
    generator.determine_best_encoding_mode()
    generator.determine_smallest_version()
    print(generator.version)
