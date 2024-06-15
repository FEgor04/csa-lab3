# csa-lab3

- Федоров Егор Владимирович. Группа P3215, ISU 367581
- `asm | acc | neum | hw | instr | struct | stream | mem | cstr | prob1`

## Синтаксис языка

```ebnf
program ::= line , [ "\n" , program ]

line ::= line_instruction | line_variable | line_comment

line_comment ::= ";" , <anything>

line_variable ::= "VAR" , spacing , var_argument , [ "#", <anything> ]
var_argument ::= LABEL | number | string_literal

line_instruction ::= [ label , ":" , spacing ] , instruction , [ "#", <anything> ]

label ::= word_of_letters_and_digits

instruction ::= instruction_name , [spacing , instruction_arg]

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
    | (label | number | char_literal)
    | (addressation_direct_left, (label | number | char_literal), addressation_direct_right)
    | (addressation_indirect_left, (label | number | char_literal), addressation_indirect_right)

addressation_direct_left = "("
addressation_direct_right = ")"

addressation_indirect_left = "["
addressation_indirect_right = "]"

string_literal ::= "'", word_of_letters_and_digits, "'"
char_literal ::= "'" , letter , "'"

word_of_letters_and_digits := letter_or_digit , [ word_of_letters_and_digits ]
word_of_letters := letter , [ word_of_letters ]

number ::= [ "+" | "-" ] | positive_number
positive_number ::= digit , [ positive_number ]

letter_or_digit ::= letter | digit
lettter ::= "a-z" | "A-Z"
digit ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

## Семантика языка

Стратегия вычислений - последовательная. Метки имеют глобальную область видимости.
Переопределение меток недопустимо.
Поддерживается исключительно целочисленный тип.
При выводе / вводе значения преобразовываются в символьный тип по коду `UTF-8`.
Также поддерживаются строковые литералы как аргументы инструкций. Тогда вместо них
будет использован их код `UTF-8`. В случае с псевдо-инструкцией
`VAR` поддерживаются строковые литералы из нескольких символов.
В таком случае они будут преобразованы в набор литералов длины 1.
(`VAR 'hello' -> VAR 'h', VAR 'e', ..., VAR 'o', VAR 0`).
Литералы из одного символа также будут преобразованы. (`VAR 'h' -> VAR 'h', VAR 0`).

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

### Инструкции

#### LD

Загружает операнд в аккумулятор.
Не меняет значения флагов ALU.

Примеры

- `LD 42` загрузит в аккумулятор число 42.
- `LD 'a'` загрузит в аккумулятор код символа `a` (97)
- `LD (4)` загрузит в аккумулятор содержимое 4-й ячейки
- `LD HELLO` загрузит в аккумулятор номер инструкции с меткой HELLO
- `LD (HELLO)` загрузит в аккумулятор содержимое инструкции с меткой HELLO
- `LD [HELLO]` загрузит в аккумулятор ячейку, адрес которой лежит в ячейке
с меткой HELLO

#### ST

Сохраняет значение аккумулятора в ячейку с адресом операнда.

Примеры

- `ST 42` сохранит аккумулятор в ячейку с индексом 42.
- `ST HELLO` сохранит аккумулятор в ячейку с меткой HELLO.
- `ST (4)` сохранит аккумулятор в ячейку,
адрес которой лежит в ячейке с индексом 4
- `ST (HELLO)` сохранит аккумулятор в ячейку,
адрес которой лежит в ячейке с меткой HELLO

#### ADD

Добавляет к аккумулятору операнд и сохраняет в аккумулятор. Обновляет флаги.

#### SUB

Вычитает из аккумулятора операнд и сохраняет в аккумулятор. Обновляет флаги.

#### MUL

Умножает аккумулятор на операнд и сохраняет в аккумулятор. Обновляет флаги.

#### DIV

Целочисленно делит аккумулятор на операнд и сохраняет в аккумулятор.
Обновляет флаги.

#### MOD

Сохраняет в аккумулятор остаток от деления аккумулятора на операнд. Обновляет флаги.

#### CMP

Выставляет флаги ALU по операции `аккумулятор - операнд`.
Не обновляет значение на выходе АЛУ.

#### JMP

Безусловный переход. Устанавливает PC на операнд.

#### JZ

Условный переход. Если установлен флаг `Z`,
то устанавливает значение PC на операнд, иначе - на PC + 1.

#### HLT

Останов

#### VAR

Псевдо-инструкция для выделения памяти.
Представляет из себя одну ячейку в памяти.

Примеры:

- `VAR 42` - ячейка памяти, содержащая число 42
- `VAR 'a'` - ячейка памяти, содержащая код символа `a` (97).
Транслятором также в конце будет добавлен null-термниатор, то есть
инструкция `VAR 'a'` будет преобразована в две инструкции `VAR 'a'` и `VAR 0`.

### Кодирование

Программа кодируется в JSON.
Итоговый json-файл содержит два ключа: `pc` и `instructions`.
`pc` содержит адрес, на который должен быть установлен program counter при
старте программы, `instructions` содержит массив инструкций, которые
должны быть загружены в память при запуске.
Инструкции будут загружены начиная с нулевой ячейки.

Пример скомпилированного файла:

```bash
python3 src/translator.py examples/hello_username.asm compiled.json
```

```json
{
  "pc": 3,
  "instructions": [
    [
      "var",
      0,
      "immediate"
    ],
    [
      "var",
      0,
      "immediate"
    ],
    ...
  ]
}
```

## Транслятор

Реализован в модуле [translator](./src/translator.py).
Интерфейс командной строки:

```bash
python3 src/translator.py <input_file> <target_file>
```

Этапы трансляции:

1. Расширение инструкций вида `LABEL: VAR 'hello'` в набор последовательных
инструкций вида `LABEL: VAR 'h', VAR 'e', ..., VAR 'o', VAR 0`.
2. Разбор меток
3. Парсинг инструкций и дальнейший перевод их в `json`

### Тестирование транслятора

Для транслятора на все его этапы написаны unit тесты в
файле [translator_test](./src/translator_test.py).
Также транслятор тестируется в golden тестах.

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

## Тестирование

### Разработанные тесты

- Golden тесты: [сами тесты](./src/golden), [golden_test](./src/golden_test.py).
Для всех тестов, кроме `prob1` включен debug режим
(отображение всего, что происходит в процессоре),
для теста `prob1` генерировался слишком большой yml файл (> 4 Мб),
было принято решение не заливать такое в git.
- Интеграционные тесты в файле [integration_test](./src/integration_test.py).
Отличаются от golden тестов тем, что

1) код вводится через массив строк
2) в некоторых тестах используется прямой доступ к памяти через `data_path.memory`.

- Unit-тесты. Реализованы unit-тесты для [control unit](#тестирование-cu),
[data path](#тестирование-DataPath) и
[транслятора](#тестирование-транслятора).

### CI

Был настроен CI для запуска всех тестов ([python.yml](./.github/workflows/python.yml)),
линтера ruff и проверки типов mypy.
Также был настроен линтер для Markdown ([markdown.yml](./.github/workflows/markdown.yml)).

### Реализованные алгоритмы

- `cat`. Реализован в [cat.asm](./examples/cat.asm),
golden тест: [cat.yml](./src/golden/cat.yml)
- `hello`. Реализован в [hello.asm](./examples/hello.asm),
golden тест: [hello.yml](./src/golden/hello.yml)
- `hello_username`. Реализован в [hello_name.asm](./examples/hello_username.asm),
golden тест: [hello_username](./src/golden/hello_name.yml)
- `prob1`. Реализован в [prob1.asm](./examples/prob1.asm),
golden тест: [prob1.yml](./src/golden/prob1.yml)

### Пример работы

Рассмотрим работу транслятора и процессора на примере алгоритма `cat`.

#### Трансляция

```bash
$ python3 src/translator.py examples/cat.asm compiled.json

