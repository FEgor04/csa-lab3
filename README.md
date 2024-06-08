# csa-lab3

- Федоров Егор Владимирович. Группа P3215, ISU 367581
- `asm | acc | neum | hw | instr | struct | stream | mem | cstr | prob1`

## Синтаксис языка

```ebnf
program ::= line , [ "\n" , program ]

line ::= line_instruction | line_variable

line_variable ::= "VAR" , spacing , (LABEL | number | ("'", word_of_letters_and_digits, "'"))

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
