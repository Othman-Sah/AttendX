#!/usr/bin/env python
"""
Compile .po translation files to .mo files without external dependencies.
This keeps local development working on machines without GNU gettext/msgfmt.
"""

import ast
import struct
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'locale'


def _parse_po_string(value):
    return ast.literal_eval(value)


def read_po(path):
    messages = {}
    msgid = None
    msgstr = None
    state = None
    fuzzy = False

    def commit():
        nonlocal msgid, msgstr, fuzzy
        if msgid is not None and msgstr is not None and not fuzzy:
            messages[msgid] = msgstr
        msgid = None
        msgstr = None
        fuzzy = False

    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line:
            commit()
            state = None
            continue
        if line.startswith('#,') and 'fuzzy' in line:
            fuzzy = True
            continue
        if line.startswith('#'):
            continue
        if line.startswith('msgid '):
            commit()
            msgid = _parse_po_string(line[6:].strip())
            msgstr = None
            state = 'msgid'
            continue
        if line.startswith('msgstr '):
            msgstr = _parse_po_string(line[7:].strip())
            state = 'msgstr'
            continue
        if line.startswith('"') and state == 'msgid':
            msgid += _parse_po_string(line)
            continue
        if line.startswith('"') and state == 'msgstr':
            msgstr += _parse_po_string(line)

    commit()
    return messages


def write_mo(messages, path):
    ids = sorted(messages)
    strs = [messages[msgid] for msgid in ids]
    ids_bytes = [msgid.encode('utf-8') for msgid in ids]
    strs_bytes = [msgstr.encode('utf-8') for msgstr in strs]

    key_offset = 7 * 4
    value_offset = key_offset + len(ids) * 8
    ids_offset = value_offset + len(ids) * 8
    strs_offset = ids_offset + sum(len(msgid) + 1 for msgid in ids_bytes)

    output = [
        struct.pack('Iiiiiii', 0x950412de, 0, len(ids), key_offset, value_offset, 0, 0)
    ]

    offset = ids_offset
    for msgid in ids_bytes:
        output.append(struct.pack('ii', len(msgid), offset))
        offset += len(msgid) + 1

    offset = strs_offset
    for msgstr in strs_bytes:
        output.append(struct.pack('ii', len(msgstr), offset))
        offset += len(msgstr) + 1

    output.extend(msgid + b'\0' for msgid in ids_bytes)
    output.extend(msgstr + b'\0' for msgstr in strs_bytes)
    path.write_bytes(b''.join(output))


def compile_messages():
    if not LOCALE_DIR.exists():
        print(f"Locale directory not found: {LOCALE_DIR}")
        return

    compiled_count = 0
    for po_file in LOCALE_DIR.glob('*/LC_MESSAGES/*.po'):
        mo_file = po_file.with_suffix('.mo')
        messages = read_po(po_file)
        write_mo(messages, mo_file)
        print(f"Compiled: {po_file.relative_to(BASE_DIR)} -> {mo_file.relative_to(BASE_DIR)}")
        compiled_count += 1

    print(f"\nSuccessfully compiled {compiled_count} translation files")


if __name__ == '__main__':
    compile_messages()
