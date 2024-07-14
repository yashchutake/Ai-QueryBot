import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

app = Flask(__name__)

def get_response(question):
    prompt_template = """
        Answer the question as detailed as possible.
            Question: \n{question}\n

        Answer:
    """
    api_key = os.getenv("GOOGLE_API_KEY")

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", 
        temperature=0.3,
        google_api_key=api_key,  
        safety_settings={ 
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
    llm_chain = prompt | llm
    response = llm_chain.invoke({'question': question})
    
    return response.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    response = get_response(question)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
