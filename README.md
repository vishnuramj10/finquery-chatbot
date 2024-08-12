# Finquery - chatbot


This is a SQL chatbot using Python Langchain framework and LLAMA-CPP - LLama 8B Instruct GGUF LLM Model.

The model can be downloaded here - https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF/blob/main/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf.

This chatbot is designed for bank queries and is an offline CPU chatbot to maintain privacy of the bank details.

The chatbot is designed using Flask Application. The LLM model can be updated when a newer version of a Quantized model is released.

The chatbot connect to any SQL DB; currently it is trained to run and generate queries for MySQL Server. If wanting to use a separate SQL engine; have to update the schema and the prompt and provide the new sql engine query parameter.

## Architecture

<img width="457" alt="Screen Shot 2024-08-12 at 2 41 15 PM" src="https://github.com/user-attachments/assets/8e6454ec-1d00-4857-81a3-92f704d4625b">

## Results 


<img width="1107" alt="Screen Shot 2024-08-12 at 2 42 33 PM" src="https://github.com/user-attachments/assets/1cc51f16-baa7-468f-95dc-2c020493cc74">

<img width="820" alt="Screen Shot 2024-08-12 at 2 42 55 PM" src="https://github.com/user-attachments/assets/01b570f1-a86c-4c8f-b4dc-96e392c32922">


## Limitations

- Using GPUs or cloud services will maximize the utilization of LLM models and provide answers within seconds, unlike CPUs which tend to maximize CPU utilization.

- Limiting ourselves to CPU GGUF quantized models compromises accuracy and restricts prompt engineering improvements needed to enhance accuracies.
  
- CPU GGUF models tend to hallucinate(inaccurate answers) more frequently than usual. Prompting again can be helpful.
  
- The model experiences significant latency and crashes due to maximum CPU utilization giving nonsensical answers.
  
- Sometimes, the LLM provides incorrect answers to the same question, but it may give the correct response if prompted again.



