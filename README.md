# navidrome歌单生成器

这是一个简单而实用的m3u歌单生成工具，可以根据指定的歌曲列表，从navidrome音乐库中匹配相应的音频文件，并生成M3U格式的播放列表。

## 功能特点

- 支持多种音频格式：flac, wav, dts, aiff, m4a, ape, aac, mp3, ogg, wma
- 智能文件匹配：使用包含关系匹配，更灵活地找到目标歌曲
- 自动提取元数据：从文件路径中提取艺术家和歌曲名信息
- 生成标准M3U播放列表

## 使用方法

1. 首先运行 `list_audio_files.py` 生成音频文件列表：
   ```bash
   python list_audio_files.py
   ```
   - 在运行前请修改脚本中的 `search_directory` 为你的音乐库路径
   - 脚本会生成 `audio_files.txt`，包含所有支持格式的音频文件路径

2. 准备目标歌曲列表文件 `list.txt`：
   - 每行一个歌曲名
   - 格式建议：`歌手名 - 歌曲名`
   - 不区分大小写
   - 支持模糊匹配

3. 运行 `main.py` 生成播放列表：
   ```bash
   python main.py
   ```
   - 程序会读取 `audio_files.txt` 和 `list.txt`
   - 自动匹配文件并生成M3U播放列表
   - 默认输出文件名为 `music_playlist.m3u`（可在代码中修改）

4. 将m3u丢到navidrome的`music/playlists`目录中

## 文件结构说明

- `list_audio_files.py`: 用于扫描音乐库并生成文件列表(请将目录共享出来以便windows读取)
- `main.py`: 主程序，用于生成播放列表
- `audio_files.txt`: 存储音频文件路径的列表文件
- `list.txt`: 目标歌曲列表文件
- `*_playlist.m3u`: 生成的播放列表文件

## 注意事项

1. 文件路径处理：
   - 程序会自动处理路径中的反斜杠
   - 会自动移除磁盘编号（如 "Y:"）
   - 支持中文路径和文件名

2. 匹配规则：
   - 使用包含关系匹配，比如目标歌曲"周深-大鱼"可以匹配到"周深-大鱼live版"
   - 匹配时不区分大小写
   - 自动去除首尾空格

3. M3U播放列表：
   - 使用UTF-8编码
   - 包含歌曲时长信息（默认300秒）
   - 包含艺术家和歌曲名信息

## 自定义配置

如需修改配置，可以编辑以下参数：

- `list_audio_files.py` 中的 `search_directory`: 设置音乐库路径
- `main.py` 中的：
  - `audio_files_list`: 音频文件列表的文件名
  - `target_songs_file`: 目标歌曲列表的文件名
  - `output_m3u`: 输出播放列表的文件名
  - `playlist_name`: 播放列表的显示名称 
