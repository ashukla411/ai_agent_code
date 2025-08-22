from langchain_ollama import ChatOllama
from pypdf import PdfReader

input_path = input("Enter the path to the PDF file: ")
if not input_path:
    input_path = "/Users/shubhave/Desktop/bcs.pdf"
reader = PdfReader(input_path)
pdf_content = ""
for page in reader.pages:
    pdf_content += page.extract_text()
llm = ChatOllama(model="qwen3:4b",format={
    "type": "object",
    "properties": {
        "total_income": {"type": "integer"},
        "income_breakdown": {
            "type": "object",
            "properties": {
                "salary": {"type": "integer"},
                "business": {"type": "integer"},
                "capital_gains": {"type": "integer"},
                "other_sources": {"type": "integer"}
            }
        },
        "tax_paid": {"type": "integer"},
        "tax_payable": {"type": "integer"},
        "tax_breakdown_by_slab": {
            "type": "object",
            "properties": {
                "0-2.5L": {"type": "integer"},
                "2.5L-5L": {"type": "integer"},
                "5L-10L": {"type": "integer"},
                "10L+": {"type": "integer"}
            }
        }
    }
}
)
messages = [
    ("system","You are expert in extracting structured data from unstructured text files, with advanced knowledge in data analysis and Indian tax computation.\nLook at the pdf content and extract how much tax is paid, how much is to be paid, what is total income and individual income from different sources.\nGive me a tax breakdown according to income tax slabs rate of India.\nFormat the response in JSON only."),
    ("user", pdf_content)
]
response = llm.invoke(messages)
print("Extracted Data:",response.content)