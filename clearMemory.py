import subprocess
import os

# 定义要执行的命令
commands = [
    'rm -rf ~/.local/share/fictionChat/short_term',
    'rm -rf ~/.local/share/fictionChat/long_term_memory_storage.db',
    'rm -rf ~/.local/share/fictionChat/latest_kickoff_task_outputs.db',
    'rm -rf ~/.local/share/fictionChat/entities'
    'rm -rf ~/.local/share/fictionChat/knowledge'
]

# 遍历命令列表并执行每个命令
for command in commands:
    subprocess.run(command, shell=True, check=True)

# 确保命令行窗口不自动关闭
os.system('pause')