import csv
import os
import re


def extract_hla(line):
    # 匹配HLA模式，允许空格但不捕获后续字母开头的内容
    pattern = r'(HLA[\s-]*[\w\.\*:]+(?:\s+(?![A-Za-z])[\w\.\*:]+)?)'
    match = re.search(pattern, line)
    if match:
        hla_str = match.group(1).strip()

        # 移除尾部非字母数字字符
        hla_str = re.sub(r'[^a-zA-Z0-9]+$', '', hla_str)

        # 移除多余的括号
        hla_str = re.sub(r'^\(+|\)+$', '', hla_str)

        return hla_str
    return None

def get_PDBID_AND_HLA_TABLE(directory,target_dir):
    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    pattern = r'HLA-([^/\s]+)|(HLA-[\w-]+)|HLA\s+(\w+)-[\w-]+'

    pdb_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.pdb')]
    results=[]

    uniqueArray = pdb_unique(directory, csv_file)


    for pdb_path in pdb_files:
        try:
            pdbid = pdb_path.split("\\")[-1].split(".")[0]
            with open(pdb_path, 'r') as file:
                found = False
                title_lines = []
                for line in file:

                    if line.startswith('TITLE'):
                        # 提取TITLE行的内容部分（从第11个字符开始）
                        title_content = line[6:].strip()
                        title_lines.append(title_content)
                    elif line.startswith('COMPND'):
                        # 如果已经收集完所有TITLE行，停止读取
                        break

                        # 合并所有TITLE行的内容
                full_title = ''.join(title_lines)
                # print(full_title)

                # 在合并后的TITLE中提取HLA信息
                if full_title:
                    hla_str = extract_hla(full_title)
                    if hla_str:
                        results.append({'pdbid': pdbid, 'hla': hla_str})
                        continue  # 找到HLA信息，继续处理下一个文件

            # 如果未找到HLA信息
            print(f"未在 {pdbid} 中找到HLA信息")

        except FileNotFoundError:
            print(f"错误：文件 {pdb_path} 未找到。")
        except Exception as e:
            print(f"错误：处理文件 {pdb_path} 时发生未知错误：{e}")
    # 写入CSV文件
    # 构建输出文件路径（在目标文件夹内）
    output_csv = os.path.join(target_dir, "hla_results1.csv")
    if results:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['pdbid', 'hla']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
            print(f"已成功将 {len(results)} 条记录写入 {output_csv}")
    else:
        print("未找到任何HLA信息，CSV文件未生成")


    return pdb_files


def get_file_names(directory):
    """获取目录中所有文件的名称（不含扩展名）"""
    if not os.path.exists(directory):
        print(f"错误：目录 '{directory}' 不存在")
        return []

    file_names = []
    for entry in os.scandir(directory):
        if entry.is_file():
            file_names.append(os.path.splitext(entry.name)[0])
    return file_names


def get_pdbids(csv_file):
    """从CSV文件中提取唯一的PDB ID"""
    if not os.path.exists(csv_file):
        print(f"错误：文件 '{csv_file}' 不存在")
        return []

    pdbids = set()
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        if 'pdbid' not in reader.fieldnames:
            print(f"错误：CSV文件中缺少 'pdbid' 列")
            return []

        for row in reader:
            pdbids.add(row['pdbid'].strip())

    return list(pdbids)

def pdb_unique(directory,csv_file):
    # 获取文件名称
    file_names = get_file_names(directory)
    print(f"目录中的文件数（不含扩展名）：{len(file_names)}")
    if file_names:
        print(f"前5个文件名：{file_names[:5]}")

    # 获取唯一的PDB ID
    pdbids = get_pdbids(csv_file)
    print(f"CSV文件中唯一的PDB ID数：{len(pdbids)}")
    if pdbids:
        print(f"前5个唯一PDB ID：{pdbids[:5]}")

    unique_pdbid=[]
    for file in file_names:
        if file not in pdbids:
            unique_pdbid.append(file)

    print(f"总共有{len(unique_pdbid)}条 ：{unique_pdbid[:]}")
    # print(unique_pdbid)
    return unique_pdbid

if __name__ == "__main__":
    directory = "D:\各种杂文件包括课件\大四下\Graduation Design\python-code\static\MHC\mhc_HLA"
    target_dir = "../static/"
    csv_file = "../static/hla_results.csv"
    get_PDBID_AND_HLA_TABLE(directory,target_dir)
    # pdb_unique(directory,csv_file)