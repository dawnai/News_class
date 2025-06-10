"""
将原始数据按照类别进行拆分
"""
# 定义输入文件和输出文件路径
input_file = 'output_all.txt'  # 替换为你的输入文件名
output_prefix = 'news_category_'  # 输出文件前缀

# 创建一个字典来存储不同类别的新闻（保持原始行不变）
category_dict = {}

# 读取输入文件并分类
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        # 检查行是否包含制表符分隔的两部分
        if '\t' in line:
            # 保留整行（包括最后的换行符）
            category = line.strip().split('\t')[-1]
            if category not in category_dict:
                category_dict[category] = []
            category_dict[category].append(line)  # 这里存储整行

# 将每个类别的新闻写入单独的文件
for category, lines in category_dict.items():
    output_filename = f"{output_prefix}{category}.txt"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)  # 直接写入所有行

print(f"处理完成！共处理了{len(category_dict)}个新闻类别。")