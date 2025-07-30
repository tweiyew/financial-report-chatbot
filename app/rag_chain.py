import os
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

from app.tools.calculator_tool import calculator
from app.tools.summarizer_tool import summarizer_tool

VECTORSTORE_DIR = "data/vectorstores"

def load_vectorstore(file_id: str):
    return Chroma(
        persist_directory=os.path.join(VECTORSTORE_DIR, file_id),
        embedding_function=VertexAIEmbeddings(model_name="text-embedding-005")
    )

def build_rag_tool(file_id: str) -> Tool:
    vectordb = load_vectorstore(file_id)
    retriever = vectordb.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatVertexAI(model_name="gemini-2.5-flash-lite", temperature=0.2),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )

    return Tool(
        name="PDF Lookup",
        func=qa_chain.run,
        description="Use this tool to answer questions from the uploaded financial report."
    )

def ask_question_with_agent(question: str, file_id: str) -> str:
    rag_tool = build_rag_tool(file_id)
    from app.tools.calculator_tool import calculator
    from app.tools.summarizer_tool import summarizer_tool

    tools = [rag_tool, calculator, summarizer_tool]
    agent = initialize_agent(
        tools=tools,
        llm=ChatVertexAI(model_name="gemini-2.5-flash-lite", temperature=0.2),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent.run(question)
