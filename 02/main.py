# https://adventofcode.com/2019/day/2
#
# Could be really dumbed down and doesn't need all that class stuff
# I wanted to write it *properly*, though

class Program(object):
    def __init__(self, intcode, noun = None, verb = None):
        # Copy program, then substitute noun and verb
        self.mem = intcode.copy()
        self.mem_size = len(self.mem)
        self.ins_ptr = 0
        if noun and verb:
            self.mem[1] = noun
            self.mem[2] = verb

    # 1 - Read three next cells (x, y, z) read memory at adresses x and y, 
    #     add them and store at address z, then move instruction pointer
    # 2 - like 1, but multiply instead of add
    # 99 - end the program
    # otherwise, something went wrong 
    def process(self):
        self.ins_ptr = 0
        while True:
            # process opcode
            ins = self.mem[self.ins_ptr]
            if ins == 1:
                self.program_do(lambda x, y: x + y)
            elif ins == 2:
                self.program_do(lambda x, y: x * y)
            elif ins == 99:
                break
            else:
                print("Exception: Unknown instruction %d at address %d" % (ins, self.ins_ptr))
                break

            if self.ins_ptr >= self.mem_size:
                print("Exception: Reached end of program without ins 99")
                break
        # Return first memory cell
        return self.mem[0]

    def program_do(self, op):
        params = self.mem[self.ins_ptr + 1 : self.ins_ptr + 4]
        self.mem[params[2]] = op(self.mem[params[0]], self.mem[params[1]])
        self.ins_ptr += len(params) + 1

    def print_memory(mem):
        mem_size = len(mem)
        mem_size_len = len(str(mem_size))
        for ins_ptr in range(0, mem_size):
            print("%s: %d" % (str(ins_ptr).rjust(mem_size_len), mem[ins_ptr]))


# Test using small programs from website
def test():
    print("Testing:")
    tests = [
        {"in": [1,0,0,0,99], "out": [2,0,0,0,99]},
        {"in": [2,3,0,3,99], "out": [2,3,0,6,99]},
        {"in": [2,4,4,5,99,0], "out": [2,4,4,5,99,9801]},
        {"in": [1,1,1,4,99,5,6,0,99], "out": [30,1,1,4,2,5,6,0,99]}
    ]

    for test_num in range(0, len(tests)):
        program = Program(tests[test_num]["in"])
        program.process()
        if program.mem == tests[test_num]["out"]:
            print("Test %d: OK" % test_num)
        else:
            print("Test %d: WRONG" % test_num)
            print("Expected:")
            Program.print_memory(tests[test_num]["out"])
            print("Got:")
            Program.print_memory(program.mem)

    print("")
  

def main():
    print("Advent of Code 2019 - Day 2\n")

    test()

    # Open input intcodes and solve
    with open("input.txt", "r") as file:
        intcode = [int(ins) for ins in file.readline().split(",")]

        # Solve part 1
        one = Program(intcode, 12, 2)
        print("Part 1: %d\n" % one.process())

        # Solve part 2
        print("Part 2:")
        for noun in range(0, 100):
            for verb in range(0, 100):
                program = Program(intcode, noun, verb)
                if program.process() == 19690720:
                    print("Found: %d %d => %d" % (noun, verb, program.mem[0]))
                    print("Result: %d" % (100 * noun + verb))


if __name__ == '__main__':
    main()