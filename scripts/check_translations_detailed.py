#!/usr/bin/env python3
import glob
import os

# 获取所有md文件
all_files = glob.glob('instructions/*.md')

# 分离英文和中文文件
en_files = [f for f in all_files if '.zh.' not in f]
zh_files = [f for f in all_files if '.zh.' in f]

print(f"英文文件数量: {len(en_files)}")
print(f"中文文件数量: {len(zh_files)}")
print("=" * 50)

# 建立中文文件的映射
zh_mapping = {}
for zh_file in zh_files:
    basename = os.path.basename(zh_file)
    # 确定对应的英文文件名
    if basename.endswith('.zh.instructions.md'):
        en_name = basename.replace('.zh.instructions.md', '.instructions.md')
    elif basename.endswith('.zh.prompt.md'):
        en_name = basename.replace('.zh.prompt.md', '.prompt.md')
    else:
        # 处理其他格式
        en_name = basename.replace('.zh.', '.')
    zh_mapping[en_name] = zh_file

# 检查每个英文文件是否有对应的中文版本
missing_zh = []
has_zh = []

for en_file in en_files:
    en_basename = os.path.basename(en_file)
    if en_basename in zh_mapping:
        has_zh.append(en_basename)
    else:
        missing_zh.append(en_basename)

# 检查是否有孤立的中文文件（没有对应的英文原版）
orphan_zh = []
en_basenames = {os.path.basename(f) for f in en_files}

for zh_basename, zh_file in zh_mapping.items():
    if zh_basename not in en_basenames:
        orphan_zh.append(os.path.basename(zh_file))

# 输出结果
if missing_zh:
    print(f"\n缺少中文版本的文件 ({len(missing_zh)}个):")
    for f in sorted(missing_zh):
        print(f"  - {f}")
else:
    print("\n✅ 所有英文文件都有对应的中文版本")

if orphan_zh:
    print(f"\n孤立的中文文件（没有英文原版）({len(orphan_zh)}个):")
    for f in sorted(orphan_zh):
        print(f"  - {f}")

# 显示统计
print("\n" + "=" * 50)
print(f"统计结果:")
print(f"  英文文件总数: {len(en_files)}")
print(f"  有中文版的英文文件: {len(has_zh)}")
print(f"  缺少中文版的英文文件: {len(missing_zh)}")
print(f"  中文文件总数: {len(zh_files)}")
print(f"  孤立的中文文件: {len(orphan_zh)}")