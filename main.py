import crew
from crew import projectCrew
from dotenv import load_dotenv
import os
import threading
import time
import sys

# 加载环境变量
load_dotenv()
file_chunk_num = int(os.environ.get('FICTION_CHUNK_NUM'))
finish_id = 0

# 显示等待符号的函数
def show_waiting_symbol():
    symbols = ["/", "-", "\\", "|"]
    i = 0
    while not done:
        sys.stdout.write("\r" + f"{f'读小说中,已完成:{round(finish_id/file_chunk_num*100,2)}% ' if crew.user_input['initial'] else '思考中'} " + symbols[i % len(symbols)])
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

# 运行 Crew 的函数
def run(character, question='', source_id=0, initial=False):
    global done
    done = False

    # 输入参数
    inputs = {
        "character": character,
        "question": question,
        "source_id": source_id,
        "initial": initial
    }
    crew.user_input = inputs

    # 启动等待符号线程
    waiting_thread = threading.Thread(target=show_waiting_symbol)
    waiting_thread.start()

    # 运行crew
    result = projectCrew().crew().kickoff(inputs=inputs)

    done = True
    waiting_thread.join()  
    sys.stdout.write("\r" + " " * 20 + "\r")  
    return result

def run2(character, character2, scene='', source_id=0, initial=False):
    global done
    done = False

    # 输入参数
    inputs = {
        "character": character,
        "character2": character2,
        "scene": scene,
        "source_id": source_id,
        "initial": initial
    }
    crew.user_input = inputs

    # 启动等待符号线程
    waiting_thread = threading.Thread(target=show_waiting_symbol)
    waiting_thread.start()

    # 运行crew
    result = projectCrew().crew().kickoff(inputs=inputs)

    done = True
    waiting_thread.join()  
    sys.stdout.write("\r" + " " * 20 + "\r")  
    return result

fiction_name = os.environ.get('FICTION_NAME')
author_name = os.environ.get('FICTION_AUTHOR_NAME')
character = os.environ.get('FICTION_CHAT_CHARACTER')
character2 = os.environ.get('FICTION_CHAT_CHARACTER2')

if __name__ == "__main__":
    print(f"** 欢迎使用fictionChat, 在这里您可以与小说人物畅聊 **\n")
    print(f"** 小说：《{fiction_name}》，作者：{author_name} **\n")

    if crew.crew_mode == 'single_character':
        print(f"** 小说人物：{character} **\n")
        # 数据读取
        if crew.isFictionSplit:
            for i in range(file_chunk_num): 
                run(character=character, source_id=i, initial=True)
                finish_id = i+1
        else:
            run(character=character, initial=True)
        print('** 数据初始化完成! **\n')
        print('** 现在可以开始对话了！请输入您的问题(输入"exit"退出): **\n')
        while True:     
            print("- 问题：")   
            question = input()
            if question == 'exit':
                break
            result = run(character, question)
            print(result.raw+'\n')
    else:
        print(f"** 小说人物：{character}、{character2} **\n")
        # 数据读取
        if crew.isFictionSplit:
            for i in range(file_chunk_num): 
                run2(character=character, character2=character2, source_id=i, initial=True)
                finish_id = i+1
        else:
            run2(character=character, character2=character2, initial=True)
        print('** 数据初始化完成! **\n')
        print("* 请输入场景：")   
        scene = input()
        result = run2(character, character2, scene)
        print(result.raw+'\n')
            
    