# Синтаксис языка

```ebnf
program ::= line , [ "\n" , program ]

line ::= line_instruction | line_variable | line_org

line_instruction ::= [ label , ":" , spacing] , instruction

label ::= word

instruction ::= instruction_name , spacing , instruction_arg

spacing ::= "\t" , " "

instruction_name ::=  | "LD"
                      | "ST"
                      | "ADD"
                      | "SUB"
                      | "CMP"
                      | "JMP"

instruction_arg ::= (addressation_direct , label) | (addressation_load_number , number)

addressation_direct ::= ""
addressation_load_number ::= "#"



line_variable ::= [ label , ":" , spacing ] , variable_type , spacing , variable_value
variable_type ::= "word" | "cstr";
variable_value ::= number | ( "'" , word , "'" )



line_org ::= "ORG" , spacing , positive_number

letter ::= "A" | "B" | ....;
word = letter , [ word ]
digit ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
positive_number ::= digit , [ positive_number ]
number ::= [ "+" | "-" ] | positive_number

```