Input file LoC: 6
Code instr: 6
```

#### Запуск

```bash
$ cat input.txt
Hello!

$ python3 src/machine.py compiled.json input.txt true
```

#### Журнал

```text
DataPath        DEBUG   acc:     0, ar:    0, alu:     0, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:     0, ar:    0, alu:     0, mem_out:     0                                Reading memory on AR #0
DataPath        DEBUG   acc:     0, ar:    0, alu:     0, mem_out:  2046                                MEM_OUT <- MEM[0]
ControlUnit     DEBUG   PC:    0, tick:      1, instr:     0, acc:     0, mem_out:  2046, ar:    0      tick!
DataPath        DEBUG   acc:     0, ar: 2046, alu:     0, mem_out:  2046                                AR <- MEM_OUT
DataPath        DEBUG   acc:     0, ar: 2046, alu:     0, mem_out:  2046                                Reading memory on AR #2046
DataPath        INFO    acc:     0, ar: 2046, alu:     0, mem_out:  2046                                Input: 'H' (72)
DataPath        DEBUG   acc:     0, ar: 2046, alu:     0, mem_out:    72                                MEM_OUT <- 'H' (72)
ControlUnit     DEBUG   PC:    0, tick:      2, instr:     0, acc:     0, mem_out:    72, ar: 2046      tick!
DataPath        DEBUG   acc:    72, ar: 2046, alu:     0, mem_out:    72                                ACC <- MEM_OUT
ControlUnit     DEBUG   PC:    1, tick:      2, instr:     0, acc:    72, mem_out:    72, ar: 2046      PC <- PC + 1
ControlUnit     DEBUG   PC:    1, tick:      3, instr:     0, acc:    72, mem_out:    72, ar: 2046      tick!
ControlUnit     INFO    PC:    1, tick:      3, instr:     1, acc:    72, mem_out:    72, ar: 2046      Executed instruction `ld (2046)` in 3 ticks
DataPath        DEBUG   acc:    72, ar:    1, alu:     0, mem_out:    72                                AR <- PC
DataPath        DEBUG   acc:    72, ar:    1, alu:     0, mem_out:    72                                Reading memory on AR #1
DataPath        DEBUG   acc:    72, ar:    1, alu:     0, mem_out:  2047                                MEM_OUT <- MEM[1]
ControlUnit     DEBUG   PC:    1, tick:      4, instr:     1, acc:    72, mem_out:  2047, ar:    1      tick!
DataPath        DEBUG   acc:    72, ar: 2047, alu:     0, mem_out:  2047                                AR <- MEM_OUT
DataPath        DEBUG   acc:    72, ar: 2047, alu:    72, mem_out:  2047                                Writing to memory on AR #2047
DataPath        INFO    acc:    72, ar: 2047, alu:    72, mem_out:  2047                                Output: 'H' (72)
ControlUnit     DEBUG   PC:    2, tick:      4, instr:     1, acc:    72, mem_out:  2047, ar: 2047      PC <- PC + 1
ControlUnit     DEBUG   PC:    2, tick:      5, instr:     1, acc:    72, mem_out:  2047, ar: 2047      tick!
ControlUnit     INFO    PC:    2, tick:      5, instr:     2, acc:    72, mem_out:  2047, ar: 2047      Executed instruction `st 2047` in 2 ticks
DataPath        DEBUG   acc:    72, ar:    2, alu:    72, mem_out:  2047                                AR <- PC
DataPath        DEBUG   acc:    72, ar:    2, alu:    72, mem_out:  2047                                Reading memory on AR #2
DataPath        DEBUG   acc:    72, ar:    2, alu:    72, mem_out:     0                                MEM_OUT <- MEM[2]
ControlUnit     DEBUG   PC:    2, tick:      6, instr:     2, acc:    72, mem_out:     0, ar:    2      tick!
ControlUnit     DEBUG   PC:    3, tick:      6, instr:     2, acc:    72, mem_out:     0, ar:    2      PC <- PC + 1
ControlUnit     DEBUG   PC:    3, tick:      7, instr:     2, acc:    72, mem_out:     0, ar:    2      tick!
ControlUnit     INFO    PC:    3, tick:      7, instr:     3, acc:    72, mem_out:     0, ar:    2      Executed instruction `cmp 0` in 2 ticks
DataPath        DEBUG   acc:    72, ar:    3, alu:    72, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:    72, ar:    3, alu:    72, mem_out:     0                                Reading memory on AR #3
DataPath        DEBUG   acc:    72, ar:    3, alu:    72, mem_out:     5                                MEM_OUT <- MEM[3]
ControlUnit     DEBUG   PC:    3, tick:      8, instr:     3, acc:    72, mem_out:     5, ar:    3      tick!
ControlUnit     DEBUG   PC:    4, tick:      8, instr:     3, acc:    72, mem_out:     5, ar:    3      PC <- PC + 1
ControlUnit     DEBUG   PC:    4, tick:      9, instr:     3, acc:    72, mem_out:     5, ar:    3      tick!
ControlUnit     INFO    PC:    4, tick:      9, instr:     4, acc:    72, mem_out:     5, ar:    3      Executed instruction `jz 5` in 2 ticks
DataPath        DEBUG   acc:    72, ar:    4, alu:    72, mem_out:     5                                AR <- PC
DataPath        DEBUG   acc:    72, ar:    4, alu:    72, mem_out:     5                                Reading memory on AR #4
DataPath        DEBUG   acc:    72, ar:    4, alu:    72, mem_out:     0                                MEM_OUT <- MEM[4]
ControlUnit     DEBUG   PC:    4, tick:     10, instr:     4, acc:    72, mem_out:     0, ar:    4      tick!
ControlUnit     DEBUG   PC:    0, tick:     10, instr:     4, acc:    72, mem_out:     0, ar:    4      PC <- MEM_OUT
ControlUnit     DEBUG   PC:    0, tick:     11, instr:     4, acc:    72, mem_out:     0, ar:    4      tick!
ControlUnit     INFO    PC:    0, tick:     11, instr:     5, acc:    72, mem_out:     0, ar:    4      Executed instruction `jmp 0` in 2 ticks
DataPath        DEBUG   acc:    72, ar:    0, alu:    72, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:    72, ar:    0, alu:    72, mem_out:     0                                Reading memory on AR #0
DataPath        DEBUG   acc:    72, ar:    0, alu:    72, mem_out:  2046                                MEM_OUT <- MEM[0]
ControlUnit     DEBUG   PC:    0, tick:     12, instr:     5, acc:    72, mem_out:  2046, ar:    0      tick!
DataPath        DEBUG   acc:    72, ar: 2046, alu:    72, mem_out:  2046                                AR <- MEM_OUT
DataPath        DEBUG   acc:    72, ar: 2046, alu:    72, mem_out:  2046                                Reading memory on AR #2046
DataPath        INFO    acc:    72, ar: 2046, alu:    72, mem_out:  2046                                Input: 'e' (101)
DataPath        DEBUG   acc:    72, ar: 2046, alu:    72, mem_out:   101                                MEM_OUT <- 'e' (101)
ControlUnit     DEBUG   PC:    0, tick:     13, instr:     5, acc:    72, mem_out:   101, ar: 2046      tick!
DataPath        DEBUG   acc:   101, ar: 2046, alu:    72, mem_out:   101                                ACC <- MEM_OUT
ControlUnit     DEBUG   PC:    1, tick:     13, instr:     5, acc:   101, mem_out:   101, ar: 2046      PC <- PC + 1
ControlUnit     DEBUG   PC:    1, tick:     14, instr:     5, acc:   101, mem_out:   101, ar: 2046      tick!
ControlUnit     INFO    PC:    1, tick:     14, instr:     6, acc:   101, mem_out:   101, ar: 2046      Executed instruction `ld (2046)` in 3 ticks
DataPath        DEBUG   acc:   101, ar:    1, alu:    72, mem_out:   101                                AR <- PC
DataPath        DEBUG   acc:   101, ar:    1, alu:    72, mem_out:   101                                Reading memory on AR #1
DataPath        DEBUG   acc:   101, ar:    1, alu:    72, mem_out:  2047                                MEM_OUT <- MEM[1]
ControlUnit     DEBUG   PC:    1, tick:     15, instr:     6, acc:   101, mem_out:  2047, ar:    1      tick!
DataPath        DEBUG   acc:   101, ar: 2047, alu:    72, mem_out:  2047                                AR <- MEM_OUT
DataPath        DEBUG   acc:   101, ar: 2047, alu:   101, mem_out:  2047                                Writing to memory on AR #2047
DataPath        INFO    acc:   101, ar: 2047, alu:   101, mem_out:  2047                                Output: 'e' (101)
ControlUnit     DEBUG   PC:    2, tick:     15, instr:     6, acc:   101, mem_out:  2047, ar: 2047      PC <- PC + 1
ControlUnit     DEBUG   PC:    2, tick:     16, instr:     6, acc:   101, mem_out:  2047, ar: 2047      tick!
ControlUnit     INFO    PC:    2, tick:     16, instr:     7, acc:   101, mem_out:  2047, ar: 2047      Executed instruction `st 2047` in 2 ticks
DataPath        DEBUG   acc:   101, ar:    2, alu:   101, mem_out:  2047                                AR <- PC
DataPath        DEBUG   acc:   101, ar:    2, alu:   101, mem_out:  2047                                Reading memory on AR #2
DataPath        DEBUG   acc:   101, ar:    2, alu:   101, mem_out:     0                                MEM_OUT <- MEM[2]
ControlUnit     DEBUG   PC:    2, tick:     17, instr:     7, acc:   101, mem_out:     0, ar:    2      tick!
ControlUnit     DEBUG   PC:    3, tick:     17, instr:     7, acc:   101, mem_out:     0, ar:    2      PC <- PC + 1
ControlUnit     DEBUG   PC:    3, tick:     18, instr:     7, acc:   101, mem_out:     0, ar:    2      tick!
ControlUnit     INFO    PC:    3, tick:     18, instr:     8, acc:   101, mem_out:     0, ar:    2      Executed instruction `cmp 0` in 2 ticks
DataPath        DEBUG   acc:   101, ar:    3, alu:   101, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:   101, ar:    3, alu:   101, mem_out:     0                                Reading memory on AR #3
DataPath        DEBUG   acc:   101, ar:    3, alu:   101, mem_out:     5                                MEM_OUT <- MEM[3]
ControlUnit     DEBUG   PC:    3, tick:     19, instr:     8, acc:   101, mem_out:     5, ar:    3      tick!
ControlUnit     DEBUG   PC:    4, tick:     19, instr:     8, acc:   101, mem_out:     5, ar:    3      PC <- PC + 1
ControlUnit     DEBUG   PC:    4, tick:     20, instr:     8, acc:   101, mem_out:     5, ar:    3      tick!
ControlUnit     INFO    PC:    4, tick:     20, instr:     9, acc:   101, mem_out:     5, ar:    3      Executed instruction `jz 5` in 2 ticks
DataPath        DEBUG   acc:   101, ar:    4, alu:   101, mem_out:     5                                AR <- PC
DataPath        DEBUG   acc:   101, ar:    4, alu:   101, mem_out:     5                                Reading memory on AR #4
DataPath        DEBUG   acc:   101, ar:    4, alu:   101, mem_out:     0                                MEM_OUT <- MEM[4]
ControlUnit     DEBUG   PC:    4, tick:     21, instr:     9, acc:   101, mem_out:     0, ar:    4      tick!
ControlUnit     DEBUG   PC:    0, tick:     21, instr:     9, acc:   101, mem_out:     0, ar:    4      PC <- MEM_OUT
ControlUnit     DEBUG   PC:    0, tick:     22, instr:     9, acc:   101, mem_out:     0, ar:    4      tick!
ControlUnit     INFO    PC:    0, tick:     22, instr:    10, acc:   101, mem_out:     0, ar:    4      Executed instruction `jmp 0` in 2 ticks
DataPath        DEBUG   acc:   101, ar:    0, alu:   101, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:   101, ar:    0, alu:   101, mem_out:     0                                Reading memory on AR #0
DataPath        DEBUG   acc:   101, ar:    0, alu:   101, mem_out:  2046                                MEM_OUT <- MEM[0]
ControlUnit     DEBUG   PC:    0, tick:     23, instr:    10, acc:   101, mem_out:  2046, ar:    0      tick!
DataPath        DEBUG   acc:   101, ar: 2046, alu:   101, mem_out:  2046                                AR <- MEM_OUT
DataPath        DEBUG   acc:   101, ar: 2046, alu:   101, mem_out:  2046                                Reading memory on AR #2046
DataPath        INFO    acc:   101, ar: 2046, alu:   101, mem_out:  2046                                Input: 'l' (108)
DataPath        DEBUG   acc:   101, ar: 2046, alu:   101, mem_out:   108                                MEM_OUT <- 'l' (108)
ControlUnit     DEBUG   PC:    0, tick:     24, instr:    10, acc:   101, mem_out:   108, ar: 2046      tick!
DataPath        DEBUG   acc:   108, ar: 2046, alu:   101, mem_out:   108                                ACC <- MEM_OUT
ControlUnit     DEBUG   PC:    1, tick:     24, instr:    10, acc:   108, mem_out:   108, ar: 2046      PC <- PC + 1
ControlUnit     DEBUG   PC:    1, tick:     25, instr:    10, acc:   108, mem_out:   108, ar: 2046      tick!
ControlUnit     INFO    PC:    1, tick:     25, instr:    11, acc:   108, mem_out:   108, ar: 2046      Executed instruction `ld (2046)` in 3 ticks
DataPath        DEBUG   acc:   108, ar:    1, alu:   101, mem_out:   108                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    1, alu:   101, mem_out:   108                                Reading memory on AR #1
DataPath        DEBUG   acc:   108, ar:    1, alu:   101, mem_out:  2047                                MEM_OUT <- MEM[1]
ControlUnit     DEBUG   PC:    1, tick:     26, instr:    11, acc:   108, mem_out:  2047, ar:    1      tick!
DataPath        DEBUG   acc:   108, ar: 2047, alu:   101, mem_out:  2047                                AR <- MEM_OUT
DataPath        DEBUG   acc:   108, ar: 2047, alu:   108, mem_out:  2047                                Writing to memory on AR #2047
DataPath        INFO    acc:   108, ar: 2047, alu:   108, mem_out:  2047                                Output: 'l' (108)
ControlUnit     DEBUG   PC:    2, tick:     26, instr:    11, acc:   108, mem_out:  2047, ar: 2047      PC <- PC + 1
ControlUnit     DEBUG   PC:    2, tick:     27, instr:    11, acc:   108, mem_out:  2047, ar: 2047      tick!
ControlUnit     INFO    PC:    2, tick:     27, instr:    12, acc:   108, mem_out:  2047, ar: 2047      Executed instruction `st 2047` in 2 ticks
DataPath        DEBUG   acc:   108, ar:    2, alu:   108, mem_out:  2047                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    2, alu:   108, mem_out:  2047                                Reading memory on AR #2
DataPath        DEBUG   acc:   108, ar:    2, alu:   108, mem_out:     0                                MEM_OUT <- MEM[2]
ControlUnit     DEBUG   PC:    2, tick:     28, instr:    12, acc:   108, mem_out:     0, ar:    2      tick!
ControlUnit     DEBUG   PC:    3, tick:     28, instr:    12, acc:   108, mem_out:     0, ar:    2      PC <- PC + 1
ControlUnit     DEBUG   PC:    3, tick:     29, instr:    12, acc:   108, mem_out:     0, ar:    2      tick!
ControlUnit     INFO    PC:    3, tick:     29, instr:    13, acc:   108, mem_out:     0, ar:    2      Executed instruction `cmp 0` in 2 ticks
DataPath        DEBUG   acc:   108, ar:    3, alu:   108, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    3, alu:   108, mem_out:     0                                Reading memory on AR #3
DataPath        DEBUG   acc:   108, ar:    3, alu:   108, mem_out:     5                                MEM_OUT <- MEM[3]
ControlUnit     DEBUG   PC:    3, tick:     30, instr:    13, acc:   108, mem_out:     5, ar:    3      tick!
ControlUnit     DEBUG   PC:    4, tick:     30, instr:    13, acc:   108, mem_out:     5, ar:    3      PC <- PC + 1
ControlUnit     DEBUG   PC:    4, tick:     31, instr:    13, acc:   108, mem_out:     5, ar:    3      tick!
ControlUnit     INFO    PC:    4, tick:     31, instr:    14, acc:   108, mem_out:     5, ar:    3      Executed instruction `jz 5` in 2 ticks
DataPath        DEBUG   acc:   108, ar:    4, alu:   108, mem_out:     5                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    4, alu:   108, mem_out:     5                                Reading memory on AR #4
DataPath        DEBUG   acc:   108, ar:    4, alu:   108, mem_out:     0                                MEM_OUT <- MEM[4]
ControlUnit     DEBUG   PC:    4, tick:     32, instr:    14, acc:   108, mem_out:     0, ar:    4      tick!
ControlUnit     DEBUG   PC:    0, tick:     32, instr:    14, acc:   108, mem_out:     0, ar:    4      PC <- MEM_OUT
ControlUnit     DEBUG   PC:    0, tick:     33, instr:    14, acc:   108, mem_out:     0, ar:    4      tick!
ControlUnit     INFO    PC:    0, tick:     33, instr:    15, acc:   108, mem_out:     0, ar:    4      Executed instruction `jmp 0` in 2 ticks
DataPath        DEBUG   acc:   108, ar:    0, alu:   108, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    0, alu:   108, mem_out:     0                                Reading memory on AR #0
DataPath        DEBUG   acc:   108, ar:    0, alu:   108, mem_out:  2046                                MEM_OUT <- MEM[0]
ControlUnit     DEBUG   PC:    0, tick:     34, instr:    15, acc:   108, mem_out:  2046, ar:    0      tick!
DataPath        DEBUG   acc:   108, ar: 2046, alu:   108, mem_out:  2046                                AR <- MEM_OUT
DataPath        DEBUG   acc:   108, ar: 2046, alu:   108, mem_out:  2046                                Reading memory on AR #2046
DataPath        INFO    acc:   108, ar: 2046, alu:   108, mem_out:  2046                                Input: 'l' (108)
DataPath        DEBUG   acc:   108, ar: 2046, alu:   108, mem_out:   108                                MEM_OUT <- 'l' (108)
ControlUnit     DEBUG   PC:    0, tick:     35, instr:    15, acc:   108, mem_out:   108, ar: 2046      tick!
DataPath        DEBUG   acc:   108, ar: 2046, alu:   108, mem_out:   108                                ACC <- MEM_OUT
ControlUnit     DEBUG   PC:    1, tick:     35, instr:    15, acc:   108, mem_out:   108, ar: 2046      PC <- PC + 1
ControlUnit     DEBUG   PC:    1, tick:     36, instr:    15, acc:   108, mem_out:   108, ar: 2046      tick!
ControlUnit     INFO    PC:    1, tick:     36, instr:    16, acc:   108, mem_out:   108, ar: 2046      Executed instruction `ld (2046)` in 3 ticks
DataPath        DEBUG   acc:   108, ar:    1, alu:   108, mem_out:   108                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    1, alu:   108, mem_out:   108                                Reading memory on AR #1
DataPath        DEBUG   acc:   108, ar:    1, alu:   108, mem_out:  2047                                MEM_OUT <- MEM[1]
ControlUnit     DEBUG   PC:    1, tick:     37, instr:    16, acc:   108, mem_out:  2047, ar:    1      tick!
DataPath        DEBUG   acc:   108, ar: 2047, alu:   108, mem_out:  2047                                AR <- MEM_OUT
DataPath        DEBUG   acc:   108, ar: 2047, alu:   108, mem_out:  2047                                Writing to memory on AR #2047
DataPath        INFO    acc:   108, ar: 2047, alu:   108, mem_out:  2047                                Output: 'l' (108)
ControlUnit     DEBUG   PC:    2, tick:     37, instr:    16, acc:   108, mem_out:  2047, ar: 2047      PC <- PC + 1
ControlUnit     DEBUG   PC:    2, tick:     38, instr:    16, acc:   108, mem_out:  2047, ar: 2047      tick!
ControlUnit     INFO    PC:    2, tick:     38, instr:    17, acc:   108, mem_out:  2047, ar: 2047      Executed instruction `st 2047` in 2 ticks
DataPath        DEBUG   acc:   108, ar:    2, alu:   108, mem_out:  2047                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    2, alu:   108, mem_out:  2047                                Reading memory on AR #2
DataPath        DEBUG   acc:   108, ar:    2, alu:   108, mem_out:     0                                MEM_OUT <- MEM[2]
ControlUnit     DEBUG   PC:    2, tick:     39, instr:    17, acc:   108, mem_out:     0, ar:    2      tick!
ControlUnit     DEBUG   PC:    3, tick:     39, instr:    17, acc:   108, mem_out:     0, ar:    2      PC <- PC + 1
ControlUnit     DEBUG   PC:    3, tick:     40, instr:    17, acc:   108, mem_out:     0, ar:    2      tick!
ControlUnit     INFO    PC:    3, tick:     40, instr:    18, acc:   108, mem_out:     0, ar:    2      Executed instruction `cmp 0` in 2 ticks
DataPath        DEBUG   acc:   108, ar:    3, alu:   108, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    3, alu:   108, mem_out:     0                                Reading memory on AR #3
DataPath        DEBUG   acc:   108, ar:    3, alu:   108, mem_out:     5                                MEM_OUT <- MEM[3]
ControlUnit     DEBUG   PC:    3, tick:     41, instr:    18, acc:   108, mem_out:     5, ar:    3      tick!
ControlUnit     DEBUG   PC:    4, tick:     41, instr:    18, acc:   108, mem_out:     5, ar:    3      PC <- PC + 1
ControlUnit     DEBUG   PC:    4, tick:     42, instr:    18, acc:   108, mem_out:     5, ar:    3      tick!
ControlUnit     INFO    PC:    4, tick:     42, instr:    19, acc:   108, mem_out:     5, ar:    3      Executed instruction `jz 5` in 2 ticks
DataPath        DEBUG   acc:   108, ar:    4, alu:   108, mem_out:     5                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    4, alu:   108, mem_out:     5                                Reading memory on AR #4
DataPath        DEBUG   acc:   108, ar:    4, alu:   108, mem_out:     0                                MEM_OUT <- MEM[4]
ControlUnit     DEBUG   PC:    4, tick:     43, instr:    19, acc:   108, mem_out:     0, ar:    4      tick!
ControlUnit     DEBUG   PC:    0, tick:     43, instr:    19, acc:   108, mem_out:     0, ar:    4      PC <- MEM_OUT
ControlUnit     DEBUG   PC:    0, tick:     44, instr:    19, acc:   108, mem_out:     0, ar:    4      tick!
ControlUnit     INFO    PC:    0, tick:     44, instr:    20, acc:   108, mem_out:     0, ar:    4      Executed instruction `jmp 0` in 2 ticks
DataPath        DEBUG   acc:   108, ar:    0, alu:   108, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:   108, ar:    0, alu:   108, mem_out:     0                                Reading memory on AR #0
DataPath        DEBUG   acc:   108, ar:    0, alu:   108, mem_out:  2046                                MEM_OUT <- MEM[0]
ControlUnit     DEBUG   PC:    0, tick:     45, instr:    20, acc:   108, mem_out:  2046, ar:    0      tick!
DataPath        DEBUG   acc:   108, ar: 2046, alu:   108, mem_out:  2046                                AR <- MEM_OUT
DataPath        DEBUG   acc:   108, ar: 2046, alu:   108, mem_out:  2046                                Reading memory on AR #2046
DataPath        INFO    acc:   108, ar: 2046, alu:   108, mem_out:  2046                                Input: 'o' (111)
DataPath        DEBUG   acc:   108, ar: 2046, alu:   108, mem_out:   111                                MEM_OUT <- 'o' (111)
ControlUnit     DEBUG   PC:    0, tick:     46, instr:    20, acc:   108, mem_out:   111, ar: 2046      tick!
DataPath        DEBUG   acc:   111, ar: 2046, alu:   108, mem_out:   111                                ACC <- MEM_OUT
ControlUnit     DEBUG   PC:    1, tick:     46, instr:    20, acc:   111, mem_out:   111, ar: 2046      PC <- PC + 1
ControlUnit     DEBUG   PC:    1, tick:     47, instr:    20, acc:   111, mem_out:   111, ar: 2046      tick!
ControlUnit     INFO    PC:    1, tick:     47, instr:    21, acc:   111, mem_out:   111, ar: 2046      Executed instruction `ld (2046)` in 3 ticks
DataPath        DEBUG   acc:   111, ar:    1, alu:   108, mem_out:   111                                AR <- PC
DataPath        DEBUG   acc:   111, ar:    1, alu:   108, mem_out:   111                                Reading memory on AR #1
DataPath        DEBUG   acc:   111, ar:    1, alu:   108, mem_out:  2047                                MEM_OUT <- MEM[1]
ControlUnit     DEBUG   PC:    1, tick:     48, instr:    21, acc:   111, mem_out:  2047, ar:    1      tick!
DataPath        DEBUG   acc:   111, ar: 2047, alu:   108, mem_out:  2047                                AR <- MEM_OUT
DataPath        DEBUG   acc:   111, ar: 2047, alu:   111, mem_out:  2047                                Writing to memory on AR #2047
DataPath        INFO    acc:   111, ar: 2047, alu:   111, mem_out:  2047                                Output: 'o' (111)
ControlUnit     DEBUG   PC:    2, tick:     48, instr:    21, acc:   111, mem_out:  2047, ar: 2047      PC <- PC + 1
ControlUnit     DEBUG   PC:    2, tick:     49, instr:    21, acc:   111, mem_out:  2047, ar: 2047      tick!
ControlUnit     INFO    PC:    2, tick:     49, instr:    22, acc:   111, mem_out:  2047, ar: 2047      Executed instruction `st 2047` in 2 ticks
DataPath        DEBUG   acc:   111, ar:    2, alu:   111, mem_out:  2047                                AR <- PC
DataPath        DEBUG   acc:   111, ar:    2, alu:   111, mem_out:  2047                                Reading memory on AR #2
DataPath        DEBUG   acc:   111, ar:    2, alu:   111, mem_out:     0                                MEM_OUT <- MEM[2]
ControlUnit     DEBUG   PC:    2, tick:     50, instr:    22, acc:   111, mem_out:     0, ar:    2      tick!
ControlUnit     DEBUG   PC:    3, tick:     50, instr:    22, acc:   111, mem_out:     0, ar:    2      PC <- PC + 1
ControlUnit     DEBUG   PC:    3, tick:     51, instr:    22, acc:   111, mem_out:     0, ar:    2      tick!
ControlUnit     INFO    PC:    3, tick:     51, instr:    23, acc:   111, mem_out:     0, ar:    2      Executed instruction `cmp 0` in 2 ticks
DataPath        DEBUG   acc:   111, ar:    3, alu:   111, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:   111, ar:    3, alu:   111, mem_out:     0                                Reading memory on AR #3
DataPath        DEBUG   acc:   111, ar:    3, alu:   111, mem_out:     5                                MEM_OUT <- MEM[3]
ControlUnit     DEBUG   PC:    3, tick:     52, instr:    23, acc:   111, mem_out:     5, ar:    3      tick!
ControlUnit     DEBUG   PC:    4, tick:     52, instr:    23, acc:   111, mem_out:     5, ar:    3      PC <- PC + 1
ControlUnit     DEBUG   PC:    4, tick:     53, instr:    23, acc:   111, mem_out:     5, ar:    3      tick!
ControlUnit     INFO    PC:    4, tick:     53, instr:    24, acc:   111, mem_out:     5, ar:    3      Executed instruction `jz 5` in 2 ticks
DataPath        DEBUG   acc:   111, ar:    4, alu:   111, mem_out:     5                                AR <- PC
DataPath        DEBUG   acc:   111, ar:    4, alu:   111, mem_out:     5                                Reading memory on AR #4
DataPath        DEBUG   acc:   111, ar:    4, alu:   111, mem_out:     0                                MEM_OUT <- MEM[4]
ControlUnit     DEBUG   PC:    4, tick:     54, instr:    24, acc:   111, mem_out:     0, ar:    4      tick!
ControlUnit     DEBUG   PC:    0, tick:     54, instr:    24, acc:   111, mem_out:     0, ar:    4      PC <- MEM_OUT
ControlUnit     DEBUG   PC:    0, tick:     55, instr:    24, acc:   111, mem_out:     0, ar:    4      tick!
ControlUnit     INFO    PC:    0, tick:     55, instr:    25, acc:   111, mem_out:     0, ar:    4      Executed instruction `jmp 0` in 2 ticks
DataPath        DEBUG   acc:   111, ar:    0, alu:   111, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:   111, ar:    0, alu:   111, mem_out:     0                                Reading memory on AR #0
DataPath        DEBUG   acc:   111, ar:    0, alu:   111, mem_out:  2046                                MEM_OUT <- MEM[0]
ControlUnit     DEBUG   PC:    0, tick:     56, instr:    25, acc:   111, mem_out:  2046, ar:    0      tick!
DataPath        DEBUG   acc:   111, ar: 2046, alu:   111, mem_out:  2046                                AR <- MEM_OUT
DataPath        DEBUG   acc:   111, ar: 2046, alu:   111, mem_out:  2046                                Reading memory on AR #2046
DataPath        INFO    acc:   111, ar: 2046, alu:   111, mem_out:  2046                                Input: '!' (33)
DataPath        DEBUG   acc:   111, ar: 2046, alu:   111, mem_out:    33                                MEM_OUT <- '!' (33)
ControlUnit     DEBUG   PC:    0, tick:     57, instr:    25, acc:   111, mem_out:    33, ar: 2046      tick!
DataPath        DEBUG   acc:    33, ar: 2046, alu:   111, mem_out:    33                                ACC <- MEM_OUT
ControlUnit     DEBUG   PC:    1, tick:     57, instr:    25, acc:    33, mem_out:    33, ar: 2046      PC <- PC + 1
ControlUnit     DEBUG   PC:    1, tick:     58, instr:    25, acc:    33, mem_out:    33, ar: 2046      tick!
ControlUnit     INFO    PC:    1, tick:     58, instr:    26, acc:    33, mem_out:    33, ar: 2046      Executed instruction `ld (2046)` in 3 ticks
DataPath        DEBUG   acc:    33, ar:    1, alu:   111, mem_out:    33                                AR <- PC
DataPath        DEBUG   acc:    33, ar:    1, alu:   111, mem_out:    33                                Reading memory on AR #1
DataPath        DEBUG   acc:    33, ar:    1, alu:   111, mem_out:  2047                                MEM_OUT <- MEM[1]
ControlUnit     DEBUG   PC:    1, tick:     59, instr:    26, acc:    33, mem_out:  2047, ar:    1      tick!
DataPath        DEBUG   acc:    33, ar: 2047, alu:   111, mem_out:  2047                                AR <- MEM_OUT
DataPath        DEBUG   acc:    33, ar: 2047, alu:    33, mem_out:  2047                                Writing to memory on AR #2047
DataPath        INFO    acc:    33, ar: 2047, alu:    33, mem_out:  2047                                Output: '!' (33)
ControlUnit     DEBUG   PC:    2, tick:     59, instr:    26, acc:    33, mem_out:  2047, ar: 2047      PC <- PC + 1
ControlUnit     DEBUG   PC:    2, tick:     60, instr:    26, acc:    33, mem_out:  2047, ar: 2047      tick!
ControlUnit     INFO    PC:    2, tick:     60, instr:    27, acc:    33, mem_out:  2047, ar: 2047      Executed instruction `st 2047` in 2 ticks
DataPath        DEBUG   acc:    33, ar:    2, alu:    33, mem_out:  2047                                AR <- PC
DataPath        DEBUG   acc:    33, ar:    2, alu:    33, mem_out:  2047                                Reading memory on AR #2
DataPath        DEBUG   acc:    33, ar:    2, alu:    33, mem_out:     0                                MEM_OUT <- MEM[2]
ControlUnit     DEBUG   PC:    2, tick:     61, instr:    27, acc:    33, mem_out:     0, ar:    2      tick!
ControlUnit     DEBUG   PC:    3, tick:     61, instr:    27, acc:    33, mem_out:     0, ar:    2      PC <- PC + 1
ControlUnit     DEBUG   PC:    3, tick:     62, instr:    27, acc:    33, mem_out:     0, ar:    2      tick!
ControlUnit     INFO    PC:    3, tick:     62, instr:    28, acc:    33, mem_out:     0, ar:    2      Executed instruction `cmp 0` in 2 ticks
DataPath        DEBUG   acc:    33, ar:    3, alu:    33, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:    33, ar:    3, alu:    33, mem_out:     0                                Reading memory on AR #3
DataPath        DEBUG   acc:    33, ar:    3, alu:    33, mem_out:     5                                MEM_OUT <- MEM[3]
ControlUnit     DEBUG   PC:    3, tick:     63, instr:    28, acc:    33, mem_out:     5, ar:    3      tick!
ControlUnit     DEBUG   PC:    4, tick:     63, instr:    28, acc:    33, mem_out:     5, ar:    3      PC <- PC + 1
ControlUnit     DEBUG   PC:    4, tick:     64, instr:    28, acc:    33, mem_out:     5, ar:    3      tick!
ControlUnit     INFO    PC:    4, tick:     64, instr:    29, acc:    33, mem_out:     5, ar:    3      Executed instruction `jz 5` in 2 ticks
DataPath        DEBUG   acc:    33, ar:    4, alu:    33, mem_out:     5                                AR <- PC
DataPath        DEBUG   acc:    33, ar:    4, alu:    33, mem_out:     5                                Reading memory on AR #4
DataPath        DEBUG   acc:    33, ar:    4, alu:    33, mem_out:     0                                MEM_OUT <- MEM[4]
ControlUnit     DEBUG   PC:    4, tick:     65, instr:    29, acc:    33, mem_out:     0, ar:    4      tick!
ControlUnit     DEBUG   PC:    0, tick:     65, instr:    29, acc:    33, mem_out:     0, ar:    4      PC <- MEM_OUT
ControlUnit     DEBUG   PC:    0, tick:     66, instr:    29, acc:    33, mem_out:     0, ar:    4      tick!
ControlUnit     INFO    PC:    0, tick:     66, instr:    30, acc:    33, mem_out:     0, ar:    4      Executed instruction `jmp 0` in 2 ticks
DataPath        DEBUG   acc:    33, ar:    0, alu:    33, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:    33, ar:    0, alu:    33, mem_out:     0                                Reading memory on AR #0
DataPath        DEBUG   acc:    33, ar:    0, alu:    33, mem_out:  2046                                MEM_OUT <- MEM[0]
ControlUnit     DEBUG   PC:    0, tick:     67, instr:    30, acc:    33, mem_out:  2046, ar:    0      tick!
DataPath        DEBUG   acc:    33, ar: 2046, alu:    33, mem_out:  2046                                AR <- MEM_OUT
DataPath        DEBUG   acc:    33, ar: 2046, alu:    33, mem_out:  2046                                Reading memory on AR #2046
DataPath        INFO    acc:    33, ar: 2046, alu:    33, mem_out:  2046                                Input: '\n' (10)
DataPath        DEBUG   acc:    33, ar: 2046, alu:    33, mem_out:    10                                MEM_OUT <- '\n' (10)
ControlUnit     DEBUG   PC:    0, tick:     68, instr:    30, acc:    33, mem_out:    10, ar: 2046      tick!
DataPath        DEBUG   acc:    10, ar: 2046, alu:    33, mem_out:    10                                ACC <- MEM_OUT
ControlUnit     DEBUG   PC:    1, tick:     68, instr:    30, acc:    10, mem_out:    10, ar: 2046      PC <- PC + 1
ControlUnit     DEBUG   PC:    1, tick:     69, instr:    30, acc:    10, mem_out:    10, ar: 2046      tick!
ControlUnit     INFO    PC:    1, tick:     69, instr:    31, acc:    10, mem_out:    10, ar: 2046      Executed instruction `ld (2046)` in 3 ticks
DataPath        DEBUG   acc:    10, ar:    1, alu:    33, mem_out:    10                                AR <- PC
DataPath        DEBUG   acc:    10, ar:    1, alu:    33, mem_out:    10                                Reading memory on AR #1
DataPath        DEBUG   acc:    10, ar:    1, alu:    33, mem_out:  2047                                MEM_OUT <- MEM[1]
ControlUnit     DEBUG   PC:    1, tick:     70, instr:    31, acc:    10, mem_out:  2047, ar:    1      tick!
DataPath        DEBUG   acc:    10, ar: 2047, alu:    33, mem_out:  2047                                AR <- MEM_OUT
DataPath        DEBUG   acc:    10, ar: 2047, alu:    10, mem_out:  2047                                Writing to memory on AR #2047
DataPath        INFO    acc:    10, ar: 2047, alu:    10, mem_out:  2047                                Output: '\n' (10)
ControlUnit     DEBUG   PC:    2, tick:     70, instr:    31, acc:    10, mem_out:  2047, ar: 2047      PC <- PC + 1
ControlUnit     DEBUG   PC:    2, tick:     71, instr:    31, acc:    10, mem_out:  2047, ar: 2047      tick!
ControlUnit     INFO    PC:    2, tick:     71, instr:    32, acc:    10, mem_out:  2047, ar: 2047      Executed instruction `st 2047` in 2 ticks
DataPath        DEBUG   acc:    10, ar:    2, alu:    10, mem_out:  2047                                AR <- PC
DataPath        DEBUG   acc:    10, ar:    2, alu:    10, mem_out:  2047                                Reading memory on AR #2
DataPath        DEBUG   acc:    10, ar:    2, alu:    10, mem_out:     0                                MEM_OUT <- MEM[2]
ControlUnit     DEBUG   PC:    2, tick:     72, instr:    32, acc:    10, mem_out:     0, ar:    2      tick!
ControlUnit     DEBUG   PC:    3, tick:     72, instr:    32, acc:    10, mem_out:     0, ar:    2      PC <- PC + 1
ControlUnit     DEBUG   PC:    3, tick:     73, instr:    32, acc:    10, mem_out:     0, ar:    2      tick!
ControlUnit     INFO    PC:    3, tick:     73, instr:    33, acc:    10, mem_out:     0, ar:    2      Executed instruction `cmp 0` in 2 ticks
DataPath        DEBUG   acc:    10, ar:    3, alu:    10, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:    10, ar:    3, alu:    10, mem_out:     0                                Reading memory on AR #3
DataPath        DEBUG   acc:    10, ar:    3, alu:    10, mem_out:     5                                MEM_OUT <- MEM[3]
ControlUnit     DEBUG   PC:    3, tick:     74, instr:    33, acc:    10, mem_out:     5, ar:    3      tick!
ControlUnit     DEBUG   PC:    4, tick:     74, instr:    33, acc:    10, mem_out:     5, ar:    3      PC <- PC + 1
ControlUnit     DEBUG   PC:    4, tick:     75, instr:    33, acc:    10, mem_out:     5, ar:    3      tick!
ControlUnit     INFO    PC:    4, tick:     75, instr:    34, acc:    10, mem_out:     5, ar:    3      Executed instruction `jz 5` in 2 ticks
DataPath        DEBUG   acc:    10, ar:    4, alu:    10, mem_out:     5                                AR <- PC
DataPath        DEBUG   acc:    10, ar:    4, alu:    10, mem_out:     5                                Reading memory on AR #4
DataPath        DEBUG   acc:    10, ar:    4, alu:    10, mem_out:     0                                MEM_OUT <- MEM[4]
ControlUnit     DEBUG   PC:    4, tick:     76, instr:    34, acc:    10, mem_out:     0, ar:    4      tick!
ControlUnit     DEBUG   PC:    0, tick:     76, instr:    34, acc:    10, mem_out:     0, ar:    4      PC <- MEM_OUT
ControlUnit     DEBUG   PC:    0, tick:     77, instr:    34, acc:    10, mem_out:     0, ar:    4      tick!
ControlUnit     INFO    PC:    0, tick:     77, instr:    35, acc:    10, mem_out:     0, ar:    4      Executed instruction `jmp 0` in 2 ticks
DataPath        DEBUG   acc:    10, ar:    0, alu:    10, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:    10, ar:    0, alu:    10, mem_out:     0                                Reading memory on AR #0
DataPath        DEBUG   acc:    10, ar:    0, alu:    10, mem_out:  2046                                MEM_OUT <- MEM[0]
ControlUnit     DEBUG   PC:    0, tick:     78, instr:    35, acc:    10, mem_out:  2046, ar:    0      tick!
DataPath        DEBUG   acc:    10, ar: 2046, alu:    10, mem_out:  2046                                AR <- MEM_OUT
DataPath        DEBUG   acc:    10, ar: 2046, alu:    10, mem_out:  2046                                Reading memory on AR #2046
DataPath        INFO    acc:    10, ar: 2046, alu:    10, mem_out:  2046                                Input: '\x00' (0)
DataPath        DEBUG   acc:    10, ar: 2046, alu:    10, mem_out:     0                                MEM_OUT <- '\x00' (0)
ControlUnit     DEBUG   PC:    0, tick:     79, instr:    35, acc:    10, mem_out:     0, ar: 2046      tick!
DataPath        DEBUG   acc:     0, ar: 2046, alu:    10, mem_out:     0                                ACC <- MEM_OUT
ControlUnit     DEBUG   PC:    1, tick:     79, instr:    35, acc:     0, mem_out:     0, ar: 2046      PC <- PC + 1
ControlUnit     DEBUG   PC:    1, tick:     80, instr:    35, acc:     0, mem_out:     0, ar: 2046      tick!
ControlUnit     INFO    PC:    1, tick:     80, instr:    36, acc:     0, mem_out:     0, ar: 2046      Executed instruction `ld (2046)` in 3 ticks
DataPath        DEBUG   acc:     0, ar:    1, alu:    10, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:     0, ar:    1, alu:    10, mem_out:     0                                Reading memory on AR #1
DataPath        DEBUG   acc:     0, ar:    1, alu:    10, mem_out:  2047                                MEM_OUT <- MEM[1]
ControlUnit     DEBUG   PC:    1, tick:     81, instr:    36, acc:     0, mem_out:  2047, ar:    1      tick!
DataPath        DEBUG   acc:     0, ar: 2047, alu:    10, mem_out:  2047                                AR <- MEM_OUT
DataPath        DEBUG   acc:     0, ar: 2047, alu:     0, mem_out:  2047                                Writing to memory on AR #2047
DataPath        INFO    acc:     0, ar: 2047, alu:     0, mem_out:  2047                                Output: '\x00' (0)
ControlUnit     DEBUG   PC:    2, tick:     81, instr:    36, acc:     0, mem_out:  2047, ar: 2047      PC <- PC + 1
ControlUnit     DEBUG   PC:    2, tick:     82, instr:    36, acc:     0, mem_out:  2047, ar: 2047      tick!
ControlUnit     INFO    PC:    2, tick:     82, instr:    37, acc:     0, mem_out:  2047, ar: 2047      Executed instruction `st 2047` in 2 ticks
DataPath        DEBUG   acc:     0, ar:    2, alu:     0, mem_out:  2047                                AR <- PC
DataPath        DEBUG   acc:     0, ar:    2, alu:     0, mem_out:  2047                                Reading memory on AR #2
DataPath        DEBUG   acc:     0, ar:    2, alu:     0, mem_out:     0                                MEM_OUT <- MEM[2]
ControlUnit     DEBUG   PC:    2, tick:     83, instr:    37, acc:     0, mem_out:     0, ar:    2      tick!
ControlUnit     DEBUG   PC:    3, tick:     83, instr:    37, acc:     0, mem_out:     0, ar:    2      PC <- PC + 1
ControlUnit     DEBUG   PC:    3, tick:     84, instr:    37, acc:     0, mem_out:     0, ar:    2      tick!
ControlUnit     INFO    PC:    3, tick:     84, instr:    38, acc:     0, mem_out:     0, ar:    2      Executed instruction `cmp 0` in 2 ticks
DataPath        DEBUG   acc:     0, ar:    3, alu:     0, mem_out:     0                                AR <- PC
DataPath        DEBUG   acc:     0, ar:    3, alu:     0, mem_out:     0                                Reading memory on AR #3
DataPath        DEBUG   acc:     0, ar:    3, alu:     0, mem_out:     5                                MEM_OUT <- MEM[3]
ControlUnit     DEBUG   PC:    3, tick:     85, instr:    38, acc:     0, mem_out:     5, ar:    3      tick!
ControlUnit     DEBUG   PC:    5, tick:     85, instr:    38, acc:     0, mem_out:     5, ar:    3      PC <- MEM_OUT
ControlUnit     DEBUG   PC:    5, tick:     86, instr:    38, acc:     0, mem_out:     5, ar:    3      tick!
ControlUnit     INFO    PC:    5, tick:     86, instr:    39, acc:     0, mem_out:     5, ar:    3      Executed instruction `jz 5` in 2 ticks
DataPath        DEBUG   acc:     0, ar:    5, alu:     0, mem_out:     5                                AR <- PC
DataPath        DEBUG   acc:     0, ar:    5, alu:     0, mem_out:     5                                Reading memory on AR #5
DataPath        DEBUG   acc:     0, ar:    5, alu:     0, mem_out:     0                                MEM_OUT <- MEM[5]
ControlUnit     DEBUG   PC:    5, tick:     87, instr:    39, acc:     0, mem_out:     0, ar:    5      tick!
Program halted successfully
Hello!

Total instructions 39
Total ticks 87
```

```text
| ФИО                       | алг        | LoC | code байт | code инстр. | инстр. | такт. | вариант                                                              |
| Федоров Егор Владимирович | hello      | 11  | -         | 23          | 99     | 237   | asm | acc | neum | hw | instr | struct | stream | mem | cstr | prob1 |
| Федоров Егор Владимирович | cat        | 6   | -         | 6           | 29     | 65    | asm | acc | neum | hw | instr | struct | stream | mem | cstr | prob1 |
| Федоров Егор Владимирович | hello_name | 49  | -         | 57          | 179    | 433   | asm | acc | neum | hw | instr | struct | stream | mem | cstr | prob1 |
| Федоров Егор Владимирович | prob1      | 42  | -         | 42          | 13063  | 30772 | asm | acc | neum | hw | instr | struct | stream | mem | cstr | prob1 |
```
