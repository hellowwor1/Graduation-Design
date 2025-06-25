import os
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, rdmolops
from rdkit.Chem.rdmolops import RDKFingerprint
from rdkit.DataStructs import FingerprintSimilarity, ExplicitBitVect
import mysql.connector
from rdkit.Chem import rdFingerprintGenerator

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
    CREATE TABLE IF NOT EXISTS mhc_HLA_sm_fp (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pdb_id VARCHAR(255) NOT NULL,
        sm_id VARCHAR(255) NOT NULL,
        morgan_fingerprint TEXT,
        rdkit_fingerprint TEXT,
        atompair_fingerprint TEXT
    )
    """
    cursor.execute(create_table_query)
    connection.commit()

def unique_pdb_fp(directory):
    cursor = connection.cursor()
    select_query = "SELECT pdb_id FROM mhc_HLA_sm_fp"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    db_pdb=[]
    for i in range(len(rows)):
        pdb_id, = rows[i]
        db_pdb.append(pdb_id,)
        # print(pdb_id)

    print(len(db_pdb))
    pdb_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.pdb')]

    print(len(pdb_files))

    for index, pdb_path in enumerate(pdb_files):
        filename = os.path.basename(pdb_path).replace(".pdb", "")

        if filename in db_pdb:
            print(filename)
            pdb_files.remove(pdb_path)

    print(len(pdb_files))

    return pdb_files
    

# 计算分子指纹
def calculate_fingerprints(mol):
    # 生成 Morgan 指纹（转换为位向量）
    morgan_generator = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    morgan_fp = morgan_generator.GetFingerprint(mol)
    morgan_bitvect = DataStructs.cDataStructs.UIntSparseIntVectToBitVect(morgan_fp)
    morgan_fingerprint = morgan_bitvect.ToBase64()

    # 生成 AtomPair 指纹（同理）
    ap_generator = rdFingerprintGenerator.GetAtomPairGenerator(fpSize=2048)
    ap_fp = ap_generator.GetFingerprint(mol)
    ap_bitvect = DataStructs.cDataStructs.UIntSparseIntVectToBitVect(ap_fp)
    atompair_fingerprint = ap_bitvect.ToBase64()


    rdkit_fingerprint = RDKFingerprint(mol).ToBase64()


    return morgan_fingerprint, rdkit_fingerprint, atompair_fingerprint

def pdb_to_fingerprintsByBit(pdb_file_path):
    try:
        # 从 PDB 文件中读取分子
        mol = Chem.MolFromPDBFile(pdb_file_path)
        if mol is None:
            print("无法从 PDB 文件中读取分子。")
            return None

        # 生成 Morgan 指纹
        morgan_fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)

        # 生成 AtomPair 指纹
        atom_pair_fp = AllChem.GetHashedAtomPairFingerprintAsBitVect(mol, nBits=1024)

        # 生成 RDKit 指纹
        rdkit_fp = AllChem.RDKFingerprint(mol, fpSize=1024)

        return morgan_fp.ToBitString(), atom_pair_fp.ToBitString(), rdkit_fp.ToBitString()

    except Exception as e:
        print(f"发生错误: {e}")
        return None


def pdb_to_fingerprintsByBit_v2(pdb_file_path):
    try:
        # 读取 PDB 文件
        mol = Chem.MolFromPDBFile(pdb_file_path)
        if mol is None:
            # 获取 RDKit 的详细错误信息
            error_msg = Chem.GetLastStructMsg()
            raise ValueError(f"无法解析 PDB 文件: {error_msg}")

        # 生成 Morgan 指纹 (ECFP4)
        morgan_fp = AllChem.GetMorganFingerprintAsBitVect()

        # 生成 AtomPair 指纹
        atom_pair_fp = AllChem.GetHashedAtomPairFingerprintAsBitVect()

        # 生成 RDKit 指纹
        rdkit_fp = AllChem.RDKFingerprint()

        # 转换为位串表示
        return (
            morgan_fp.ToBitString(),
            atom_pair_fp.ToBitString(),
            rdkit_fp.ToBitString()
        )

    except Exception as e:
        print(f"错误: {e}")
        return None

def pdb_to_fingerprints(pdb_file_path):
    try:
        # 从 PDB 文件中读取分子
        mol = Chem.MolFromPDBFile(pdb_file_path)
        if mol is None:
            print("无法从 PDB 文件中读取分子。")
            return None

        # 生成 Morgan 指纹
        morgan_fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)

        # 生成 AtomPair 指纹
        atom_pair_fp = AllChem.GetHashedAtomPairFingerprintAsBitVect(mol, nBits=1024)

        # 生成 RDKit 指纹
        rdkit_fp = AllChem.RDKFingerprint(mol, fpSize=1024)

        return morgan_fp, atom_pair_fp, rdkit_fp

    except Exception as e:
        print(f"发生错误: {e}")
        return None


# 处理PDB文件并存储指纹到数据库
def process_pdb_files(connection, directory):
    pdb_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.pdb')]

    total_files = len(pdb_files)
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO mhc_hla_sm_fp (pdb_id,sm_id, morgan_fingerprint, rdkit_fingerprint, atompair_fingerprint)
    VALUES (%s,%s, %s, %s, %s)
    """
    for index, pdb_path in enumerate(pdb_files, start=1):
        try:
                filename = os.path.basename(pdb_path).replace(".pdb","")
                sm_id = filename[-1]
                # print(filename[:4])
                morgan_fingerprint, rdkit_fingerprint, atompair_fingerprint = pdb_to_fingerprintsByBit(pdb_path)
                cursor.execute(insert_query, (filename[:4],sm_id, morgan_fingerprint, rdkit_fingerprint, atompair_fingerprint))
                connection.commit()
                progress = (index / total_files) * 100
                print(f"Processed {filename} ({index}/{total_files}, {progress:.2f}%)")
        except Exception as e:
            print(f"Error processing {pdb_path}: {e}")


