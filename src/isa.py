"""Файл с описанием архитекутуры инструкций (и псевдо-инструкций)
"""

from enum import Enum
from typing import NamedTuple

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

    def __str__(self):
        return str(self.value)
    

class Instruction(NamedTuple):
    """Инструкция
    `opcode` - опкод инструкции
    `arg` - аргумент инструкции (опционален)
    """
    opcode: Opcode
    arg: int | None
