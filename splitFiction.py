from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 定义小说分割长度
split_size = int(os.environ.get('FICTION_SPLIT_LENGTH'))

def split_text_into_chunks(text, chunk_size=split_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

file_name = os.environ.get('FICTION_FILE_NAME')
file_path = f'knowledge/{file_name}'
text = read_text_file(file_path)
chunks = split_text_into_chunks(text, chunk_size=split_size)

# 保存分段后的文本到多个文件
counts = 0
for i, chunk in enumerate(chunks):
    with open(f'knowledge/fiction_chunk_{i+1}.txt', 'w', encoding='utf-8') as file:
        file.write(chunk)
        counts += 1

print(f"文本分割完成，分割段数为{counts}")

# 修改环境变量
def update_env_variable(file_path, key, new_value):
    # 读取 .env 文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 遍历每一行，找到目标变量并更新
    with open(file_path, 'w') as file:
        for line in lines:
            if line.startswith(key + ' ='):
                # 更新变量值
                file.write(f"{key} = {new_value}\n")
            else:
                # 保持其他行不变
                file.write(line)

# 示例：修改 .env 文件中的变量
update_env_variable('.env', 'FICTION_CHUNK_NUM', f'{counts}')

print(f"环境变量已更新，FICTION_CHUNK_NUM = {counts}")

# 确保命令行窗口不自动关闭
os.system('pause')