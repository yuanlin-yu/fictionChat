# fictionChat
fictionChat 是有一个基于crewai框架开发的，调用大模型和读取本地txt文件，实现扮演小说角色与用户对话，以及在用户输入特定场景下指定小说人物对话的AI应用。

![DEMO](https://github.com/yuanlin-yu/fictionChat/blob/main/imgs/demo.png)

主要功能：

* 对话模式：模拟小说角色，实现与小说人物对话；
* 场景模式：输入场景，选取小说人物，生成在指定场景下对话；
* 文件读取：通过txt文件读取小说，对于较长的小说可通过分段读取；

更多功能持续开发中

## :rocket: 开始使用

**1. 克隆本仓库链接**:

或从本页面下载。

**2. 安装依赖**:
打开项目目录，运行poetry安装依赖：
```
poetry install
```

**3. 完成部署大模型**:
1、设置大语言模型参数
国内推荐使用deepseek，crewai通过liteLlm调用大模型，支持国内deepseek大模型，其他模型可能要科学上网，其他支持的大模型请查看crewai官网。
申请并获取LLM调用的api key完成后(具体申请过程查看各大LLM官方网站)，修改`.env`中的大模型参数，此处以deepseek为例：
```
# 定义大模型参数
OPENAI_API_BASE = "https://api.deepseek.com/v1" # 大模型api
OPENAI_API_KEY = "xxxxxxxx" # api key
OPENAI_MODEL_NAME = "deepseek/deepseek-chat" # 大模型引用名
```

2、设置嵌入式模型（embedding模型）参数
txt文件读取需要用到embedding模型，由于crewai支持的embedding模型有限，大多是国外的模型，需要科学上网，故此处推荐使用Ollama本地部署的大模型。

安装Ollama，下载embedding模型，此处以windows系统操作为例：
1）登录https://www.ollama.com/，下载ollama并安装完成，打开运行ollama即可在右下角小图标看见，代表正在运行；
2）打开cmd，输入以下命令下载大模型(此处推荐使用nomic-embed-text嵌入式模型)：
```
ollama run nomic-embed-text
```
3）修改`.env`中的embedding模型参数：
```
# 定义embedding模型参数
EMBEDDER_MODEL_PROVIDER = 'ollama' # e.g. 'ollama'
EMBEDDER_MODEL_NAME = 'nomic-embed-text' # e.g. 'nomic-embed-text'
```

**2. 拷贝txt文件，修改变量**:

1、拷贝目标txt文件放置在项目根目录的`knowledge`文件夹下。

2、填写根目录下`.env`文件的crew模式参数，小说参数。

提供两种crew模式：
- 'single_character'：与指定小说人物单独对话; 
- 'scene_characters'：指定场景，生成小说人物之间的对话；

```
# crew模式
CREW_MODE = 'scene_characters' 

# 小说参数
FICTION_NAME = '三国演义' # 小说名
FICTION_AUTHOR_NAME = '罗贯中' # 作者
FICTION_FILE_NAME = '三国演义.txt' # 小说txt文件
FICTION_CHAT_CHARACTER = '孔明' # 小说角色，'single_character'模式下调用
FICTION_CHAT_CHARACTER2 = '刘备' # 'scene_characters'模式下调用两个角色
```

**3. 运行**:

运行`run.py`，等待读取文件完成，即可开始，按提示输入。

windows系统可直接打开.py文件，或者在powershell中输入以下命令：

```
python run.py
```

注意：每次运行会生成相关记忆文件作为ai上下文，故进行新的小说文件读取前建议把记忆文件删掉，详见下面常见问题3。


**常见问题**:

1、若小说长度较长，可能会出现读取错误，出现以下提示：
```
[ERROR]: Failed to upsert documents: timed out in upsert.
```
可通过运行项目根目录下的`splitFiction.py`对txt文件进行分段读取，步骤如下：

1）设置根目录`.env`文件中环境变量：

```
FICTION_SPLIT = TRUE # TRUE or FALSE
FICTION_SPLIT_LENGTH = 30000 # 按此字数分割小说文件, 默认30000字
```
2）运行根目录下的`splitFiction.py`文件，运行成功后便可在`knowledge`文件夹看到分段文件，同时`.env`中`FICTION_CHUNK_NUM`变量自动更新。

2、读取txt文件等待时间较长？

首次运行，需要读取txt文件，请耐心等待。读取完成之后，第二次运行可跳过此步骤，把`main.py`文件中的以下语句取消：

```
# 数据读取
if crew.isFictionSplit:
    for i in range(file_chunk_num): 
        run(character=character, source_id=i, initial=True)
        finish_id = i+1
else:
    run(character=character, initial=True)
```

3、程序的记忆储存在哪里？
记忆储存的地址默认为：
- windows：C:\Users\<user name>\AppData\Local\CrewAI\<fictionChatx项目文件夹名>
- linux: ~/.local/share/<fictionChatx项目文件夹名>

包含短期记忆，长期记忆，知识库等文件及文件夹，建议每次进行新的读取前把这些文件删掉，清除记忆（linux可运行根目录下的`clearMemory.py`）

4、好像txt文件加载报错也可以运行？

若加载过程中出现以下错误，文件通常没加载成功：
```
[ERROR]: Failed to upsert documents: timed out in upsert.
```
但对于比较知名的小说，调用的大模型训练数据中通常已经包含，也能形成对话，但效果肯定不如本地完成读取文件后。
对于一些小众一点的小说，没有完成读取文件，可能大模型无法识别目标小说人物。

5、运行错误输出到哪里？
运行错误log文件输出到根目录下的log\error.log文件。


## :green_book: 许可证

[Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).
