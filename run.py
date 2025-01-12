import sys
import os
import subprocess

# 确保 log 目录存在
log_dir = "log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 定义日志文件路径
error_log_path = os.path.join(log_dir, "error.log")

# 运行 main.py 并重定向标准错误输出到 log/error.log
try:
    with open(error_log_path, "w") as error_log:
        # 使用 subprocess 运行 main.py，并重定向 stderr
        result = subprocess.run(
            [sys.executable, "main.py"],  # 使用当前 Python 解释器运行 main.py
            stderr=error_log,             # 重定向 stderr 到 error_log
            text=True                     # 以文本模式处理输出
        )
        # 检查命令是否成功执行
        if result.returncode == 0:
            print("main.py 执行成功！")
        else:
            print(f"main.py 执行失败，返回码: {result.returncode}")
except Exception as e:
    print(f"运行 main.py 时发生异常: {e}")

os.system('pause')