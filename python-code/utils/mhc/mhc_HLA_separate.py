import os
import mysql.connector
from Bio.PDB import PDBParser, PDBIO, Select


# 连接到MySQL数据库
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aa123456",
            database="uni"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# 创建表
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS mhc_pdb_fp (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pdb_id VARCHAR(255) NOT NULL,
        morgan_fingerprint TEXT,
        rdkit_fingerprint TEXT,
        atompair_fingerprint TEXT
    )
    """
    cursor.execute(create_table_query)
    connection.commit()



def split_HLA(directory,target_dir):
    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    pdb_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.pdb')]

    for pdb_path in pdb_files:
        try:
            with open(pdb_path, 'r') as file:
                found = False
                for line in file:
                    # if line.startswith('TITLE') and ('HLA' in line or 'T-CELL' in line.upper()):
                    #     found = True
                    #     break
                    if line.startswith('TITLE') and ('T-CELL' in line in line.upper()):
                        found = True
                        break

                if found:
                    target_path = os.path.join(target_dir, os.path.basename(pdb_path))
                    with open(pdb_path, 'r') as src_file, open(target_path, 'w') as dst_file:
                        dst_file.write(src_file.read())

        except FileNotFoundError:
            print(f"错误：文件 {pdb_path} 未找到。")
        except Exception as e:
            print(f"错误：处理文件 {pdb_path} 时发生未知错误：{e}")


    return pdb_files

class NonAminoAndNonWaterSelect(Select):
    def accept_residue(self, residue):
        # 检查残基是否为水分子
        if residue.get_resname().strip() == 'HOH':
            return False
        return True

# 遍历所有HLA的pbd文件，生成对应的小分子文件
def extract_small_molecules(pdb_dir, target_dir,dir_remove_SM):
    # 如果目标目录不存在，则创建它
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍历指定目录下的所有文件
    for filename in os.listdir(pdb_dir):
        if filename.endswith('.pdb'):
            pdb_file = os.path.join(pdb_dir, filename)
            parser = PDBParser()
            structure = parser.get_structure('hla_structure', pdb_file)
            io = PDBIO()

            small_molecule_count = 0
            small_molecule_residues = []
            for model in structure:
                for chain in model:
                    residues = list(chain.get_residues())
                    if len(residues) < 20:
                        selected_residues = [res for res in residues if NonAminoAndNonWaterSelect().accept_residue(res)]
                        if len(selected_residues) == 0:
                            print(f"Chain {chain.get_id()} in {filename} has no non - amino and non - water residues.")
                            continue
                        small_molecule_count += 1
                        chain_id = chain.get_id()
                        output_file = os.path.join(target_dir, f"{filename[:-4]}_small_molecule_{small_molecule_count}.pdb")
                        io.set_structure(chain)
                        # 使用自定义的选择器来保存非氨基酸和非水分子
                        io.save(output_file, select=NonAminoAndNonWaterSelect())
                        print(f"已将长度小于 20 的小分子（链 {chain_id}）从 {filename} 保存到 {output_file}")
                        small_molecule_residues.extend(selected_residues)

            # 将HLA的小分子抽离之后，剩下的蛋白质文件保存下来.
            # 移除小分子残基
            if len(small_molecule_residues) == 0:
                continue

            for model in structure:
                for chain in model:
                    residues_to_remove = []
                    for residue in chain:
                        if residue in small_molecule_residues:
                            residues_to_remove.append(residue)
                    for residue in residues_to_remove:
                            chain.detach_child(residue.get_id())
            # 保存剩余的蛋白质结构
            protein_output_file = os.path.join(dir_remove_SM, f"{filename[:4]}_removeSM_protein.pdb")
            io.set_structure(structure)
            io.save(protein_output_file)
            print(f"已将蛋白质部分从 {filename} 保存到 {protein_output_file}")

def split_mutil_PDB(pdb_dir, target_dir,):
    # 遍历指定目录下的所有文件
    chains_to_extract =['A', 'B']
    for filename in os.listdir(pdb_dir):
        if filename.endswith('.pdb'):
            pdb_file = os.path.join(pdb_dir, filename)
            parser = PDBParser()
            structure = parser.get_structure('hla_structure', pdb_file)
            io = PDBIO()
            new_structure = structure.copy()
            # 逐个移除模型
            for model in list(new_structure):
                new_structure.detach_child(model.id)

            for model in structure:
                new_model = model.copy()
                # 逐个移除链
                for chain in list(new_model):
                    new_model.detach_child(chain.id)
                for chain in model:
                    if chain.id in chains_to_extract:
                        new_chain = chain.copy()
                        new_model.add(new_chain)
                if len(new_model) > 0:
                    new_structure.add(new_model)

            io.set_structure(new_structure)
            try:
                protein_output_file = os.path.join(target_dir, f"{filename[:4]}_removeSM_protein.pdb")
                io.save(protein_output_file)
                print(f"成功提取链并保存到 {protein_output_file}。")
            except Exception as e:
                print(f"保存文件时出错：{e}")



# 删掉空的小分子pdb文件
def delet_empty_(directory):
    pdb_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.pdb')]

    for pdb_path in pdb_files:
        try:
            with open(pdb_path, 'r') as file:
                lines = file.readlines()
                if len(lines) == 1 and lines[0].strip() == 'END':
                    # os.remove(pdb_path)
                    print(f"文件 {pdb_path} 已删除。")
                # else:
                #     print(f"文件 {pdb_path} 不满足删除条件。")

        except FileNotFoundError:
            print(f"错误：文件 {pdb_path} 未找到。")
        except Exception as e:
            print(f"错误：处理文件 {pdb_path} 时发生未知错误：{e}")


if __name__ == "__main__":
    directory = "../static/mhc_pdb_file/"
    mhc_HLA_dir = 'D:\各种杂文件包括课件\大四下\Graduation Design\python-code\static\MHC\mhc_HLA'
    mhc_TCELL_dir = '../static/mhc_T-CELL/'
    mhc_HLA_SmallMolecule_dir_v1 ='../static/mhc_HLA_SmallMolecule/'
    mhc_HLA_remove_SM_v1 ='../static/mhc_HLA_remove_SM/'
    # split_HLA(directory,target_dir2)
    mhc_HLA_SmallMolecule_dir_v2 = 'D:\各种杂文件包括课件\大四下\Graduation Design\python-code\static\MHC\mhc_HLA_SmallMolecule_v2'
    mhc_HLA_remove_SM_v2 = 'D:\各种杂文件包括课件\大四下\Graduation Design\python-code\static\MHC\mhc_HLA_remove_SM_v2'
    mhc_HLA_remove_SM_v3 = 'D:\各种杂文件包括课件\大四下\Graduation Design\python-code\static\MHC\mhc_HLA_remove_SM_v3'
    # extract_small_molecules(mhc_HLA_dir,mhc_HLA_SmallMolecule_dir_v2,mhc_HLA_remove_SM_v2)
    split_mutil_PDB(mhc_HLA_remove_SM_v2,mhc_HLA_remove_SM_v3)
    # delet_empty_(target_dir3)
    # connection = connect_to_db()
    # if connection:
    #
    #
    #     connection.close()

