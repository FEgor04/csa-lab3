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
