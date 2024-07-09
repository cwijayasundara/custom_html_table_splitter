import warnings
from langchain_core.documents import Document
from token_calculator import num_tokens_from_string
from langchain_community.vectorstores import Chroma
from generic_html_parser import extract_table_rows, extract_other_elements
from research.summerizer import summarise_text
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from json_loader import load_json_file

warnings.filterwarnings('ignore')
_ = load_dotenv()

max_token_size = 4000

# filename = "./docs/sales.html"
# filename = "./docs/nvidia_financial_results_q1_fiscal_2025.html"

file_name = "docs/sales_sample.json"

data_in_json = load_json_file(file_name)

html_text = data_in_json["content"]

""" extract the table rows and other elements from the html file"""

table_rows = extract_table_rows(html_text)

table_rows_to_embed = []

# loop and print the table row elements sizes
for row in table_rows:
    num_tokens = num_tokens_from_string(row.page_content, "cl100k_base")
    if num_tokens > max_token_size:
        print("there are more tokens than I can handle!")
        row_summaries = summarise_text(row)
        table_rows_to_embed.append(Document(page_content=row_summaries))
    else:
        table_rows_to_embed.append(row)

other_elements = extract_other_elements(html_text)

# loop and print the other elements sizes
for element in other_elements:
    num_tokens = num_tokens_from_string(element.page_content, "cl100k_base")
    if num_tokens > max_token_size:
        print("there are more tokens than I can handle!")
        element_summaries = summarise_text(element)
        table_rows_to_embed.append(Document(page_content=element_summaries))
    else:
        table_rows_to_embed.append(element)

embeddings = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(table_rows_to_embed, embeddings)

# query = "$26,044"
query = "quarterly cash dividend"

retriever = vectorstore.as_retriever()

result = retriever.invoke(query, k=4)

print(result)
