import os
from pathlib import Path

# 支持的音频文件扩展名
SUPPORTED_EXTENSIONS = {'.flac', '.wav', '.dts', '.aiff', '.m4a', 
                       '.ape', '.aac', '.mp3', '.ogg', '.wma'}

def is_audio_file(filename: str) -> bool:
    """检查文件是否为支持的音频格式"""
    return Path(filename).suffix.lower() in SUPPORTED_EXTENSIONS

def normalize_path(path: str) -> str:
    """将路径中的反斜杠替换为正斜杠，并移除磁盘编号"""
    # 首先替换反斜杠
    path = path.replace('\\', '/')
    # 移除磁盘编号（比如 "Y:"）
    if ':' in path:
        path = path[path.index(':') + 1:]
    return path

def list_audio_files(directory: str, output_file: str) -> None:
    """遍历目录下的所有音频文件并输出到文件
    
    Args:
        directory: 要遍历的目录路径
        output_file: 输出文件的路径
    """
    try:
        # 存储所有音频文件的完整路径
        audio_files = []
        
        # 规范化搜索目录路径
        normalized_directory = normalize_path(directory)
        
        # 遍历目录
        print("正在扫描目录...")
        for root, _, files in os.walk(directory):
            for file in files:
                if is_audio_file(file):
                    # 获取完整路径
                    full_path = os.path.join(root, file)
                    # 将完整路径规范化并移除磁盘编号
                    normalized_path = normalize_path(full_path)
                    audio_files.append(normalized_path)
        
        # 将文件路径排序并写入文件
        print("正在写入文件...")
        with open(output_file, 'w', encoding='utf-8') as f:
            for filepath in sorted(audio_files):
                f.write(f"{filepath}\n")
        
        print(f"完成！共找到 {len(audio_files)} 个音频文件")
        print(f"结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"发生错误: {e}")

def main():
    # 配置参数
    search_directory = 'Y:/music'  # 要搜索的目录，例如: 'D:/Music'
    output_file = 'audio_files.txt'  # 输出文件名
    
    # 检查目录是否存在
    if not os.path.exists(search_directory):
        print(f"错误：目录 '{search_directory}' 不存在")
        return
    
    # 执行文件列表生成
    list_audio_files(search_directory, output_file)

if __name__ == '__main__':
    main() 
