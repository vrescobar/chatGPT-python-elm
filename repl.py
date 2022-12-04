import code
import sys

from elm_parser import parse
from elm_types import Program
from llvm_gen import compile_program, run_llvm_ir


def repl():
    while True:
        try:
            input_text = input("> ")
            if not input_text:
                continue
            program = parse(input_text)
            assert isinstance(program, Program)
            llvm_ir = compile_program(program)
            result = run_llvm_ir(llvm_ir)
            print(result)
        except (EOFError, KeyboardInterrupt):
            break


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "python":
        code.interact(local={"repl": repl})
    else:
        repl()


if __name__ == "__main__":
    sys.exit(main())
