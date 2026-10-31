---
id: 30-07
title: PYTHONUTF8=1 в окружении ломает pkit: UnicodeDecodeError на cp866-выводе tasklist, сессия не поднимается
tags: [python, utf-8, окружение, subprocess]
applies_to: Windows 10 (рус.), Python 3.13, pkit 0.1.0 (до правки 2026-10-31)
status: проверено
verified: 2026-10-31 — с PYTHONUTF8=1/PYTHONIOENCODING=utf-8 в окружении
  выгрузки падают, без них те же выгрузки проходят; после errors="replace"
  в env.py выгрузка при PYTHONUTF8=1 прошла, test_dump 10/0
source: эксперимент
---

# UTF-8-режим Python против ANSI-консоли Windows

## Что происходит

В окружении заданы `PYTHONUTF8=1` (или `PYTHONIOENCODING=utf-8`).
Текстовые подпроцессы pkit (`subprocess.run(..., text=True)`: сборка
хоста, `tasklist` в `sch_running`) декодируют вывод консоли как UTF-8,
а tasklist на русской Windows пишет cp866: первая же строка
«Информация: …» даёт `UnicodeDecodeError` (байт 0x88 = «И» в cp866) в
reader-потоке. Исключение остаётся в потоке, `communicate` возвращает
пустой вывод, а сессия дальше падает или даёт мусор уже в другом месте.

## Почему

`text=True` берет кодировку из локали, но UTF-8-режим Python
принудительно назначает UTF-8 всем потокам, игнорируя реальную
OEM-кодировку консоли (cp866).

## Как правильно

* pkit (с 2026-10-31): у текстовых subprocess задано `errors="replace"`
  — поиск `Sch.exe` в выводе по ASCII-подстроке не зависит от
  кракозябр.
* На старом клоне без правки — снимать переменные на время запуска:
  `env -u PYTHONUTF8 -u PYTHONIOENCODING python …`.

## Как неправильно

* Искать причину в DDE/DbxHost: decode падает до всякого DDE, в потоке
  чтения вывода подпроцесса.
* Добавлять `encoding="utf-8"` вместо `errors` — упадёт так же.

## Чем подтверждено

2026-10-31: на машине с PYTHONUTF8=1 в профиле — шесть запусков подряд
с UnicodeDecodeError в reader-потоке и ошибками дальше; `env -u
PYTHONUTF8 -u PYTHONIOENCODING` — те же шесть прошли. После
`errors="replace"` в env.py выгрузка при PYTHONUTF8=1 проходит:
tests/test_dump.py 10 проверок / 0 провалов.
