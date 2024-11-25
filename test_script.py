from asm import Assembler
from interpretator import Interpretator

if __name__ == '__main__':
    assembler = Assembler('vectors.txt', 'assembled.bin', 'logs.xml')
    try:
        assembler.assembly()
        assembler.write()

        interpretator = Interpretator('assembled.bin', 'output.xml', 0, 100)
        interpretator.read_file()
        interpretator.interpret()
        interpretator.write_output()
    except SyntaxError | ValueError as e:
        print(e)

# 1 вектор: 5, 10, 17, 21
# 2 вектор: 100, 1, 8, 12
# результат: 105, 11, 25, 33
