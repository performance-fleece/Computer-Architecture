"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MLT = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.running = False
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[MLT] = self.handle_mlt

    def load(self):
        """Load a program into memory."""
        program = open(sys.argv[1], "r")
        lines = program.readlines()
        print(lines)

        address = 0

        # For now, we've just hardcoded a program:

        for instruction in lines:
            if len(instruction) > 1 and instruction.split()[0] != '#':

                self.ram[address] = int('0b' + instruction.split()[0], 2)

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):

        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def handle_ldi(self, register, value):
        self.reg[register] = value
        self.pc += 3

    def handle_hlt(self, op_a, op_b):
        self.running = False

    def handle_prn(self, register, op_b):
        num = self.reg[register]
        print(num)
        self.pc += 2

    def handle_mlt(self, op_a, op_b):
        multiplied = self.reg[op_a] * self.reg[op_b]
        self.pc += 3

    def run(self):
        """Run the CPU."""

        # LDI = 0b10000010
        # PRN = 0b01000111
        # HLT = 0b00000001
        # MLT = 0b10100010

        self.running = True
        while self.running:
            try:
                IR = self.ram_read(self.pc)
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)

                self.branchtable[IR](operand_a, operand_b)
            except:
                print('unknown error')

        # while running:
        #     IR = self.ram_read(self.pc)
        #     operand_a = self.ram_read(self.pc + 1)
        #     operand_b = self.ram_read(self.pc + 2)

        #     try:

        #         if IR == LDI:
        #             # write following 2 commands, register, value
        #             register = operand_a
        #             value = operand_b
        #             self.branchtable[IR](register, value)

        #             self.pc += 3

        #         if IR == PRN:
        #             register = operand_a
        #             number = self.reg[register]
        #             print(number)
        #             self.pc += 2

        #         if IR == MULT:
        #             number = self.reg[operand_a] * self.reg[operand_b]
        #             print(number)
        #             self.pc += 3

        #         if IR == HLT:
        #             running = False
