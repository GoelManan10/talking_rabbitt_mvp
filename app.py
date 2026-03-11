import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

st.title("🐰 Talking Rabbitt - Conversational Data Intelligence")

uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    tab1, tab2 = st.tabs(["Chat", "Data"])

    with tab2:

        st.subheader("Dataset Viewer")

        st.write("Shape:", df.shape)

        st.dataframe(df, use_container_width=True)

        st.download_button(
            label="Download Dataset",
            data=df.to_csv(index=False),
            file_name="dataset.csv",
            mime="text/csv"
        )

    with tab1:

        question = st.text_input("Ask a question about your data")

        if question:

            query_prompt = f"""
You are a senior data analyst.

Dataset columns:
{list(df.columns)}

User Question:
{question}

Write pandas python code.

Rules:
- dataframe name is df
- final answer stored in variable result
- dataframe for chart stored in variable plot_df
- ensure chart data corresponds exactly to the query result
- no explanation

Example:

result = df[df["Quarter"]=="Q1"].groupby("Region")["Sales"].sum().idxmax()

plot_df = df[df["Quarter"]=="Q1"].groupby("Region")["Sales"].sum().reset_index()
"""

            response = client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct",
                messages=[{"role": "user", "content": query_prompt}]
            )

            code = response.choices[0].message.content
            code = code.replace("```python", "").replace("```", "").strip()

            try:

                local_vars = {"df": df}

                exec(code, {}, local_vars)

                result = local_vars["result"]
                plot_df = local_vars.get("plot_df", None)

                st.subheader("Answer")
                st.success(result)

            except Exception as e:

                st.error("Query execution failed")
                st.code(code)
                st.stop()

            if plot_df is not None:

                st.subheader("Visualization")

                chart_prompt = f"""
Choose best chart type.

Columns in chart data:
{list(plot_df.columns)}

Return only one word:

bar
line
pie
scatter
"""

                chart_response = client.chat.completions.create(
                    model="meta-llama/llama-3.1-8b-instruct",
                    messages=[{"role": "user", "content": chart_prompt}]
                )

                chart_type = chart_response.choices[0].message.content.strip().lower()

                fig, ax = plt.subplots()

                try:

                    if chart_type == "bar":

                        ax.bar(plot_df.iloc[:,0], plot_df.iloc[:,1])

                        ax.set_xlabel(plot_df.columns[0])
                        ax.set_ylabel(plot_df.columns[1])

                    elif chart_type == "line":

                        ax.plot(plot_df.iloc[:,0], plot_df.iloc[:,1], marker="o")

                        ax.set_xlabel(plot_df.columns[0])
                        ax.set_ylabel(plot_df.columns[1])

                    elif chart_type == "pie":

                        ax.pie(
                            plot_df.iloc[:,1],
                            labels=plot_df.iloc[:,0],
                            autopct="%1.1f%%"
                        )

                    elif chart_type == "scatter":

                        ax.scatter(plot_df.iloc[:,0], plot_df.iloc[:,1])

                        ax.set_xlabel(plot_df.columns[0])
                        ax.set_ylabel(plot_df.columns[1])

                    else:

                        ax.bar(plot_df.iloc[:,0], plot_df.iloc[:,1])

                    st.pyplot(fig)

                except:

                    st.warning("Chart generation failed")

            insight_prompt = f"""
Dataset columns: {list(df.columns)}

User question: {question}

Answer: {result}

Give a concise business insight in 2 lines.
"""

            insight_response = client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct",
                messages=[{"role": "user", "content": insight_prompt}]
            )

            insight = insight_response.choices[0].message.content

            st.subheader("AI Insight")
            st.info(insight)