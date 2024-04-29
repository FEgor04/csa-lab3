"""Файл с описанием архитекутуры инструкций (и псевдо-инструкций)
"""

from enum import Enum
from collections import namedtuple

class Opcode(str, Enum):
    """Opcode инструкций (и псевдоинструкций).

    Можно разделить на два типа:
    1. Непосредственнно инструкции (ADD, SUB, etc.)
    2. Управление процессом выполнения (JMP, JZ, etc.)
    """
    ADD="add"
    SUB="sub"
    LD="ld"
    ST="st"
    JMP="jmp"
    JZ="jz"
    HLT="hlt"

    def __str__(self: Opcode):
        return str(self.value)
    

class Insturction(NamedTuple):
    """Инструкция
    `opcode` - опкод инструкции
    `arg` - аргумент инструкции (опционален)
    """
    opcode: Opcode
    arg: int | None