# 从数据库读取指纹并计算相似度
def read_fingerprints_and_compute(connection):
    cursor = connection.cursor()
    select_query = "SELECT pdb_id, morgan_fingerprint, rdkit_fingerprint, atompair_fingerprint FROM mhc_HLA_sm_fp"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    for i in range(len(rows)):
        pdb_id_1, morgan_bitst_1, rdkit_bitst_1, atompair_bitst_1 = rows[i]
        # 将二进制字符串还原为 ExplicitBitVect 对象
        morgan_fp_1 = DataStructs.CreateFromBitString(morgan_bitst_1)
        atom_pair_fp_1 = DataStructs.CreateFromBitString(atompair_bitst_1)
        rdkit_fp_1 = DataStructs.CreateFromBitString(rdkit_bitst_1)

        for j in range(i + 1, len(rows)):
            pdb_id_2, morgan_bitst_2, rdkit_bitst_2, atompair_bitst_2 = rows[j]
            # 将二进制字符串还原为 ExplicitBitVect 对象
            morgan_fp_2 = DataStructs.CreateFromBitString(morgan_bitst_2)
            atom_pair_fp_2 = DataStructs.CreateFromBitString(atompair_bitst_2)
            rdkit_fp_2 = DataStructs.CreateFromBitString(rdkit_bitst_2)

            morgan_similarity = FingerprintSimilarity(morgan_fp_1, morgan_fp_2)
            rdkit_similarity = FingerprintSimilarity(rdkit_fp_1, rdkit_fp_2)
            atompair_similarity = FingerprintSimilarity(atom_pair_fp_1, atom_pair_fp_2)

            print(f"Similarity between {pdb_id_1} and {pdb_id_2}:")
            print(f"Morgan Similarity: {morgan_similarity}")
            print(f"RDKit Similarity: {rdkit_similarity}")
            print(f"AtomPair Similarity: {atompair_similarity}")
            print("-" * 30)



if __name__ == "__main__":
    directory = "D:\各种杂文件包括课件\大四下\Graduation Design\python-code\static\MHC\mhc_HLA_SmallMolecule_v2"
    connection = connect_to_db()
    d1="./1A6A_small_molecule_1.pdb"
    d2="./static/MHC/mhc_HLA_SmallMolecule_v2/"
    if connection:

        # create_table(connection)
        process_pdb_files(connection, d2)
        # read_fingerprints_and_compute(connection)

        # unique_pdb_fp(directory)

        connection.close()

