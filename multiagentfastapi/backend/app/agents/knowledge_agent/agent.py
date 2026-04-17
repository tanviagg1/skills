from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .vectorstore import get_vectorstore
from app.config import settings

SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the provided documents.

Use only the context below to answer. If the answer is not in the context, say "I couldn't find that information in the uploaded documents."

Context:
{context}
"""


def format_docs(docs) -> str:
    return "\n\n---\n\n".join(
        f"[{doc.metadata.get('source_file', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )


class KnowledgeAgent:
    def __init__(self):
        self.llm = ChatGroq(api_key=settings.groq_api_key, model="llama-3.3-70b-versatile")

    async def query(self, question: str, send_event) -> str:
        await send_event({"type": "status", "message": "Searching documents..."})

        vectorstore = get_vectorstore()

        # Check collection has documents
        count = vectorstore._collection.count()
        if count == 0:
            return "No documents have been uploaded yet. Please upload a PDF or text file first."

        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        docs = retriever.invoke(question)

        if not docs:
            return "I couldn't find relevant information in the uploaded documents."

        await send_event({"type": "status", "message": f"Found {len(docs)} relevant chunks, generating answer..."})

        context = format_docs(docs)

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{question}"),
        ])

        chain = prompt | self.llm | StrOutputParser()

        answer = await chain.ainvoke({"context": context, "question": question})
        return answer
