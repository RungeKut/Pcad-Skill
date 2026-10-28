# Pcad-Skill — схемы P-CAD 2002 скриптами

Чтение и правка схем P-CAD 2002 (.SCH) из Python через штатный DBX API
редактора — без ручной работы в Sch.exe. По образцу Allegro-Skill (Cadence).

```
pcad/
├── SKILL.md                — скилл агента: что это, первый шаг, железные правила
├── pkit/                   — Python-пакет: env / dbx / sch / verify
├── tools/dbx-host/         — DbxHost.cs → DbxHost.exe (x86, JSON stdin/stdout)
├── tools/check_docs.py     — обёртка общей проверки skill-skill
├── tools/kit_local.py      — особое набора для этой проверки
├── knowledge/              — база проверенного опытом знания (INDEX.md)
└── tests/                  — сквозные тесты (python tests\test_*.py <схема>)
```

| Модуль | Что в нём |
|---|---|
| `pkit.env` | пути P-CAD, сборка DbxHost, рабочие папки, `utf8_console` |
| `pkit.dbx` | `open_design` (пакетный), `open_live` (живой), `Session`, `Host`, `DbxError` |
| `pkit.sch` | `dump`, `dump_live`, `Schematic` (comps, nets, bom, pin_nets) |
| `pkit.verify` | `Report` — накопитель проверок |
| `tools/dbx-host` | DbxHost.exe — x86-хост DBX с JSON-протоколом stdin/stdout |

## Как это устроено

`Dbx32.dll` из поставки P-CAD 2002 — DDE-клиент к **запущенному** редактору:
файл сама DLL не читает, `TOpenDesign("sch")` подключается к Sch.exe, в
котором схема открыта. DLL 32-битная, поэтому вызовы живут в x86-процессе
`DbxHost.exe` (собирается штатным `csc.exe` .NET Framework 4), а Python
(любой разрядности) говорит с ним JSON-строками через stdin/stdout.

Два режима (`knowledge/20_ПРИЁМЫ/20-02`):

* **пакетный** — `pk.dump(path)`: копия в `Temp\pkit`, свой Sch.exe,
  выгрузка, процесс погашен; оригинал не трогается (проверено по mtime);
* **живой** — `pk.dump_live()`: чтение дизайна из уже открытого человеком
  Sch.exe; только чтение, редактор не сохраняем и не закрываем.

## Быстрый старт

```python
import sys
sys.path.insert(0, r"<папка скиллов>\pcad")
import pkit as pk

pk.utf8_console()
s = pk.dump(r"D:\проект\схема.SCH")
print(s)                    # число компонентов и цепей
print(s.bom())              # перечень элементов
print(s.pin_nets())         # {(refdes, pindes): netname}
```

## Установка

```bash
git clone https://github.com/RungeKut/Pcad-Skill.git "<папка скиллов агента>/pcad"
```

Рядом нужен скилл skill-skill (общие правила, проверки, хук). Настройка
клона — skill-skill, `knowledge/40_СРЕДА/40-01`; зависимости набора
(P-CAD 2002, Python 3.11+, .NET Framework 4 из коробки Windows) и сборка
`DbxHost.exe` — `knowledge/40_СРЕДА/40-01` здесь.

## Что проверено

2026-10-07, P-CAD 2002 V17.01.22, Python 3.14 x64: полная выгрузка
реальной схемы (компоненты, цепи, выводы, атрибуты с кириллицей, узлы
цепей) в пакетном и живом режиме — `tests/test_dump.py`.
Правка (TModify*/TPlace*) в pkit пока не выносилась — API разобран,
реализация по мере надобности. Записи без `verified` силы не имеют —
см. `knowledge/00_ПРАВИЛА.md`.

## Работа с репозиторием

По общим правилам — соседний скилл skill-skill, 40-02: в начале
`git pull --rebase`, после правки `git diff` глазами,
`python tools/check_docs.py`, коммит, push сразу; без права записи — PR
из форка, сливает владелец. **В набор не попадает ничего о
проектируемом изделии** — ни в файлы, ни в текст коммита
(`knowledge/40_СРЕДА/40-02`).

## Лицензия

MIT. P-CAD и ACCEL — торговые марки правообладателей; набор не
аффилирован с ними.
