from enum import Enum


class Signal(int, Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Automatically generates enum values a power of two
        See: https://docs.python.org/3/library/enum.html#enum.Enum._generate_next_value_
        """
        return 2 ** (count + 1)


    # Buffer Register Input
    SEL_BUFFER_IN_ALU_OUT = auto()
    SEL_BUFFER_IN_MEM_OUT = auto()
    LATCH_BUFFER = auto()
    # Accumulator Input
    SEL_ACC_IN_ALU_OUT = auto()
    SEL_ACC_IN_MEM_OUT = auto()
    LATCH_ACC = auto()
    # ALU Inputs
    SEL_ALU_LEFT = auto()
    SEL_ALU_RIGHT = auto()
    # ALU Operations
    ALU_ADD = auto()
    ALU_SUB = auto()
    ALU_MUL = auto()
    ALU_DIV = auto()
    ALU_MOD = auto()
    ALU_INC = auto()
    ALU_DEC = auto()
    # Memory
    SEL_AR_IN_OPERAND = auto()
    SEL_AR_IP_ADDR = auto()
    LATCH_AR = auto()
    LATCH_MEMORY_WRITE = auto()


