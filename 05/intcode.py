# Parameter modes:
# 0 - position mode (parameter is position)
# 1 - immediate mode (parameter is value)
#
# Opcodes:
# 1 - add: Read three next cells (x, y, z) read memory at adresses x and y, 
#     add them and store at address z, then move instruction pointer
# 2 - multiply: like 1, but multiply instead of add
# 3 - input and store at address given by parameter
# 4 - output from address given by parameter
# 5 - jump-if-true: if first params is non-zero, jump to second param
# 6 - jump-if-false: if first params is zero, jump to second param
# 7 - less than: store logical value of (first param < second param) to position
#     given by third param
# 8 - equals: store logical value of (first param == second param) to position
#     given by third param
# 99 - end the program
# otherwise, something went wrong
#
#
# ABCDE
#  1002
# 
# DE - two-digit opcode,      02 == opcode 2
#  C - mode of 1st parameter,  0 == position mode
#  B - mode of 2nd parameter,  1 == immediate mode
#  A - mode of 3rd parameter,  0 == position mode,
#                                   omitted due to being a leading zero

# Define opcodes
OP_ADD =  1 # Add
OP_MUL =  2 # Multiply
OP_IN  =  3 # Input
OP_OUT =  4 # Output
OP_JNZ =  5 # Jump if non-zero (true)
OP_JZR =  6 # Jump if zero (false)
OP_LT  =  7 # Less than
OP_EQ  =  8 # Equals
OP_END = 99 # End

# Define modes
MODE_POS = 0 # Position
MODE_IMM = 1 # Immediate

class Instruction(object):
    def __init__(self, instruction):
        # Store raw instruction and opcode
        self.raw = str(instruction)
        self.opcode = int(self.raw[-2:])
        self.auto_inc = True # Whether ins pointer should auto increase after op
        self.params_num = 0

        # Set params number
        if self.opcode in [OP_ADD, OP_MUL, OP_LT, OP_EQ]:
            self.params_num = 3
        elif self.opcode in [OP_IN, OP_OUT]:
            self.params_num = 1
        elif self.opcode in [OP_JZR, OP_JNZ]:
            self.params_num = 2
            self.auto_inc = False

        # Set default modes to 0
        self.params_modes = [MODE_POS for i in range(0, self.params_num)]
        # Create params array for later use
        self.params = [None for i in range(0, self.params_num)]

        # print("Instruction: raw: %s" % self.raw)
        # print("\topcode: %d, params_num: %d" % (self.opcode, self.params_num))

        # If params modes specified
        if len(self.raw) > 2:
            params_raw = str(int(instruction / 100))
            # print("\traw longer than 2, cool")
            # print("\t\tparams_raw:", params_raw)
            # print("\t\tparams_num:", self.params_num)
            for i in range(0, len(params_raw)):
                self.params_modes[i] = int(params_raw[len(params_raw) - i - 1])

        # TODO: CONSIDER MODES IN OTHER OPS
        # Last parameter (output) in OP_ADD and OP_MULL is always in immediate mode
        # Even though the site says: "Parameters that an instruction writes to will never be in immediate mode."?
        # Oh, okay, seems like my code kinda works around this.
        if self.opcode in [OP_ADD, OP_MUL, OP_EQ, OP_LT]:
            self.params_modes[2] = MODE_IMM

        # print("\tmodes:", self.params_modes)


    # Apply modes to params
    def apply_modes(self, program):
        params_start = program.ins_ptr + 1
        params = program.mem[params_start : params_start + self.params_num]

        for i in range(0, self.params_num):
            if self.params_modes[i] == MODE_POS:
                # Address mode
                self.params[i] =  program.mem[params[i]]
            else:
                # Immediate mode
                self.params[i] = params[i]
            # print("\t[@ %d, m %d]\t= %d" % (params[i], self.params_modes[i], self.params[i]))

        # print("\tself.params:", self.params)



# TODO: Shouldn't opcodes 3 and 4 process param modes as well?
# TODO: Put IO in program do or some other helper to keep main loop clean
class Program(object):
    def __init__(self, intcode):
        # Copy program, then substitute noun and verb
        self.mem = intcode.copy()
        self.mem_size = len(self.mem)
        self.ins_ptr = 0


    def process(self):
        self.ins_ptr = 0
        while True:
            # print("\n[ptr %d]" % self.ins_ptr)
            # Process opcode
            ins = Instruction(self.mem[self.ins_ptr])
            ins.apply_modes(self)

            if ins.opcode == OP_ADD:
                self._math(ins, lambda x, y: x + y)
            elif ins.opcode == OP_MUL:
                self._math(ins, lambda x, y: x * y)
            elif ins.opcode in [OP_IN,  OP_OUT]:
                self._io(ins)
            elif ins.opcode in [OP_EQ, OP_LT]:
                self._logic_cmp(ins)
            elif ins.opcode in [OP_JNZ, OP_JZR]:
                self._logic_jmp(ins)
            elif ins.opcode == OP_END:
                # End
                break
            else:
                print("Exception: Unknown instruction %s at address %d" % (ins.raw, self.ins_ptr))
                break

            # Move instruction pointer forwards
            if ins.auto_inc:
                self.ins_ptr += ins.params_num + 1

            if self.ins_ptr >= self.mem_size:
                print("Exception: Reached end of program without ins 99")
                break
        # Return first memory cell
        return self.mem[0]


    def _math(self, ins, op):
        # print("_math: params:", params)
        self.mem[ins.params[2]] = op(ins.params[0], ins.params[1])


    def _io(self, ins):
        print("IO")
        addr = self.mem[self.ins_ptr + 1]
        print("addr:", addr)
        if ins.opcode == OP_IN:
            # Assume okay input
            inp = input("IN(%d): " % addr)
            self.mem[addr] = int(inp)
        else:
            print("[%d] OUT(%d) >> %d" % (self.ins_ptr, addr, self.mem[addr]))


    def _logic_jmp(self, ins):
        print("ins.params:", ins.params)
        if ins.opcode == OP_JNZ and ins.params[0] != 0:
            self.ins_ptr = ins.params[1]
        elif ins.opcode == OP_JZR and ins.params[0] == 0:
            self.ins_ptr = ins.params[1]
        else:
            self.ins_ptr += ins.params_num + 1


    def _logic_cmp(self, ins):
        # print("ins.params", ins.params)
        if ins.opcode == OP_EQ:
            self.mem[ins.params[2]] = int(ins.params[0] == ins.params[1])
        elif ins.opcode == OP_LT:
            self.mem[ins.params[2]] = int(ins.params[0] < ins.params[1])


    def print_memory(mem):
        mem_size = len(mem)
        mem_size_len = len(str(mem_size))
        for ins_ptr in range(0, mem_size):
            print("%s: %d" % (str(ins_ptr).rjust(mem_size_len), mem[ins_ptr]))
