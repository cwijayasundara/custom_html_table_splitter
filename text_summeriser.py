import warnings
from dotenv import load_dotenv
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from typing import List

warnings.filterwarnings('ignore')
_ = load_dotenv()

prompt_template = """
Write a concise summary of the following: {text} without dropping any important information like codes etc
CONCISE SUMMARY:
"""

prompt = PromptTemplate.from_template(prompt_template)

llm = ChatOpenAI(temperature=0,
                 model_name="gpt-4o")


def summarise_text(text):

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain,
                                      document_variable_name="text")

    return stuff_chain.invoke(text)
