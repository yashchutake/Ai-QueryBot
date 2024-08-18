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
    try:
        # Define a basic template for code-related queries
        code_related_keywords = ["code", "program", "script", "algorithm", "print"]

        # Check if the question is related to programming
        if any(keyword in question.lower() for keyword in code_related_keywords):
            prompt_template = """
            You are a programming assistant. Please provide the code for the following request, ensuring that it is properly formatted and readable.

            Question: {question}

            Answer:
            """
        else:
            # Use a general template for non-programming queries
            prompt_template = """
            You are a helpful assistant. Please provide a concise and accurate response to the following query.

            Question: {question}

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
        
        # Clean and format the response
        formatted_response = response.content.strip()

        # Ensure the response is in a code block if it's code-related
        if any(keyword in question.lower() for keyword in code_related_keywords):
            if not formatted_response.startswith("```"):
                formatted_response = "```\n" + formatted_response + "\n```"

        return formatted_response
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    response = get_response(question)
    return jsonify({'response': response})

# if __name__ == '__main__':
#     app.run(debug=True)




# import os
# from dotenv import load_dotenv
# from flask import Flask, render_template, request, jsonify
# from langchain_google_genai import (
#     ChatGoogleGenerativeAI,
#     HarmBlockThreshold,
#     HarmCategory,
# )
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# load_dotenv()

# app = Flask(__name__)

# def get_response(question):
#     prompt_template = """
#         Answer the question as detailed as possible.
#             Question: \n{question}\n

#         Answer:
#     """
#     api_key = os.getenv("GOOGLE_API_KEY")

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-pro", 
#         temperature=0.3,
#         google_api_key=api_key,  
#         safety_settings={ 
#             HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#         },
#     )

#     prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
#     llm_chain = prompt | llm
#     response = llm_chain.invoke({'question': question})
    
#     return response.content

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/ask', methods=['POST'])
# def ask():
#     data = request.json
#     question = data['question']
#     response = get_response(question)
#     return jsonify({'response': response})

# if __name__ == '__main__':
#     app.run(debug=True)
