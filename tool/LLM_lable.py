import json
import openai
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional
from queue import Queue

# 配置API密钥
openai.api_key = "sk-6CmV9qfScsx16xG8ZgqrinQLpCUGeDrqD77P9H53pZ9klwLU"
openai.api_base = "https://llm.jnu.cn/v1"

# 分类标签列表
CATEGORIES = [
    "科技", "股票", "体育", "娱乐", "时政", "社会", "教育", 
    "财经", "家居", "游戏", "房产", "时尚", "彩票", "星座"
]

# 速率限制配置
RATE_LIMIT = 5  # 每秒最大请求数
MIN_REQUEST_INTERVAL = 1.0 / RATE_LIMIT  # 最小请求间隔(秒)
MAX_RETRIES = 3  # 最大重试次数

# 线程安全的计数器
class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

# 速率限制控制器
class RateLimiter:
    def __init__(self):
        self.last_request_time = 0
        self.lock = threading.Lock()
    
    def wait_for_request(self):
        with self.lock:
            current_time = time.time()
            elapsed = current_time - self.last_request_time
            if elapsed < MIN_REQUEST_INTERVAL:
                time.sleep(MIN_REQUEST_INTERVAL - elapsed)
            self.last_request_time = time.time()

counter = Counter()
rate_limiter = RateLimiter()

def classify_news_content(content: str, title: str, description: str) -> str:
    """
    使用大模型API对新闻内容进行分类，带有速率限制和重试机制
    """
    prompt = f"""
    请根据以下新闻内容判断它属于哪一类（只能选择以下14个分类中的一个）：
    分类选项：{", ".join(CATEGORIES)}
    
    新闻标题：{title}
    新闻描述：{description}
    新闻内容（摘要）：{content[:200]}...  # 只发送前200字符以避免过长
    
    请只返回最匹配的分类标签，不要包含其他任何文字。
    """
    
    for attempt in range(MAX_RETRIES):
        try:
            # 等待直到可以发送下一个请求
            rate_limiter.wait_for_request()
            
            response = openai.ChatCompletion.create(
                model="Qwen2.5-72B-Instruct",
                messages=[
                    {"role": "system", "content": "你是一个专业的新闻分类助手，请准确判断新闻类别。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            category = response.choices[0].message.content.strip()
            return category if category in CATEGORIES else "社会"
            
        except Exception as e:
            if attempt == MAX_RETRIES - 1:  # 最后一次尝试仍然失败
                print(f"分类最终失败: {title[:50]}... 错误: {str(e)}")
                return "社会"
            
            wait_time = (attempt + 1) * 2  # 指数退避
            print(f"分类出错 (尝试 {attempt + 1}/{MAX_RETRIES}): {title[:50]}... 错误: {str(e)}. {wait_time}秒后重试...")
            time.sleep(wait_time)

def process_record(record):
    """
    处理单条记录并返回处理后的记录
    """
    current_count = counter.increment()
    title = record.get("title", "无标题")
    print(f"正在处理第 {current_count} 条: {title}")
    
    content = record.get("content", "")
    description = record.get("description", "")
    
    category = classify_news_content(content, title, description)
    record["category"] = category
    record["processed"] = True
    
    return record

def process_json_file(input_path: str, output_path: str, max_items: Optional[int] = None, max_workers: int = 5):
    """
    多线程处理JSON文件，为每条新闻添加分类标签
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = data.get("RECORDS", [])
    
    if max_items:
        records = records[:max_items]
    
    # 使用线程池处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_record, record) for record in records]
        
        processed_records = []
        for future in as_completed(futures):
            try:
                processed_records.append(future.result())
            except Exception as e:
                print(f"处理记录时出错: {str(e)}")
    
    # 保持原始顺序
    data["RECORDS"] = processed_records
    
    # 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"处理完成！结果已保存到 {output_path}")

if __name__ == "__main__":
    input_file = "../data/paywall_news_2.json"
    output_file = "output_with_categories.json"
    
    # 设置线程数 (建议不超过RATE_LIMIT值)
    process_json_file(input_file, output_file, max_items=None, max_workers=5)