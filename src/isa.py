"""Файл с описанием архитекутуры инструкций (и псевдо-инструкций)"""

from enum import Enum
from typing import NamedTuple
import json


class Opcode(str, Enum):
    """Opcode инструкций (и псевдоинструкций).

    Можно разделить на два типа:
    1. Непосредственнно инструкции (ADD, SUB, etc.)
    2. Управление процессом выполнения (JMP, JZ, etc.)
    3. Псевдоинструкция только для транслятора (VAR)
    """

    # Arithmetics
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"
    CMP = "cmp"
    # Memory
    LD = "ld"
    ST = "st"
    # Control
    JMP = "jmp"
    JZ = "jz"
    HLT = "hlt"
    # псевдоинструкция для хранения данных. выделяет блок в одно слово и заполняет укзаанным литералом / числом.
    # если используется как `var 'длинная строка'`, то создает  (|s|+1) слов в памяти, последнее из которых - 0
    VAR = "var"

    def __str__(self):
        return str(self.value)


class Addressing(str, Enum):
    # Операнд - аргумент
    # Пример: `LD 10` - загружает число 10 в аккумулятор
    IMMEDIATE = "immediate"
    # Операнд - `memory[ARG]`
    # Пример: `LD (10)` - загружает содержимое ячейки памяти с адресом 10 в аккумулятор
    # `LD (KEK1)` - загружает содержимое ячейки памяти с меткой `KEK1`
    DIRECT = "direct"
    # Операнд - `memory[memory[ARG]]`
    # Пример: `LD [INDEX]` - загружает в память значение ячейки памяти, чей адрес хранится в ячейке памяти с меткой INDEX.
    # Если `memory[index] = 10`, то `LD [INDEX]` эквивалентен LD (10)
    INDIRECT = "indirect"


class Instruction(NamedTuple):
    """Инструкция
    `opcode` - опкод инструкции
    `arg` - аргумент инструкции (опционален)
    """

    opcode: Opcode
    arg: int | None
    addressing: Addressing | None = Addressing.IMMEDIATE


def read_json(input: str):
    code = json.loads(input)
    instructions_raw = code["instructions"]
    pc = code["pc"]
    instructions: list[Instruction] = []
    for opcode, arg, addressing in instructions_raw:
        instructions += [
            Instruction(
                Opcode[opcode.upper()],
                arg,
                Addressing[addressing.upper()]
                if addressing is not None
                else addressing,
            )
        ]
    return instructions, pc
