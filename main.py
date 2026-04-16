import os
from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv(override=True)

app = FastAPI()

PROMPT_TEMPLATE = """
You are a friendly and helpful customer service agent for AB Ventures Hub, a Nigerian business that sells phones, computer gadgets, and real estate properties.

Answer the customer's question using ONLY the information in the context below.
Keep your answers concise and friendly — this is a WhatsApp conversation.
Use simple, clear English suitable for Nigerian customers.

If the answer is not in the context, say exactly this:
"I don't have that information right now. Please call or visit our store directly and our team will be happy to help. We are open Monday to Saturday, 8am to 7pm."

Never make up prices, availability, or property details. Always be honest.

Context:
{context}

Customer question: {question}

Your answer:
"""

retriever = None

def load_knowledge_base():
    global retriever
    if retriever is not None:
        return retriever
    loader = DirectoryLoader("docs", glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=".chroma"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return retriever

def ask_question(question):
    r = load_knowledge_base()
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
    parser = StrOutputParser()
    chain = (
        {
            "context": r,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | parser
    )
    return chain.invoke(question)

@app.on_event("startup")
async def startup_event():
    print("Loading AB Ventures Hub knowledge base...")
    load_knowledge_base()
    print("Knowledge base ready.")

@app.post("/whatsapp")
async def whatsapp_reply(Body: str = Form(...)):
    customer_message = Body.strip()
    print(f"Incoming message: {customer_message}")
    answer = ask_question(customer_message)
    response = MessagingResponse()
    response.message(answer)
    return Response(content=str(response), media_type="application/xml")