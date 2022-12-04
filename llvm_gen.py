from typing import Any

from llvmlite import ir
import llvmlite.binding as lib
from elm_types import BinOp, Literal, Program


class LLVMGenerator:
    def __init__(self):
        self.llvm_ir = ""
        self.__initialize_llvm()

    def __initialize_llvm(self):
        lib.initialize_native_target()
        lib.initialize_native_asmprinter()


    def generate_llvm_ir(self, program: Any) -> str:
        self.__reset_llvm_state()
        self.__visit_program(program)
        return self.llvm_ir

    def __reset_llvm_state(self):
        self.llvm_ir = ""
        self.module = ir.Module()
        self.builder = None
        self.function_name_to_function = {}

    def __visit_program(self, program: Any):
        self.builder = ir.IRBuilder()
        for expression in program.expressions:
            self.__visit_expression(expression)

    def __visit_expression(self, expression: Any):
        method_name = f"__visit_expression_{expression.__class__.__name__}"
        method = getattr(self, method_name, self.__visit_expression_default)
        return method(expression)

    def __visit_expression_default(self, expression: Any):
        raise NotImplementedError(f"No visitor method for {expression}")

    def __visit_expression_Literal(self, expression: Any):
        if isinstance(expression.value, int):
            return self.builder.constant(ir.IntType(64), expression.value)
        elif isinstance(expression.value, float):
            return self.builder.constant(ir.DoubleType(), expression.value)
        elif isinstance(expression.value, str):
            value = expression.value
            string = ir.Constant(ir.ArrayType(ir.IntType(8), len(
                value)), bytearray(value.encode("utf-8")))
            return self.builder.gep(string, [self.builder.constant(ir.IntType(64), 0), self.builder.constant(ir.IntType(64), 0)])
        else:
            raise NotImplementedError(f"No visitor method for {expression}")

    def __visit_expression_Ident(self, expression: Any):
        name = expression.name
        if name in self.function_name_to_function:
            return self.function_name_to_function[name]
        else:
            return self.builder.alloca(ir.IntType(64), name=name)


def __visit_expression_BinOp(self, expression: Any):
    lhs = self.__visit_expression(expression.left)
    rhs = self.__visit_expression(expression.right)
    if expression.op == "+":
        return self.builder.add(lhs, rhs)
    elif expression.op == "-":
        return self.builder.sub(lhs, rhs)
    elif expression.op == "*":
        return self.builder.mul(lhs, rhs)
    elif expression.op == "/":
        return self.builder.sdiv(lhs, rhs)
    elif expression.op == "<":
        return self.builder.icmp_signed("<", lhs, rhs)
    elif expression.op == ">":
        return self.builder.icmp_signed(">", lhs, rhs)
    elif expression.op == "=":
        return self.builder.icmp_signed("==", lhs, rhs)
    else:
        raise NotImplementedError(f"No visitor method for {expression}")


def __visit_expression_UnOp(self, expression: Any):
    operand = self.__visit_expression(expression.operand)
    if expression.op == "-":
        return self.builder.neg(operand)
    elif expression.op == "not":
        return self.builder.not_(operand)
    else:
        raise NotImplementedError(f"No visitor method for {expression}")


def __visit_expression_Let(self, expression: Any):
    names = expression.names
    values = [self.__visit_expression(expr)
              for expr in expression.expressions]
    for name, value in zip(names, values):
        self.builder.store(value, self.builder.alloca(
            ir.IntType(64), name=name))
    return self.__visit_expression(expression.body)


def __visit_expression_LetRec(self, expression: Any):
    for func in expression.functions:
        self.__visit_function(func)
    return self.__visit_expression(expression.body)


def __visit_function(self, func: Any):
    function_type = ir.FunctionType(ir.IntType(
        64), [ir.IntType(64)] * len(func.arguments))
    function = ir.Function(self.module, function_type, func.name)
    self.function_name_to_function[func.name] = function

    bb_entry = function.append_basic_block(name="entry")
    self.builder = ir.IRBuilder(bb_entry)

    for arg, name in zip(function.args, func.arguments):
        self.builder.store(arg, self.builder.alloca(
            ir.IntType(64), name=name))

    self.__visit_expression(func.body)

    if isinstance(function.terminator, ir.Terminator):
        return

    retval = self.__visit_expression(Literal(0))
    self.builder.ret(retval)

    self.builder.ret(retval)

    def __visit_expression_FunctionCall(self, expression: Any):
        function = self.__visit_expression(expression.function)
        arguments = [self.__visit_expression(
            arg) for arg in expression.arguments]
        return self.builder.call(function, arguments)

    def __visit_expression_Match(self, expression: Any):
        match_value = self.__visit_expression(expression.expr)

        for case in expression.cases:
            with self.builder.if_then(
                self.__visit_expression(
                    BinOp(case.pattern, "=", expression.expr)
                )
            ) as (then, _):
                self.builder = then
                self.__visit_expression(case.body)
                return

    def __finalize_llvm(self):
        self.llvm_ir = str(self.module)


def run_llvm_ir(llvm_ir: str) -> float:
    # compile the llvm ir
    llvm_ir = bytes(llvm_ir, "utf8")
    module = lib.add_global("main_module")
    lib.LLVMParseIR(module, llvm_ir, len(llvm_ir), lib.ffi.NULL)

    # verify the module
    error = lib.ffi.new("char **")
    if lib.LLVMVerifyModule(module, lib.LLVMReturnStatusAction, error):
        raise ValueError(lib.ffi.string(error[0]).decode("utf8"))

    # optimize the module
    pass_manager = lib.LLVMCreatePassManager()
    lib.LLVMAddConstantPropagationPass(pass_manager)
    lib.LLVMAddInstructionCombiningPass(pass_manager)
    lib.LLVMAddPromoteMemoryToRegisterPass(pass_manager)
    lib.LLVMAddGVNPass(pass_manager)
    lib.LLVMAddCFGSimplificationPass(pass_manager)
    lib.LLVMRunPassManager(pass_manager, module)

    # create a JIT engine
    engine = lib.LLVMCreateJITCompilerForModule(module, 2)

    # create a function pointer
    function_ptr = lib.LLVMGetPointerToGlobal(
        engine, lib.LLVMGetNamedFunction(module, b"main"))
    function_ptr = lib.ffi.cast("double (*)()", function_ptr)

    # run the function and return its result
    result = function_ptr()
    # dispose of the JIT engine
    lib.LLVMDisposeExecutionEngine(engine)
    # dispose of the module
    lib.LLVMDisposeModule(module)
    return result


def compile_program(program: Program) -> str:
    generator = LLVMGenerator()
    generator.visit_program(program)
    return str(generator.module)
