# main.py

class QRCodeGenerator:
    NUMERIC_CHARSET = set('0123456789')
    ALPHANUMERIC_CHARSET = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:')

    def __init__(self, data):
        self.data = data
        self.version = None
        self.encoding_mode = None
        self.error_correction = None
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
        # Determine encoding mode based on choosen option
        match self.encoding_mode:
            case 'numeric':
                return self.encode_numeric()
            case 'alphanumeric':
                return self.encode_alphanumeric()
            case 'byte':
                return self.encode_byte()
            case _:
                raise ValueError(f'Unknown encoding mode: {self.encoding_mode}')

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
    generator = QRCodeGenerator('test?')
    generator.determine_best_encoding_mode()
    print(generator.encoding_mode)
