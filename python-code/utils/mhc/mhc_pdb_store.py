import mysql.connector
import os

# 数据库连接配置
config = {
    'user': 'root',  # 替换为你的 MySQL 用户名
    'password': 'Aa123456',  # 替换为你的 MySQL 密码
    'host': 'localhost',  # 数据库主机地址
    'database': 'uni',  # 数据库名称
}

# 连接到数据库
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# PDB 文件存储路径（相对路径）
pdb_folder = "D:\各种杂文件包括课件\大四下\Graduation Design\python-code\static\mhc_pdb_file"  # 当前工程目录下的文件夹路径

# 获取所有 PDB 文件
pdb_files = [file_name for file_name in os.listdir(pdb_folder) if file_name.endswith(".pdb")]
total_files = len(pdb_files)
processed_files = 0

# 遍历文件夹中的 PDB 文件并存储到数据库
for file_name in pdb_files:
    pdb_id = file_name.split('.')[0]  # 获取 PDB ID
    file_path = "./static/mhc_pdb_file"+"/"+file_name

    # 插入数据到数据库
    query = "INSERT INTO mhc_pdb_file (pdb_id, file) VALUES (%s, %s)"
    cursor.execute(query, (pdb_id, file_path))

    # 更新进度
    # processed_files += 1
    # progress = (processed_files / total_files) * 100
    # print(f"Progress: {progress:.2f}% ({processed_files}/{total_files})")

# 提交事务并关闭连接
conn.commit()
cursor.close()
conn.close()

print("All PDB files have been indexed in the database.")