from asm import Assembler

if __name__ == '__main__':
    assembler = Assembler('program.txt', 'assembled.bin', 'logs.xml')
    try:
        assembler.assembly()
    except SyntaxError | ValueError as e:
        print(e)
