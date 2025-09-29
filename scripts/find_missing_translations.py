#!/usr/bin/env python3
import glob
import os

# 获取所有非中文的md文件
all_files = glob.glob('instructions/*.md')
non_zh_files = [f for f in all_files if '.zh.' not in f]

# 获取所有中文版文件
zh_files = [f for f in all_files if '.zh.' in f]

# 创建中文版文件名集合
zh_basenames = set()
for zh_file in zh_files:
    # 移除 .zh.instructions.md 或 .zh.prompt.md 或 .zh.md 后缀
    if zh_file.endswith('.zh.instructions.md'):
        base = os.path.basename(zh_file).replace('.zh.instructions.md', '')
        zh_basenames.add(base)
    elif zh_file.endswith('.zh.prompt.md'):
        base = os.path.basename(zh_file).replace('.zh.prompt.md', '')
        zh_basenames.add(base)
    elif zh_file.endswith('.zh.md'):
        base = os.path.basename(zh_file).replace('.zh.md', '')
        zh_basenames.add(base)

# 检查哪些非中文文件没有对应的中文版
missing_translations = []
for non_zh_file in non_zh_files:
    basename = os.path.basename(non_zh_file)

    # 检查不同类型的文件
    if basename.endswith('.instructions.md'):
        base = basename.replace('.instructions.md', '')
        if base not in zh_basenames:
            missing_translations.append(non_zh_file)
    elif basename.endswith('.prompt.md'):
        base = basename.replace('.prompt.md', '')
        if base not in zh_basenames:
            missing_translations.append(non_zh_file)
    elif basename.endswith('.md'):
        base = basename.replace('.md', '')
        if base not in zh_basenames:
            missing_translations.append(non_zh_file)

print(f"非中文md文件总数: {len(non_zh_files)}")
print(f"中文版文件总数: {len(zh_files)}")
print(f"缺少中文版本的文件数: {len(missing_translations)}")

if missing_translations:
    print("\n缺少中文版本的文件:")
    for f in missing_translations:
        print(f"  - {os.path.basename(f)}")