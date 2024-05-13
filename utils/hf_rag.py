import os
from typing import Any

from dotenv import dotenv_values
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

from configs.hf_rag import *

READER_MODEL_API_KEY = None
EMBEDDING_MODEL = None
READER_MODEL = None
VECTOR_DB = None
CONV_BUFF_MEMORY = None
CONV_RET_CHAIN = None


def load_reader_model_api_key() -> str:
    global READER_MODEL_API_KEY

    if not READER_MODEL_API_KEY:
        secrets = dotenv_values("../secrets.env")
        READER_MODEL_API_KEY = secrets.get("NVIDIA_API_KEY")
        os.environ["NVIDIA_API_KEY"] = READER_MODEL_API_KEY
    return READER_MODEL_API_KEY


def load_embeddings() -> NVIDIAEmbeddings:
    global EMBEDDING_MODEL

    if not EMBEDDING_MODEL:
        EMBEDDING_MODEL = NVIDIAEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            max_length=CHUNK_SIZE
        )
    return EMBEDDING_MODEL


def load_vector_db() -> Any:
    global VECTOR_DB

    if not VECTOR_DB:
        VECTOR_DB = FAISS.load_local(
            VECTOR_DB_FILE_PATH,
            load_embeddings(),
            allow_dangerous_deserialization=True
        )
    return VECTOR_DB


def load_reader_model() -> ChatNVIDIA:
    global READER_MODEL

    if not READER_MODEL:
        load_reader_model_api_key()
        READER_MODEL = ChatNVIDIA(
            model=READER_MODEL_NAME,
            temperature=0.3,
            max_tokens=512
        )
    return READER_MODEL


def load_buffer_memory() -> ConversationBufferMemory:
    global CONV_BUFF_MEMORY

    if not CONV_BUFF_MEMORY:
        CONV_BUFF_MEMORY = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return CONV_BUFF_MEMORY


def load_conv_ret_chain() -> ConversationalRetrievalChain:
    global CONV_RET_CHAIN

    if not CONV_RET_CHAIN:
        CONV_RET_CHAIN = ConversationalRetrievalChain.from_llm(
            llm=load_reader_model(),
            chain_type="stuff",
            retriever=load_vector_db().as_retriever(),
            memory=load_buffer_memory()
        )
    return CONV_RET_CHAIN


def generate_query_answer(query: str) -> str:
    conversational_chain = load_conv_ret_chain()
    response = conversational_chain.invoke({"question": query})
    return response["answer"]
