import unittest
from asm import Assembler
from interpretator import Interpretator

class TestAsmInterpret(unittest.TestCase):
    def test_asm_1(self):
        src = '''LOAD_CONST 920\nLOAD_CONST 50\nWRITE_MEM\nREAD_MEM 50\nLOAD_CONST 100\nWRITE_MEM\nADD 0'''
        with open('test.txt', 'w') as f:
            f.writelines(src)
        asm = Assembler('test.txt', '', '')
        asm.assembly()
        expected = [['0x68', '0xCC', '0x01', '0x00'], ['0x68', '0x19', '0x00', '0x00'], ['0x08', '0x00', '0x00', '0x00'], ['0x2D', '0x19', '0x00', '0x00'], ['0x68', '0x32', '0x00', '0x00'], ['0x08', '0x00', '0x00', '0x00'], ['0x5B', '0x00', '0x00', '0x00']]
        self.assertEqual(expected, asm.bytes)

    def test_asm_2(self):
        src = '''LOAD_CONST 920\nLOAD_CONST 50\nLOAD_CONST 100\nLOAD_CONST 231\nLOAD_CONST 555\nWRITE_MEM\nREAD_MEM 231'''
        with open('test.txt', 'w') as f:
            f.writelines(src)
        asm = Assembler('test.txt', '', '')
        asm.assembly()
        expected = [['0x68', '0xCC', '0x01', '0x00'], ['0x68', '0x19', '0x00', '0x00'], ['0x68', '0x32', '0x00', '0x00'], ['0xE8', '0x73', '0x00', '0x00'], ['0xE8', '0x15', '0x01', '0x00'], ['0x08', '0x00', '0x00', '0x00'], ['0xAD', '0x73', '0x00', '0x00']]
        self.assertEqual(expected, asm.bytes)

    def test_asm_3(self):
        src = '''LOAD_CONST 4\nLOAD_CONST 7\nLOAD_CONST 100\nLOAD_CONST 231\nLOAD_CONST 555\nWRITE_MEM\nREAD_MEM 231\nADD 324'''
        with open('test.txt', 'w') as f:
            f.writelines(src)
        asm = Assembler('test.txt', '', '')
        asm.assembly()
        expected = [['0x68', '0x02', '0x00', '0x00'], ['0xE8', '0x03', '0x00', '0x00'], ['0x68', '0x32', '0x00', '0x00'], ['0xE8', '0x73', '0x00', '0x00'], ['0xE8', '0x15', '0x01', '0x00'], ['0x08', '0x00', '0x00', '0x00'], ['0xAD', '0x73', '0x00', '0x00'], ['0x5B', '0xA2', '0x00', '0x00']]
        self.assertEqual(expected, asm.bytes)

    def test_interpr_1(self):
        byts = [['0x68', '0xCC', '0x01', '0x00'], ['0x68', '0x19', '0x00', '0x00'], ['0x08', '0x00', '0x00', '0x00'], ['0x2D', '0x19', '0x00', '0x00'], ['0x68', '0x32', '0x00', '0x00'], ['0x08', '0x00', '0x00', '0x00'], ['0x5B', '0x00', '0x00', '0x00']]
        with open('test.bin', 'wb') as file:
            for mass in byts:
                for string in mass:
                    byte_value = bytes.fromhex(string[2:])
                    file.write(byte_value)
        interpretator = Interpretator('test.bin', '', 0, 100)
        interpretator.read_file()
        interpretator.interpret()
        self.assertEqual({50: 50, 100: 100}, interpretator.memory)

    def test_interpr_2(self):
        byts = [['0x68', '0xCC', '0x01', '0x00'], ['0x68', '0x19', '0x00', '0x00'], ['0x68', '0x32', '0x00', '0x00'], ['0xE8', '0x73', '0x00', '0x00'], ['0xE8', '0x15', '0x01', '0x00'], ['0x08', '0x00', '0x00', '0x00'], ['0xAD', '0x15', '0x01', '0x00']]
        with open('test.bin', 'wb') as file:
            for mass in byts:
                for string in mass:
                    byte_value = bytes.fromhex(string[2:])
                    file.write(byte_value)
        interpretator = Interpretator('test.bin', '', 0, 100)
        interpretator.read_file()
        interpretator.interpret()
        self.assertEqual({555: 555}, interpretator.memory)

    def test_interpr_3(self):
        byts = [['0x68', '0x02', '0x00', '0x00'], ['0xE8', '0x03', '0x00', '0x00'], ['0x68', '0x32', '0x00', '0x00'], ['0xE8', '0x73', '0x00', '0x00'], ['0x08', '0x00', '0x00', '0x00'], ['0xE8', '0x15', '0x01', '0x00'], ['0x08', '0x00', '0x00', '0x00'], ['0xAD', '0x73', '0x00', '0x00'], ['0x5B', '0xA2', '0x00', '0x00']]
        with open('test.bin', 'wb') as file:
            for mass in byts:
                for string in mass:
                    byte_value = bytes.fromhex(string[2:])
                    file.write(byte_value)
        interpretator = Interpretator('test.bin', '', 0, 100)
        interpretator.read_file()
        interpretator.interpret()
        self.assertEqual([4, 7, 655], interpretator.stack)


if __name__ == '__main__':
    unittest.main()