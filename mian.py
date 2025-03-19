import os
from pathlib import Path
from typing import Set, List, Tuple
import time

def get_filename_without_extension(filename: str) -> str:
    """获取不带扩展名的文件名"""
    return Path(filename).stem

def read_audio_files(filename: str) -> List[str]:
    """读取audio_files.txt中的完整文件路径列表"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"读取音频文件列表出错: {e}")
        return []

def read_target_songs(filename: str) -> Set[str]:
    """读取list.txt中的目标歌曲名列表"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return {line.strip().lower() for line in f if line.strip() and not line.startswith('熊猫无损音乐')}
    except Exception as e:
        print(f"读取目标歌曲列表出错: {e}")
        return set()

def extract_metadata_from_path(file_path: str) -> Tuple[str, str]:
    """从文件路径中提取元数据
    返回：(歌手名, 歌曲名)
    """
    try:
        # 将路径分割成组件
        parts = Path(file_path).parts
        if len(parts) >= 4 and parts[0] == 'music':
            artist = parts[1]
            song_name = get_filename_without_extension(parts[3])
            return artist, song_name
        else:
            # 如果路径结构不符合预期，返回文件名作为歌曲名
            filename = get_filename_without_extension(os.path.basename(file_path))
            return "", filename
    except Exception as e:
        print(f"提取元数据出错: {e}")
        return "", get_filename_without_extension(os.path.basename(file_path))

def find_matching_files(audio_files: List[str], target_songs: Set[str]) -> List[str]:
    """查找匹配的文件，使用包含关系匹配"""
    matching_files = []
    unmatched_songs = set(target_songs)  # 用于跟踪未匹配的歌曲
    
    print("正在查找匹配文件...")
    for file_path in audio_files:
        # 获取不带扩展名的文件名并转小写
        filename_without_ext = get_filename_without_extension(os.path.basename(file_path)).lower()
        
        # 检查是否有目标歌曲名包含在文件名中
        for target_song in target_songs:
            if target_song in filename_without_ext:
                matching_files.append(file_path)
                unmatched_songs.discard(target_song)  # 从未匹配集合中移除
                break  # 找到匹配就跳出内层循环
    
    # 按文件名排序
    matching_files.sort(key=lambda x: get_filename_without_extension(os.path.basename(x)).lower())
    
    # 只显示未匹配歌曲的数量
    if unmatched_songs:
        print(f"\n未找到 {len(unmatched_songs)} 首歌曲")
    
    return matching_files

def create_m3u_playlist(output_file: str, file_list: List[str], playlist_name: str = "MyPlaylist") -> None:
    """创建M3U播放列表文件"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            f.write(f'#PLAYLIST:{playlist_name}\n')
            
            for file_path in file_list:
                # 从文件路径提取元数据
                artist, song_name = extract_metadata_from_path(file_path)
                
                # 写入扩展信息
                display_name = f"{artist} - {song_name}" if artist else song_name
                f.write(f'#EXTINF:300,{display_name}\n')
                f.write(f'{file_path}\n')
                
        print(f"已生成播放列表: {output_file}")
    except Exception as e:
        print(f"创建播放列表出错: {e}")

def main():
    # 配置参数
    audio_files_list = 'audio_files.txt'  # 包含完整文件路径的列表
    target_songs_file = 'list.txt'  # 目标歌曲名列表
    output_m3u = 'music_playlist.m3u'  # 输出的m3u文件名
    playlist_name = '歌单名称'  # 播放列表名称

    print("开始处理...")
    
    # 读取音频文件列表
    audio_files = read_audio_files(audio_files_list)
    if not audio_files:
        print("错误：音频文件列表为空")
        return
    
    # 读取目标歌曲列表
    target_songs = read_target_songs(target_songs_file)
    if not target_songs:
        print("错误：目标歌曲列表为空")
        return
    
    # 查找匹配的文件
    matching_files = find_matching_files(audio_files, target_songs)
    
    # 显示匹配结果并创建播放列表
    if matching_files:
        print(f"\n找到 {len(matching_files)}/{len(target_songs)} 个匹配文件")
        create_m3u_playlist(output_m3u, matching_files, playlist_name)
        print(f"处理完成！")

if __name__ == '__main__':
    main()
