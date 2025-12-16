import argparse
import math


OP_LOAD_CONST = 8
OP_READ = 3
OP_WRITE = 7
OP_POW = 10



def mask(n: int) -> int:
    return (1 << n) - 1



def decode_command(data: bytes, offset: int):
    if offset + 4 > len(data):
        raise EOFError("Incomplete command")

    word = int.from_bytes(data[offset:offset + 4], "little")

    A = word & mask(4)

    if A == OP_LOAD_CONST:
        return {
            "op": "load_const",
            "B": (word >> 4) & mask(7),
            "C": (word >> 11) & mask(14)
        }, 4

    elif A == OP_READ:
        return {
            "op": "read_value",
            "B": (word >> 4) & mask(7),
            "C": (word >> 11) & mask(7),
            "D": (word >> 18) & mask(12)
        }, 4

    elif A == OP_WRITE:
        return {
            "op": "write_value",
            "B": (word >> 4) & mask(7),
            "C": (word >> 11) & mask(11)
        }, 4

    elif A == OP_POW:
        return {
            "op": "pow",
            "B": (word >> 4) & mask(7),
            "C": (word >> 11) & mask(7),
            "D": (word >> 18) & mask(7)
        }, 4

    else:
        raise ValueError(f"Unknown opcode: {A}")



def execute(bytecode: bytes, mem_size: int = 4096):
    memory = [0] * mem_size
    pc = 0

    while pc < len(bytecode):
        cmd, size = decode_command(bytecode, pc)

        if cmd["op"] == "load_const":
            memory[cmd["B"]] = cmd["C"]

        elif cmd["op"] == "read_value":
            addr = memory[cmd["B"]] + cmd["D"]
            memory[cmd["C"]] = memory[addr]

        elif cmd["op"] == "write_value":
            memory[cmd["C"]] = memory[cmd["B"]]

        elif cmd["op"] == "pow":
            base = memory[cmd["D"]]
            exp = memory[memory[cmd["B"]]]
            memory[cmd["C"]] = int(math.pow(base, exp))

        pc += size

    return memory



def parse_range(rng: str):
    a, b = rng.split("-")
    return int(a), int(b)


def main():
    parser = argparse.ArgumentParser(description="UVM Interpreter (Variant 12)")
    parser.add_argument("-i", "--input", required=True, help="Input binary file")
    parser.add_argument("-o", "--output", required=True, help="CSV dump output")
    parser.add_argument("-r", "--range", required=True, help="Memory range a-b")

    args = parser.parse_args()

    with open(args.input, "rb") as f:
        bytecode = f.read()

    memory = execute(bytecode)

    start, end = parse_range(args.range)

    with open(args.output, "w", encoding="utf-8") as out:
        out.write("addr,value\n")
        for i in range(start, end + 1):
            out.write(f"{i},{memory[i]}\n")

    print("Memory dump written to", args.output)


if __name__ == "__main__":
    main()
