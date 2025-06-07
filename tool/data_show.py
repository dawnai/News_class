# 类别映射字典
category_map = {
    "科技": 0,
    "股票": 1,
    "体育": 2,
    "娱乐": 3,
    "时政": 4,
    "社会": 5,
    "教育": 6,
    "财经": 7,
    "家居": 8,
    "游戏": 9,
    "房产": 10,
    "时尚": 11,
    "彩票": 12,
    "星座": 13
}

# 反转字典，方便数字到类名的查找
reverse_map = {v: k for k, v in category_map.items()}

# 初始化计数器
category_counts = {k: 0 for k in category_map.keys()}

# 读取文件并统计
with open('./output.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # 假设每行格式是"标题 数字"
        parts = line.strip().split()
        if len(parts) >= 2:
            try:
                category_num = int(parts[-1])  # 取最后一个元素作为类别数字
                if category_num in reverse_map:
                    category_name = reverse_map[category_num]
                    category_counts[category_name] += 1
            except ValueError:
                continue  # 如果无法转换为数字则跳过

# 计算总数和占比
total = sum(category_counts.values())
print(f"总数据量: {total}")
print("\n类别统计:")
for category, count in category_counts.items():
    percentage = (count / total) * 100 if total > 0 else 0
    print(f"{category}: {count}条, 占比: {percentage:.2f}%")