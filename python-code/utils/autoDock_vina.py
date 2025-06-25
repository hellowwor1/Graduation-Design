import os
import re


def parse_vina_log(log_file):
    """
    解析AutoDock Vina生成的log文件，提取结合能表格数据
    支持传入文件路径字符串或os.DirEntry对象
    """
    # 处理DirEntry对象，获取文件路径
    if isinstance(log_file, os.DirEntry):
        file_path = log_file.path
    else:
        file_path = log_file

    data = []

    try:
        with open(file_path, 'r') as file:
            log_content = file.read()

            # 使用正则表达式匹配表格数据
            pattern = r'^\s+(\d+)\s+([\-\d\.]+)\s+([\-\d\.]+)\s+([\-\d\.]+)'
            matches = re.finditer(pattern, log_content, re.MULTILINE)

            for match in matches:
                model = int(match.group(1))
                affinity = float(match.group(2))
                rmsd_lb = float(match.group(3))
                rmsd_ub = float(match.group(4))

                data.append({
                    'model': model,
                    'affinity': affinity,
                    'rmsd_lb': rmsd_lb,
                    'rmsd_ub': rmsd_ub
                })

        return data

    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return []
    except Exception as e:
        print(f"发生未知错误：{e}")
        return []