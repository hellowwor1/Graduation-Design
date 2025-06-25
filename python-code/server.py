import base64
import json
import os
import zipfile

from collections import defaultdict
from tempfile import NamedTemporaryFile

import mysql.connector
from Bio.PDB import PDBParser, PDBIO
from flask import Flask, request, jsonify, send_file, Response
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, RDKFingerprint
from rdkit.DataStructs import FingerprintSimilarity

from openbabel import pybel
from openbabel import openbabel as ob

from utils.mhc.mhc_pdc_fingerprint import connect_to_db, pdb_to_fingerprints
from utils.response import ResultResponse
from utils.tasks import insert_task, update_task
from utils.autoDock_vina import parse_vina_log


# 任务状态存储
task_status = defaultdict(dict)
app = Flask(__name__)
# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Aa123456',
    'database': 'uni'
}

@app.route('/upload-3d/visualize-pdb-pymol', methods=['POST'])
def visualize_pdb_pymol():

    return  jsonify(ResultResponse.to_dict(200,"暂未开发",""))


# 弃用
@app.route('/upload-3d/getPdbFile/<string:id>_out', methods=['GET'])
def get_mhc_pdb_file(id):
    conn = None
    cursor = None
    try:
        # 数据库查询部分保持不变
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT file FROM mhc_pdb_file WHERE pdb_id = %s", (id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "PDB ID not found"}), 404

        file_path = result['file']

        # 读取文件内容
        with open(file_path, 'rb') as f:  # 二进制模式读取
            file_content = f.read()

        # 方案选择：根据文件类型决定编码方式
        if file_path.lower().endswith('.pdb'):
            # 文本文件直接UTF-8编码
            content = file_content.decode('utf-8')
            encoding = 'text'
        else:
            # 二进制文件使用Base64编码
            content = base64.b64encode(file_content).decode('utf-8')
            encoding = 'base64'

        return jsonify({
            "status": "success",
            "filename": os.path.basename(file_path),
            "content": content,
            "encoding": encoding,
            "mime_type": "chemical/x-pdb",
            "code": 0
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return "Internal server error", 500
    finally:
        # 确保关闭数据库连接
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/upload-3d/getPdbFile/<string:id>', methods=['GET'])
def new_get_mhc_pdb_file(id):
    conn = None
    cursor = None
    try:
        file_path = f"./static/MHC/mhc_pdb_file/{id}.pdb"
        # 读取文件内容
        with open(file_path, 'rb') as f:  # 二进制模式读取
            file_content = f.read()

        # 方案选择：根据文件类型决定编码方式
        if file_path.lower().endswith('.pdb'):
            # 文本文件直接UTF-8编码
            content = file_content.decode('utf-8')
            encoding = 'text'
        else:
            # 二进制文件使用Base64编码
            content = base64.b64encode(file_content).decode('utf-8')
            encoding = 'base64'

        return jsonify({
            "status": "success",
            "filename": os.path.basename(file_path),
            "content": content,
            "encoding": encoding,
            "mime_type": "chemical/x-pdb",
            "code": 0
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return "Internal server error", 500
    finally:
        # 确保关闭数据库连接
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()



# 废弃了
@app.route('/upload-3d/getDockingPdbFile_out', methods=['POST'])
def get_Docking_pdb_file():
        res=request.get_json()
        pdbId=res['pdbId']
        smName=res['smName']
        pdb_path = f'./static/MHC/mhc_HLA_remove_SM_v3/{pdbId}_removeSM_protein_v3.pdb'
        sm_path=f'./static/uploads/{smName}.pdb'
        output_pdb_file=f'./static/Dockings/{pdbId}_DK_{smName}_.pdb'
        print(smName)
        Docking_pdb_file(pdb_path,sm_path,output_pdb_file)
        try:
            # 读取文件内容
            with open(output_pdb_file, 'rb') as f:  # 二进制模式读取
                file_content = f.read()

            # 方案选择：根据文件类型决定编码方式
            if output_pdb_file.lower().endswith('.pdb'):
                # 文本文件直接UTF-8编码
                content = file_content.decode('utf-8')
                encoding = 'text'
            else:
                # 二进制文件使用Base64编码
                content = base64.b64encode(file_content).decode('utf-8')
                encoding = 'base64'

            return jsonify({
                "status": "success",
                "filename": os.path.basename(output_pdb_file),
                "content": content,
                "encoding": encoding,
                "mime_type": "chemical/x-pdb",
                "code": 0
            })

        except Exception as e:
            print(f"Error: {str(e)}")
            return "Internal server error", 500

@app.route('/upload-3d/getDockingPdbFile', methods=['POST'])
def new_get_Docking_pdb_file():
        res=request.get_json()
        pdbId=res['pdbId']
        smName=res['smName']
        NewFileName = f"{smName}_DOCK_{pdbId}.pdb"

        # task_id=insert_task(2,NewFileName,'对接完成',0)
        # task_status[task_id] = {
        #     'status': '对接完成',
        #     'progress': 0,
        #     'message': '任务已创建'
        # }

        pdb_path = f'./static/MHC/mhc_HLA_remove_SM_v3/{pdbId}_removeSM_protein_v3.pdb'
        sm_path=f'./static/uploads/{smName}.pdb'

        output_pdb_dir=f'./static/Tasks/task_id'

        # 做演示用途
        res = new_Docking_pdb_file(pdb_path,sm_path,output_pdb_dir)
        if res == None:
           output_pdb_dir="./static/"
           print("开启演示功能")
           convert_pdbqt_to_multimodel_pdb("./static/1A6A_small_molecule_1_out.pdbqt")
        try:
            # 遍历目录中的所有条目
            with os.scandir(output_pdb_dir) as entries:
                for entry in entries:
                    # 只处理文件，跳过子目录
                    if entry.is_file():
                        filename = entry.name
                        # 检查文件扩展名
                        if filename.lower().endswith('.pdb'):
                            # 读取文件内容
                            with open(entry.path, 'rb') as f:
                                file_content = f.read()
                            content = file_content.decode('utf-8')
                            encoding = 'text'
                            print("读取含多模型.pdb文件成功")
                        if filename.lower().endswith('.log'):
                            # 读取文件内容
                            binding_energies = parse_vina_log(entry)
                            print("解析.log文件成功")
                            # print(binding_energies)

            return jsonify({
                "status": "success",
                "filename": NewFileName,
                # .pdbqt文件内容
                "content": content,
                "binding_energies":binding_energies,
                "encoding": encoding,
                "mime_type": "chemical/x-pdb",
                "code": 0
            })

        except Exception as e:
            print(f"Error: {str(e)}")
            return "Internal server error", 500


def Docking_pdb_file(protein_pdb_file,small_molecule_pdb_file,output_pdb_file):
    # 初始化 PDB 解析器
    parser = PDBParser()

    # 解析蛋白质 PDB 文件
    protein_structure = parser.get_structure('protein', protein_pdb_file)

    # 解析小分子 PDB 文件
    small_molecule_structure = parser.get_structure('small_molecule', small_molecule_pdb_file)

    # 获取蛋白质结构的第一个模型
    protein_model = protein_structure[0]

    # 获取小分子结构的第一个模型
    small_molecule_model = small_molecule_structure[0]

    # 生成一个未使用的链 ID
    used_chain_ids = [chain.id for chain in protein_model]
    new_chain_id = 'A'
    while new_chain_id in used_chain_ids:
        new_chain_id = chr(ord(new_chain_id) + 1)

    # 把小分子的链添加到蛋白质模型中
    for chain in small_molecule_model:
        chain.id = new_chain_id
        protein_model.add(chain)

    # 初始化 PDB 写入器
    io = PDBIO()
    # 设置要写入的结构
    io.set_structure(protein_structure)
    # 保存合并后的结构到输出文件
    io.save(output_pdb_file)



#预留的接口
def new_Docking_pdb_file(protein_pdb_file,small_molecule_pdb_file,output_pdb_file):
    # protein_pdb_file 是靶标蛋白的位置
    # small_molecule_pdb_file 是用户提交的小分子文件的位置
    # output_pdb_file 是最后对接之后生成.pdbqt文件 与 .log 文件的位置
    return None


def convert_pdbqt_to_multimodel_pdb(pdbqt_path, output_path=None):
    """将 PDBQT 文件转换为包含所有构象的多模型 PDB 文件"""
    if output_path is None:
        output_path = os.path.splitext(pdbqt_path)[0] + "_multi.pdb"
        print("解析的路径:"+output_path)
    conv = ob.OBConversion()
    if not conv.SetInFormat("pdbqt"):
        raise ValueError("不支持输入格式 pdbqt")
    if not conv.SetOutFormat("pdb"):
        raise ValueError("不支持输出格式 pdb")

    # 设置追加模式和多模型处理
    conv.AddOption("a", ob.OBConversion.OUTOPTIONS)

    mol = ob.OBMol()
    total_models = 0
    not_end = conv.ReadFile(mol, pdbqt_path)

    if not not_end:
        print("错误：未找到任何模型！")
        return 0

    while not_end:
        if total_models == 0:
            conv.WriteFile(mol, output_path)  # 首次写入创建文件
        else:
            conv.Write(mol)  # 后续追加

        mol.Clear()
        not_end = conv.Read(mol)
        total_models += 1

    print(f"成功写入 {total_models} 个模型到 {output_path}")


def get_pdb_fp():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        select_query = "SELECT pdb_id, morgan_fingerprint, rdkit_fingerprint, atompair_fingerprint FROM mhc_pdb_fp"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        pdb_fp =[]
        for i in range(len(rows)):
            pdb_id_1, morgan_1, rdkit_1, atompair_1 = rows[i]
            if pdb_id_1=="1A0Q":
                continue
            # 从Base64字符串恢复指纹
            morgan_fp_1 = AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles('C'), 2)
            morgan_fp_1.FromBase64(morgan_1)
            rdkit_fp_1 = RDKFingerprint(Chem.MolFromSmiles('C'))
            rdkit_fp_1.FromBase64(rdkit_1)
            atompair_fp_1 = AllChem.GetHashedAtomPairFingerprintAsBitVect(Chem.MolFromSmiles('C'))
            atompair_fp_1.FromBase64(atompair_1)
            pdb_fp.append({
                "pdb_id": pdb_id_1,
                "morgan": morgan_fp_1,
                "rdkit" :rdkit_fp_1,
                "atompair": atompair_fp_1,
            })
        connection.close()
        return  pdb_fp



def get_sm_fp(pdb_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        select_query = "SELECT pdb_id,sm_id, morgan_fingerprint, rdkit_fingerprint, atompair_fingerprint FROM mhc_hla_sm_fp"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        sm_fp =[]
        for i in range(len(rows)):
            pdb_id_1,sm_id, morgan_bitst_1, rdkit_bitst_1, atompair_bitst_1 = rows[i]
            # if pdb_id_1==pdb_id:
            #     continue
            # 将二进制字符串还原为 ExplicitBitVect 对象
            morgan_fp_1 = DataStructs.CreateFromBitString(morgan_bitst_1)
            atom_pair_fp_1 = DataStructs.CreateFromBitString(atompair_bitst_1)
            rdkit_fp_1 = DataStructs.CreateFromBitString(rdkit_bitst_1)

            sm_fp.append({
                "pdb_id": pdb_id_1,
                "sm_id" : sm_id,
                "morgan": morgan_fp_1,
                "rdkit" :rdkit_fp_1,
                "atompair": atom_pair_fp_1,
            })
        connection.close()
        return  sm_fp


# 废弃了
@app.route('/upload-3d/cal_out', methods=['POST'])
def upload_pdb():
    try:
        file = request.files['file']
        save_path = os.path.join('./static/uploads', file.filename)
        file.save(save_path)
        query_fp={}
        # 展示用途
        if file.filename =="1A0Q.pdb":
            print("作展示用途")
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                pdb_id = '1A0Q'
                select_query = "SELECT pdb_id, morgan_fingerprint, rdkit_fingerprint, atompair_fingerprint " \
                               "FROM mhc_pdb_fp WHERE pdb_id = %s"
                cursor.execute(select_query, (pdb_id,))
                rows = cursor.fetchall()
                pdb_id_1, morgan_1, rdkit_1, atompair_1 = rows[0]
                # 从Base64字符串恢复指纹
                morgan_fp_1 = AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles('C'), 2)
                morgan_fp_1.FromBase64(morgan_1)
                rdkit_fp_1 = RDKFingerprint(Chem.MolFromSmiles('C'))
                rdkit_fp_1.FromBase64(rdkit_1)
                atompair_fp_1 = AllChem.GetHashedAtomPairFingerprintAsBitVect(Chem.MolFromSmiles('C'))
                atompair_fp_1.FromBase64(atompair_1)
                query_fp={
                    'pdb_id':"1A0Q",
                    'morgan':morgan_fp_1,
                    'rdkit': rdkit_fp_1,
                    'atompair':atompair_fp_1,
                }
            connection.close()

        else :
            # 计算查询分子的指纹
            mol = Chem.MolFromPDBFile(save_path)
            query_fp = {
                'pdb_id': file.filename.replace(".pdb", ""),
                'morgan': AllChem.GetMorganFingerprintAsBitVect(mol, 2),
                'rdkit': RDKFingerprint(mol),
                'atompair': AllChem.GetHashedAtomPairFingerprintAsBitVect(mol),
            }

        pdb_fps=get_pdb_fp()


        # 计算相似度
        results = []
        for fp_type in ['morgan', 'rdkit', 'atompair']:
            similarities = []
            for pdb_fp in pdb_fps:
                sim = FingerprintSimilarity(query_fp[fp_type], pdb_fp[fp_type])
                similarities.append((pdb_fp['pdb_id'], sim))

            # 按相似度排序
            similarities.sort(key=lambda x: x[1], reverse=True)
            # 只保留前20个元素
            similarities = similarities[:20]
            results.append({
                "method": fp_type.upper() + " 指纹",
                "ranking": [{"name": name, "score": score} for name, score in similarities],
                "code": 0,
                "status": "success",
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "code": 0,
        },), 500

@app.route('/upload-3d/cal', methods=['POST'])
def new_upload_pdb():
    try:
        file = request.files['file']
        task_id=insert_task(1,file.filename,'开始处理',0)
        task_status[task_id] = {
            'status': '开始处理',
            'progress': 0,
            'message': '任务已创建'
        }
        save_path = os.path.join('./static/uploads', file.filename)
        file.save(save_path)
        pdb_id=file.filename[:4]

        # 更新任务状态
        task_status[task_id].update({
            'status': '正在计算指纹',
            'progress': 20,
            'message': '正在计算分子指纹'
        })
        update_task(task_id,'正在计算指纹',20)

        # 计算用户上传的小分子的指纹
        morgan_fingerprint, rdkit_fingerprint, atompair_fingerprint =pdb_to_fingerprints(save_path)
        query_fp = {
            'pdb_id': pdb_id,
            'morgan': morgan_fingerprint,
            'rdkit': rdkit_fingerprint,
            'atompair': atompair_fingerprint,
        }

        # 更新任务状态
        task_status[task_id].update({
            'status': '正在查询数据库',
            'progress': 40,
            'message': '正在查询相似分子'
        })
        update_task(task_id, '正在查询相似分子', 40)

        # 不去把用户上传的同一个pdb_id取出来
        sm_fps=get_sm_fp(pdb_id)

        # 更新任务状态
        task_status[task_id].update({
            'status': '正在计算相似度',
            'progress': 60,
            'message': '正在计算相似度'
        })
        update_task(task_id, '正在计算相似度', 60)

        # 计算相似度
        results = []
        for fp_type in ['morgan', 'rdkit', 'atompair']:
            similarities = []
            for sm_fp in sm_fps:
                sim = FingerprintSimilarity(query_fp[fp_type], sm_fp[fp_type])
                similarities.append((sm_fp['pdb_id'],sm_fp['sm_id'], sim))

            # 按相似度排序
            similarities.sort(key=lambda x: x[2], reverse=True)
            # 只保留前30个元素
            similarities = similarities[:30]
            results.append({
                "method": fp_type.upper() + " 指纹",
                # "ranking": [{"name": name, "score": score} for name, score in similarities],
                "ranking": [{"name": f"{pdb_id}","smid":f"{sm_id}", "score": sim} for pdb_id, sm_id, sim in similarities],
                "code": 0,
                "status": "success",
            })

            # 任务完成
            task_status[task_id].update({
                'status': '已完成',
                'progress': 100,
                'message': '任务处理完成'
            })
            update_task(task_id, '已完成', 100,json.dumps(results))

        return jsonify(results)

    except Exception as e:
        # 异常终止
        task_status[task_id].update({
            'status': '异常',
            'progress': 0,
            'message': '异常终止'
        })
        update_task(task_id, '失败', 0)
        return jsonify({
            "error": str(e),
            "code": 0,
        },), 500


@app.route('/upload-3d/download/docking-files', methods=['POST'])
def download_docking_files():
    # 获取前端传递的参数
    res = request.get_json()
    pdb_name = res['pdbId'] #靶标蛋白
    smpdb = res['smName']#小分子
    flag = res['mode']
    # if not pdb_name or not smpdb:
    #     return "缺少必要参数：pdbName 或 currentPdb", 400

    # 构造文件存储路径（根据实际存储结构调整）
    # base_dir = f"/app/data/docking_results/{smpdb}/{pdb_name}"  # 替换为实际存储路径
    # log_path = os.path.join(base_dir, "result.log")
    # pdbqt_path = os.path.join(base_dir, "docking.pdbqt")

    # 做演示用途
    base_dir = f"./static/"
    log_path = os.path.join(base_dir, "1A6A_small_molecule_1.log")
    pdbqt_path = os.path.join(base_dir, "1A6A_small_molecule_1_out.pdbqt")
    # 检查文件是否存在
    if not all([os.path.exists(log_path), os.path.exists(pdbqt_path)]):
        return "文件不存在", 400

    # 设置响应头（包含X-Code）
    if flag ==0:
        sendfile=log_path
    else :
        sendfile=pdbqt_path
    sendname=sendfile.split("/")[-1]
    response = send_file(
        sendfile,
        as_attachment=True,
        download_name=f"{sendname}",
        mimetype='text/plain'
    )
    response.headers['X-Code'] = '0'
    return response



if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True,threaded=True)
