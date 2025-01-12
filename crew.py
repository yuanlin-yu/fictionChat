from crewai import Agent, Crew, Process, Task, LLM, Knowledge
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from dotenv import load_dotenv
import os

user_input = ''

# 加载环境变量
load_dotenv()
crew_mode = os.environ.get('CREW_MODE')

# 定义大模型参数
deepseek_llm = LLM(
    model=os.environ.get('OPENAI_MODEL_NAME'),
    api_key=os.environ.get('OPENAI_API_KEY'),
    temperature=0.5
	# temperature参数用于控制模型生成文本的随机性和创造性。temperature值越高，生成的文本越随机和创造性；temperature值越低，生成的文本越确定和一致。
	# 0.0：生成的文本非常确定和一致，几乎没有随机性。模型将尽可能地生成最可能的下一个词。
	# 1.0：这是默认值，通常表示模型在生成文本时具有中等程度的随机性。它既不会过度确定，也不会过度随机。
	# 大于1.0：随着 temperature 值的增加，生成的文本将变得更加随机和创造性。模型将更有可能生成不太常见的词和短语。
	# 大于0.0但小于1.0：随着 temperature 值的减小，生成的文本将变得更加确定和一致。模型将更倾向于生成最常见的词和短语。
	# temperature 参数的范围通常是从0.0到无穷大，但实际使用中，temperature 值通常在0.5到2.0之间。
)

embedder_model = {
		"provider": os.environ.get('EMBEDDER_MODEL_PROVIDER'),
		"config": {
			"model": os.environ.get('EMBEDDER_MODEL_NAME')
		}
	}

# 定义信息源
isFictionSplit = os.environ.get('FICTION_SPLIT') == 'TRUE'
if isFictionSplit:
	# 使用分段文件输入
	file_path_array = []
	file_chunk_num = int(os.environ.get('FICTION_CHUNK_NUM'))
	for i in range(file_chunk_num):
		file_path_array.append(f"fiction_chunk_{i+1}.txt")

	text_source = []
	for i in range(file_chunk_num):
		text_source.append(TextFileKnowledgeSource(
			file_path = file_path_array[i],
			metadata={"author": os.environ.get('FICTION_AUTHOR_NAME')},
			chunk_size=500, #根据自己电脑配置设置
			chunk_overlap=100
		))
else:
	text_source = TextFileKnowledgeSource(
		file_path = [os.environ.get('FICTION_FILE_NAME')],
		metadata={"author": os.environ.get('FICTION_AUTHOR_NAME')},
		chunk_size=500, #根据自己电脑配置设置
		chunk_overlap=100
	)

# 定义crew
@CrewBase
class projectCrew():
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def fiction_character(self) -> Agent:
		return Agent(
			config=self.agents_config['fiction_character'],
			verbose=False,
			llm=deepseek_llm
		)
	
	@agent
	def dialog_summrizer(self) -> Agent:
		return Agent(
			config=self.agents_config['dialog_summrizer'],
			verbose=False,
			llm=deepseek_llm
		)

	@task
	def answer_question_task(self) -> Task:
		return Task(
			config=self.tasks_config['answer_question_task'],
		)
	
	@task
	def summurize_dialog(self) -> Task:
		return Task(
			config=self.tasks_config['summurize_dialog']
		)

	@crew
	def crew(self) -> Crew:
		if crew_mode == 'single_character':
			if user_input["initial"]:
				return Crew(
					agents=[self.fiction_character()],
					tasks=[self.answer_question_task()],
					process=Process.sequential,
					verbose=False,
					knowledge_sources=[text_source[user_input["source_id"]]] if isFictionSplit else [text_source],
					embedder=embedder_model,
					memory=True
				)
			else:		
				return Crew(
					agents=[self.fiction_character()],
					tasks=[self.answer_question_task()],
					process=Process.sequential,
					verbose=False,
					knowledge_sources=[],
					embedder=embedder_model,
					memory=True
				)
		else:
			if user_input["initial"]:
				return Crew(
					agents=[self.dialog_summrizer()],
					tasks=[self.summurize_dialog()],
					process=Process.sequential,
					verbose=False,
					knowledge_sources=[text_source[user_input["source_id"]]] if isFictionSplit else [text_source],
					embedder=embedder_model,
					memory=True
				)
			else:		
				return Crew(
					agents=[self.dialog_summrizer()],
					tasks=[self.summurize_dialog()],
					process=Process.sequential,
					verbose=False,
					knowledge_sources=[],
					embedder=embedder_model,
					memory=True
				)
