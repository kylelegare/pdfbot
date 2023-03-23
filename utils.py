import os
import streamlit as st
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import VectorDBQA
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
chat = ChatOpenAI(temperature=0)

#Set OpenAI API Key
openai_api_key = st.secrets['OPENAI_API_KEY']

@st.cache_data
def parse_pdf(file):
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        output.append(text)

    return "\n\n".join(output)


@st.cache_data
def embed_text(text):
    """Split the text and embed it in a FAISS vector store"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=0, separators=["\n\n", ".", "?", "!", " ", ""]
    )
    texts = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    index = FAISS.from_texts(texts, embeddings)

    return index


def get_answer(index, query):
    system_template = "You are a helpful assistant analyzing a document someone gave you"
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("for the question below answer solely based on the provided context. If the context is irrelevant reply ‘I cannot answer based on the context of the document’ "),
        HumanMessagePromptTemplate.from_template("Keep in mind the importance of clear and concise answers."),
        HumanMessagePromptTemplate.from_template("Answer in an unbiased tone."),
        HumanMessagePromptTemplate.from_template("{context}"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain_type_kwargs = {"prompt": prompt}
    chain = VectorDBQA.from_chain_type(
        llm=ChatOpenAI(),
        chain_type="stuff",
        vectorstore=index,
        chain_type_kwargs=chain_type_kwargs,
    )

    answer = chain({"query": query}, return_only_outputs=True)

    return answer





