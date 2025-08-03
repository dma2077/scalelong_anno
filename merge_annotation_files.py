import json
import os
import re
from collections import defaultdict

def parse_filename_range(filename):
    """
    解析文件名中的行号范围
    例如: 1_45_1.jsonl -> (1, 45)
         46_90_1.jsonl -> (46, 90)
         91-135_1.jsonl -> (91, 135)
    """
    # 移除文件扩展名
    name = filename.replace('.jsonl', '')
    
    # 匹配不同的格式
    patterns = [
        r'(\d+)_(\d+)_\d+',  # 1_45_1
        r'(\d+)-(\d+)_\d+',  # 91-135_1
        r'(\d+)_(\d+)',      # 1_45 (备用)
    ]
    
    for pattern in patterns:
        match = re.match(pattern, name)
        if match:
            start = int(match.group(1))
            end = int(match.group(2))
            return start, end
    
    return None, None

def merge_annotation_files(annotation_dir, output_file):
    """
    合并annotation目录下的所有文件
    优先使用_2文件，如果不存在则使用_1文件
    
    Args:
        annotation_dir (str): annotation目录路径
        output_file (str): 输出文件路径
    """
    # 存储所有数据，按行号索引
    all_data = {}
    
    # 获取所有jsonl文件
    all_files = [f for f in os.listdir(annotation_dir) if f.endswith('.jsonl')]
    
    # 按行号范围分组文件
    file_groups = defaultdict(list)
    for filename in all_files:
        start_line, end_line = parse_filename_range(filename)
        if start_line is not None and end_line is not None:
            key = (start_line, end_line)
            file_groups[key].append(filename)
    
    print(f"找到 {len(file_groups)} 个行号范围组:")
    for (start, end), files in sorted(file_groups.items()):
        print(f"  行号范围 {start}-{end}: {files}")
    
    # 处理每个行号范围
    for (start_line, end_line), files in sorted(file_groups.items()):
        print(f"\n处理行号范围: {start_line}-{end_line}")
        
        # 优先选择_2文件，如果没有则选择_1文件
        target_file = None
        for filename in files:
            if filename.endswith('_2.jsonl'):
                target_file = filename
                break
        
        if target_file is None:
            for filename in files:
                if filename.endswith('_1.jsonl'):
                    target_file = filename
                    break
        
        if target_file is None:
            print(f"  警告: 行号范围 {start_line}-{end_line} 没有找到合适的文件")
            continue
        
        print(f"  使用文件: {target_file}")
        
        file_path = os.path.join(annotation_dir, target_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # 提取指定行号范围的数据
            extracted_count = 0
            for i, line in enumerate(lines, 1):
                if start_line <= i <= end_line:
                    try:
                        data = json.loads(line.strip())
                        all_data[i] = data
                        extracted_count += 1
                    except json.JSONDecodeError as e:
                        print(f"  警告: 第{i}行JSON解析错误: {e}")
                        continue
            
            print(f"  提取了 {extracted_count} 行数据")
            
        except Exception as e:
            print(f"  错误: 处理文件 {target_file} 时出错: {e}")
            continue
    
    # 按行号排序并写入输出文件
    print(f"\n开始写入合并文件: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for line_num in sorted(all_data.keys()):
            f.write(json.dumps(all_data[line_num], ensure_ascii=False) + '\n')
    
    print(f"合并完成！总共处理了 {len(all_data)} 行数据")
    print(f"输出文件: {output_file}")
    
    # 显示统计信息
    print(f"\n=== 统计信息 ===")
    print(f"总行数: {len(all_data)}")
    print(f"行号范围: {min(all_data.keys())} - {max(all_data.keys())}")
    
    # 检查是否有缺失的行号
    expected_lines = set(range(min(all_data.keys()), max(all_data.keys()) + 1))
    actual_lines = set(all_data.keys())
    missing_lines = expected_lines - actual_lines
    
    if missing_lines:
        print(f"缺失的行号: {sorted(missing_lines)}")
    else:
        print("所有行号都已包含")

def show_sample_data(output_file, num_samples=3):
    """
    显示合并后文件的样本数据
    
    Args:
        output_file (str): 输出文件路径
        num_samples (int): 显示的样本数量
    """
    print(f"\n=== 合并后文件样本 (前{num_samples}行) ===")
    
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if i > num_samples:
                    break
                
                data = json.loads(line.strip())
                video_id = list(data.keys())[0]
                questions = data[video_id]
                
                print(f"\n行 {i}:")
                print(f"  视频ID: {video_id}")
                print(f"  问题数量: {len(questions)}")
                print(f"  第一个问题: {questions[0]['question'][:50]}...")
                
    except Exception as e:
        print(f"读取样本数据时出错: {e}")

if __name__ == "__main__":
    annotation_dir = "/Users/dehua/scalelong_annotation/annotation"
    output_file = "/Users/dehua/scalelong_annotation/merged_annotation.jsonl"
    
    # 执行合并
    merge_annotation_files(annotation_dir, output_file)
    
    # 显示样本数据
    show_sample_data(output_file, num_samples=3)