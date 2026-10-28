# tests/test_dump.py — сквозная выгрузка схемы: копия -> Sch.exe -> DBX -> объекты.
#   python tests/test_dump.py <схема.SCH> [--components N] [--nets N]
import os

from _common import start
import pkit as pk


def main():
    r, args = start("test_dump")
    live = pk.env.sch_running()
    mtime_before = os.path.getmtime(args.sch)
    if live:
        r.note("Sch.exe уже запущен — выгрузка из живого редактора (только чтение)")
        s = pk.dump_live()
    else:
        s = pk.dump(args.sch)
    print(s)

    r.truth(len(s.comps) > 0, "компоненты выгружены")
    r.truth(len(s.nets) > 0, "цепи выгружены")
    if args.components is not None:
        r.equal(len(s.comps), args.components, "число компонентов")
    if args.nets is not None:
        r.equal(len(s.nets), args.nets, "число цепей")

    for ref in s.refdes()[:1]:
        r.equal(s.comp(ref).attrs.get("RefDes"), ref,
                "атрибут RefDes = позиционное обозначение")

    with_pins = [n for n in s.nets.values() if n.pins]
    r.truth(with_pins, "есть цепь с узлами-выводами")
    if with_pins:
        node = with_pins[0].pins[0]
        r.truth(node[0] in s.comps, "узел цепи ссылается на выгруженный компонент")

    pn = s.pin_nets()
    r.truth(len(pn) > 0, "карта выводов непуста")

    bom = s.bom()
    r.truth(len(bom) > 0, "перечень элементов непуст")
    r.note("групп в перечне: %d" % len(bom))

    r.equal(os.path.getmtime(args.sch), mtime_before,
            "оригинал не тронут (mtime)")
    r.done()
    print("test_dump OK")


if __name__ == "__main__":
    main()
