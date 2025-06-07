import xml.etree.ElementTree as ET
import pandas as pd
import xmltodict
import json

def parse_alteryx_anb(anb_file, output_format="csv"):
    """
    解析 Alteryx ANB/YXMD 文件，提取数据并转换为 CSV 或 JSON。
    
    Args:
        anb_file (str): ANB/YXMD 文件路径。
        output_format (str): 输出格式，支持 "csv" 或 "json"。
    """
    # 1. 读取 XML 文件
    tree = ET.parse(anb_file)
    root = tree.getroot()

    # 2. 处理 XML 命名空间（如果有）
    ns = {'al': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}
    
    # 3. 查找所有包含数据的节点（假设数据在 <Node> 或 <Output> 下）
    data_nodes = root.findall('.//al:Node', ns) or root.findall('.//Node')  # 兼容有无命名空间
    
    if not data_nodes:
        print("未找到数据节点！请检查 XML 结构。")
        return

    # 4. 提取数据
    data = []
    for node in data_nodes:
        # 获取节点属性
        node_attrs = node.attrib
        
        # 提取子节点数据（假设数据在 <Configuration> 或 <Output> 下）
        config = node.find('al:Configuration', ns) or node.find('Configuration')
        if config is not None:
            # 提取所有字段
            fields = {}
            for field in config:
                fields[field.tag.replace(f"{{{ns.get('al', '')}}}", "")] = field.text  # 去除命名空间
            data.append({**node_attrs,​**fields})

    # 5. 转换为 DataFrame
    df = pd.DataFrame(data)
    
    # 6. 导出
    if output_format == "csv":
        df.to_csv("output.csv", index=False)
        print("数据已导出为 CSV: output.csv")
    elif output_format == "json":
        df.to_json("output.json", orient="records", indent=4)
        print("数据已导出为 JSON: output.json")
    else:
        print("请选择正确的输出格式（'csv' 或 'json'）。")

# 示例调用
if __name__ == "__main__":
    parse_alteryx_anb("./1.anb", output_format="csv")