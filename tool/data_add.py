import openai
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 配置OpenAI API
openai.api_key = "sk-6CmV9qfScsx16xG8ZgqrinQLpCUGeDrqD77P9H53pZ9klwLU"
openai.api_base = "https://llm.jnu.cn/v1"

# 文件路径
input_file = 'news_category_8.txt'
output_file = 'news_8_cha.txt'

# 最大并行请求数（根据API限制调整）
MAX_WORKERS = 3  # 建议设置为3-10之间，具体取决于API的速率限制

def translate_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="Qwen2.5-72B-Instruct",
            messages=[
                {"role": "system", "content": "你是一个专业的新闻翻译员，请将以下英文新闻标题准确翻译成中文，保持标题的简洁性和新闻性，不要添加任何额外解释，如果新闻本就是中文，请直接返回原始文本，不要做任何解释。"},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"翻译出错: {e}")
        return None

def process_line(line, line_number, total_lines):
    line = line.strip()
    if not line:
        return None
        
    # 使用正则表达式分割最后一个数字和前面的文本
    match = re.search(r'(\d+)$', line)
    if not match:
        print(f"无法找到数字在行中: {line}")
        return None
        
    number = match.group(1)
    title = line[:match.start()].strip()
    
    print(f"正在处理 [{line_number}/{total_lines}]: {title} (数字: {number})")
    
    # 翻译标题
    translated_title = translate_text(title)
    if not translated_title:
        translated_title = title
        
    # 构建新行
    return f"{translated_title} {number}\n"

def process_file():
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        total = len(lines)
        
        # 准备处理的行数据
        line_data = [(line.strip(), i+1, total) for i, line in enumerate(lines) if line.strip()]
        
        # 使用线程池并行处理
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(process_line, *data) for data in line_data]
            
            translated_lines = []
            for future in as_completed(futures):
                result = future.result()
                if result:
                    translated_lines.append(result)
                    
    # 按原始顺序排序（如果需要保持顺序）
    # 注意：由于并行处理，输出顺序可能与输入顺序不同
    # 如果需要保持顺序，可以修改process_line返回行号，然后在这里排序
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)
    
    print(f"\n翻译完成！结果已保存到 {output_file}")

if __name__ == '__main__':
    start_time = time.time()
    process_file()
    print(f"总耗时: {time.time() - start_time:.2f}秒")