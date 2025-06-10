import json

# 定义类别到数字的映射
category_to_num = {
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

# 1. 读取JSON文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 2. 提取title和category并转换
def extract_data(json_data):
    records = json_data.get("RECORDS", [])
    extracted = []
    for record in records:
        title = record.get("title", "").strip()
        category = record.get("category", "").strip()
        if title and category in category_to_num:
            num = category_to_num[category]
            extracted.append(f"{title}\t{num}")
    return extracted

# 3. 写入txt文件
def save_to_txt(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(data))

# 主流程
if __name__ == "__main__":
    input_json = "../data/news_2.json"  # 替换为你的JSON文件路径
    output_txt = "output_2.txt"  # 输出文件路径
    
    # 执行步骤
    json_data = load_json(input_json)
    extracted = extract_data(json_data)
    save_to_txt(extracted, output_txt)
    
    print(f"处理完成！共提取 {len(extracted)} 条数据，已保存到 {output_txt}")