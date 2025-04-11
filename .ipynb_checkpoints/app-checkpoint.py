import streamlit as st
import nbformat
from nbconvert import PythonExporter
import uuid

# Function to load the Jupyter notebook and convert it to Python code
def load_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)
    
    # Convert notebook content to Python code
    python_exporter = PythonExporter()
    python_code, _ = python_exporter.from_notebook_node(notebook_content)
    
    return python_code

# Function to execute Python code dynamically in Streamlit
def execute_notebook_code(python_code):
    exec(python_code, globals())

# RAG System Components (from your notebook code)
def start_new_session():
    session_id = str(uuid.uuid4())
    return session_id

def remove_think_tags(text):
    start_tag = "<think>"
    end_tag = "</think>"
    
    while start_tag in text and end_tag in text:
        start_index = text.find(start_tag)
        end_index = text.find(end_tag, start_index) + len(end_tag)
        
        text = text[:start_index] + text[end_index:]
    
    return text

def get_answer_from_rag(user_query):
    session_id = start_new_session()  # Start a new session
    # Assuming conversational_rag_chain is already defined and ready to use
    response = conversational_rag_chain.invoke(
        {"input": user_query}, 
        {"configurable": {"session_id": session_id}}  # Pass session_id in the configuration
    )
    answer = response.get("answer", "Sorry, I couldn't get an answer.")
    cleaned_answer = remove_think_tags(answer)
    return cleaned_answer

# Streamlit interface
st.title("Conversational RAG System")
st.write("This interface will run your RAG system directly from the notebook!")

# Load the notebook content dynamically
notebook_path = './Test_conversational_RAG.ipynb'

# Read the notebook and convert to Python code
python_code = load_notebook(notebook_path)

# Execute the notebook code (i.e., run the RAG system functions)
execute_notebook_code(python_code)

# Accept user query input
user_query = st.text_input("Ask a question:")

if user_query:
    # Pass the query to the RAG system function and get the response
    answer = get_answer_from_rag(user_query)
    st.write(f"**AI Response**: {answer}")
