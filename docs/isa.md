# Instruction Set Architecture

### Режимы адресации

- Прямая адресация. Напрямую адресует ячейку. Пример: `LD x`.
- Прямая загрузка операнда. Напрямую загружает значение операнда.
Пример: `LD #5` загрузит в аккумулятор число 5.

### Команды

- `LD x` --- загружает в аккумулятор `x`. `x` может быть как адресом ячейки, так и числом (режим прямой загрузки).
Пример использования: `LD adr` - загружает значение, находящееся по адресу `adr`, `LD #5` загружает число 5.
- `ST x` --- сохраняет значение аккумулятора в ячейку `x`.
- TODO

### Псевдо-инструкция
Существует единственная псевдо-инструкция ORG.
Она устанавливает адрес следующей инструкции / переменной на заданный.
Например:
```asm
ORG 100
LD x
ORG 200
A: WORD 5
```
будет транслировано в 2 ячейки памяти:
- ячейка с адресом `100` будет содержать код команды `LD x`.
- ячейка с адресом `200` будет содержать значение `5`.