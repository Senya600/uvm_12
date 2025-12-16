# UVM на допуск (Вариант №12)
## Описание проекта<br>
Проект реализует учебную виртуальную машину (УВМ) для варианта №12, а также полный набор инструментов для работы с ней:

Ассемблер — преобразует программу, заданную в JSON-формате, в бинарный код УВМ

Интерпретатор — исполняет бинарный код и формирует дамп памяти

GUI-приложение (desktop и web) — позволяет писать, ассемблировать и запускать программы 

Тестовые программы и дампы памяти — демонстрируют корректность вычислений
## Язык ассемблера УВМ
Программа для УВМ задаётся в JSON-формате.<br>
Каждая инструкция описывается объектом со следующими полями:<br>
{<br>
  "op": "имя_операции",<br>
  "B": число,<br>
  "C": число,<br>
  "D": число<br>
}
## Поддерживаемые инструкции
1. Загрузка константы в память. load_const <br>
Формат: { "op": "load_const", "B": B, "C": C }<br>
Описание: memory[B] = C.<br>
2. Чтение значения из памяти по адресу. read_value<br>
Формат: { "op": "read_value", "B": B, "C": C, "D": D }<br>
Описание:<br>
addr = memory[B] + D<br>
memory[C] = memory[addr]<br>
3. Запись значения в память. write_value<br>
Формат: { "op": "write_value", "B": B, "C": C }<br>
Описание: memory[C] = memory[B]
4. Возведение в степень. pow<br>
Формат: { "op": "pow", "B": B, "C": C, "D": D }<br>
Описание: <br>
base = memory[D]<br>
exp  = memory[ memory[B] ]<br>
memory[C] = base ^ exp

| Команда     | Размер  | Описание кодирования |
| ----------- | ------- | -------------------- |
| load_const  | 4 байта | opcode + B + C       |
| read_value  | 4 байта | opcode + B + C + D   |
| write_value | 4 байта | opcode + B + C       |
| pow         | 4 байта | opcode + B + C + D   |


## Структура проекта
uvm-project/<br>
│<br>
├── json/                 # Исходные .json программы<br>
├── bin/                  # Скомпилированные .bin файлы<br>
├── dump/                # Дамп памяти после выполнения программ (.csv)<br>
│<br>
├── uvm_asm.py            # Ассемблер<br>
├── uvm_interp.py         # Интерпретатор<br>
├── uvm_gui.py            # GUI<br>
├── uvm_gui_web.py        # Web GUI<br>
├── templates/<br>
│   └── index.html        # HTML-шаблон Web GUI
│<br>
├── README.md             # Документация 

# Запуск ассемблера
python uvm_asm.py -i asm/example.json -o bin/example.bin -t<br>
Опция -t выводит IR и байткод.
# Запуск интерпретатора
python uvm_interp.py -i bin/example.bin -o dumps/example.csv -r 95-135<br>
# Запуск GUI
python uvm_gui.py<br>
Позволяет:<br> 
✔ редактировать программу<br>
✔ ассемблировать<br>
✔ запускать интерпретатор<br>
✔ смотреть дамп памяти<br>
✔ копировать байткод<br>
# Запуск GUI Web
python uvm_gui_web.py<br>
После запуска открыть в браузере: http://127.0.0.1:5000
## Этап 5: Решение тестовой задачи
Программа vector_pow.json<br>
[<br>
  { "op": "load_const", "B": 10, "C": 2 },<br>
  { "op": "load_const", "B": 11, "C": 3 },<br>
  { "op": "load_const", "B": 12, "C": 4 },<br>
  { "op": "load_const", "B": 13, "C": 2 },<br>
  { "op": "load_const", "B": 14, "C": 3 },<br>
  { "op": "load_const", "B": 15, "C": 2 },<br>
  { "op": "load_const", "B": 16, "C": 4 },<br>
  { "op": "load_const", "B": 17, "C": 3 },<br>
  { "op": "load_const", "B": 18, "C": 2 },<br>

  { "op": "load_const", "B": 20, "C": 1 },<br>
  { "op": "load_const", "B": 21, "C": 2 },<br>
  { "op": "load_const", "B": 22, "C": 3 },<br>
  { "op": "load_const", "B": 23, "C": 1 },<br>
  { "op": "load_const", "B": 24, "C": 2 },<br>
  { "op": "load_const", "B": 25, "C": 3 },<br>
  { "op": "load_const", "B": 26, "C": 1 },<br>
  { "op": "load_const", "B": 27, "C": 2 },<br>
  { "op": "load_const", "B": 28, "C": 3 },<br>

  { "op": "write_value", "B": 10, "C": 100 },<br>
  { "op": "write_value", "B": 11, "C": 101 },<br>
  { "op": "write_value", "B": 12, "C": 102 },<br>
  { "op": "write_value", "B": 13, "C": 103 },<br>
  { "op": "write_value", "B": 14, "C": 104 },<br>
  { "op": "write_value", "B": 15, "C": 105 },<br>
  { "op": "write_value", "B": 16, "C": 106 },<br>
  { "op": "write_value", "B": 17, "C": 107 },<br>
  { "op": "write_value", "B": 18, "C": 108 },<br>

  { "op": "write_value", "B": 20, "C": 110 },<br>
  { "op": "write_value", "B": 21, "C": 111 },<br>
  { "op": "write_value", "B": 22, "C": 112 },<br>
  { "op": "write_value", "B": 23, "C": 113 },<br>
  { "op": "write_value", "B": 24, "C": 114 },<br>
  { "op": "write_value", "B": 25, "C": 115 },<br>
  { "op": "write_value", "B": 26, "C": 116 },<br>
  { "op": "write_value", "B": 27, "C": 117 },<br>
  { "op": "write_value", "B": 28, "C": 118 },<br>

  { "op": "load_const", "B": 0, "C": 110 },<br>
  { "op": "pow", "B": 0, "C": 120, "D": 100 },<br>

  { "op": "load_const", "B": 0, "C": 111 },<br>
  { "op": "pow", "B": 0, "C": 121, "D": 101 },<br>

  { "op": "load_const", "B": 0, "C": 112 },<br>
  { "op": "pow", "B": 0, "C": 122, "D": 102 },<br>

  { "op": "load_const", "B": 0, "C": 113 },<br>
  { "op": "pow", "B": 0, "C": 123, "D": 103 },<br>

  { "op": "load_const", "B": 0, "C": 114 },<br>
  { "op": "pow", "B": 0, "C": 124, "D": 104 },<br>

  { "op": "load_const", "B": 0, "C": 115 },<br>
  { "op": "pow", "B": 0, "C": 125, "D": 105 },<br>

  { "op": "load_const", "B": 0, "C": 116 },<br>
  { "op": "pow", "B": 0, "C": 126, "D": 106 },<br>

  { "op": "load_const", "B": 0, "C": 117 },<br>
  { "op": "pow", "B": 0, "C": 127, "D": 107 },<br>

  { "op": "load_const", "B": 0, "C": 118 },<br>
  { "op": "pow", "B": 0, "C": 128, "D": 108 }<br>
]<br>
Дамп: dump_vector_pow.csv

Также еще две тестовые программы vector_pow_1.json и vector_pow_2.json<br>
Дамп: dump_vector_pow_1.csv и dump_vector_pow_2.csv
