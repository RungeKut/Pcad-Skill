# -*- coding: utf-8 -*-
"""Особое Pcad-Skill в общей проверке skill-skill/tools/check_docs.py.

TEXT_EXT — исходник DbxHost.cs тоже сверяется со стоп-листом;
PROJECT_EXT — имена файлов P-CAD из папки проекта становятся стоп-словами;
GENERIC — слова имён схем, не считающиеся приметой проекта.
"""
GENERIC = {"pcad", "accel", "блока", "лист", "листы", "плата", "печатная"}
TEXT_EXT = (".cs",)
PROJECT_EXT = (".sch", ".pcb", ".lib")
