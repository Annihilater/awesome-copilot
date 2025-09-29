import re
import sys
import time
from pathlib import Path

from deep_translator import GoogleTranslator


CODE_PATTERN = re.compile(r"`[^`]+`")


def safe_translate(translator, text):
    original = text
    work = text.strip("\n")
    if not work:
        return original
    for attempt in range(5):
        try:
            result = translator.translate(work)
            if result:
                return result
            return original
        except Exception:
            if attempt == 4:
                return original
            time.sleep(1.5)
    return original


def restore_formatting(text):
    replaced = (
        text.replace('＃', '#')
        .replace('（', '(')
        .replace('）', ')')
        .replace('“', '"')
        .replace('”', '"')
        .replace('‘', "'")
        .replace('’', "'")
    )
    return re.sub(r'^(#+)(\S)', r'\1 \2', replaced)


def translate_line(translator, line):
    placeholders = {}

    def _replace(match):
        key = f"__CODEPLACEHOLDER_{len(placeholders)}__"
        placeholders[key] = match.group(0)
        return key

    buffered = CODE_PATTERN.sub(_replace, line)
    translated = safe_translate(translator, buffered)
    if translated is None:
        translated = line
    for key, value in placeholders.items():
        translated = translated.replace(key, value)
    return restore_formatting(translated)


def main():
    if len(sys.argv) != 2:
        print("Usage: translate_instructions.py <file>")
        return

    src = Path(sys.argv[1])
    if not src.exists():
        raise SystemExit(f"File not found: {src}")

    stem = src.name
    base = stem[:-len('.instructions.md')] if stem.endswith('.instructions.md') else src.stem
    dst = src.with_name(f"{base}.zh.instructions.md")

    translator = GoogleTranslator(source='auto', target='zh-CN')
    lines = src.read_text(encoding='utf-8').splitlines()
    out_lines = []
    idx = 0
    in_code = False

    if lines and lines[0].strip() == '---':
        out_lines.append('---')
        idx = 1
        while idx < len(lines):
            line = lines[idx]
            stripped = line.strip()
            if stripped == '---':
                out_lines.append('---')
                idx += 1
                break
            if stripped.startswith('description:'):
                key, value = line.split(':', 1)
                value = value.strip()
                quote = ''
                if value and value[0] in ("'", '"'):
                    quote = value[0]
                    value = value[1:]
                    if value.endswith(quote):
                        value = value[:-1]
                translated = safe_translate(translator, value) if value else value
                if quote:
                    out_lines.append(f"{key}: {quote}{translated}{quote}")
                else:
                    out_lines.append(f"{key}: {translated}")
            elif stripped.startswith('applyTo:'):
                out_lines.append(line)
            else:
                out_lines.append(line)
            idx += 1

    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if stripped.startswith('```'):
            out_lines.append(line)
            in_code = not in_code
            idx += 1
            continue

        if in_code or not stripped or (stripped.startswith('<') and stripped.endswith('>')):
            out_lines.append(line)
            idx += 1
            continue

        translated = translate_line(translator, line)
        out_lines.append(translated)
        idx += 1

    dst.write_text("\n".join(out_lines) + "\n", encoding='utf-8')
    print(f"Translated {src.name} -> {dst.name}")


if __name__ == '__main__':
    main()
