import random
from datetime import datetime

import mysql.connector


def generate_PRED_task_id():
    # 获取当前日期
    current_date = datetime.now().strftime("%Y%m%d")
    # 生成一个随机的增量，范围在 1 到 10000 之间
    random_increment = random.randint(1, 10000)
    # 组合日期和随机增量生成 task_id
    task_id = f"PRED-{current_date}{random_increment:04d}"
    return task_id
def generate_DOCK_task_id():
    # 获取当前日期
    current_date = datetime.now().strftime("%Y%m%d")
    # 生成一个随机的增量，范围在 1 到 10000 之间
    random_increment = random.randint(1, 10000)
    # 组合日期和随机增量生成 task_id
    task_id = f"DOCK-{current_date}{random_increment:04d}"
    return task_id

def get_creation_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_connection():
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


def insert_task(Type,file_name, status, progress, result=None):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        task_id=""
        if Type ==1 :
            task_id=generate_PRED_task_id()
        else:
            task_id=generate_DOCK_task_id()
        create_time = get_creation_time()
        try:
            sql = "INSERT INTO pdb_prediction_tasks (task_id, file_name, status, create_time, progress, result) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (task_id, file_name, status, create_time, progress, result)
            cursor.execute(sql, values)
            connection.commit()
            print("Task inserted successfully.")
            return  task_id
        except mysql.connector.Error as err:
            print(f"Error inserting task: {err}")
        finally:
            cursor.close()
            connection.close()


def query_tasks():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            sql = "SELECT * FROM pdb_prediction_tasks"
            cursor.execute(sql)
            tasks = cursor.fetchall()
            for task in tasks:
                print(task)
            return  tasks
        except mysql.connector.Error as err:
            print(f"Error querying tasks: {err}")
        finally:
            cursor.close()
            connection.close()


def update_task(task_id, status, progress, result=None):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            sql = "UPDATE pdb_prediction_tasks SET status = %s, progress = %s, result = %s WHERE task_id = %s"
            values = (status, progress, result, task_id)
            cursor.execute(sql, values)
            connection.commit()
            print(f"{task_id}: Task updated successfully.")
        except mysql.connector.Error as err:
            print(f"{task_id}: Error updating task: {err}")
        finally:
            cursor.close()
            connection.close()


