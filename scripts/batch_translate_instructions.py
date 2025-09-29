#!/usr/bin/env python3
"""
批量翻译 instructions 目录下的所有英文 .instructions.md 文件到中文版
"""

import os
import re
import sys
import time
from pathlib import Path
from deep_translator import GoogleTranslator
import glob

CODE_PATTERN = re.compile(r"`[^`]+`")


def safe_translate(translator, text):
    """安全翻译，带重试机制"""
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
    """恢复格式化字符"""
    replaced = (
        text.replace('＃', '#')
        .replace('（', '(')
        .replace('）', ')')
        .replace('"', '"')
        .replace('"', '"')
        .replace(''', "'")
        .replace(''', "'")
    )
    return re.sub(r'^(#+)(\S)', r'\1 \2', replaced)


def translate_line(translator, line):
    """翻译单行，保护代码块"""
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


def translate_file(src_path):
    """翻译单个文件"""
    src = Path(src_path)
    if not src.exists():
        print(f"文件不存在: {src}")
        return False

    stem = src.name
    base = stem[:-len('.instructions.md')] if stem.endswith('.instructions.md') else src.stem
    dst = src.with_name(f"{base}.zh.instructions.md")

    # 如果目标文件已存在，跳过
    if dst.exists():
        print(f"跳过已存在: {dst.name}")
        return True

    print(f"正在翻译: {src.name} -> {dst.name}")

    translator = GoogleTranslator(source='auto', target='zh-CN')
    lines = src.read_text(encoding='utf-8').splitlines()
    out_lines = []
    idx = 0
    in_code = False

    # 处理 YAML 前置元数据
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

    # 处理正文内容
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        # 保护代码块
        if stripped.startswith('```'):
            out_lines.append(line)
            in_code = not in_code
            idx += 1
            continue

        # 跳过代码块内容和特殊标记
        if in_code or not stripped or (stripped.startswith('<') and stripped.endswith('>')):
            out_lines.append(line)
            idx += 1
            continue

        # 翻译普通文本行
        translated = translate_line(translator, line)
        out_lines.append(translated)
        idx += 1

    # 写入翻译结果
    dst.write_text("\n".join(out_lines) + "\n", encoding='utf-8')
    print(f"✓ 已翻译: {dst.name}")
    return True


def main():
    """主函数 - 批量翻译所有文件"""
    # 获取所有需要翻译的文件
    pattern = 'instructions/*.instructions.md'
    all_files = glob.glob(pattern)

    # 过滤掉已经是中文版的文件
    files_to_translate = [f for f in all_files if not f.endswith('.zh.instructions.md')]
    files_to_translate.sort()

    if not files_to_translate:
        print("没有找到需要翻译的文件")
        return

    print(f"找到 {len(files_to_translate)} 个需要翻译的文件")
    print("-" * 50)

    # 批量处理
    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, file_path in enumerate(files_to_translate, 1):
        print(f"\n[{i}/{len(files_to_translate)}]", end=" ")

        try:
            result = translate_file(file_path)
            if result:
                success_count += 1
            else:
                fail_count += 1

            # 添加延迟避免请求过快
            if i < len(files_to_translate):  # 最后一个文件不需要延迟
                time.sleep(0.5)

        except Exception as e:
            print(f"错误: {e}")
            fail_count += 1

    # 打印统计信息
    print("\n" + "=" * 50)
    print("翻译完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {fail_count} 个文件")
    print(f"总计: {len(files_to_translate)} 个文件")

    # 检查是否有跳过的文件（已存在的）
    existing_zh_files = glob.glob('instructions/*.zh.instructions.md')
    if existing_zh_files:
        print(f"\n已存在的中文版文件: {len(existing_zh_files)} 个")


if __name__ == '__main__':
    main()