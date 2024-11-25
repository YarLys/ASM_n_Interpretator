import sys
class Interpretator:
    def __init__(self, binary_path, output_path, mem_begin, mem_end):
        self.mem_begin = mem_begin
        self.mem_end = mem_end
        self.binary_file_path = binary_path
        self.output_path = output_path
        self.byte_code = []
        self.hex_code = []
        self.commands = []
        self.stack = []  # стек согласно заданию
        self.memory = dict()  # словарь для моделирования памяти
        self.output = '<?xml version="1.0" encoding="UTF-8"?>'
        self.output += '\n<output>'

    def read_file(self):
        with open(self.binary_file_path, 'rb') as binary_file:
            self.byte_code = binary_file.read()
        # преобразуем байты в список шестнадцатеричных строк
        for i in range(0, len(self.byte_code), 1):
            hex_string = '0x' + format(self.byte_code[i], '02x')
            self.hex_code.append(hex_string)

        # Преобразуем шестнадцатеричные строки в байты
        byte_data = [bytes.fromhex(hex_string[2:]) for hex_string in self.hex_code]
        # Объединяем байты в команды по 4 байта
        for i in range(0, len(byte_data), 4):
            command = bytearray()
            for j in range(4):
                if i + j < len(byte_data):
                    command.extend(byte_data[i + j])  # Добавляем байт
            # Добавляем команду в список
            self.commands.append(command)

    def get_low_bits(self, command, n):  # Функция для получения n младших битов
        result = 0
        for i in range(n):
            byte_index = i // 8
            bit_index = i % 8
            if byte_index < len(command):
                bit = (command[byte_index] >> bit_index) & 1
                result |= (bit << i)
        return result

    def get_high_bits(self, command, n):  # Функция для получения n младших битов
        total_bits = 32
        remaining_bits = total_bits - n
        result = 0
        for i in range(remaining_bits):
            byte_index = (n + i) // 8
            bit_index = (n + i) % 8
            if byte_index < len(command):
                bit = (command[byte_index] >> bit_index) & 1
                result |= (bit << i)

        return result

    def interpret(self):
        for command in self.commands:
            code = self.get_low_bits(command, 7) # получим код текущей команды (первые 7 бит)
            match code:
                case 104: # LOAD_CONST
                    operand = self.get_high_bits(command, 7) # получим операнд (старшие биты, начиная с 8)
                    self.stack.append(operand) # выполним команду, добавим элемент на стэк
                case 45: # READ_MEM
                    operand = self.get_high_bits(command, 7)  # получим операнд (старшие биты, начиная с 8)
                    try:
                        self.stack.append(self.memory[operand]) # добавим элемент по этому адресу в стэк
                    except IndexError:
                        raise IndexError(f'Значения, по адресу которого производится чтение из памяти, не существует: READ_MEM {operand}')
                case 8: # WRITE_MEM
                    try:
                        adr = self.stack.pop()
                        self.memory[adr] = adr # записываем по адресу = элементу из стэка этот же элемент (судя из задания, надо так)
                    except IndexError:
                        raise IndexError('Стек пуст, невозможно получить значение для выполнения операции!')
                    except KeyError:
                        raise KeyError('Не существует значения в памяти по используемому адресу!')
                case 91: # ADD
                    try:
                        offset = self.get_high_bits(command, 7)  # получим операнд (старшие биты, начиная с 8)
                        addr = self.stack.pop()
                        operand1 = self.memory[addr + offset]
                        operand2 = self.stack.pop()
                        self.stack.append(operand1 + operand2)
                    except IndexError:
                        raise IndexError('Стек пуст, невозможно получить значение для выполнения операции!')
                    except KeyError:
                        raise KeyError('Не существует значения в памяти по используемому адресу!')
        print(self.stack)
        print(self.memory)

    def write_output(self):
        for i in range(self.mem_begin, self.mem_end + 1):
            if (i in self.memory):
                self.output += f'\n\t<MEMORY ADDR={i}>{self.memory[i]}</MEMORY>'
        self.output += '\n</output>'
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(self.output)


def main():
    # получаем аргументы из командной строки
    arguments = sys.argv[1:]  # пропускаем первый элемент (название программы)
    bin_file_path, output_path, mem_begin, mem_end = arguments
    interpretator = Interpretator(bin_file_path, output_path, int(mem_begin), int(mem_end))
    interpretator.read_file()
    interpretator.interpret()
    interpretator.write_output()

if __name__ == "__main__":
    main()