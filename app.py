import streamlit as st
import groq
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2']= "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with Groq"

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user queries."),
    ("user", "Question: {question}")
])

def generate_response(question,api_key,llm,temperature,max_tokens):
    groq.api_key = api_key
    llm = ChatGroq(model=llm)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer

st.title("Q&A Chatbot with Groq")
api_key = st.sidebar.text_input("Enter your open AI API Key:",type="password")

llm= st.sidebar.selectbox("Select an Groq model",["llama-3.3-70b-versatile","deepseek-r1-distill-llama-70b","qwen-qwq-32b"])

temperature= st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)


st.write("Go ahead and ask any question")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)

else:
    st.write("Please provide the query")