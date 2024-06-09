# csa-lab3

- Федоров Егор Владимирович. Группа P3215, ISU 367581
- `asm | acc | neum | hw | instr | struct | stream | mem | cstr | prob1`

## Синтаксис языка

```ebnf
program ::= line , [ "\n" , program ]

line ::= line_instruction | line_variable

line_variable ::= "VAR" , spacing , var_argument
var_argument ::= LABEL | number | ("'", word_of_letters_and_digits, "'")

line_instruction ::= [ label , ":" , spacing ] , instruction

label ::= word_of_letters_and_digits

instruction ::= instruction_name , spacing , instruction_arg

spacing ::= "\t" , " " , [ spacing ]

instruction_name ::=  | "LD"
                      | "ST"
                      | "ADD"
                      | "SUB"
                      | "MUL"
                      | "DIV"
                      | "MOD"
                      | "CMP"
                      | "JMP"
                      | "JZ"
                      | "HLT"

instruction_arg ::= 
    | (label | positive_number)
    | (addressation_direct_left, (label | number | literal), addressation_direct_right)
    | (addressation_indirect_left, (label | number | literal), addressation_indirect_right)

addressation_direct_left = "("
addressation_direct_right = ")"

addressation_indirect_left = "["
addressation_indirect_right = "]"

word_of_lettrs_and_digits := letter_or_digit , [ word_of_letters_and_digits ]
word_of_letters := letter , [ word_of_letters ]

number ::= [ "+" | "-" ] | positive_number
positive_number ::= digit , [ positive_number ]

literal ::= "'" , letter , "'"
letter_or_digit ::= letter | digit
lettter ::= "a-z" | "A-Z"
digit ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

## Семантика языка

Стратегия вычислений - последовательная. Метки имеют глобальную область видимости.
Переопределение меток недопустимо. (*TODO: добавить тест на это*)
Поддерживается исключительно целочисленный тип.
При выводе / вводе значения преобразовываются в символьный тип по коду `UTF-8`.
Также поддерживаются литералы как аргументы инструкций. Тогда вместо них
будет использован их код `UTF-8`. В случае с псевдо-инструкцией
`VAR` поддерживаются литералы из нескольких символов.
В таком случае они будут преобразованы в набор литералов длины 1.
(`VAR 'hello' -> VAR 'h', VAR 'e', ..., VAR 'o', VAR 0`)

Выполнение инструкций начинается с инструкции, имеющей метку `START` или
с самой первой ячейки памяти, если метка `START` отсутствует.

## Организация памяти

Архитектура фон Неймана, память хранится в массиве длины 2048.
Индексация начинатся с 0.
Размер машинного слова неопределен.
Последние две ячейки памяти выделены под ввод и вывод соответственно.
| Memory  |
|----------|
| 0    |
| 1    |
| ...    |
| 2046 = Input    |
| 2047 = Output    |

## ISA

### Режимы адрессации

- Непосредственная (immediate) - операнд содержится в аргументе инструкции.
`operand = arg`.
На address fetch и operand fetch не нужны дополнительные такты.
Пример: `LD 42` загрузит в аккумулятор число 42.
`LD 'a'` загрузит в аккумулятор код символа `'a'`.

- Прямая (direct) - операнд содержится в памяти по аргуметну инструкции.
`operand = memory[arg]`.
На operand fetch необходим дополнительный такт.
Пример: `LD (HELLO)` загрузит в аккумулятор содержимое ячейки с меткой HELLO.
`LD (4)` загрузит в аккумулятор ячейку с индексом 4.

- Косвенная (indirect) - `operand = memory[memory[arg]]`.
Необходимо два дополнительных такта.

### Кодирование

Программа кодируется в JSON.
Итоговый json-файл содержит два ключа: `pc` и `instructions`.
`pc` содержит адрес, на который должен быть установлен program counter при
старте программы, `instructions` содержит массив инструкций, которые
должны быть загружены в память при запуске.
Инструкции будут загружены начиная с нулевой ячейки.

## Транслятор

TODO

## Модель процессора

Реализовано в модуле [machine.py](./src/machine.py).

Интерфейс командной строки:

```bash
python3 machine.py <code_file> <input_file> <debug: true | false>
```

- Ключ `debug` отвечает за количество информации, показываемой в логах.
Если поставить его на `false`, то в логах будет только информация по окончании
каждой инструкции.
Если поставить его на `true`,
то в логах также будет информация о сигналах и тактах в процессоре.

### DataPath

![DataPath scheme](./docs/schemes/datapath.svg)

Реализован в классе `DataPath`. АЛУ отдельно вынесен в класс `ALU` в модуле [alu](./src/alu.py).

#### Сигналы DataPath

- `latch_acc` - защелкивает в аккумуляторе выбранное значение
- `latch_ar` - защелкивает в adress register выбранное значение
- `latch_memory_write` - защелкивает в памяти по адресу `address register`
значение с выхода ALU
- `alu_operation` - выбор операции ALU.
Возможные опции: ADD, SUB, MUL, DIV, MOD, CMP
- `alu_modifier` - выбор модификатора ALU, возможные опции:
+1, -1, инверсия левого/правого входа

#### Флаги DataPath

- `Z` - наличие нуля на выходе ALU
- `N` - выход ALU < 0

#### Тестирование DataPath

Для DataPath также реализованы unit-тесты в файле [datapath_test](./src/datapath_test.py).
На данный момент в нем тестируются только операции чтения / записи в память.
Для ALU реализованы unit-тесты в файле [alu_test](./src/alu_test.py).
В них тестируется обработка операций и модификаторов АЛУ.

### Control Unit

![Control Unit scheme](./docs/schemes/cu.svg)

Реализован в классе `ControlUnit`.
Метод `decode_and_execute` реализует цикл исполнения инструкции.
На нем:

- инструкция загружается в регистр `program` за 1 такт (метод `program_fetch`)
- адрес операнда загружается в `AR` за 0 или 1 такт (метод `address_fetch`)
- операнд загружается в регистр `MEM_OUT` за 0 или 1 такт
(метод `operand_fetch`)
- инструкция исполняется за 1 такт (метод `execute`).
Для разных типов инструкций (память, арифметика, контроль потока выполнения)
реализованы разные методы

#### Сигналы CU

- `latch_pc` - защелкивает значение `pc`
- `latch_program` - защелкивает текущую инструкцию

#### Тестирование CU

Control unit тестируется как golden тестами, так и дополнительно интеграционными
тестами в файле [integration_test](./src/integration_test.py) и unit-тестами в
файле [control_unit_test](./src/control_unit_test.py).
В интеграционных тестах тестируется работа control unit на программах
(например, вывод `hello world`), в unit тестах тестируется работа control unit
на разных этапах исполнения инструкций.
