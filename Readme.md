Talking Rabbitt – Conversational Data Intelligence

Talking Rabbitt is an AI-powered data analytics app that allows users to ask questions about their datasets in natural language. The system automatically generates Pandas queries, visualizations, and business insights using an LLM.

🚀 Features

📂 Upload CSV datasets

💬 Ask questions about your data in plain English

🧠 LLM generates Pandas code automatically

📊 Automatic chart generation (bar, line, pie, scatter)

💡 AI-generated business insights

📑 Dataset viewer with download option

🛠 Tech Stack

Streamlit – UI

Pandas – Data processing

Matplotlib – Visualization

OpenRouter API – LLM access

LLaMA 3.1 – Code & insight generation

Python

⚙️ Installation
1. Clone the repository
git clone https://github.com/GoelManan10/talking_rabbitt_mvp.git
cd talking_rabbitt_mvp
2. Install dependencies
pip install streamlit pandas matplotlib python-dotenv openai
3. Add API Key

Create a .env file:

OPENROUTER_API_KEY=your_api_key_here
4. Run the app
streamlit run app.py
📊 Example Query
Which region had the highest sales in Q1?

The app will automatically:

Generate a Pandas query

Display the result

Create a chart

Provide a business insight

Problem : 
I faced an issue related to the API key during deployment on Streamlit Cloud. The application works perfectly on my local environment (localhost), where the API key is successfully fetched and the system runs without any errors.

However, after deploying the project on Streamlit Cloud, the application is unable to fetch the API key. As a result, the API-dependent functionalities are not working properly in the deployed version.

Despite verifying the code and ensuring that the environment variables are correctly configured, Streamlit Cloud still fails to retrieve the API key during runtime. The issue appears to be specific to the deployment environment rather than the local setup.

Author
Manan Goel
