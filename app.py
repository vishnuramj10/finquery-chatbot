from flask import Flask, render_template, request, jsonify

from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
import re


print('---------------->>>>>>>>>>Imported packages>>>>>>>>>>>>>>>--------------')

#model_path = "C:/Users/ankee/OneDrive/Desktop/My_Chatbot/llama_model/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"
model_path = "C:/Users/ankee/OneDrive/Desktop/My_Chatbot/llama_model/llama-2-7b-chat.Q4_K_M.gguf"

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(
    model_path=model_path,
    #temperature=0.01, # to give variety of responses
    temperature=0.5,
    max_tokens=500,
    #top_p=1,
    top_p=0.9,
    n_ctx=8192,
    n_batch=512,
    callback_manager=callback_manager,
    verbose=True,
)
print('-------------------->>> LLM Model Imported >>>--------------------------')

server ='ANKEETA\\SQLEXPRESS'
database = 'chatbot_db'
connection_string = f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
# Create the SQLDatabase instance
db = SQLDatabase.from_uri(connection_string)
print('-------------------->>> Database connected >>>--------------------------')

schema = """
            CREATE TABLE [chatbot_db].[dbo].[bank_details] (
                [Bank_Name] NVARCHAR(50) NOT NULL,
                [Currency] NVARCHAR(50) NOT NULL,
                [Balance] FLOAT NOT NULL
            );
            """
print('-------------------->>> We have the Schema >>>--------------------------')

template = """You are a Bing search who understands all the bank names all over the world and also SQL expert chatbot engaged in a conversation with a human. 
Based on the table schema below, write an SQL query to answer the user's question.

Try to recognize the bank's name and correct its spelling if it is entered incorrectly.
For example, if the user enters 'wello fargo', correct it to 'Wells Fargo'.

The SQL query should include both the [Bank_Name] and [Currency].

If the user's question provides only the [Currency] but not the [Bank_Name], retrieve the bank name from the previous conversation stored in memory and include it in the query.

Additionally, pay careful attention to the following: when writing the query where [Bank_Name]='', use a bank name only from the list below. 

Just provide the SQL queries, stick to the question asked, and do not provide any explanations:

Previous conversation:
{chat_history}

Table schema:
{schema}

Question: {question}
SQL Query: """

prompt = ChatPromptTemplate.from_template(template)
print('-------------------->>> We have the prompt >>>--------------------------')

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", input_key='question') # Specify the input key for the memory
print('-------------------->>>   We have memory   >>>--------------------------')

# Combine everything into an LLMChain
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)
print('-------------------->>>  We have LLM Chain >>>--------------------------')


            

app = Flask(__name__)
print('Hi, I am in app.py....')

@app.route('/')
def home():
    print('---------- Hi, I am at home in flask -------------')
    return render_template('chat.html') 

@app.route('/ask', methods=['POST'])
def ask():
    print('---------- We are in flask, ASK, asking question to user -----------')
    question = request.form['message']
    print('Received user message:',question)
    
    '''>>>>>>>>>>>>>>>>>>>>>  Code for Question Answer  >>>>>>>>>>>>>>>>>>>>>>>'''
    
    print('My schema is: ',schema)
    llm_response = conversation.invoke({"question": question, "schema": schema}) # This is LLM Chain
    print('LLMResponse:')
    print(llm_response['text'])
    
    query = llm_response['text'].split(';')[0]+';'
    print('Query:')
    print(query)
    
    #answer = run_query(query)
    
    try:
        answer = db.run(query)
        print('----------Got answer: ',answer)
        if answer == '':
            final_answer = 'No records found.'
        answer = float(re.findall(r'\d+\.\d+', answer)[0])
        print(type(answer))
        final_answer = answer
    
    except Exception as e:
        print("No result found: ",e)
    
    print('User asked question: ',question)
    print('My query is: ',query)
    print('My answer is: ',final_answer)

    
    
    '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''

    bot_response = final_answer  # Get the response from the chatbot
    print('Bot will give response to user:',bot_response)
    return jsonify({'message': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
