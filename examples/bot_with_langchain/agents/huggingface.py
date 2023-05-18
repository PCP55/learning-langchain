# References
# https://github.com/hwchase17/langchain/issues/2667

from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from langchain.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, T5Tokenizer, T5ForConditionalGeneration, GPT2TokenizerFast
from transformers import LlamaForCausalLM, LlamaTokenizer


template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
print(prompt)

# Local model path
model_path = "/sd_models/llama/chavinlo/gpt4-x-alpaca"
model = LlamaForCausalLM.from_pretrained(model_path, device_map="auto", load_in_8bit=True)
tokenizer = AutoTokenizer.from_pretrained(model_path)

print('making a pipeline...')
#max_length has typically been deprecated for max_new_tokens 
pipe = pipeline(
    "text-generation", model=model, tokenizer=tokenizer, max_new_tokens=64, model_kwargs={"temperature":0}
)
hf = HuggingFacePipeline(pipeline=pipe)

llm_chain = LLMChain(prompt=prompt, llm=hf)
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
print(llm_chain.run(question))
