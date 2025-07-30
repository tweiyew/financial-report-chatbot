from langchain.agents import Tool
from langchain_google_vertexai import ChatVertexAI

def summarize(text: str) -> str:
    """Summarize a block of text, such as fund strategy or risk disclosures."""
    llm = ChatVertexAI(model_name="gemini-2.5-flash-lite", temperature=0.3)
    prompt = f"Please summarize the following financial content in simple terms:\n\n{text}"
    return llm.invoke(prompt)

summarizer_tool = Tool(
    name="Summarizer",
    func=summarize,
    description="Summarize financial sections such as fund strategies or risk disclosures."
)
