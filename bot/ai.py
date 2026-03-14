import os
import re
import logging
import fitz
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from asgiref.sync import sync_to_async

# ====== ១. Configuration =======
load_dotenv()
# #កំណត់ Logging System** សម្រាប់បង្ហាញ log នៅក្នុង terminal
# - `level=logging.INFO` → បង្ហាញ messages ដែលជា INFO, WARNING, ERROR
# - `format="%(asctime)s [%(levelname)s] %(message)s"` → format លទ្ធផលបែបនេះ:
# ```
#   2024-01-15 10:30:00 [INFO] Starting application...
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sophy")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_FOLDER = os.path.join(BASE_DIR, "texts")
PDF_FOLDER  = os.path.join(BASE_DIR, "pdfs")
DB_PATH     = os.path.join(BASE_DIR, "chroma_db")

# ====== ២. Embeddings & Database ======
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
if os.path.exists(DB_PATH):
    logger.info("កំពុងដំណើរការ Database ដែលមានស្រាប់...")
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
else:
    logger.info("កំពុងបង្កើត Database ថ្មី...")
    all_data = []
#ឆែកមេីលថាមានFile text  ក្នុងFloder textsឬអត់បេីគ្នានCodeនឹងerror
    if os.path.exists(TEXT_FOLDER):
        for txt_file in os.listdir(TEXT_FOLDER):
            if txt_file.endswith(".txt"):
                try:
                    loader = TextLoader(os.path.join(TEXT_FOLDER, txt_file), encoding="utf-8")
                    all_data.extend(loader.load())
                except Exception as e:
                    logger.warning(f"បញ្ហា TXT {txt_file}: {e}")
#ឆែកមេីលថាមានFile PDF  ក្នុង Floder pdfs ឬអត់បេីគ្នានCodeនឹងerror
    if os.path.exists(PDF_FOLDER):
        for pdf_file in os.listdir(PDF_FOLDER):
            if pdf_file.endswith(".pdf"):
                try:
                    doc  = fitz.open(os.path.join(PDF_FOLDER, pdf_file))
                    text = "".join([page.get_text() for page in doc])
                    if text.strip():
                        all_data.append(Document(page_content=text, metadata={"source": pdf_file}))
                except Exception as e:
                    logger.warning(f"បញ្ហា PDF {pdf_file}: {e}")

    if not all_data:
        raise ValueError("រកមិនឃើញឯកសារទេ!")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", "។", "៕", " ", ""]
    )
    chunks = text_splitter.split_documents(all_data)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    logger.info("Database បង្កើតរួចរាល់!")

# ====== ៣. LLM & Prompt ======
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

system_template = """អ្នកគឺជា សុភី (Sophy) ជំនួយការកសិកម្មខ្មែរ។
ច្បាប់:
1. ឆ្លើយតែពី Context ខាងក្រោមប៉ុណ្ណោះ។
2. បើ Context គ្មានព័ត៌មាន ត្រូវឆ្លើយថា "សូមអភ័យទោស នាងខ្ញុំមិនមានព័ត៌មាននេះទេ។"
3. កុំបង្កើតព័ត៌មានក្រៅ Context។
4. ឆ្លើយជាភាសាខ្មែរ។

Context: {context}"""

prompt    = ChatPromptTemplate.from_messages([("system", system_template), ("human", "{question}")])
llm_chain = prompt | llm | StrOutputParser()

# ====== ៤. Identity ======
IDENTITY_PATTERN = re.compile(
    r"(តើអ្នកណាបង្កេីតអ្នកឡេីង|អ្នកជានរណា|ឈ្មោះ.*អ្នក|អ្នក.*ឈ្មោះ|"
    r"នរណា.*បង្កើត|បង្កើត.*អ្នក|sophy|សុភី|អ្នកណា.*ជា|ជា.*AI|"
    r"តើអ្នកជាអ្វី|អ្នកធ្វើការឱ្យនរណា|ស្គាល់សុភីទេ|"
    r"who created you|who are you|your name|maker|developer)",
    re.IGNORECASE
)

IDENTITY_ANSWER = (
    "នាងខ្ញុំឈ្មោះ សុភី ជា AI ជំនួយការកសិកម្ម បង្កើតដោយ និស្សិត ឈ្មោះ Ry Ravin "
    "និស្សិតនៃសកលវិទ្យាល័យកម្ពុជា។ នាងខ្ញុំត្រូវបានបណ្តុះបណ្តាលដើម្បីជួយលោកពូ/អ្នកមីង "
    "ក្នុងការដាំដុះ ថែទាំដំណាំ និងដោះស្រាយបញ្ហាកសិកម្ម។"
)

# ====== ៥. similarity_search wrapper ======
def _search_with_score(q):
    return vectorstore.similarity_search_with_score(q, k=5)

search_with_score_async = sync_to_async(_search_with_score, thread_sensitive=False)

# ====== ៦. ask() ======
async def ask(question: str) -> dict:

    # ក. Identity check
    if IDENTITY_PATTERN.search(question):
        return {"success": True, "answer": IDENTITY_ANSWER, "sources": ["identity"]}

    # ខ. Search DB with score
    raw_docs = await search_with_score_async(question)

    # Log scores សម្រាប់ debug
    for doc, score in raw_docs:
        logger.info(f"[SCORE] {score:.4f} | {doc.metadata.get('source', '?')}")

    # Filter: L2 distance < 1.5 = relevant
    SCORE_THRESHOLD = 1.5
    relevant_docs = [doc for doc, score in raw_docs if score < SCORE_THRESHOLD]

    # គ. មាន relevant → ឆ្លើយពី DB
    if relevant_docs:
        context = "\n\n".join([d.page_content for d in relevant_docs])
        answer  = await llm_chain.ainvoke({"context": context, "question": question})
        sources = list(set([
            os.path.basename(d.metadata.get("source", "unknown"))
            for d in relevant_docs
        ]))
        return {"success": True, "answer": answer.strip(), "sources": sources}

    # ឃ. គ្មាន relevant → LLM general knowledge (គ្មាន web search)
    try:
        fallback_prompt = (
            f"អ្នកគឺជា សុភី ជំនួយការកសិកម្មខ្មែរ។\n"
            f"សំណួរ: {question}\n\n"
            f"ចូរឆ្លើយជាភាសាខ្មែរ ដោយផ្អែកលើចំណេះដឹងកសិកម្មទូទៅ។\n"
            f"បើមិនទាក់ទងកសិកម្មទេ ត្រូវឆ្លើយថា 'សូមអភ័យទោស នាងខ្ញុំជំនួយការកសិកម្មប៉ុណ្ណោះ។'\n"
            f"ឆ្លើយខ្លី មិនលើស ៣ ប្រយោគ។"
        )
        answer = await llm.ainvoke(fallback_prompt)
        return {"success": True, "answer": answer.content, "sources": ["Internet"]}
    except Exception as e:
        logger.error(f"Fallback failed: {e}")
        return {"success": False, "answer": "សូមអភ័យទោស នាងខ្ញុំរកមិនឃើញព័ត៌មាននេះទេ។"}