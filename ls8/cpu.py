"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.reg[7] = 0xF4
        self.running = False
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop

    def load(self):
        """Load a program into memory."""

        address = 0
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    if len(line) > 1 and line.split()[0] != '#':

                        self.ram[address] = int('0b' + line.split()[0], 2)

                        address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def handle_ldi(self, pc):
        reg_idx = self.ram_read(pc + 1)
        value = self.ram_read(pc + 2)
        self.reg[reg_idx] = value

    def handle_hlt(self, pc):
        self.running = False

    def handle_prn(self, pc):
        reg_idx = self.ram_read(pc+1)
        num = self.reg[reg_idx]
        print(num)

    def handle_mul(self, pc):
        idx_a = self.ram_read(self.pc + 1)
        idx_b = self.ram_read(self.pc + 2)
        self.alu("MUL", idx_a, idx_b)

    def handle_push(self, pc):
        reg_to_push = self.ram_read(pc + 1)
        value = self.reg[reg_to_push]
        self.reg[7] -= 1
        self.ram_write(self.reg[7], value)

    def handle_pop(self, pc):
        reg_to_write = self.ram_read(pc + 1)
        idx_to_pop = self.reg[7]
        value = self.ram_read(idx_to_pop)
        self.reg[reg_to_write] = value

        self.reg[7] += 1

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            try:
                IR = self.ram_read(self.pc)

                self.branchtable[IR](self.pc)
                self.pc += 1 + (IR >> 6)
            except:
                print('unknown error')
