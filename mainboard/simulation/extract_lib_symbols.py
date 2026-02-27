#!/usr/bin/env python3
"""Extract specific symbol definitions from installed KiCad 9 library files.

Reads the specified KiCad symbol library files, extracts the requested symbols,
renames them with their library prefix (e.g. "C" -> "Device:C"), adds two-tab
indentation, and outputs them as Python string constants suitable for inclusion
in a generated file.
"""

import sys
import os

# ---------------------------------------------------------------------------
# Configuration: (library_file, library_prefix, symbol_name, python_const_name)
# ---------------------------------------------------------------------------
EXTRACTIONS = [
    ("/usr/share/kicad/symbols/Device.kicad_sym",
     "Device", "C", "LIB_DEVICE_C"),
    ("/usr/share/kicad/symbols/Device.kicad_sym",
     "Device", "R", "LIB_DEVICE_R"),
    ("/usr/share/kicad/symbols/Simulation_SPICE.kicad_sym",
     "Simulation_SPICE", "VDC", "LIB_VDC"),
    ("/usr/share/kicad/symbols/Simulation_SPICE.kicad_sym",
     "Simulation_SPICE", "VSIN", "LIB_VSIN"),
    ("/usr/share/kicad/symbols/Simulation_SPICE.kicad_sym",
     "Simulation_SPICE", "VPULSE", "LIB_VPULSE"),
    ("/usr/share/kicad/symbols/Simulation_SPICE.kicad_sym",
     "Simulation_SPICE", "SWITCH", "LIB_SWITCH"),
    ("/usr/share/kicad/symbols/power.kicad_sym",
     "power", "GND", "LIB_GND"),
    ("/usr/share/kicad/symbols/power.kicad_sym",
     "power", "PWR_FLAG", "LIB_PWR_FLAG"),
]


def extract_symbol(filepath, symbol_name):
    """Extract a top-level symbol definition from a KiCad .kicad_sym file.

    Returns the raw text of the symbol block, from the opening
    ``(symbol "NAME"`` through its matching closing ``)``, inclusive.
    The returned text preserves the original file indentation exactly.
    """
    target_line_prefix = '\t(symbol "' + symbol_name + '"'

    with open(filepath, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Phase 1: Find the starting line index.
    start_idx = None
    for i, line in enumerate(lines):
        if line.startswith(target_line_prefix):
            # Make sure the name matches exactly: "C" should not match "C_Polarized".
            # After '(symbol "NAME"' there should be nothing else before newline,
            # or there could be more S-expression content on the same line.
            rest = line[len(target_line_prefix):]
            # Valid continuations: end of line, whitespace, or closing paren
            if rest == "" or rest[0] in ("\n", "\r", " ", "\t", ")"):
                start_idx = i
                break
    if start_idx is None:
        raise ValueError(
            'Symbol "{}" not found as a top-level symbol in {}'.format(
                symbol_name, filepath))

    # Phase 2: Walk from start_idx, counting parentheses to find the matching close.
    depth = 0
    end_idx = None
    for i in range(start_idx, len(lines)):
        for ch in lines[i]:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end_idx = i
                    break
        if end_idx is not None:
            break

    if end_idx is None:
        raise ValueError(
            'Could not find matching closing parenthesis for symbol '
            '"{}" starting at line {} in {}'.format(
                symbol_name, start_idx + 1, filepath))

    # Extract the lines (inclusive).
    block_lines = lines[start_idx:end_idx + 1]
    return "".join(block_lines)


def rename_symbol(block, old_name, new_name):
    """Rename the top-level symbol in its definition block.

    Only the very first occurrence of ``(symbol "OLD_NAME"`` is changed
    to ``(symbol "NEW_NAME"``.  Sub-symbol references (e.g. "C_0_1")
    are left unchanged.
    """
    old_token = '(symbol "' + old_name + '"'
    new_token = '(symbol "' + new_name + '"'
    return block.replace(old_token, new_token, 1)


def add_extra_indent_to_block(block):
    """Add one extra tab to every line so the block fits inside lib_symbols.

    The original library file has one tab for top-level symbols. Inside a
    KiCad schematic's (lib_symbols ...) section, everything needs two tabs
    at the top level, so we prepend one tab to every non-empty line.
    """
    lines = block.split("\n")
    result = []
    for line in lines:
        if line:
            result.append("\t" + line)
        else:
            result.append(line)
    return "\n".join(result)


def escape_for_python_triple_quote(s):
    """Escape a string for safe inclusion inside Python triple-double-quotes."""
    s = s.replace("\\", "\\\\")
    s = s.replace('"""', '\\"\\"\\"')
    return s


def main():
    results = []

    for filepath, lib_prefix, sym_name, const_name in EXTRACTIONS:
        if not os.path.isfile(filepath):
            print("ERROR: Library file not found: " + filepath, file=sys.stderr)
            sys.exit(1)

        # 1. Extract the raw symbol block.
        raw_block = extract_symbol(filepath, sym_name)

        # 2. Rename the top-level symbol to include the library prefix.
        prefixed_name = lib_prefix + ":" + sym_name
        renamed_block = rename_symbol(raw_block, sym_name, prefixed_name)

        # 3. Add one extra tab of indentation to every line.
        indented_block = add_extra_indent_to_block(renamed_block)

        results.append((const_name, indented_block))

    # Output as Python source with triple-quoted string constants.
    print('"""Extracted KiCad 9 symbol definitions for use in simulation schematics.')
    print("")
    print("Auto-generated by extract_lib_symbols.py -- do not edit manually.")
    print('"""')
    print("")

    for const_name, block in results:
        escaped = escape_for_python_triple_quote(block)
        escaped = escaped.rstrip("\n")
        print(const_name + ' = """\\')
        print(escaped)
        print('"""')
        print("")


if __name__ == "__main__":
    main()
