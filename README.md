# Prolog Parser

Чтобы запустить парсер, нужно передать ему в качестве аргумента имя файла, который мы хотим анализировать.
По желанию, получившееся выражение можно вывести, для этого там есть функция `pr`

Файл test.py содержит внутри себя тесты.

В файле parser.py реализована другая версия парсера. 
### Грамматика для парсера:
```
Rule 0     S' -> prog
Rule 1     prog -> oper POINT prog
Rule 2     prog -> oper POINT
Rule 3     oper -> atom OP disj
Rule 4     oper -> atom
Rule 5     disj -> conj OR disj
Rule 6     disj -> conj
Rule 7     conj -> expression AND conj
Rule 8     conj -> expression
Rule 9     expression -> OBR disj CBR
Rule 10    expression -> atom
Rule 11    atom -> ID
Rule 12    atom -> ID seq_atom
Rule 13    seq_atom -> OBR atom CBR
Rule 14    seq_atom -> ID
Rule 15    seq_atom -> ID seq_atom
```
В связи с этим не допускаются выражения с головным атомом в скобках, в частности, ((b)), он считает, что (b) -- атом, а он должен начинаться с идентификатора.

В качестве параметра программе передается имя файла, который необходимо распарсить. В случае успеха результат выводится в файл с таким же названием и переносом после каждой точки. 
