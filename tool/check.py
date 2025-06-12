import re

def check_txt_format(file_path):
    """
    检查TXT文件格式是否规范
    规范格式：每行应为"新闻标题+空格+数字"，且不允许空白行
    
    参数:
        file_path (str): 要检查的TXT文件路径
        
    返回:
        tuple: (是否全部规范, 不规范的行列表)
    """
    line_pattern = re.compile(r'^.+\s\d+$')  # 匹配"任意非空字符+空格+数字"的模式
    incorrect_lines = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            stripped_line = line.strip()
            
            # 检查是否为空行
            if not stripped_line:
                incorrect_lines.append((line_num, "[空白行]"))
                continue
                
            # 检查是否符合"标题+空格+数字"格式
            if not line_pattern.fullmatch(stripped_line):
                incorrect_lines.append((line_num, stripped_line))
    
    is_correct = len(incorrect_lines) == 0
    return is_correct, incorrect_lines

# 使用示例
if __name__ == "__main__":
    file_path = "news_category_11.txt"  # 替换为你的文件路径
    is_correct, incorrect_lines = check_txt_format(file_path)
    
    if is_correct:
        print("✅ 文件格式完全规范！")
    else:
        print(f"❌ 发现 {len(incorrect_lines)} 行不规范：")
        for line_num, line in incorrect_lines:
            if line == "[空白行]":
                print(f"行 {line_num}: 空白行（不允许）")
            else:
                print(f"行 {line_num}: 格式错误 → {line}")