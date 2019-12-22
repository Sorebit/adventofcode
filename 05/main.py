# https://adventofcode.com/2019/day/5
#
# Turns out it was worth it.

import intcode import Instruction
from intcode import Program

# Test using small programs from website
def test():
    print("Testing:")
    tests = [
        {"in": [1,0,0,0,99], "out": [2,0,0,0,99]},
        {"in": [2,3,0,3,99], "out": [2,3,0,6,99]},
        {"in": [2,4,4,5,99,0], "out": [2,4,4,5,99,9801]},
        {"in": [1,1,1,4,99,5,6,0,99], "out": [30,1,1,4,2,5,6,0,99]},
        # {"in": [3,9,8,9,10,9,4,9,99,-1,8], "out": [3,9,8,9,10,9,4,9,99,1,8], "info": "Position mode OP_EQ test\nInput 8 to pass"},
        # {"in": [3,9,7,9,10,9,4,9,99,-1,8], "out": [3,9,7,9,10,9,4,9,99,1,8], "info": "Position mode OP_LT test\nInput 7 or less to pass"}, 
        # {"in": [3,3,1108,-1,8,3,4,3,99], "out": [3,3,1108,1,8,3,4,3,99], "info": "Immediate mode OP_EQ test\nInput 8 to pass"},
        # {"in": [3,3,1107,-1,8,3,4,3,99], "out": [3,3,1107,1,8,3,4,3,99], "info": "Immediate mode OP_LT test\nInput 7 or less to pass"},
        # {"in": [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], "out": [], "info": "[MOD_POS] input was zero => 0, input is non-zero => 1"},
        # {"in": [3,3,1105,-1,9,1101,0,0,12,4,12,99,1], "out": [], "info": "[MOD_IMM] input was zero => 0, input is non-zero => 1"},
        {
            "in": [
            3,21,
            1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
            "info": "Input < 8 => 999, input == 8 => 1000, input > 8 => 1001"
        },
    ]

    for test_num in range(0, len(tests)):
        if "info" in tests[test_num]:
            print(tests[test_num]["info"])

        program = Program(tests[test_num]["in"])
        program.process()

        if not "out" in tests[test_num]:
            print("Test %d: OK, no out specified" % test_num)
        elif program.mem == tests[test_num]["out"]:
            print("Test %d: OK" % test_num)
        else:
            print("Test %d: WRONG" % test_num)
            print("Expected:")
            Program.print_memory(tests[test_num]["out"])
            print("Got:")
            Program.print_memory(program.mem)

    print("")
  

def main():
    test()

    raw_intcode = None
    # Open input intcodes and solve
    with open("input.txt", "r") as file:
        raw_intcode = [int(ins) for ins in file.readline().split(",")]

    # Solve part 1
    one = Program(raw_intcode)
    print("Part 1: %d\n" % one.process())



if __name__ == '__main__':
    main()
