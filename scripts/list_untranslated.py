#!/usr/bin/env python3
import glob
import os

# 获取所有 .instructions.md 文件
all_files = glob.glob('instructions/*.instructions.md')
# 过滤掉已经是中文版的
en_files = [f for f in all_files if not f.endswith('.zh.instructions.md')]

# 检查哪些还没有中文版
untranslated = []
for en_file in en_files:
    base = os.path.basename(en_file).replace('.instructions.md', '')
    zh_file = f'instructions/{base}.zh.instructions.md'
    if not os.path.exists(zh_file):
        untranslated.append(base)

print(f"还需要翻译的文件（{len(untranslated)}个）：")
for name in untranslated:
    print(name)