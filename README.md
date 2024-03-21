# Genta Customer Service Bot with RAG and Management System
This open-source repository presents a comprehensive customer service bot solution that leverages advanced technologies such as Retrieval Augmented Generation (RAG), a management system/dashboard, and seamless API integration. The bot is designed to be easily connected to websites or modified as needed, providing businesses with a powerful tool to enhance their customer support capabilities.

## Key Features
1. **Genta API Integration**: The repository fully utilizes the Genta API for AI LLM Inference and Embedding, enabling efficient and accurate responses to customer queries. Genta Technology provides a cutting-edge AI inference solution for developers and businesses.

2. **FastAPI Backend**: The Chatbot API is developed using FastAPI, a modern and fast web framework for building APIs with Python. It ensures high performance and easy integration with other systems.

3. **Streamlit Dashboard and Chat Demo**: The repository includes a user-friendly dashboard and chat demo built with Streamlit, allowing businesses to monitor and manage the customer service bot effectively. The dashboard provides insights into bot performance, conversation history, and analytics.

4. **RAG System with LangChain**: The RAG system is implemented using LangChain, a powerful library for building applications with large language models. The repository integrates LangChain with Genta using the GentaLangchain repository, enabling efficient retrieval and generation of responses.

5. **Chroma Vector Database**: The repository utilizes Chroma, a high-performance vector database, to store and retrieve relevant information for the RAG system. Chroma enables fast and accurate retrieval of similar documents based on embeddings.

## Getting Started
To get started with the customer service bot, follow these steps:
1. Clone this repository:
    ```sh
    git clone https://github.com/Genta-Technology/GentaLangchain.git
    ```

2. Install the dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Setup the environment variables, by copying the `.env.example` file to `.env`
   ```sh
   cp .env.example .env
   ```
   Then fill in the values in the `.env` file with your own values. 

4. Run the system
    - To run the API and dashboard, use:
        ```sh
        ```