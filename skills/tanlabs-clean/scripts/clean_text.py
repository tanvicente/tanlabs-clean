#!/usr/bin/env python3
"""Tanlabs Clean: deterministic, local-only Unicode hygiene for UTF-8 prose."""
import argparse
import json
import sys
from pathlib import Path

MAX_BYTES = 2 * 1024 * 1024
MAX_UTF16 = 500_000
INVISIBLE = {
    0x00AD: "Hífen condicional", 0x034F: "Combinador de grafemas",
    0x180E: "Separador vocálico mongol", 0x200B: "Espaço de largura zero",
    0x2060: "Unidor de palavras", 0xFEFF: "BOM / espaço de largura zero",
    0x2061: "Aplicação invisível", 0x2062: "Multiplicação invisível",
    0x2063: "Separador invisível", 0x2064: "Adição invisível",
}
BIDI = {
    0x061C: "Marca de letra árabe", 0x200E: "Marca esquerda para direita",
    0x200F: "Marca direita para esquerda", 0x202A: "Incorporação esquerda para direita",
    0x202B: "Incorporação direita para esquerda", 0x202C: "Fim de formatação direcional",
    0x202D: "Sobreposição esquerda para direita", 0x202E: "Sobreposição direita para esquerda",
    0x2066: "Isolamento esquerda para direita", 0x2067: "Isolamento direita para esquerda",
    0x2068: "Isolamento direcional", 0x2069: "Fim de isolamento direcional",
}
SPACES = {
    0x00A0: "Espaço inseparável", 0x1680: "Espaço ogham",
    **{cp: "Espaço tipográfico" for cp in range(0x2000, 0x200B)},
    0x202F: "Espaço inseparável estreito", 0x205F: "Espaço matemático",
    0x3000: "Espaço ideográfico",
}
PUNCTUATION = {"“": '"', "”": '"', "„": '"', "‘": "'", "’": "'", "‚": "'", "–": "-", "—": "-", "…": "..."}


def clean_text(text, *, invisible=True, spaces=True, bidi=False, typography=False):
    """Return cleaned text and a report that contains no input/output prose."""
    if not isinstance(text, str):
        raise TypeError("O conteúdo precisa ser texto.")
    if len(text.encode("utf-16-le")) // 2 > MAX_UTF16:
        raise ValueError("O texto ultrapassa 500 mil unidades UTF-16. Divida-o em partes.")
    output, findings = [], {}
    removed = normalized = 0
    for char in text:
        cp = ord(char)
        category = name = replacement = None
        if cp in INVISIBLE:
            category, name, replacement, applied = "invisible", INVISIBLE[cp], "", invisible
        elif cp in BIDI:
            category, name, replacement, applied = "bidi", BIDI[cp], "", bidi
        elif cp in SPACES:
            category, name, replacement, applied = "spaces", SPACES[cp], " ", spaces
        elif char in PUNCTUATION:
            category, name, replacement, applied = "typography", f"Pontuação tipográfica {char}", PUNCTUATION[char], typography
        else:
            output.append(char)
            continue
        code = f"U+{cp:04X}"
        if code not in findings:
            findings[code] = {"code": code, "name": name, "category": category, "count": 0,
                              "action": ("Remover" if replacement == "" else "Normalizar") if applied else "Preservar"}
        findings[code]["count"] += 1
        output.append(replacement if applied else char)
        if applied:
            if replacement == "":
                removed += 1
            else:
                normalized += 1
    result = "".join(output)
    return result, {"input_characters": len(text), "output_characters": len(result),
                    "removed": removed, "normalized": normalized, "changed": removed + normalized,
                    "findings": list(findings.values())}


def load_text(path):
    if path == "-":
        data = sys.stdin.buffer.read(MAX_BYTES + 1)
    else:
        file = Path(path)
        if file.suffix.lower() not in (".txt", ".md"):
            raise ValueError("Use arquivos .txt ou .md em UTF-8, ou - para stdin.")
        with file.open("rb") as handle:
            data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("A entrada ultrapassa 2 MB.")
    text = data.decode("utf-8", errors="strict")
    if any(ord(c) < 32 and c not in "\t\r\n" for c in text):
        raise ValueError("A entrada contém dados binários ou caracteres de controle incompatíveis.")
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(description="Tanlabs Clean — limpeza Unicode local, sem rede ou dependências externas.")
    parser.add_argument("input", help="Arquivo TXT/MD UTF-8 ou - para stdin")
    parser.add_argument("-o", "--output", help="Novo arquivo de saída; nunca sobrescreve arquivos existentes")
    parser.add_argument("--report", help="Novo arquivo JSON com relatório sem o conteúdo do texto")
    parser.add_argument("--inspect", action="store_true", help="Exibe somente o relatório JSON, sem escrever texto limpo")
    parser.add_argument("--keep-invisible", action="store_true")
    parser.add_argument("--keep-spaces", action="store_true")
    parser.add_argument("--remove-bidi", action="store_true")
    parser.add_argument("--plain-punctuation", action="store_true")
    args = parser.parse_args(argv)
    if args.inspect and args.output:
        parser.error("--inspect não pode ser usado com --output")
    try:
        destinations = [Path(p) for p in (args.output, args.report) if p]
        if len({str(p.resolve()) for p in destinations}) != len(destinations):
            raise ValueError("Texto e relatório precisam ter destinos diferentes.")
        if any(p.exists() or p.is_symlink() for p in destinations):
            raise ValueError("Um destino já existe. Escolha novos nomes; o original será preservado.")
        text = load_text(args.input)
        result, report = clean_text(text, invisible=not args.keep_invisible, spaces=not args.keep_spaces,
                                    bidi=args.remove_bidi, typography=args.plain_punctuation)
        report_json = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.inspect:
            sys.stdout.buffer.write(report_json.encode("utf-8"))
        elif args.output:
            with Path(args.output).open("x", encoding="utf-8", newline="") as handle:
                handle.write(result)
        else:
            sys.stdout.buffer.write(result.encode("utf-8"))
        if args.report:
            with Path(args.report).open("x", encoding="utf-8", newline="") as handle:
                handle.write(report_json)
        print(f"Tanlabs Clean: {report['removed']} removidos; {report['normalized']} normalizados.", file=sys.stderr)
        return 0
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Tanlabs Clean: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
