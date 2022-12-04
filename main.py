import argparse
import sys

from elm_parser import parse
from elm_types import Program
from llvm_gen import compile_program


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("input_file", type=argparse.FileType("r"))
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    with open(args.filename) as f:
        text = f.read()

    program = parse(text)
    assert isinstance(program, Program)
    llvm_ir = compile_program(program)
    print(llvm_ir)


if __name__ == "__main__":
    sys.exit(main())
