from click import prompt
from langchain_community.vectorstores import PGVector
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from dotenv import load_dotenv
from os import getenv
import gradio as gr

load_dotenv()

tokens = {'prompt': 0, 'completion': 0}


def askChatbot(message, history, tokens):
    response = client.invoke(input=formatHistory(history, message))
    token_usage = response.response_metadata['token_usage']
    print(token_usage)
    tokens['prompt'] = tokens['prompt'] + token_usage['prompt_tokens']
    tokens['completion'] = tokens['completion'] + token_usage['completion_tokens']
    print(tokens)
    return response.content


if __name__ == '__main__':

    client = AzureChatOpenAI(
        deployment_name="gpt-4o",
    )

    connection = getenv("DATABASE_CONNECTION_STRING")

    embeddings = AzureOpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = PGVector(
        connection_string=connection,
        embedding_function=embeddings,
        use_jsonb=True,
    )

    retriever = vector_store.as_retriever()


    def formatHistory(grHistory, humanMessage):
        chunks = retriever.invoke(input=humanMessage)
        context = "\n\n".join(f"data:{chunk.page_content}\n, zdroj:{chunk.metadata['source']}" for chunk in chunks)
        with open('./resources/hciPrompt.md', 'r', encoding="utf8") as file:
            print(file.name)
            hci_system_prompt = getenv("SYSTEM_PROMPT_TEMPLATE").replace("%prompt", file.read()).replace('%context', context)

        messages = [SystemMessage(f"{hci_system_prompt}")]

        for message in grHistory:
            if message["role"] == "user": messages.append(HumanMessage(message["content"]))
            if message["role"] == "assistant": messages.append(AIMessage(message["content"]))

        messages.append(HumanMessage(humanMessage))
        return messages


    gr.ChatInterface(lambda m,h: askChatbot(m, h, tokens), type = "messages").launch()
