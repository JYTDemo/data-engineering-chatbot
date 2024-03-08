from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
import autopep8
import pandas as pd
import os

class datachat():

    def __init__(self,file_path):
        FILENAME='mistral-7b-openorca.Q4_K_S.gguf'
        model_path=f'D:/01MyFolder/code/model/{FILENAME}'
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        self.llm = LlamaCpp(
            model_path=model_path,
            repetition_penalty= 2.0,
            temperature=0.00,
            #do_sample=True,
            max_tokens=2000,
            n_ctx=2048,
            context_length=4000,
            callback_manager=callback_manager,
            #top_k=50,
            #top_p=0.95,
        )
        self.instruction = """
        As a python coder create a pythonic response for the query with reference to the columns in my pandas dataframe{columns}.
        Instruction:
        Do not write the whole script just give me a pythonic response for this query and do not extend more than asked. Assume a dataframe variable df_temp.
        Enclose the generated code in Markdown code embedding format. Do not generate sample output. Answer the question and provide a one-line explanation and stop.

        example:
        ```python
        output = df['region'].unique()
        ```
                
        question: {input}

        answer:

        """
        self.file_path=file_path


    def extract_code(self,response):
        start = 0
        q = ""
        temp_block=""
        for line in response.splitlines(): 
            if '```python' in line and start==0:
                start=1
            if '```' == line.strip() and start==1:
                start =0
                break
            if start ==1 and '```' not in line:
                q=q+'\n'+line
        return q


    def data_ops(self,query):
        if os.path.isfile('./data/output.csv'):
            df=pd.read_csv('./data/output.csv') 
        else:
            df=pd.read_csv(self.file_path) 
        query = query 
        columns=df.columns.tolist()
        prompt = PromptTemplate.from_template(self.instruction)
        agent = LLMChain(llm=self.llm,prompt=prompt)
        response = agent.invoke(input={"columns":columns,"input":query})
        response = self.extract_code(response['text'])
        gencode=autopep8.fix_code(response)
        df_temp=df
        exec(gencode)
        df_temp.to_csv('./data/output.csv',index=False)
        return df_temp

