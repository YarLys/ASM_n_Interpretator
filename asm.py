import sys
class Assembler:
    def __init__(self, source_path, binary_path, log_path):
        self.binary_file_path = binary_path
        self.code_path = source_path
        self.log_path = log_path
        self.bytes = []
        self.logs = '<?xml version="1.0" encoding="UTF-8"?>\n'
        self.logs += '<log>'

    def load_const(self, x):
        if not (0 <= x < 8388608):
            raise ValueError("\nКонстанта должна быть в диапазоне от 0 до 8388607")
        # Объединяем код операции и константу
        combined = (x << 7) | 104
        # Получаем 4 байта в шестнадцатеричном формате
        hex_bytes = combined.to_bytes(4, byteorder='little')
        out = [f"0x{byte:02X}" for byte in hex_bytes]
        # Запишем информацию в log-файл
        self.logs += f'\n\t<LOAD_CONST A="104" B="{x}">{''.join(out)}</LOAD_CONST>'
        # Возвращаем результат в виде списка шестнадцатеричных значений
        return out

    def read_mem(self, x):
        if not (0 <= x < 2097152):
            raise ValueError("\nАдрес в памяти должен быть в диапазоне от 0 до 2097151")
        # Объединяем код операции и константу
        combined = (x << 7) | 45
        # Получаем 4 байта в шестнадцатеричном формате
        hex_bytes = combined.to_bytes(4, byteorder='little')
        out = [f"0x{byte:02X}" for byte in hex_bytes]
        # Запишем информацию в log-файл
        self.logs += f'\n\t<READ_MEM A="45" B="{x}">{''.join(out)}</READ_MEM>'
        # Возвращаем результат в виде списка шестнадцатеричных значений
        return out

    def write_mem(self):
        combined = 8
        hex_bytes = combined.to_bytes(4, byteorder='little')
        out = [f"0x{byte:02X}" for byte in hex_bytes]
        # Запишем информацию в log-файл
        self.logs += f'\n\t<WRITE_MEM A="8">{''.join(out)}</WRITE_MEM>'
        return out

    def add(self, x):
        if not (0 <= x < 4096):
            raise ValueError("\n быть в диапазоне от 0 до 4095")
        combined = (x << 7) | 91
        hex_bytes = combined.to_bytes(4, byteorder='little')
        out = [f"0x{byte:02X}" for byte in hex_bytes]
        # Запишем информацию в log-файл
        self.logs += f'\n\t<ADD A="91" B="{x}">{''.join(out)}</ADD>'
        return out

    def write(self):
        with open(self.binary_file_path, 'wb') as file:
            for mass in self.bytes:
                for string in mass:
                    byte_value = bytes.fromhex(string[2:]) # убираем '0x' и преобразуем строку в байты
                    file.write(byte_value) # записываем байты в файл
        with open(self.log_path, 'w', encoding='utf-8') as f:
            f.write(self.logs)

    def assembly(self):
        with open(self.code_path) as file:
            s = file.readline()
            s = s.split()
            while s != []:
                match s[0]:
                    case 'LOAD_CONST':
                        if (s[1] == ''):
                            raise SyntaxError('\nУ операции загрузки константы должен быть аргумент')
                        self.bytes.append(self.load_const(int(s[1])))

                    case 'READ_MEM':
                        if (s[1] == ''):
                            raise SyntaxError('\nУ операции чтения из памяти должен быть аргумент')
                        self.bytes.append(self.read_mem(int(s[1])))

                    case 'WRITE_MEM':
                        self.bytes.append(self.write_mem())

                    case 'ADD':
                        if (s[1] == ''):
                            raise SyntaxError('\nУ операции сложения должен быть аргумент')
                        self.bytes.append(self.add(int(s[1])))

                s = file.readline()
                s = s.split()

        self.logs += '\n</log>'

def main():
    # получаем аргументы из командной строки
    arguments = sys.argv[1:]  # пропускаем первый элемент (название программы)
    prog_path, bin_file_path, log_file_path = arguments
    asm = Assembler(prog_path, bin_file_path, log_file_path)
    asm.assembly()
    asm.write()

if __name__ == "__main__":
    main()