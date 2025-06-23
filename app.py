import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq 


load_dotenv()
lang_api = os.getenv("lang_api")
langsmith_project = os.getenv("LANGSMITH_PROJECT")
Groq_api_key="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" 

if lang_api:
    os.environ["lang_api"] = lang_api

if langsmith_project:
    os.environ["LANGSMITH_PROJECT"] = langsmith_project

st.title("Q&A chatbot")


st.markdown("""
    <style>
       <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            height: 500px;
            overflow-y: auto;
        }

        .message {
            padding: 12px 18px;
            border-radius: 20px;
            margin-bottom: 15px;
            max-width: 75%;
            font-size: 16px;
            line-height: 1.4;
        }

        .message-user {
            background-color: #222;
            color: white;
            margin-left: auto;
            text-align: right;
            border-bottom-right-radius: 0;
        }

        .message-bot {
            background-color: #ddd;
            color: black;
            margin-right: auto;
            text-align: left;
            border-bottom-left-radius: 0;
        }
    </style>
""", unsafe_allow_html=True)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("user", "Question: {question}")
    ]
)


llm = ChatGroq(
    model="Gemma2-9b-It", 
    api_key=Groq_api_key
)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

chat_history = []

with st.container():
    for message in chat_history:
        if message['role'] == 'user':
            st.markdown(f'<div class="message message-user">{message["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message message-bot">{message["text"]}</div>', unsafe_allow_html=True)

input_text = st.text_input("What question do you have in mind?")

if input_text:
   
    chat_history.append({"role": "user", "text": input_text})
    
    
    response = chain.invoke({"question": input_text})
   
    chat_history.append({"role": "bot", "text": response})

    with st.container():
        for message in chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="message message-user">{message["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message message-bot">{message["text"]}</div>', unsafe_allow_html=True)