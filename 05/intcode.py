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

        # If params modes specified
        if len(self.raw) > 2:
            params_raw = str(int(instruction / 100))

            for i in range(0, len(params_raw)):
                self.params_modes[i] = int(params_raw[len(params_raw) - i - 1])


        # Assignment fix
        # E.g.
        # pvalue = ins.param[0] + ins.param[1]
        # mem[ins.param[2]] = pvalue
        #
        # If we actually treat param[2] in address mode, self.apply_modes is
        # going to break this assignment
        #
        # Fix instructions whose last param is an assignment address
        if self.opcode in [OP_ADD, OP_MUL, OP_EQ, OP_LT, OP_IN]:
            self.params_modes[self.params_num - 1] = MODE_IMM


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


class Program(object):
    def __init__(self, intcode):
        # Copy program, then substitute noun and verb
        self.mem = intcode.copy()
        self.mem_size = len(self.mem)
        self.ins_ptr = 0
        self.finished = False


    def process(self, verbose = True):
        self.ins_ptr = 0
        while True:
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
                self.finished = True
                break
            else:
                print("Exception: Unknown instruction %s at address %d" % (ins.raw, self.ins_ptr))
                break

            # Move instruction pointer forwards
            if ins.auto_inc:
                self.ins_ptr += ins.params_num + 1

            if self.ins_ptr >= self.mem_size:
                print("Exception: Reached end of program without OP_END")
                break

        if verbose:
            print("Done.")
        print()


    def _math(self, ins, op):
        self.mem[ins.params[2]] = op(ins.params[0], ins.params[1])


    def _io(self, ins):
        param = ins.params[0]

        if ins.opcode == OP_IN:
            # Assume okay input
            inp = int(input("IN: "))
            self.mem[param] = inp
        else:
            print("OUT >> %d" % param)


    def _logic_jmp(self, ins):
        if ins.opcode == OP_JNZ and ins.params[0] != 0:
            self.ins_ptr = ins.params[1]
        elif ins.opcode == OP_JZR and ins.params[0] == 0:
            self.ins_ptr = ins.params[1]
        else:
            self.ins_ptr += ins.params_num + 1


    def _logic_cmp(self, ins):
        if ins.opcode == OP_EQ:
            self.mem[ins.params[2]] = int(ins.params[0] == ins.params[1])
        elif ins.opcode == OP_LT:
            self.mem[ins.params[2]] = int(ins.params[0] < ins.params[1])


    def print_memory(mem):
        mem_size = len(mem)
        mem_size_len = len(str(mem_size))
        for ins_ptr in range(0, mem_size):
            print("%s: %d" % (str(ins_ptr).rjust(mem_size_len), mem[ins_ptr]))
