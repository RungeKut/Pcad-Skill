# tests/_common.py — общее для тестов pkit.
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pkit as pk  # noqa: E402

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vyvod")


def start(name):
    """Аргументы теста: схема и необязательные ожидания; -> (Report, args).

    Путь к схеме не хранится в наборе: схема человека — его проект (40-02).
    """
    pk.utf8_console()
    ap = argparse.ArgumentParser(prog=name)
    ap.add_argument("sch", help="схема P-CAD 2002 (.SCH); оригинал не меняется")
    ap.add_argument("--components", type=int,
                    help="ожидаемое число компонентов из независимого источника")
    ap.add_argument("--nets", type=int, help="ожидаемое число цепей")
    args = ap.parse_args()
    print("=== %s ===" % name)
    if not os.path.isfile(args.sch):
        print("нет тестовой схемы:", args.sch)
        sys.exit(2)
    os.makedirs(OUT_DIR, exist_ok=True)
    print("pkit", pk.__version__, "| схема:", args.sch)
    return pk.Report(name), args
