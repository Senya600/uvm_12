import argparse
import json
from typing import List, Tuple

OP_LOAD_CONST = 8     # load_const
OP_READ = 3           # read_value
OP_WRITE = 7          # write_value
OP_POW = 10           # pow


def mask(n: int) -> int:
    return (1 << n) - 1



def pack_load_const(B: int, C: int) -> bytes:
    """
    A(4) | B(7) | C(14)
    """
    A = OP_LOAD_CONST & mask(4)
    val = (
        A |
        ((B & mask(7)) << 4) |
        ((C & mask(14)) << 11)
    )
    return val.to_bytes(4, 'little')


def pack_read(B: int, C: int, D: int) -> bytes:
    """
    A(4) | B(7) | C(7) | D(12)
    """
    A = OP_READ & mask(4)
    val = (
        A |
        ((B & mask(7)) << 4) |
        ((C & mask(7)) << 11) |
        ((D & mask(12)) << 18)
    )
    return val.to_bytes(4, 'little')


def pack_write(B: int, C: int) -> bytes:
    """
    A(4) | B(7) | C(11)
    """
    A = OP_WRITE & mask(4)
    val = (
        A |
        ((B & mask(7)) << 4) |
        ((C & mask(11)) << 11)
    )
    return val.to_bytes(4, 'little')


def pack_pow(B: int, C: int, D: int) -> bytes:
    """
    A(4) | B(7) | C(7) | D(7)
    """
    A = OP_POW & mask(4)
    val = (
        A |
        ((B & mask(7)) << 4) |
        ((C & mask(7)) << 11) |
        ((D & mask(7)) << 18)
    )
    return val.to_bytes(4, 'little')


# =========================
# Assembler
# =========================

def assemble_ir(program: List[dict]):
    """
    JSON -> IR
    """
    ir = []

    for instr in program:
        op = instr["op"]

        if op == "load_const":
            ir.append((
                "load_const",
                instr["B"],
                instr["C"]
            ))

        elif op == "read_value":
            ir.append((
                "read_value",
                instr["B"],
                instr["C"],
                instr["D"]
            ))

        elif op == "write_value":
            ir.append((
                "write_value",
                instr["B"],
                instr["C"]
            ))

        elif op == "pow":
            ir.append((
                "pow",
                instr["B"],
                instr["C"],
                instr["D"]
            ))

        else:
            raise ValueError(f"Unknown instruction: {op}")

    return ir

def assemble_json(program):
    """
    program: list[dict] — JSON IR
    return: (bytecode: bytes, IR: list)
    """
    bytecode = bytearray()
    IR = []

    for cmd in program:
        op = cmd["op"]

        if op == "load_const":
            B = cmd["B"]
            C = cmd["C"]
            IR.append(("load_const", B, C))
            word = (8) | (B << 4) | (C << 11)

        elif op == "read_value":
            B = cmd["B"]
            C = cmd["C"]
            D = cmd["D"]
            IR.append(("read_value", B, C, D))
            word = (3) | (B << 4) | (C << 11) | (D << 18)

        elif op == "write_value":
            B = cmd["B"]
            C = cmd["C"]
            IR.append(("write_value", B, C))
            word = (7) | (B << 4) | (C << 11)

        elif op == "pow":
            B = cmd["B"]
            C = cmd["C"]
            D = cmd["D"]
            IR.append(("pow", B, C, D))
            word = (10) | (B << 4) | (C << 11) | (D << 18)

        else:
            raise ValueError(f"Unknown op: {op}")

        bytecode += word.to_bytes(4, "little")

    return bytes(bytecode), IR

def assemble_machine(ir):
    """
    IR -> bytecode
    """
    bytecode = bytearray()

    for instr in ir:
        name = instr[0]

        if name == "load_const":
            _, B, C = instr
            bytecode += pack_load_const(B, C)

        elif name == "read_value":
            _, B, C, D = instr
            bytecode += pack_read(B, C, D)

        elif name == "write_value":
            _, B, C = instr
            bytecode += pack_write(B, C)

        elif name == "pow":
            _, B, C, D = instr
            bytecode += pack_pow(B, C, D)

    return bytecode


def main():
    parser = argparse.ArgumentParser(description="UVM Assembler (Variant 12)")
    parser.add_argument("-i", "--input", required=True, help="Input JSON file")
    parser.add_argument("-o", "--output", required=True, help="Output binary file")
    parser.add_argument("-t", "--test", action="store_true", help="Test mode")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        program = json.load(f)

    ir = assemble_ir(program)
    bytecode = assemble_machine(ir)

    with open(args.output, "wb") as f:
        f.write(bytecode)

    print(f"Commands assembled: {len(ir)}")

    if args.test:
        print("\nIR:")
        for instr in ir:
            print(instr)

        print("\nBytecode:")
        print(" ".join(f"{b:02X}" for b in bytecode))


if __name__ == "__main__":
    main()
